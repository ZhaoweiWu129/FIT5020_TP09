#!/bin/sh
set -e

JAR=graphhopper-web-10.2.jar
PBF=melb.osm.pbf
CONFIG=config.yml

# If graph-cache doesn't exist, run import
if [ ! -d "graph-cache" ]; then
    echo "No graph-cache found - running import..."
    java $JAVA_OPTS -jar $JAR import $PBF
else
    echo "graph-cache found - skipping import."
fi

# Start server
echo "Starting GraphHopper server..."
exec java $JAVA_OPTS -jar $JAR server $CONFIG
