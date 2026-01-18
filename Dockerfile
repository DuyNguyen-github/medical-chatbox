# Dockerfile for Medical Chatbot
FROM python:3.10-slim

# Set workdir
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose port (Flask default 8080)
EXPOSE 8080

# Set environment variables (optional, can override with --env-file)
# ENV PINECONE_API_KEY=your_key_here

# Run the Flask app
CMD ["python", "app.py"]
