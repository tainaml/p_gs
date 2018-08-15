FROM python:2.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /config
ADD /requirements.txt /
RUN pip install -r requirements.txt
RUN mkdir /src;
WORKDIR /src
