FROM python:3.8

WORKDIR /code

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "scale_workers.py" ]