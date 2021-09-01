from unittest import TestCase
from typing import Any, Dict
import requests
from task_3 import House
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(f'sqlite:///houses.sqlite')
session = sessionmaker(bind=engine)
s = session()


class SystemTest(TestCase):
    def _check_working_app(self, body: Dict[str, Any], expected: House):
        url = "http://localhost:8000/"
        response = requests.post(url, json=body)
        query = s.query(House).filter(House.house_id == response.text).first()
        self.assertEqual(query.house_id, expected.house_id)
        self.assertEqual(query.latitude, expected.latitude)
        self.assertEqual(query.longitude, expected.longitude)
        self.assertEqual(query.family_count, expected.family_count)

    def test_add_entry_to_the_table(self):
        body = get_body(15, 47.85, 45.18, 3)
        expected = House(15, 47.85, 45.18, 3)
        self._check_working_app(body, expected)

    def test_update_entry_to_the_table(self):
        body = get_body(15, 50.85, 50.18, 3)
        expected = House(15, 50.85, 50.18, 3)
        self._check_working_app(body, expected)

    def test_add_entry_not_have_field_family_count(self):
        body = get_body(16, 22.18, 23.15)
        expected = House(16, 22.18, 23.15)
        self._check_working_app(body, expected)

    def test_update_entry_not_have_field_family_count(self):
        body = get_body(16, 25.88, 25.55)
        expected = House(16, 25.88, 25.55)
        self._check_working_app(body, expected)


def get_body(house_id: int, latitude: float, longitude: float, family_count: Any = None) -> Dict[str, Any]:
    """
        Возвращает тело запроса
    """
    return {
        "house_id": house_id,
        "latitude": latitude,
        "longitude": longitude,
        "family_count": family_count
    }
