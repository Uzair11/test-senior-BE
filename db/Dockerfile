FROM postgres:14

COPY ./scripts/create-user.sh  /docker-entrypoint-initdb.d/1.sh
RUN chmod +x /docker-entrypoint-initdb.d/1.sh