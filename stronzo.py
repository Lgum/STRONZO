__author__ = 'David'

import datetime

import sys
sys.path.append('/home/lgum/BitBucket/stravalib')
import stravalib
import requests
import json
import unicodedata
from stravalib import protocol
import numpy as np
from bokeh.plotting import figure, output_file, show, vplot
# import h5py

# from stravalib import Client
# client = Client()
# # url = client.authorization_url(client_id=10889082,
# #                                redirect_uri='http://myapp.example.com/authorization')
#
# url = client.authorization_url(client_id=10889082,
#                                redirect_uri='http://127.0.0.1:5000/authorization')
#
# access_token = client.exchange_code_for_token(client_id=10889082,
#                                               client_secret=MY_STRAVA_CLIENT_SECRET,
#                                               code=code)

from stravalib.client import Client

# test = np.load('/home/lgum/BitBucket/STRONZO/efforts.npz')

with open('/home/lgum/BitBucket/STRONZO/credentials.json', 'r') as credentials_file:
    credentials = json.load(credentials_file)


client = Client()

# authorize_url = client.authorization_url(client_id=10889082,
#                                redirect_uri='http://localhost:8282/authorized')
authorize_url = client.authorization_url(client_id=credentials['client_id'],
                               redirect_uri='http://localhost:8282/authorized')
# Have the user click the authorization URL, a 'code' param will be added to the redirect_uri
# .....
# Extract the code from your webapp response
# code = requests.get('code') # or whatever your framework does

access_token = str(credentials['access_token'])

# Now store that access token somewhere (a database?)
client.access_token = access_token
athlete = client.get_athlete()

# datetime.datetime(2005, 7, 14, 12, 30)
# start = datetime.datetime(2015, 10, 1, 0, 0)
# end = datetime.datetime(2015, 11, 20, 0, 0)

# activities = client.get_activities(end, start)
# gets all activities
#activity = client.get_activity(428095411, True)

#types = ['time', 'latlng', 'altitude', 'heartrate', 'temp', ]

#streams = client.get_activity_streams(428095411)
# protocol.get('/activities/{id}', id=activity_id,
  #                               include_all_efforts=include_all_efforts)
# activities = client.get_activities()

datetime.datetime(2005, 7, 14, 12, 30)
start = datetime.datetime(2016, 1, 1, 0, 0)
end = datetime.datetime(2016, 1, 3, 0, 0)

activities = client.get_activities(end, start)
STRONZO = list(activities)
types = ['time', 'latlng', 'altitude', 'heartrate', 'temp', 'segments', 'segment']

# get all streams and push efforts into array
segment_array = []
stream_types = ['time', 'latlng', 'distance', 'altitude', 'velocity_smooth', 'heartrate', 'cadence', 'watts', 'temp', 'moving', 'grade_smooth']
iterator = 0

for entry in STRONZO:
    print (float(iterator) / float(len(STRONZO)))
    iterator += 1
    activity = client.get_activity(entry.id, True)
    # stream = client.get_activity_streams(entry.id, stream_types)
    # segment_array.append(stream)
    if activity.segment_efforts:
        for efforts in activity.segment_efforts:
            # segment_activity.effort_stream = client.get_effort_streams(efforts.id, stream_types)
            # segment_activity = client.get_effort_streams(efforts.id, stream_types)
            # segment_activity.activity_id = activity.id
            # segment_activity.effort_id = efforts.id
            for leaderboard_entry in efforts.segment.leaderboard.entries:
                segment_activity = client.get_effort_streams(leaderboard_entry.effort.id, stream_types)
                segment_array.append({
                    'id': leaderboard_entry.effort.id,
                    'name': leaderboard_entry.athlete_name,
                    'streams': segment_activity
                })



ActivityArray = np.asarray(segment_array)

np.savez('/home/lgum/BitBucket/STRONZO/efforts.npz', ActivityArray)
test = np.load('/home/lgum/BitBucket/STRONZO/efforts.npz')

p = figure(width=500, height=500)
output_file('/home/lgum/BitBucket/STRONZO/lines.html', title='line plot example')
p.circle(np.linspace(0, len(segment_array[0]['streams']['heartrate'].data), len(segment_array[0]['streams']['heartrate'].data)), segment_array[0]['streams']['heartrate'].data, size=7, color="firebrick", alpha=0.5)
show(p)
# h5f = h5py.File('/home/lgum/BitBucket/STRONZO/activities.h5', 'w')
# h5f.create_dataset('segment_effort_array', ActivityArray)
# h5f.close()

print("For {id}, I now have an access token {token}".format(id=athlete.id, token=access_token))