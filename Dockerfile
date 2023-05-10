# syntax=docker/dockerfile:1
FROM python:3.11-slim-buster
LABEL maintainer="daniel_tay_from.tp@cpf.litemail.gov.sg"
RUN pip install --upgrade pip
COPY . /src
WORKDIR /src
RUN pip3 install -r requirements.txt
EXPOSE 80
ENTRYPOINT ["python"]
CMD ["src/app.py"]