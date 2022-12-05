# pull the official base image
FROM python:3.8-bullseye

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV SECRET_KEY 'secret_key'


# install dependencies
COPY ./requirements.txt /usr/src/app
RUN pip install -r requirements.txt

# copy project
COPY . /usr/src/app

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
