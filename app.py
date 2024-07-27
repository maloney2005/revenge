from flask import Flask, request, jsonify
import requests
import logging
import os

app = Flask(__name__)

API_KEY = '6370291c17671b61a6ddacab5161c185951f013f959e5f0cf8a3baf1'

# Configure logging
if 'DYNO' in os.environ:  # Only configure logging when running on Heroku
    import logging
    import logging.handlers
    handler = logging.handlers.SysLogHandler(address='/dev/log')
    formatter = logging.Formatter('%(asctime)s %(message)s')
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
else:
    logging.basicConfig(level=logging.INFO)

@app.route('/ipdata', methods=['GET'])
def get_ipdata():
    try:
        if request.headers.getlist("X-Forwarded-For"):
            ip = request.headers.getlist("X-Forwarded-For")[0]
        else:
            ip = request.remote_addr
        app.logger.info(f'IP requested: {ip}')
        if ip:
            response = requests.get(f'https://api.ipdata.co/{ip}?api-key={API_KEY}')
            response.raise_for_status()
            data = response.json()
            app.logger.info(f'Geodata: {data}')
            return jsonify(data)
        else:
            app.logger.error("No IP address found")
            return jsonify({"error": "No IP address found"}), 400
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Request error: {e}")
        return jsonify({"error": "An internal error occurred"}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error: {e}")
        return jsonify({"error": "An internal error occurred"}), 500

if __name__ == '__main__':
    app.run(debug=True)
