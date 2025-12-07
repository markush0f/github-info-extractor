FROM pgvector/pgvector:pg16

# Copy initialization SQL scripts
COPY ./init/*.sql /docker-entrypoint-initdb.d/
