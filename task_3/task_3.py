from flask import Flask, request
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, Float
from dataclasses import dataclass
from typing import Any, Dict

Base = declarative_base()


class House(Base):
    __tablename__ = 'houses'

    house_id = Column(Integer, nullable=False,  primary_key=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    family_count = Column(Integer)

    def __init__(self, house_id: int, latitude: float, longitude: float, family_count: Any = None):
        self.house_id = house_id
        self.latitude = latitude
        self.longitude = longitude
        self.family_count = family_count

    def __repr__(self):
        return f"""
            "house_id": {self.house_id},
            "latitude": {self.latitude},
            "longitude": {self.longitude},
            "family_count": {self.family_count}
        """

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False


@dataclass
class RequestBody:
    """
        Класс для удобного хранения полученного тела запроса
    """
    house_id: int
    latitude: float
    longitude: float
    family_count: Any

    def to_dict(self) -> Dict[str, Any]:
        return {
            "house_id": self.house_id,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "family_count": self.family_count
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "RequestBody":
        house_id = d["house_id"]
        latitude = d["latitude"]
        longitude = d["longitude"]
        if len(d) == 4:
            family_count = d["family_count"]
        else:
            family_count = None
        return RequestBody(house_id, latitude, longitude, family_count)


engine = create_engine(f'sqlite:///houses.sqlite')
session = sessionmaker(bind=engine)
s = session()
app = Flask(__name__)


@app.route('/', methods=['POST'])
def data_house():
    data = request.get_json()
    body = RequestBody.from_dict(data)
    house = s.query(House).filter(House.house_id == body.house_id).first()
    if house:
        house.latitude = body.latitude
        house.longitude = body.longitude
        house.family_count = body.family_count
    else:
        new_house = House(
            house_id=body.house_id,
            latitude=body.latitude,
            longitude=body.longitude,
            family_count=body.family_count
        )
        s.add(new_house)
    s.commit()
    return str(body.house_id)


if __name__ == '__main__':
    db_is_created = os.path.exists("houses.sqlite")
    if not db_is_created:

        Base.metadata.create_all(engine)
    app.run(host='0.0.0.0', port=8000, debug=False)
