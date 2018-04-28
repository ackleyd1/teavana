FROM python:3.5-slim
ENV PYTHONUNBUFFERED 1
WORKDIR /teavana/web
ADD requirements.txt /teavana/web
RUN pip install -r requirements.txt
ADD . /teavana/web
WORKDIR /teavana/web/teavana
