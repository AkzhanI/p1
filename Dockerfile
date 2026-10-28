FROM python:3.12-slim
COPY tracker.py /app/tracker.py
WORKDIR /data
CMD ["python", "/app/tracker.py"]
