FROM python:3.12-slim

# Set the working directory
WORKDIR /app

COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY rtde-2.7.2-release.zip /app

RUN pip install rtde-2.7.2-release.zip

CMD ["python", "main.py"]