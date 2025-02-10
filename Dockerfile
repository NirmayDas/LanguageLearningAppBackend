# Use Ubuntu as the base image
FROM ubuntu:20.04

# Install dependencies, including Python 3.13 and pip
RUN apt-get update && apt-get install -y \
    software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa -y \
    && apt-get update && apt-get install -y \
    python3.13 \
    python3.13-venv \
    python3.13-dev \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /code

# Copy the requirements file and install dependencies
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the FastAPI application code
COPY ./app /code/app

# Expose the necessary port
EXPOSE 80

# Set environment variables to ensure Python runs properly
ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=UTF-8

# Command to run FastAPI with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]