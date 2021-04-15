# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install python packages specified in requirements
COPY requirements/base.txt /tmp/base.txt
COPY requirements/prod.txt /tmp/prod.txt
RUN pip install --trusted-host pypi.org --no-cache-dir --upgrade pip && \
    pip install --trusted-host pypi.org --no-cache-dir -r /tmp/prod.txt

# Add base user
RUN useradd -m -s /bin/bash -d /home/manti manti && \
    mkdir -p /srv/churchill/src/ /var/lib/churchill/static/ /var/lib/churchill/media/ /var/lib/churchill/data/ /var/log/churchill/ && \
    chown -R manti:manti /srv/churchill/src/ /var/lib/churchill/ /var/log/churchill/

# Select user, set working directory and run server
USER manti
WORKDIR /srv/churchill/src/
CMD python manage.py runserver
