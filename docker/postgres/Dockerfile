FROM postgres:13.1

RUN apt update -y && apt install -y --no-install-recommends curl ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && curl https://apt.secrethub.io | bash
ENTRYPOINT ["secrethub", "run", "--"]
CMD ["/docker-entrypoint.sh", "postgres"]