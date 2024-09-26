FROM python:3.10

RUN apt-get update && apt-get install -y ffmpeg

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt


RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt


COPY ./ /code/app


CMD ["python3", "app/api_gateway.py"]