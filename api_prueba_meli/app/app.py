from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

# Estos serian Datos simulados de dispositivos para facilitar la prueba de meli
devices = {
    "device1": {"usage": 75},
    "device2": {"usage": 50},
    "device3": {"usage": 40},
    "device4": {"usage": 30},
    "device5": {"usage": 80},
}

@app.route('/usage', methods=['GET'])
def get_usage():
    device_id = request.args.get('device_id')
    if device_id:
        usage = devices.get(device_id)
        if usage:
            return jsonify(usage), 200
        else:
            return jsonify({"error": "Dispositivo no responde"}), 404
    else:
        return jsonify(devices), 200

@app.route('/run_script', methods=['POST'])
def run_script():
    script_name = request.json.get('script_name')
    if not script_name:
        return jsonify({"error": "No script name provided"}), 400

    try:
        # Ejecutar el script 
        result = subprocess.run([f'scripts/{script_name}'], capture_output=True, text=True, check=True)
        return jsonify({"output": result.stdout}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({"error": e.stderr}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
