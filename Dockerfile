FROM python:3.9-slim

WORKDIR /src

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Use tail -f /dev/null to keep the container running indefinitely
CMD ["tail", "-f", "/dev/null"]