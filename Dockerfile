FROM python:3.7

COPY . /usr/src/idwall
WORKDIR /usr/src/idwall

RUN pip install -r requirements.txt
RUN pip install -e .
