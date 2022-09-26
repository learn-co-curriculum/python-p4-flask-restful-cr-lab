import json

from app import app
from models import db, Plant

class TestPlant:
    '''Flask application in app.py'''

    def test_plants_get_route(self):
        '''has a resource available at "/plants".'''
        response = app.test_client().get('/plants')
        assert(response.status_code == 200)

    def test_plants_get_route_returns_list_of_plant_objects(self):
        '''returns JSON representing Plant objects at "/plants".'''
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

    def test_plants_post_route_creates_plant_record_in_db(self):
        '''allows users to create Plant records through the "/plants" POST route.'''
        response = app.test_client().post(
            '/plants',
            json = {
                "name": "Live Oak",
                "image": "https://www.nwf.org/-/media/NEW-WEBSITE/Shared-Folder/Wildlife/Plants-and-Fungi/plant_southern-live-oak_600x300.ashx",
                "price": 250.00,
            }
        )

        with app.app_context():
            lo = Plant.query.filter_by(name="Live Oak").first()
            assert(lo.id)
            assert(lo.name == "Live Oak")
            assert(lo.image == "https://www.nwf.org/-/media/NEW-WEBSITE/Shared-Folder/Wildlife/Plants-and-Fungi/plant_southern-live-oak_600x300.ashx")
            assert(lo.price == 250.00)

            db.session.delete(lo)
            db.session.commit()

    def test_plant_by_id_get_route(self):
        '''has a resource available at "/plants/<int:id>".'''
        response = app.test_client().get('/plants/1')
        assert(response.status_code == 200)

    def test_plant_by_id_get_route_returns_one_plant(self):
        '''returns JSON representing one Plant object at "/plants/<int:id>".'''
        response = app.test_client().get('/plants/1')
        data = json.loads(response.data.decode())

        assert(type(data) == dict)
        assert(data["id"])
        assert(data["name"])
                