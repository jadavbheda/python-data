FROM python:3.8 AS build

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN python -m venv /opt/venv
ENV PATH=/opt/venv/bin:$PATH

COPY requirements.txt /tmp/requirements.txt

RUN /opt/venv/bin/pip install -r /tmp/requirements.txt

COPY /app /opt/app

WORKDIR /opt

CMD ["python", "/opt/app/main.py"]

#------

FROM build as validate

COPY requirements-dev.txt /tmp/requirements-dev.txt

RUN /opt/venv/bin/pip install -r /tmp/requirements-dev.txt

COPY /tests /opt/tests

#------

FROM python:3.8-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

COPY --from=build /opt /opt
ENV PATH=/opt/venv/bin:$PATH

RUN groupadd -g 999 appusr && \
    useradd -r -d /opt/app -u 999 -g appusr appusr

WORKDIR /opt

USER appusr

CMD ["python", "/opt/app/main.py"]
