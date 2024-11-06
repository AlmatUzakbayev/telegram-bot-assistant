# Use the python:3.10-slim-bullseye image as a base image
FROM python:3.11-slim-bullseye

# Set the working directory in the container to /app
WORKDIR /app

# Copy the entire project into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install .

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Set the Python PATH to include /app
ENV PYTHONPATH=/app

# Run the command to start your application
CMD ["python", "bot/app/run.py"]