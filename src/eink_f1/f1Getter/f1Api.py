import requests
from datetime import datetime
from datetime import timezone
from time import sleep

class F1getter:
    def __init__(self):
        self.base_url = "https://api.openf1.org/v1/"
        self.session_ind = "none"

    def current_year_as_string(self):
        from datetime import datetime
        return str(datetime.now().year)

    def get_next_race(self):
        current_year = self.current_year_as_string()
        current_week_date = datetime.today().replace(day=datetime.today().day - datetime.today().weekday()).strftime('%Y-%m-%d')
        url = f"{self.base_url}meetings?year={current_year}&date_start>={current_week_date}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            #get first race in the list of meetings
            if data:
                output = []
                output.append({
                    "meeting_key": data[0].get("meeting_key"),
                    "meeting_name": data[0].get("meeting_name"),
                    "meeting_official_name": data[0].get("meeting_official_name"),
                    "date_start": data[0].get("date_start"),
                    "date_end": data[0].get("date_end"),
                    "gmt_offset": data[0].get("gmt_offset"),
                    "is_cancelled": data[0].get("is_cancelled", False),
                    "circuit_short_name": data[0].get("circuit_name"),
                    "circuit_image": data[0].get("circuit_image"),
                    "circuit_type": data[0].get("circuit_type"),
                    "country_flag": data[0].get("country_flag"),
                    "country_name": data[0].get("country_name")
                })
                next_race = data[0]
                return next_race
            else:
                return None
        else:
            return None

    def get_next_session(self, meeting_key):#

        def get_weather_data(meeting_key, session_key):
            url = f"{self.base_url}weather?meeting_key={meeting_key}&session_key={session_key}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if data:
                    return data[0]
                else:
                    return None
            else:
                return None

        current_utc_time = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        url = f"{self.base_url}sessions?meeting_key={meeting_key}&date_start>={current_utc_time}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data:
                output = []
                next_session = data[0]

                weather_data = get_weather_data(meeting_key, next_session.get("session_key"))

                output.append({
                    "session_key": next_session.get("session_key"),
                    "session_name": next_session.get("session_name"),
                    "date_end": next_session.get("date_end"),
                    "date_start": next_session.get("date_start"),
                    "gmt_offset": next_session.get("gmt_offset"),
                    "is_cancelled": next_session.get("is_cancelled", False),
                    "weather_data": weather_data
                })
                return output
            else:
                return None
        else:
            return None

    def get_session_by_name(self, session_name, meeting_key):
        url = f"{self.base_url}sessions?meeting_key={meeting_key}&session_name={session_name}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data:
                data = {
                    "session_key": data[0].get("session_key"),
                    "session_name": data[0].get("session_name"),
                    "date_end": data[0].get("date_end"),
                    "date_start": data[0].get("date_start"),
                    "gmt_offset": data[0].get("gmt_offset")
                }
                return data
            else:
                return None
        else:
            return None

    def get_session_results(self, session_key, meeting_key):
        url = f"{self.base_url}session_result?session_key={session_key}&meeting_key={meeting_key}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            output = []
            sleep(1)
            drivers_info = self.get_drivers_info(session_key, meeting_key)
            if drivers_info is None:
                drivers_info = []
            print(f"Drivers info: {drivers_info}")
            for result in data:
                #get driver info for each result
                driver_id = result.get("driver_number")
                driver_info = next((driver for driver in drivers_info if driver.get("driver_number") == driver_id), None)
                output.append({
                    "position": result.get("position"),
                    "driver_number": driver_id,
                    "driver_info": driver_info if driver_info else {},
                    "time": result.get("duration"),
                    "DNF": any(
                            str(result.get(field, "")).lower() == "true"
                            for field in ("dnf", "dns", "dsq")
                            ),
                    "position": result.get("position")
                })
            return output
        else:
            return None

    def get_drivers_info(self,session_key ,meeting_key):
        url = f"{self.base_url}drivers?session_key={session_key}&meeting_key={meeting_key}"
        response = requests.get(url)
        if response.status_code == 200:
            #get full_name, headshot_url, team_name, team_colour, name_acronym, driver_number
            output = []
            data = response.json()
            for driver in data:
                driver_info = {
                    "full_name": driver.get("full_name", ""),
                    "headshot_url": driver.get("headshot_url", ""),
                    "team_name": driver.get("team_name", ""),
                    "team_colour": driver.get("team_colour", ""),
                    "name_acronym": driver.get("name_acronym", ""),
                    "driver_number": driver.get("driver_number", "")
                }
                output.append(driver_info)
                print(f"Driver info: {driver_info}")
            return output
        else:
            return None
