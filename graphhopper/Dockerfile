FROM eclipse-temurin:21-jdk-alpine

WORKDIR /data

# Copy your jar, config, and pbf into the image
COPY graphhopper-web-10.2.jar /data/
COPY config.yml /data/
COPY entrypoint.sh /data/
COPY melb.osm.pbf /data/
COPY gtfs.zip /data/

# Make entrypoint executable
RUN chmod +x /data/entrypoint.sh

# Default memory settings (can be overridden in Compose)
ENV JAVA_OPTS="-Xmx4g"

ENTRYPOINT ["/data/entrypoint.sh"]
