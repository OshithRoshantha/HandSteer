FROM python:3.11.8-slim

WORKDIR /handsteer

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "handTracking.py"]