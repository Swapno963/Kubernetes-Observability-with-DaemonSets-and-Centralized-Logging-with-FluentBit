from flask import Flask
import logging
import os

app = Flask(__name__)

os.makedirs('/app/logs', exist_ok=True)

logging.basicConfig(
    filename='/app/logs/order-service.log',
    level=logging.INFO,
    format='%(asctime)s - ORDER-SERVICE - %(levelname)s - %(message)s'
)

@app.route('/orders')
def orders():
    logging.info("Request received at /orders")
    return {"service": "order-service", "status": "ok", "message": "Hello from Order Service"}

@app.route('/health')
def health():
    return {"status": "healthy"}

if __name__ == '__main__':
    logging.info("Order Service starting...")
    app.run(host='0.0.0.0', port=8000)
