FROM python:3.9
ENV PYTHONPATH ${PYTHONPATH}:/app

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

RUN useradd -m dk
#USER dk