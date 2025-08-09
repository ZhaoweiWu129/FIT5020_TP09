
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

class OsmParkNRide(Base):
    __tablename__ = "osm_park_and_ride"
    id = Column(Integer, primary_key=True)
    geom = Column(Geometry("MULTIPOLYGON", srid=7844))
    zone_name = Column(String)
    nearest_ts_id = Column(String)
    other_tags = Column(String)

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

class NearRouteRequest(BaseModel):

    maxdistance: int = 500
    coordinates: list

    def to_shape(self):
        return shape({"type": "LineString", "coordinates": self.coordinates})

@app.post("/stations/near_route")
def stations_near_route(line: NearRouteRequest):

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

@app.post("/parking/near_location")
def parking_near_loc(req: NearLocRequest):

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
                "parking_area_multipolygon": r.geom_wkt,
                "parking_area_centroid": {
                    "lat": r.cen_lat,
                    "long": r.cen_long
                },
                "distance_meters": r.distance
            }
            for r in results
        ]
    finally:
        session.close()

@app.post("/park_ride")
def park_n_ride(req: NearRouteRequest):

    line_shape = req.to_shape()
    line_geom = from_shape(line_shape, srid=7844)

    session = SessionLocal()
    try:

        centroid = func.ST_Transform(func.ST_Centroid(OsmParkNRide.geom), 7844)

        park_and_rides = (
            session.query(
                OsmParkNRide.id,
                OsmParkNRide.zone_name,
                OsmParkNRide.nearest_ts_id,
                TrainStation.name.label('nearest_ts_name'),
                OsmParkNRide.other_tags,
                func.ST_AsText(OsmParkNRide.geom).label('geom_wkt'),
                func.ST_X(centroid).label('cen_long'),
                func.ST_Y(centroid).label('cen_lat'),
                func.ST_Distance(
                    cast(OsmParkNRide.geom, Geography(srid=7844)),
                    cast(line_geom, Geography(srid=7844))
                ).label("distance")
            )
            .join(
                TrainStation,
                OsmParkNRide.nearest_ts_id == TrainStation.id,
                isouter=False
            )
            .filter(
                func.ST_DWithin(
                    cast(OsmParkNRide.geom, Geography(srid=7844)),
                    cast(line_geom, Geography(srid=7844)),
                    req.maxdistance
                )
            )
            .order_by("distance")
            .all()
        )

        results = [
            {
                "id": p.id,
                "zone_name": p.zone_name,
                "nearest_train_station_name": p.nearest_ts_name,
                "other_tags": parse_hstore(p.other_tags),
                "nearest_station_multipolygon": p.geom_wkt,
                "nearest_station_centroid": {
                    "lat": p.cen_lat,
                    "long": p.cen_long
                },
                "distance_meters": p.distance
            }
            for p in park_and_rides
        ]

        return {"park_and_ride": results}
    
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