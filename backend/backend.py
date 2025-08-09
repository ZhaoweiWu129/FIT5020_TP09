
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from geoalchemy2.shape import from_shape, to_shape
from shapely.geometry import shape, mapping, Point
from sqlalchemy import create_engine, cast
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, String, Boolean, Integer
from geoalchemy2 import Geometry, Geography
from sqlalchemy import func
import re
import os

# default url for local development
# DATABASE_URL = "postgresql+psycopg://postgres:pass@localhost:5432/melb"

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://postgres:pass@localhost:5432/melb")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class TrainStation(Base):
    __tablename__ = "train_station"
    id = Column(String, primary_key=True)
    name = Column(String)
    geom = Column(Geometry('POINT', srid=7844))
    whlchr_accss = Column(Boolean)

class OsmPublicParking(Base):
    __tablename__ = "osm_public_parking"
    id = Column(Integer, primary_key=True)
    geom = Column(Geometry("MULTIPOLYGON", srid=7844))
    name = Column(String)
    other_tags = Column(String)

app = FastAPI()

@app.get("/stations/{station_id}")
def read_station(station_id: str):
    session = SessionLocal()
    station = session.query(TrainStation).filter(TrainStation.id == station_id).first()
    session.close()
    if not station:
        return {"error": "Not found"}
    return {
        "id": station.id,
        "name": station.name,
        "geom": str(station.geom),  # or format as needed
        "wheelchair_accessible": bool(station.whlchr_accss)
    }

class NearRouteStationsRequest(BaseModel):

    maxdistance: int = 500
    coordinates: list

    def to_shape(self):
        return shape({"type": "LineString", "coordinates": self.coordinates})

@app.post("/stations/near_route")
def stations_near_route(line: NearRouteStationsRequest):

    """
    {
        "type": "LineString",
        "coordinates": [
          [
            145.123387,
            -37.906601
          ],
          [
            145.123198,
            -37.90658
          ],
          [
            145.122415,
            -37.910754
          ],
          [
            145.122068,
            -37.9127
          ],
          [
            145.1219,
            -37.913653
          ],
          [
            145.121862,
            -37.91397
          ],
          [
            145.121667,
            -37.915039
          ],
          [
            145.120829,
            -37.91937
          ],
          [
            145.120843,
            -37.919621
          ],
          [
            145.12084,
            -37.91975
          ],
          [
            145.120797,
            -37.920119
          ],
          [
            145.120759,
            -37.920336
          ],
          [
            145.120706,
            -37.920601
          ],
          [
            145.120583,
            -37.921012
          ],
          [
            145.120512,
            -37.921364
          ],
          [
            145.120484,
            -37.921484
          ],
          [
            145.120387,
            -37.921742
          ],
          [
            145.120204,
            -37.92262
          ],
          [
            145.119973,
            -37.923854
          ],
          [
            145.121433,
            -37.924959
          ],
          [
            145.122107,
            -37.925457
          ],
          [
            145.123887,
            -37.926817
          ]
        ]
      }"""

    line_shape = line.to_shape()

    # Convert to WKBElement for PostGIS
    line_geom = from_shape(line_shape, srid=7844)

    session = SessionLocal()
    try:

        stations = (
            session.query(
                TrainStation.id,
                TrainStation.name,
                func.ST_Distance(
                    cast(TrainStation.geom, Geography(srid=7844)), 
                    cast(line_geom, Geography(srid=7844))
                ).label("distance")
            )
            .filter(
                func.ST_DWithin(
                    cast(TrainStation.geom, Geography(srid=7844)),
                    cast(line_geom, Geography(srid=7844)), 
                    line.maxdistance)
            )
            .order_by("distance")
            .all()
        )
        

        results = [
            {"id": s.id, "name": s.name, "distance_m": s.distance}
            for s in stations
        ]
        return {"stations": results}

    finally:
        session.close()

class Coordinates(BaseModel):
    lat: float
    long: float

class NearLocRequest(BaseModel):

    maxdistance: int = 500
    coordinates: Coordinates


@app.post("/stations/near_location")
def stations_near_loc(req: NearLocRequest):

    # return 400 if coordinates are missing
    if not req.coordinates or req.coordinates.lat is None or req.coordinates.long is None:
        raise HTTPException(status_code=400, detail="Missing coordinates")

    point_shape = shape({
        "type": "Point",
        "coordinates": [req.coordinates.long, req.coordinates.lat]
    })
    point_geom = from_shape(point_shape, srid=7844)

    # print(req.coordinates)

    session = SessionLocal()
    try:
        stations = (
            session.query(
                TrainStation.id,
                TrainStation.name,
                TrainStation.geom,
                func.ST_Distance(
                    cast(TrainStation.geom, Geography(srid=7844)),
                    cast(point_geom, Geography(srid=7844))
                ).label("distance")
            )
            .filter(
                func.ST_DWithin(
                    cast(TrainStation.geom, Geography(srid=7844)),
                    cast(point_geom, Geography(srid=7844)),
                    req.maxdistance
                )
            )
            .order_by("distance")
            .all()
        )

        results = []
        for s in stations:
            shapely_geom = to_shape(s.geom)  # Convert WKBElement to Shapely Point
            results.append({
                "id": s.id,
                "name": s.name,
                "location": {
                    "lat": shapely_geom.y,
                    "long": shapely_geom.x
                },
                "distance_m": s.distance
            })

        return {"stations": results}
    
    finally:
        session.close()

# class ParkingNearLocReq()

@app.post('/parking/near_location')
def parking_near_loc(req: NearLocRequest):

    # return 400 if coordinates are missing
    if not req.coordinates or req.coordinates.lat is None or req.coordinates.long is None:
        raise HTTPException(status_code=400, detail="Missing coordinates")

    point_shape = shape({
        "type": "Point",
        "coordinates": [req.coordinates.long, req.coordinates.lat]
    })
    point_geom = from_shape(point_shape, srid=7844)

    session = SessionLocal()
    try:
        zones = (
            session.query(
                OsmPublicParking.id,
                OsmPublicParking.name,
                OsmPublicParking.geom,
                func.ST_Distance(
                    cast( OsmPublicParking.geom, Geography(srid=7844) ),
                    cast( point_geom, Geography(srid=7844) )
                ).label("distance")
            )
            .filter(
                func.ST_DWithin(
                    cast(OsmPublicParking.geom, Geography(srid=7844)),
                    cast(point_geom, Geography(srid=7844)),
                    req.maxdistance
                )
            )
            .order_by("distance")
            .all()
        )

        results = []
        for z in zones:
            shapely_geom = to_shape(z.geom)
            results.append({
                "id": z.id,
                "name": z.name,
                "location": {
                    "lat": shapely_geom.y,
                    "long": shapely_geom.x
                },
                "distance_m": z.dist
            })

        return {"parking_zones": results}
    
    finally:
        session.close()

@app.post("/parking/nearby")
def parking_nearby(req: NearLocRequest):

    if not req.coordinates or req.coordinates.lat is None or req.coordinates.long is None:
        raise HTTPException(status_code=400, detail="Missing coordinates")

    session = SessionLocal()
    try:
        
        centroid = func.ST_Transform(func.ST_Centroid(OsmPublicParking.geom), 7844)

        # Query the closest parking areas ordered by distance
        query = (
            session.query(
                OsmPublicParking.id,
                OsmPublicParking.name,
                OsmPublicParking.other_tags,
                func.ST_AsText(OsmPublicParking.geom).label('geom_wkt'),
                func.ST_X(centroid).label('cen_long'),
                func.ST_Y(centroid).label('cen_lat'),
                func.ST_Distance(
                    cast(OsmPublicParking.geom, Geography(srid=7844)),
                    func.ST_SetSRID(
                        func.ST_Point(req.coordinates.long, req.coordinates.lat),
                        7844
                    )
                ).label("distance")
            )
            .filter(
                func.ST_DWithin(
                    cast(OsmPublicParking.geom, Geography(srid=7844)),
                    func.ST_SetSRID(
                        func.ST_Point(req.coordinates.long, req.coordinates.lat),
                        7844
                    ),
                    req.maxdistance
                )
            )
            .order_by("distance")
        )

        results = query.all()

        if not results:
            raise HTTPException(status_code=404, detail="No parking areas found")

        # Format results to JSON
        return [
            {
                "id": r.id,
                "name": r.name,
                "other_tags": parse_hstore(r.other_tags),
                "multipolygon": r.geom_wkt,
                "centroid": {
                    "lat": r.cen_lat,
                    "long": r.cen_long
                },
                "distance_meters": r.distance
            }
            for r in results
        ]
    finally:
        session.close()

def parse_hstore(hstore_str: str):
    """
    Parse a simple Postgres hstore string like
    '"key1"=>"val1","key2"=>"val2"' into a dict.
    """
    if not hstore_str:
        return {}

    # regex to find key=>"value" pairs
    pattern = r'"([^"]+)"=>(?:"([^"]*)"|NULL)'

    matches = re.findall(pattern, hstore_str)
    return {k: (v if v != 'NULL' else None) for k, v in matches}