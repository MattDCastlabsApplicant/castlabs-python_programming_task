# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster
WORKDIR /castlabs
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt 
COPY . .
CMD ["python", "castlabsProxyServer.py", "--host=0.0.0.0"]
EXPOSE 8080


