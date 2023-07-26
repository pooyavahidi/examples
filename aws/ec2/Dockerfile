# Use an official Python runtime as a parent image
FROM python:3.11-slim-bookworm

# Set the working directory in the container to /app
WORKDIR /app

# Copy only the requirements.txt first to leverage Docker cache
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the files
COPY . .

# Set the entrypoint to be the python script.
ENTRYPOINT ["python", "single_win_instance.py"]
