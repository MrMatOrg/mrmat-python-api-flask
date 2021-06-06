FROM python:3.9.5-slim

ADD requirements.txt /
ADD migrations /migrations
COPY dist/mrmat-python-api-flask-*.tar.gz /
RUN \
    groupadd -g 1000 flask \
    && useradd -u 1000 -g 1000 -c "Flask User" -M flask \
    && mkdir -p /app/instance \
    && chown -R 1000:1000 /app /app/instance

USER 1000:1000

ENV FLASK_APP=mrmat_python_api_flask
RUN \
    python -mvenv /app/venv \
    && . /app/venv/bin/activate \
    && pip install gunicorn wheel \
    && pip install -r /requirements.txt \
    && pip install /mrmat-python-api-flask-*.tar.gz \
    && flask db upgrade

USER 0:0
RUN \
    rm -rf /requirements.txt /mrmat-python-api-flask-*.tar.gz /migrations

EXPOSE 8080
USER 1000:1000
ENTRYPOINT /app/venv/bin/gunicorn -w 4 -b 0.0.0.0:8080 'mrmat_python_api_flask:create_app()'
