FROM python:3.12

RUN useradd --create-home userapi
WORKDIR /films_api

RUN pip install --upgrade pipenv
COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy --python /usr/local/bin/python3.12
COPY . .
RUN chown -R userapi:userapi ./
USER userapi

EXPOSE 5000
CMD ["python", "./wsgi.py"]