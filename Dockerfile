# Python base
FROM python:3.13-slim

# Install system dependencies for Chromium and fonts
RUN apt-get update && apt-get install -y \
	chromium \
	chromium-driver \
	fonts-liberation \
	wget \
	curl \
	gnupg \
	&& rm -rf /var/lib/apt/lists/*

# Create app dir
WORKDIR /app

# Copy requirement files and install
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY . .

# Environment for Flask and Chrome
ENV PYTHONUNBUFFERED=1 \
	FLASK_APP=app.py \
	PORT=10000 \
	CHROME_BIN=/usr/bin/chromium \
	CHROMEDRIVER_BIN=/usr/bin/chromedriver

# Expose port for Render
EXPOSE 10000

# Start the web service
CMD ["python", "app.py"]
