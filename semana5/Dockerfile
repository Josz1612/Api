FROM python:3.9-slim

WORKDIR /app

# Install build deps and pip dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app

EXPOSE 8000

# Simple HEALTHCHECK that queries the /health endpoint using Python
# Updated for HTTP on port 8000 (SSL Termination handled by Nginx)
HEALTHCHECK --interval=10s --timeout=3s --start-period=5s --retries=3 \
	CMD python -c "import sys, urllib.request as u; resp=u.urlopen('http://127.0.0.1:8000/'); sys.exit(0 if resp.getcode()==200 else 1)"

CMD ["uvicorn", "central_api:app", "--host", "0.0.0.0", "--port", "8000"]