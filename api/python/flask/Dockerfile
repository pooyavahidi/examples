FROM python:3.10-slim

# Pull docker-in-docker image and copy the docker cli to this image.
# This can be used in case of call to docker cli from the /processes resource.
COPY --from=docker:20.10 /usr/local/bin/docker /usr/local/bin/

RUN mkdir /app
WORKDIR /app

RUN set -e \
    && apt-get update \
    && apt-get install -y stress

COPY wsgi.py requirements.txt ./
RUN pip install -r requirements.txt

COPY api/ ./api

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app", "--workers=4"]
