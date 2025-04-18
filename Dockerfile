# Use the official Selenium image with Chrome preinstalled (headless + ARM-compatible)
FROM selenium/standalone-chrome:120.0

# Set working directory
WORKDIR /app

# Install Python and pip (already available in the base image, but ensure it's set)
RUN apt-get update && apt-get install -y python3-pip && apt-get clean

# Copy only requirements first to cache dependencies
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Now copy your project files
COPY . .

# Run tests (can be overridden)
CMD ["pytest", "tests/ui_tests", "--html=reports/test_report.html", "--self-contained-html"]
