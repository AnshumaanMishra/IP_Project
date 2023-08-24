from matplotlib import pyplot as plt
import pandas as pd
from datetime import datetime as dt
from datetime import timedelta
import re

# Convert 12 hour to 24 Hour Format
def convert24(time):
    t = dt.strptime(time, '%I:%M %p')
    return t.strftime('%H:%M')

# Load Data
flight_data = pd.read_csv('flight_data.csv')

# Input
id = input("Enter Flight ID: ")

#FInd Flight using ID
extracted_data = flight_data[flight_data['Flight_No']==id]

# Regex to extract Time
timeRegex = re.compile('..:.. .m')

# Find index corresponding to flight
imdex = flight_data['Flight_No']==id
index = 0
for j in range(0, len(imdex)):    
    if imdex.iat[j]==True:
        index = j
        break

# Convert Arrival and Departure to Datetime
extract = convert24(re.findall(timeRegex, extracted_data.Departure[index])[0].strip())
depart = dt.strptime(extract, '%H:%M')

extract = convert24(re.findall(timeRegex, extracted_data.Arrival[index])[0].strip())
arrival = dt.strptime(extract, '%H:%M')

now = dt.strptime(dt.now().strftime("%H:%M"),'%H:%M')

# Status Finder
status = ''
statindex = 0

# For 12 AM flights
if arrival<depart:
    arrival += timedelta(hours=24)

# Main code
if now < depart:
    status = 'Not Yet Started'

elif now > arrival: 
    status = 'FLight Has Landed At Its Destination'

else:
    statindex = (now-depart)/(arrival-depart)
    status = 'Flight In Progress'

# Stops = Sections of markers - 1
stops = extracted_data.Stops[index]
sections = 1/(stops+1)

# Create List for X coordinates
i = 0 
a1 = list()
while i <= 1:
    a1.append(i)
    i += sections

# Plotting
print(status)

# Stops
plt.plot(a1, [5]*len(a1), marker='o')

# Current Location
plt.plot([statindex], [5], marker='X', markeredgecolor='k')
plt.legend(['Path', 'Current Location'])
plt.show()
