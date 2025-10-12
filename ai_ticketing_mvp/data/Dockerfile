# Dockerfile
# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend and nlp directories into the container at /app
COPY ./backend /app/backend
COPY ./nlp /app/nlp

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run main.py when the container launches
# The --host 0.0.0.0 makes the app accessible from outside the container
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]