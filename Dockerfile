# syntax=docker/dockerfile:1
FROM python:3.11-slim-buster
LABEL maintainer="daniel_tay_from.tp@cpf.litemail.gov.sg"
RUN pip install --upgrade pip
COPY . /src
WORKDIR /src
RUN pip3 install -r requirements.txt
EXPOSE 80
# ENTRYPOINT ["python"]
CMD ["python3", "src/app.py"]
# RUN python3 src/app.py


# Stage 1: Build the frontend
FROM node:18
WORKDIR /src
COPY src/node/package*.json ./
COPY src/node/validator.json ./
RUN npm ci
COPY . .
CMD ["node", "src/node/validator.js"]
# RUN npm run build

# # Stage 2: Build the backend
# FROM python:3.9 AS backend
# WORKDIR /app/backend
# # Copy backend dependencies
# COPY src/requirements.txt ./
# RUN pip install --no-cache-dir -r requirements.txt
# # Copy backend code
# COPY src/ ./

# # Set environment variables
# ENV FLASK_APP=app.py
# ENV FLASK_RUN_HOST=0.0.0.0

# # Expose the necessary ports
# EXPOSE 5000

# # Start the backend server
# CMD ["flask", "run"]