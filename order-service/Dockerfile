FROM python:3.9-slim

WORKDIR /app
RUN pip install flask
RUN mkdir -p /app/logs
COPY app.py .
EXPOSE 8000
CMD ["python", "app.py"]
