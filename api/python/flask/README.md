# Flask API
This API is useful as a base PoC project for testing different technologies. 
This API can be deployed in a VM or container.

## Prerequisites
- Make sure docker and docker-compose are installed.
```
$ docker --version
$ docker-compose --version
```
Links:
    - https://docs.docker.com/compose/install/

> Initial build pulls the base images and build the dockerfile. It could take
a few minutes depending on the size of the
containers and speed of the internet.

## Run the containers
```
docker-compose build
docker-compose up -d
docker-compose down
```
If you have multiple docker-compose files, you can specify the file using `-f`.
```
docker-compose -f docker-compose.yaml up -d
```

## Test the container locally with curl
```
curl http://localhost:5000/

curl -X POST -d '{"args":["stress","-c","2","-t","10"]}' -H 'Content-Type: application/json' http://localhost:5000/processes

curl -X POST -d '{"args":["docker","run","-d","-p","80:80","--name","test-web","nginx"]}' -H 'Content-Type: application/json' http://localhost:5000/processes
```

## To run a test case from the command line.
https://docs.python.org/3/library/unittest.html

```
.env/Script/activate
python -m unittest test_load_balancing.TestLoadBalancing.test_simple_load_balancing
```
To run all the test cases, go to the root of the source code and then run this:
```
python -m unittest discover --verbose
```

## Run Performance Test using Locust
```
$ . .env/bin/activate
$ locust -f tests/perf/locustfile.py
```
