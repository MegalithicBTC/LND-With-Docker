FROM python:3
ENV PYTHONUNBUFFERED 1
COPY . /lndg
WORKDIR /lndg
RUN pip install -r requirements.txt
RUN pip install supervisor whitenoise