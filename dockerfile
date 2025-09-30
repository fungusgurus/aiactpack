# Dockerfile
FROM python:3.11-slim

# set working directory
WORKDIR /app

# copy dependency list
COPY requirements.txt .

# install python packages
RUN pip install --no-cache-dir -r requirements.txt

# copy source code
COPY . .

# expose port (Railway/Fly.io default)
EXPOSE 8080

# run streamlit on 0.0.0.0:8080
CMD ["streamlit", "run", "home.py", "--server.port=8080", "--server.address=0.0.0.0"]
Save → exit.
