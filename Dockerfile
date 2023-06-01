# Use an official Python runtime as a parent image
FROM python:3.10-bullseye

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable

# Run main.py when the container launches
CMD ["gunicorn", "-b", "0.0.0.0", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--access-logfile", "-"]

# FROM tiangolo/uvicorn-gunicorn:python3.10

# COPY ./requirements.txt /app/requirements.txt

# RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# COPY . /app