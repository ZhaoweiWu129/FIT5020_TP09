FROM postgis/postgis:latest

ENV POSTGRES_USER=postgres \
    POSTGRES_PASSWORD=pass \
    POSTGRES_DB=melb

# Copy SQL file into the container
COPY load_data.sql /tmp/init.sql

# Initialize database and run SQL at build time
RUN mkdir -p /var/run/postgresql && chown postgres:postgres /var/run/postgresql && \
    su postgres -c "pg_ctl initdb -D /var/lib/postgresql/data" && \
    su postgres -c "pg_ctl start -D /var/lib/postgresql/data -o '-p 5432' -w && \
    psql --username=postgres --dbname=postgres -c \"CREATE DATABASE ${POSTGRES_DB}\" && \
    psql --username=postgres --dbname=postgres -c \"ALTER USER postgres WITH PASSWORD '${POSTGRES_PASSWORD}';\" && \
    psql --username=postgres --dbname=${POSTGRES_DB} -f /tmp/init.sql && \
    pg_ctl stop -D /var/lib/postgresql/data -m fast"

RUN echo "host all all 0.0.0.0/0 md5" >> /var/lib/postgresql/data/pg_hba.conf

# Expose Postgres port
EXPOSE 5432

# Start Postgres normally
CMD ["postgres", "-D", "/var/lib/postgresql/data"]
