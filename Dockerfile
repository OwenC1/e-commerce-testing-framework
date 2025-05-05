FROM --platform=linux/amd64 selenium/standalone-chrome:120.0

USER root
WORKDIR /app

# Install Python pip
RUN apt-get update && apt-get install -y python3-pip && apt-get clean

# Install Python dependencies
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copy all test code
COPY . .

# Prevent Chrome crash by allocating shm
VOLUME /dev/shm

# Run tests with HTML report
CMD ["pytest", "--maxfail=1", "--disable-warnings", "--html=report.html", "-v"]
