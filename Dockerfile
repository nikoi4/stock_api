# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.10.6

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./eureka_stock_api /app

EXPOSE 8000

CMD python app/manage.py makemigrations && python app/manage.py migrate && python app/manage.py runserver 0.0.0.0:8000
