# docker build . -t <tag>
# docker run -p port:port <tag>
# syntax=docker/dockerfile:1
FROM node:18
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . ./
EXPOSE 80 3000
CMD ["node", "validator.js"]