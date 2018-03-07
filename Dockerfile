FROM python:3.6-slim
ENV PYTHONUNBUFFERED 1
WORKDIR /teavana
ADD requirements.txt /teavana/
RUN pip install -r requirements.txt
ADD . /teavana/
