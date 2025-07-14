import requests


stationDetailHeaders = {'X-Requested-Alias': 'rally.fetchRoutes'}
stationsHeaders = {
    'X-Requested-Alias': 'rally.startStations',
    'User-Agent': 'Mozilla/5.0 (compatible; WebRequests/1.0)'
}


def get_json_from_url(url, headers):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error getting data from {url}: {response.text} with status code {response.status_code} and headers {headers}")
        return None

def notify(message):
    url = 'https://ntfy.sh/reid-02-17-2024'

    response = requests.post(url, data=message.encode(encoding='utf-8'))

    if response.status_code == 200:
        print(f"Message sent successfully: {message}")
    else:
        print(f"Error sending message: {response.text}")


def get_trips():
    notifications = []
    stations = get_json_from_url('https://booking.roadsurfer.com/api/en/rally/stations', stationsHeaders)
    import ipdb; ipdb.set_trace()

    desired_cities = [
        "Amsterdam",
        "Rotterdam",
    ]


    if stations:
        for station in stations:
            if station['one_way'] is True:
                if station['name'] in desired_cities:
                    # notify
                    station_detail = get_json_from_url(f"https://booking.roadsurfer.com/api/en/rally/stations/{station['id']}", stationDetailHeaders)
                    if station_detail:
                        return_ids = station_detail['returns']
                        for id in return_ids:
                            station_detail = get_json_from_url(f"https://booking.roadsurfer.com/api/en/rally/stations/{str(id)}", stationDetailHeaders)
                            if station_detail:
                                notifications.append(f"There is a trip from {station['name']} to {station_detail['name']}")


                station_detail = get_json_from_url(f"https://booking.roadsurfer.com/api/en/rally/stations/{station['id']}", stationDetailHeaders)
                if station_detail:
                    return_ids = station_detail['returns']
                    for id in return_ids:
                        station_detail = get_json_from_url(f"https://booking.roadsurfer.com/api/en/rally/stations/{str(id)}", stationDetailHeaders)
                        if station_detail:
                            if station_detail['name'] in desired_cities:
                                notifications.append(f"There is a trip from {station['name']} to {station_detail['name']}")
    return notifications


def main():
    import time as sleeptime
    from datetime import datetime, time

    def is_time_between(begin_time, end_time, check_time=None):
        # If check time is not given, default to current UTC time
        check_time = check_time or datetime.utcnow().time()
        if begin_time < end_time:
            return check_time >= begin_time and check_time <= end_time
        else: # crosses midnight
            return check_time >= begin_time or check_time <= end_time


    trips_notified = []
    while True:
        try:
            # run every 60 minute
            while True:
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                print("Starting Current Time =", current_time)

                # if time is between 1:30-1:30am
                if is_time_between(time(3,00), time(4,10)):
                        trips_notified = []
                        open('log.txt', 'w').close()
                        sleeptime.sleep(80*60)
                        continue

                trips = get_trips()
                for trip in trips:
                    if trip not in trips_notified:
                        if is_time_between(time(8,00), time(23,30)):
                            print(f"notify: {trip}")
                            notify(f"Roadsurfer: {trip}")
                            trips_notified.append(trip)

                sleeptime.sleep(3600)

        except Exception as e:
            print(e)
            print("trying again")
            sleeptime.sleep(60)



if __name__ == "__main__":
    main()
