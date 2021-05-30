FROM python:3.7.7-stretch

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt

RUN bash TransInstaller.sh

CMD ["python", "run.py"]