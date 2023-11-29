FROM python:3.11-slim
ARG OPENAI_KEY
ENV OPENAI_KEY=$OPENAI_KEY
ENV PORT 8000

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1

COPY requirements.txt /
RUN pip install -r requirements.txt

COPY ./src /src
COPY ./assets /assets
COPY ./models /models
#COPY .env /.env

CMD uvicorn src.main:app --host 0.0.0.0 --port ${PORT}
