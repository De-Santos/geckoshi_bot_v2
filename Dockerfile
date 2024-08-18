# Use the official Python image from the Docker Hub
FROM python:3.12.3-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application into the container
COPY . /app/

# Ensure the entrypoint script is executable
RUN chmod +x /app/entrypoint.sh

# Set the entrypoint to the entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]

# Expose any ports if needed (e.g., 80 for web applications)
# EXPOSE 80

# Specify the default command
CMD ["python", "main.py"]
