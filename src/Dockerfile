# docker build . -t <tag>
# docker run -p port:port <tag>
# syntax=docker/dockerfile:1
FROM python:3.11-slim-buster
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . ./
EXPOSE 8080
CMD ["python3", "app.py"]
