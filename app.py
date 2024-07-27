# app.py
from flask import Flask, request, jsonify
import requests
import logging

app = Flask(__name__)

API_KEY = '6370291c17671b61a6ddacab5161c185951f013f959e5f0cf8a3baf1'

# Configure logging
logging.basicConfig(filename='ip_requests.log', level=logging.INFO, format='%(asctime)s - %(message)s')

@app.route('/ipdata', methods=['GET'])
def get_ipdata():
    ip = request.remote_addr
    if ip:
        # Log the IP address and geodata
        logging.info(f'IP requested: {ip}')
        
        response = requests.get(f'https://api.ipdata.co/{ip}?api-key={API_KEY}')
        data = response.json()
        
        # Log geodata
        logging.info(f'Geodata: {data}')
        
        return jsonify(data)
    else:
        return jsonify({"error": "No IP address found"}), 400

if __name__ == '__main__':
    app.run(debug=True)
