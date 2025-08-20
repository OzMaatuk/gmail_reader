# Use the Playwright image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /workspace

# Copy the current directory contents into the container at /workspace
COPY . /workspace

# 1. Install system-wide Python dependencies. 'playwright' will now be in /usr/local/bin
RUN pip install --no-cache-dir -r requirements.txt

# Default command (can be overridden)
CMD ["python", "main.py"]