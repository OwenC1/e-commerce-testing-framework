FROM --platform=linux/amd64 selenium/standalone-chrome:120.0

USER root
WORKDIR /app

# Install Python pip & cleanup
RUN apt-get update && apt-get install -y python3-pip && apt-get clean

# Install dependencies
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copy code
COPY . .

CMD ["pytest", "--maxfail=1", "--disable-warnings", "-v"]
