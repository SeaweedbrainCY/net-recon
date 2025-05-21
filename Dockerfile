FROM python:3.12-slim

COPY scanner/ /app/scanner
WORKDIR /app

RUN apt-get clean \
    && apt-get -y update

RUN apt-get -y install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools gcc default-libmysqlclient-dev pkg-config jq curl nmap
RUN pip install --upgrade pip
RUN pip install -r ./scanner/requirements.txt
EXPOSE 8080

CMD ["python", "-m", "scanner"]
