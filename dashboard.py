from flask import Flask, jsonify, render_template
import os
import json

app = Flask(__name__, template_folder="web/templates", static_folder="web/static")

# Configuration paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
POLICY_FILE = os.path.join(BASE_DIR, 'config', 'allowlist.json')
LOG_FILE = os.path.join(BASE_DIR, 'logs', 'usb_audit.log')

def read_policy():
    if not os.path.exists(POLICY_FILE):
        return {"authorized_devices": [], "blocked_devices": [], "settings": {}}
    with open(POLICY_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def tail_logs(lines=50):
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE, 'r', encoding='utf-8') as f:
        # A simple way to get last N lines without reading the whole file in memory if it was huge,
        # but for a 5MB log file, reading lines is acceptable.
        all_lines = f.readlines()
        return [line.strip() for line in all_lines[-lines:] if line.strip()]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/policy')
def api_policy():
    policy = read_policy()
    return jsonify(policy)

@app.route('/api/logs')
def api_logs():
    logs = tail_logs(50)
    return jsonify({"logs": logs})

@app.route('/api/active')
def api_active():
    active_file = os.path.join(BASE_DIR, 'logs', 'active_devices.json')
    if not os.path.exists(active_file):
        return jsonify([])
    try:
        with open(active_file, 'r', encoding='utf-8') as f:
            return jsonify(json.load(f))
    except Exception:
        return jsonify([])

@app.route('/api/stats')
def api_stats():
    policy = read_policy()
    authorized = len(policy.get("authorized_devices", []))
    blocked = len(policy.get("blocked_devices", []))
    settings = policy.get("settings", {})
    return jsonify({
        "authorized_count": authorized,
        "blocked_count": blocked,
        "settings": settings,
        "status": "Monitoring Active" # Hardcoded for now since monitor runs separately
    })

if __name__ == '__main__':
    # Run the Flask development server without reloader to prevent watchdog/Python 3.13 crash
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
