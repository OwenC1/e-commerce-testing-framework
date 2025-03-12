# Start with the base Python image - this gives us a clean Python installation
FROM --platform=linux/arm64 python:3.9-slim

# Set up a working directory in the container - like creating a dedicated workspace
WORKDIR /app

# Copy your requirements file first - this helps with caching during builds
COPY requirements.txt .

# Install all your Python dependencies
RUN pip install -r requirements.txt

# Copy all your project files into the container
COPY . .

# Command that will run when the container starts
CMD ["pytest", "tests/"]