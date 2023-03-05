import json
import os
import pytz
from datetime import datetime, timedelta
import time


central = pytz.timezone("US/Central")
current_time = datetime.now(central)

# Get the path to the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Specify the file path relative to the current directory
file_path = os.path.join(current_dir, 'data.json')

# Open the file in read mode
with open(file_path, 'r', encoding="utf8") as file:
    # Load the JSON data from the file
    data = json.load(file)

# Extract the Time values from the Schedule list
times = [item['Time'] for item in data['Schedule'] if 'Time' in item]
location = [item['Stop'] for item in data['Schedule'] if 'Stop' in item]
day = [item['Day'] for item in data['Schedule'] if 'Day' in item]
stop = [item['Stop'] for item in data['Schedule'] if 'Stop' in item]

#Phone Number variable
phone_number = data['Phone Number']
#Times per day
timesM = times[0]
timesT = times[1]
timesW = times[2]
timesR = times[3]
timesF = times[4]
#Locations per Day
locationM = location[0]
locationT = location[1]
locationW = location[2]
locationR = location[3]
locationF = location[4]

current_time = current_time.strftime("%H:%M")


timesM.append(to_military_time(datetime.strptime(timesM, '%I:%M%p') - timedelta(minutes=45)))


timeM = military_times[0]
timeT = military_times[1]
timeW = military_times[2]
timeR = military_times[3]
timeF = military_times[4]

DayM = day[0]
DayT = day[1]
DayW = day[2]
DayR = day[3]
DayF = day[4]

stopM = stop[0]
stopT = stop[1]
stopW = stop[2]
stopR = stop[3]
stopF = stop[4]



#Loop to continuously check users schedules
while True:
    
    current_time = datetime.now(central)
    current_day = current_time.strftime("%A")
    current_time = current_time.strftime("%H:%M")

    if current_day == DayM and current_time == timeM:
        print("IT IS WORKING")
        #SEND STOPM to transitland
        # Call your function to send API request for Monday's schedule

    elif current_day == DayT and current_time == timeT:
        print("It's time for Tuesday's schedule")
        # Call your function to send API request for Tuesday's schedule

    elif current_day == DayW and current_time == timeW:
        print("It's time for Wednesday's schedule")
        # Call your function to send API request for Wednesday's schedule

    elif current_day == DayR and current_time == timeR:
        print("It's time for Thursday's schedule")
        # Call your function to send API request for Thursday's schedule

    elif current_day == DayF and current_time == timeF:
        print("It's time for Friday's schedule")

    time.sleep(20)