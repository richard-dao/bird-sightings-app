"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:

    http://127.0.0.1:8000/{app_name}/{path}

If app_name == '_default' then simply

    http://127.0.0.1:8000/{path}

If path == 'index' it can be omitted:

    http://127.0.0.1:8000/

The path follows the bottlepy syntax.

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""

import json
from py4web import action, request, abort, redirect, URL
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from py4web.utils.url_signer import URLSigner
from py4web.utils.grid import Grid, GridClassStyleBulma
from .models import get_user_email
import csv

url_signer = URLSigner(session)
drawn_coordinates = []

@action('index')
@action.uses('index.html', db, auth.user, url_signer)
def index():
    return dict(
        # COMPLETE: return here any signed URLs you need.
        my_callback_url = URL('my_callback', signer=url_signer),
        get_user_statistics_url = URL('get_user_statistics'),
        search_url = URL('search'),
        get_bird_sightings_url = URL('get_bird_sightings'),
        save_coords_url = URL('save_coords'),
    )

@action('get_bird_sightings', method=['POST'])
@action.uses(db, auth.user, url_signer)
def get_bird_sightings():
    north = request.json.get('north')
    south = request.json.get('south')
    east = request.json.get('east')
    west = request.json.get('west')

    events_in_bounds = db(
        (db.checklist.LATITUDE <= north) & 
        (db.checklist.LATITUDE >= south) &
        (db.checklist.LONGITUDE <= east) &
        (db.checklist.LONGITUDE >= west)
    ).select(db.checklist.SAMPLING_EVENT_IDENTIFIER)

    # print("Events In Bounds: ", events_in_bounds[0])

    event_ids = [event.SAMPLING_EVENT_IDENTIFIER for event in events_in_bounds]

    # print("Event Ids: ", event_ids[0])

    sightings = db(db.sightings.SAMPLING_EVENT_IDENTIFIER.belongs(event_ids)).select()

    # print("Sightings: ", sightings[0])

    sightings_list = []

    for sighting in sightings:
        event_location = db(db.checklist.SAMPLING_EVENT_IDENTIFIER == sighting.SAMPLING_EVENT_IDENTIFIER).select().first()
        if event_location:
            try:
                intensity = int(sighting.OBSERVATION_COUNT)
            except ValueError:
                intensity = 0
            sightings_list.append({
                'species': sighting.COMMON_NAME,
                'lat': event_location.LATITUDE,
                'lon': event_location.LONGITUDE,
                'intensity': intensity # Check parsing errors if OBSERVATION_COUNT == 'X'
            })

    # print("Sightings List: ", sightings_list[0:2])
    print("Loading Map...")
    return dict(sightings=sightings_list)

@action('save_coords', method='POST')
@action.uses(db, auth.user, url_signer, session)
def save_coords():
    data = request.json
    session['drawn_coordinates'] = data.get('drawing_coords')
    print("Session Drawn Coordinates", session['drawn_coordinates'])
    return 'Coordinates saved successfully.'

@action('checklist')
@action.uses('checklist.html', db, auth.user, url_signer, session)
def checklist():
    drawn_coordinates = session.get('drawn_coordinates', [])
    print("Checklist Call - Drawn Coordinates: ", drawn_coordinates)
    return dict(
        my_callback_url = URL('my_callback', signer=url_signer),
        load_user_statistics_url = URL('load_user_statistics'),
        search_url = URL('search'),
        observation_dates_url = URL('observation_dates'),
        # Richard's Note:
        # These are the coordinates for the region that the user selects on the map
        # They are of format: [{lat: 0.0, lng: 0.0}, {lat: 0.0, lng: 0.0}, ..., etc.]
        drawn_coordinates = json.dumps(drawn_coordinates),
    )

@action('submit_checklist', method='POST')
@action.uses(db, auth.user, url_signer)
def submit_checklist():
    data = request.json

    # Extract data from the request
    SAMPLING_EVENT_IDENTIFIER = data.get('SAMPLING_EVENT_IDENTIFIER')
    LATITUDE = data.get('LATITUDE')
    LONGITUDE = data.get('LONGITUDE')
    OBSERVATION_DATE = data.get('OBSERVATION_DATE')
    TIME_OBSERVATIONS_STARTED = data.get('TIME_OBSERVATIONS_STARTED')
    OBSERVER_ID = data.get('OBSERVER_ID')
    DURATION_MINUTES = data.get('DURATION_MINUTES')

    # Save the checklist to the database
    checklist_id = db.checklist.insert(
        SAMPLING_EVENT_IDENTIFIER=SAMPLING_EVENT_IDENTIFIER,
        LATITUDE=LATITUDE,
        LONGITUDE=LONGITUDE,
        OBSERVATION_DATE=OBSERVATION_DATE,
        TIME_OBSERVATIONS_STARTED=TIME_OBSERVATIONS_STARTED,
        OBSERVER_ID=OBSERVER_ID,
        DURATION_MINUTES=DURATION_MINUTES
    )

    return dict(checklist_id=checklist_id)


@action('location')
@action.uses('location.html', db, auth.user, url_signer, session)
def location():
    drawn_coordinates = session.get('drawn_coordinates', [])
    print("Location Call - Drawn Coordinates: ", type(drawn_coordinates))
    return dict(
        my_callback_url = URL('my_callback', signer=url_signer),

        # Richard's Note:
        # These are the coordinates for the region that the user selects on the map
        # They are of format: [{lat: 0.0, lng: 0.0}, {lat: 0.0, lng: 0.0}, ..., etc.]
        drawn_coordinates = json.dumps(drawn_coordinates),
    )

@action('user_statistics')
@action.uses('user_statistics.html', db, auth.user, url_signer)
def user_statistics():
    return dict(
        load_user_statistics_url = URL('load_user_statistics'),
        search_url = URL('search'),
        observation_dates_url = URL('observation_dates')
    )
    
@action('load_user_statistics')
@action.uses(db, auth.user, url_signer)
def get_user_statistics():
    query = (db.sightings.OBSERVATION_COUNT.regexp('^[0-9]+$')) & (db.sightings.OBSERVATION_COUNT.cast('integer') > 0)

    common_names = db(query).select(db.sightings.COMMON_NAME, distinct=True).as_list()
    print("user statistics contains all birds")
    return dict(common_names = common_names)

@action('search', method=["POST"])
@action('search')
@action.uses(db, auth.user, url_signer)
def search():
    data = request.json  # Get the JSON payload
    q = data.get("params", {}).get("q")  # Extract 'q' from 'params'
    print("query", q)
    if not q:
        common_names = db(query).select(db.sightings.COMMON_NAME, distinct=True).as_list()
        print("user statistics contains all birds")
        return dict(common_names = common_names)
    
    query = (db.sightings.OBSERVATION_COUNT.regexp('^[0-9]+$')) & (db.sightings.OBSERVATION_COUNT.cast('integer') > 0)
    query &= (db.sightings.COMMON_NAME.contains(q))
    
    common_names = db(query).select(db.sightings.COMMON_NAME, distinct=True).as_list()
    print("searched by query" , q)
    return dict(common_names=common_names)
    
@action('observation_dates', method=["POST"]) 
@action('observation_dates')
@action.uses(db, auth.user, url_signer)
def observation_date():
    data = request.json
    common_name = data.get("common_name")
    print("retrieving observation dates by ", common_name)
    if not common_name:
        print("ERROR: common_name not found")
        return dict(observation_dates=[])
    
    query = (db.sightings.COMMON_NAME == common_name) & (db.sightings.SAMPLING_EVENT_IDENTIFIER == db.sightings.SAMPLING_EVENT_IDENTIFIER)
    observation_dates = db(query).select(db.checklist.OBSERVATION_DATE).as_list()
    print("observation_dates: ", observation_dates)
    return dict(observation_dates=observation_dates)

@action('my_callback')
@action.uses() # Add here things like db, auth, etc.
def my_callback():
    # The return value should be a dictionary that will be sent as JSON.

    if db(db.species).isempty():
        with open('species.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                species = db.species.insert(name=row[0])
    if db(db.sightings).isempty():
        with open('sightings.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                sightings = db.sightings.insert(name=row[0],
                                                bird_count=row[1])
    if db(db.checklist).isempty():
        with open('checklist.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                checklist = db.sightings.insert(name=row[0])

    return dict(my_value=3, species = species, sightings = sightings, checklist = checklist)


