FROM python:3.9.2-alpine3.13

ADD requirements.txt /
COPY dist/mrmat-python-api-flask-*.tar.gz /
RUN \
    pip install gunicorn \
    && pip install -r /requirements.txt \
    && pip install /mrmat-python-api-flask-*.tar.gz \
    && rm -f /requirements.txt /mrmat-python-api-flask-*.tar.gz

USER 1000:1000
EXPOSE 8080
ENTRYPOINT gunicorn -w 4 -b 0.0.0.0:8080 mrmat_python_api_flask.app:app
