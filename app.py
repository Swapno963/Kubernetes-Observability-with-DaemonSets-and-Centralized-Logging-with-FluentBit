from flask import Flask
import logging
import os

app = Flask(__name__)

# Ensure log directory exists
os.makedirs('/app/logs', exist_ok=True)

# Configure file logging
logging.basicConfig(
    filename='/app/logs/api-gateway.log',
    level=logging.INFO,
    format='%(asctime)s - API-GATEWAY - %(levelname)s - %(message)s'
)

@app.route('/api/test')
def test():
    logging.info("Request received at /api/test")
    return {"service": "api-gateway", "status": "ok", "message": "Hello from API Gateway"}

@app.route('/health')
def health():
    return {"status": "healthy"}

if __name__ == '__main__':
    logging.info("API Gateway starting...")
    app.run(host='0.0.0.0', port=8000)
