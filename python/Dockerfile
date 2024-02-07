FROM python:3.12-slim

# Set the working directory
WORKDIR /app

COPY requirements.txt /app

RUN pip install -r requirements.txt

CMD ["python", "WebsocketProxy.py"]