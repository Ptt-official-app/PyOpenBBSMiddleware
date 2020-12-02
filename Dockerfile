FROM python:3.7-slim-buster

ENV APP=openbbs_middleware

RUN apt update && apt install -y git python3 python3-dev python3-pip g++ make

COPY . /srv/${APP}

RUN mkdir -p /etc/${APP}

WORKDIR /srv/${APP}
RUN pip3 install --upgrade pip && pip3 install .

EXPOSE 3457

CMD ["./scripts/run_docker.sh", "0.0.0.0"]
