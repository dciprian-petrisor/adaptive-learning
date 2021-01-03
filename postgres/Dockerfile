FROM postgres:13.1

RUN apt update --yes && apt install curl --yes
RUN curl https://apt.secrethub.io | bash
ENTRYPOINT ["secrethub", "run", "--"]
CMD ["/docker-entrypoint.sh", "postgres"]