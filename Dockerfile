# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Add directories
RUN mkdir -p /srv/churchill/src/ && \
    mkdir -p /srv/churchill/static/ && \
    mkdir -p /srv/churchill/media/ && \
    mkdir -p /var/log/churchill/

# Install any needed packages specified in requirements
COPY requirements/base.txt /tmp/base.txt
COPY requirements/prod.txt /tmp/prod.txt
RUN pip install --trusted-host pypi.org --no-cache-dir --upgrade pip && \
    pip install --trusted-host pypi.org --no-cache-dir -r /tmp/prod.txt

# Run gunicorn
EXPOSE 8000
WORKDIR /srv/churchill/src/

# Run
ENV DJANGO_SETTINGS_MODULE=churchill.settings.prod
CMD exec gunicorn churchill.wsgi:application --bind 0.0.0.0:8000 --workers 2
