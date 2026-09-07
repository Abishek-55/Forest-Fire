from flask import Flask, render_template, jsonify, request
import config
import os, json, csv
import requests
from alert import dispatch_nearest_authority_alert

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", bbox=config.NEPAL_BBOX)

@app.route("/api/communities")
def api_communities():
    file_path = os.path.join(os.path.dirname(__file__), "data", "communities.json")
    if not os.path.exists(file_path):
        return jsonify([])
    with open(file_path, encoding="utf-8") as f:
        return jsonify(json.load(f))

@app.route("/api/hotspots")
def api_hotspots():
    source = request.args.get("source", getattr(config, "FIRMS_SOURCE", "VIIRS_NOAA21_NRT"))
    days = request.args.get("days", "1")
    target_bbox = request.args.get("bbox", config.NEPAL_BBOX)
    
    url = f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/{config.FIRMS_MAP_KEY}/{source}/{target_bbox}/{days}"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200 or "Invalid" in response.text:
            print(f"[FIRMS API Error]: {response.text.strip()}")
            return jsonify([])

        reader = csv.DictReader(response.text.strip().splitlines())
        hotspots = []
        
        for row in reader:
            try:
                frp = float(row.get("frp", 0.0))
                raw_conf = row.get("confidence", "n").lower()
                
                if raw_conf in ["l", "low"] or (raw_conf.isdigit() and int(raw_conf) < 40):
                    confidence = "low"
                elif raw_conf in ["h", "high"] or (raw_conf.isdigit() and int(raw_conf) >= 80):
                    confidence = "high"
                else:
                    confidence = "nominal"

                hotspots.append({
                    "latitude": float(row["latitude"]),
                    "longitude": float(row["longitude"]),
                    "frp": frp,
                    "confidence": confidence,
                    "acq_time": f"{row.get('acq_date', '')} {row.get('acq_time', '')}".strip()
                })
            except (ValueError, KeyError):
                continue
        # Print requested FIRMS hotspot data to the terminal
            print("\n--- FIRMS API Hotspot Data Received ---")
            print(f"Total Hotspots Found: {len(hotspots)}")
            print(json.dumps(hotspots, indent=2))
            print("----------------------------------------\n")
        return jsonify(hotspots)
    except Exception as e:
        print(f"[Error fetching FIRMS]: {e}")
        return jsonify([])

@app.route("/api/send-alert", methods=["POST"])
def send_alert():
    data = request.json or {}
    fires = data.get("fires", [])
    communities = data.get("communities", [])

    result = dispatch_nearest_authority_alert(fires, communities)
    status_code = 200 if result.get("status") == "success" else 400
    return jsonify(result), status_code

if __name__ == "__main__":
    app.run(host=config.FLASK_HOST, port=config.FLASK_PORT, debug=config.DEBUG)