# # check=skip=JSONArgsRecommended
# FROM eclipse-temurin:21-jdk

# # Set working directory
# WORKDIR /graphhopper

# # Copy GraphHopper jar and PBF file
# COPY graphhopper-web-10.2.jar /graphhopper/
# COPY melb.osm.pbf /graphhopper/

# # Import first, then start in web mode
# CMD java $JAVA_OPTS -jar graphhopper-web-10.2.jar web melb.osm.pbf

FROM eclipse-temurin:21-jdk-alpine

WORKDIR /data

# Copy your jar, config, and pbf into the image
COPY graphhopper-web-10.2.jar /data/
COPY config.yml /data/
COPY entrypoint.sh /data/
COPY melb.osm.pbf /data/

# Make entrypoint executable
RUN chmod +x /data/entrypoint.sh

# Default memory settings (can be overridden in Compose)
ENV JAVA_OPTS="-Xmx4g"

ENTRYPOINT ["/data/entrypoint.sh"]
