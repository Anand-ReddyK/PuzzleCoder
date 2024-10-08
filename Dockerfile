FROM python:3.8

WORKDIR /code

COPY requirements.txt /code

RUN pip install -r requirements.txt

COPY . /code/

ENTRYPOINT [ "python", "manage.py", "runserver",  "0.0.0.0:8000"]