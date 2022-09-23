import json
from os import environ
import re

from app import app
from models import db, Plant

class TestPlant:
    '''Flask application in app.py'''

    def test_plants_route(self):
        '''has a resource available at "/plants".'''
        response = app.test_client().get('/plants')
        assert(response.status_code == 200)

    def test_plants_route_returns_list_of_plant_objects(self):
        '''returns JSON representing Plant objects.'''
        with app.app_context():
            p = Plant(name="Douglas Fir")
            db.session.add(p)
            db.session.commit()

            response = app.test_client().get('/plants')
            data = json.loads(response.data.decode())
            assert(type(data) == list)
            for record in data:
                assert(type(record) == dict)
                assert(record['id'])
                assert(record['name'])

            db.session.delete(p)
            db.session.commit()

    def test_plant_by_id_route(self):
        '''has a resource available at "/plants/<int:id>".'''
        response = app.test_client().get('/plants/1')
        assert(response.status_code == 200)
