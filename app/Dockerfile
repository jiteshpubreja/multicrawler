FROM python:3.7.7-stretch

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY ./nltk.txt /app/nltk.txt
COPY ./nltk_downloader.py /app/nltk_downloader.py
RUN python nltk_downloader.py