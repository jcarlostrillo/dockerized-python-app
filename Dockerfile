# FROM tiangolo/uwsgi-nginx-flask:python2.8
FROM tiangolo/uwsgi-nginx-flask:python3.8

RUN apt-get update

RUN apt-get install -y build-essential postgresql-server-dev-all npm

RUN npm install -g @angular/cli

RUN pip install psycopg2

RUN pip install flask-cors

RUN pip install marshmallow

RUN pip install sqlalchemy

COPY ./src /app

WORKDIR /app

CMD ["flask", "run", "--host=0.0.0.0"]
