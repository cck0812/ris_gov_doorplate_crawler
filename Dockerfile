# syntax=docker/dockerfile:1
ARG FUNCTION_DIR="/code/"
ARG RUNTIME_VERSION="3.8.10"

FROM python:${RUNTIME_VERSION}
ENV PYTHONUNBUFFERED=1
RUN apt update -y && \
    apt install -y tesseract-ocr python3-opencv
ARG FUNCTION_DIR
WORKDIR ${FUNCTION_DIR}
COPY . ${FUNCTION_DIR}
RUN pip install -r requirements.txt