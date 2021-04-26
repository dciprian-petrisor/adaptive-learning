FROM postgres:13.1

RUN apt update -y && apt install curl -y  && rm -rf /var/lib/apt/lists/*
RUN curl https://apt.secrethub.io | bash
ENTRYPOINT ["secrethub", "run", "--"]
CMD ["/docker-entrypoint.sh", "postgres"]