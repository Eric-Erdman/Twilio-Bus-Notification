import json
import urllib.request
import os
import pytz
from datetime import datetime, timedelta
import time
from twilio.rest import Client
from dataclasses import dataclass

from secret import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN

central = pytz.timezone("US/Central")

# This is the schedule stored in memory
schedule = {}
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']

stop_names: dict = {
    2: "Langdon & N Park (WB)",
    3: "Observatory & Bascom (WB)",
    4: "Observatory & N Charter (WB)",
    5: "Linden & N Charter (WB)",
    6: "Linden & Henry (WB)",
    7: "Linden & Babcock (WB)",
    8: "Observatory & Babcock (WB)",
}

stop_urls: dict = {
    2: "s-dp8mj9sz3r-langdon~nparkwb",
    3: "s-dp8mj9dpze-observatory~bascomwb",
    4: "s-dp8mj9bb9h-observatory~ncharterwb",
    5: "s-dp8mj3xe4p-linden~ncharterwb",
    6: "s-dp8mj3t7d3-linden~henrywb",
    7: "s-dp8mj3eg89-linden~babcockwb",
    8: "s-dp8mj3g6ux-observatory~babcockwb",
}

def set_schedule(new_schedule: dict):
    """
    Parses the JSON file and returns a BusSchedule object.
    Input format: {'phone_number': '+15075200656', 'schedule': {'monday': {'time': '3:33pm', 'stop': '2'}, 'tuesday': {'time': '3:33pm', 'stop': '5'}, 'wednesday': {'time': '3:33pm', 'stop': '3'}, 'thursday': {'time': '3:33pm', 'stop': '8'}, 'friday': {'time': '3:33pm', 'stop': '5'}}}
    """

    schedule = new_schedule

    return 1


def send_text_message(phone_number: str, stop: str = "3", minutes: int = 10):
    account_sid = TWILIO_ACCOUNT_SID
    auth_token = TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)
    # Send text message using twilio
    
    message = client.messages.create(
        body=f"Bus is leaving in {minutes} minutes at stop {stop}",
        from_="+15676777869",
        to=phone_number
    )
    
    print(message.sid)

def get_transitland_data(stop_url: str):
    """Queries the Transitland API for the next bus arrival time at the given stop."""

    # print(stop_url)
    url = "https://transit.land/api/v2/rest/stops/" + stop_url + \
        "/departures?apikey=k5HqkAgVTVNIGoPpbPzYEDoLcNizhsRe"

    with urllib.request.urlopen(url) as response:
        json_data = response.read()

    """
    Response format:
    b'{"stops":[{"departures":[{"arrival":{"delay":null,"estimated":"11:48:00","estimated_utc":"2023-03-05T17:48:00Z","scheduled":"11:48:00","uncertainty":null},"arrival_time":"11:48:00","continuous_drop_off":null,"continuous_pickup":null,"departure":{"delay":null,"estimated":"11:48:00","estimated_utc":"2023-03-05T17:48:00Z","scheduled":"11:48:00","uncertainty":null},"departure_time":"11:48:00","drop_off_type":1,"interpolated":null,"pickup_type":0,"service_date":"2023-03-05","shape_dist_traveled":0,"stop_headsign":"MEMORIAL UNION: VIA EAGLE HTS","stop_sequence":1,"timepoint":1,"trip":{"bikes_allowed":1,"block_id":"203017","direction_id":0,"frequencies":[],"id":1928671352,"route":{"agency":{"agency_id":"MMT","agency_name":"Metro Transit-City of Madison","id":333376,"onestop_id":"o-dp8m-metrotransit~cityofmadison"},"continuous_drop_off":null,"continuous_pickup":null,"id":20000534,"onestop_id":"r-dp8mj-80","route_color":"CE2A1E","route_desc":"Daily schedule trips operate at least every 50 minutes. Additional weekday schedule trips operate at least every 15 minutes from approximately 7 AM until 6 PM. Limited trips operate on Holidays.","route_id":"10395","route_long_name":"","route_short_name":"80","route_text_color":"000000","route_type":3,"route_url":"http://www.cityofmadison.com/metro/routes-schedules/route-80"},"shape":{"generated":false,"id":95531373,"shape_id":"62305"},"stop_pattern_id":152,"timestamp":"2023-03-05T17:01:44Z","trip_headsign":"MEMORIAL UNION: VIA EAGLE HTS","trip_id":"1125122","trip_short_name":"","wheelchair_accessible":1}}],"feed_version":{"feed":{"id":216,"onestop_id":"f-dp8m-metrotransit~cityofmadison"},"fetched_at":"2023-02-07T23:00:47.36167Z","id":307058,"sha1":"6b5041eec24c860e6443e1fcac07f8a066818362"},"geometry":{"coordinates":[-89.400154,43.075933],"type":"Point"},"id":432943781,"location_type":0,"onestop_id":"s-dp8mj9sz3r-langdon~nparkwb","parent":null,"platform_code":null,"stop_code":"0010","stop_desc":"This stop (#0010) is westbound on the 898 block of Langdon St nearside Park St (n)","stop_id":"10","stop_name":"Langdon \\u0026 N Park (WB)","stop_timezone":"","stop_url":"","tts_stop_name":null,"wheelchair_boarding":1,"zone_id":""}]}'
    """

    data = json.loads(json_data)

    return data

def get_next_time(data, stop: str = "3", bus: str = "80") -> datetime:

    # TODO parse data variable to find next bus arrival time

    # return a datetime object of the next bus arrival time

    return datetime.now(central)+timedelta(minutes=7)


def get_bus_schedule(stop: str = "3", bus: str = "80"):
    """Queries the Transitland API for the next bus arrival time at the given stop."""

    try:
        stop_number = int(stop)
    except ValueError:
        print("Invalid stop number")
        return

    # TODO: set stop_number based on stored schedule variable rather than assuming stop 3

    # this will change. It will be based off of what the user selected in the GUI
    stop_url = stop_urls[stop_number]

    transitland_data = get_transitland_data(stop_url)
    
    bus_time = get_next_time(transitland_data, stop, bus)
    current_time = datetime.now(central)

    print(f"Bus is scheduled to leave at {bus_time} and it is currently {current_time}")

    # if bus is within 10 minutes of leaving
    d = bus_time - current_time
    print(f"Bus is scheduled to leave in {d} minutes")

    if d < timedelta(minutes=30):
        # Send text message
        minutes = int(d.total_seconds() / 60)
        send_text_message(phone_number="+16083773043", stop=stop, minutes=minutes)
        print("Text message sent")

    send_text_message(phone_number="+16083773043", stop=stop, minutes=10)
    print("Text message sent")


"""

def run():
    #Phone Number variable
    phone_number = schedule['phone_number']

    for day in days:
        # Convert schedule[day][time] to datetime object
        bus_time = datetime.strptime(schedule[day]['time'], '%I:%M%p')

        # Get current time
        current_time = datetime.now(central)

        # if bus is scheduled to leave in the next 10 minutes
        if bus_time - current_time < timedelta(minutes=30):
            # Send text message
            send_text_message(phone_number, schedule[day]['stop'])
            

def run():
    # Extract arrival times from JSON data for the 80 bus
    #define body1 as an array
    body1 = ""
    i = 0

    root_node = json.loads(json_data)
    stops_node = root_node["stops"]
    for stop_node in stops_node:
        departures_node = stop_node["departures"]
        for departure_node in departures_node:
            arrival_time_node = departure_node["arrival_time"]
            trip_node = departure_node["trip"]
            route_node = trip_node["route"]
            route_short_name = route_node["route_short_name"]
            print (route_short_name)
            if route_short_name == bus:
                arrival_time = arrival_time_node
                body1 += ("Arrival time for the " + bus + " bus: " + arrival_time + " at " + stopFinder2(stop_url)) + "\n"
                #print (body1)
                
"""
