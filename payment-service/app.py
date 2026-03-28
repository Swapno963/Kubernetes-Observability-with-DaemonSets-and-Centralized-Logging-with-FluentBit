from flask import Flask
import logging
import os

app = Flask(__name__)

os.makedirs('/app/logs', exist_ok=True)

logging.basicConfig(
    filename='/app/logs/payment-service.log',
    level=logging.INFO,
    format='%(asctime)s - PAYMENT-SERVICE - %(levelname)s - %(message)s'
)

@app.route('/payments')
def payments():
    logging.info("Request received at /payments")
    return {"service": "payment-service", "status": "ok", "message": "Hello from Payment Service"}

@app.route('/health')
def health():
    return {"status": "healthy"}

if __name__ == '__main__':
    logging.info("Payment Service starting...")
    app.run(host='0.0.0.0', port=8000)
