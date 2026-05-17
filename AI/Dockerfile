FROM python:3.10-slim

WORKDIR /app

# install system deps
RUN apt-get update && apt-get install -y git

# copy files
COPY . .

# install python deps
RUN pip install --no-cache-dir -r requirements.txt

# default command
CMD ["python", "main.py"]