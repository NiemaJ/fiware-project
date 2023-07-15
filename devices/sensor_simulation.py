import json
import requests

class Sensor():
    "This class will mimic a real sensor"

    def create(self):

        url = 'http://localhost:8080/api/2/things'

        headers = {
            'Content-Type': 'application/json'
        }

        data = json.dumps(
            {
                "definition": "digital-twin:sensor:2.1.0",
                "features": {
                    "sensor": {
                        "definition": [
                            "dtwin:sensor:1.0.0"
                        ],
                        "properties": {
                            "temperature": 0.0,
                            "et0": 0.0,
                            "pluviometry": 0.0,
                            "relativehumidiry": 0.0,
                            "soilmoisturetotal": 0.0,
                            "soiltemperature": 0.0,
                            "winddirection": 0.0,
                            "windspeed": 0.0,
                            "hour": 0,
                            "day": 0,
                            "month": 0,
                            "year": 0
                        }
                    }
                }
            }
        )

        auth = ('ditto', 'ditto')

        response = requests.post(
            url=url,
            headers=headers,
            data=data,
            auth=auth
        )

        if response.status_code > 200:
            print(response.status_code)

    def update(self):

        url = 'http://localhost:8080/api/2/things/org.eclipse.ditto:f2c5c1cf-88c7-468c-93db-84393aab4e03'

        headers = {
            'Content-Type': 'application/json'
        }

        data = json.dumps(
            {
                "definition": "digital-twin:sensor:2.1.0",
                "features": {
                    "sensor": {
                        "definition": [
                            "dtwin:sensor:1.0.0"
                        ],
                        "properties": {
                            "et0": 6.2,
                            "pluviometry": 0,
                            "relativehumidity": 55.2,
                            "soilmoisturetotal": 48.19,
                            "soiltemperature": 28.399,
                            "winddirection": 148.9,
                            "windspeed": 1.5,
                            "temperature": 26,
                            "hour": 15,
                            "day": 6,
                            "month": 9,
                            "year": 2021
                        }
                    }
                }
            }
        )

        auth = ('ditto', 'ditto')

        response = requests.put(
            url=url,
            headers=headers,
            data=data,
            auth=auth,
            timeout=1
        )

        if response.status_code != 200:
            print(response.status_code)

        print(response.headers)

    def send_message(self):

        url = 'http://localhost:8080/api/2/things/org.eclipse.ditto:f2c5c1cf-88c7-468c-93db-84393aab4e03/features/sensor/inbox/messages/update'

        headers = {
            'Content-Type': 'application/json'
        }

        data = json.dumps(
            {
                "definition": "digital-twin:sensor:2.1.0",
                "features": {
                    "sensor": {
                        "definition": [
                            "dtwin:sensor:1.0.0"
                        ],
                        "properties": {
                            "et0": 6.2,
                            "pluviometry": 0,
                            "relativehumidity": 55.2,
                            "soilmoisturetotal": 48.19,
                            "soiltemperature": 28.399,
                            "winddirection": 148.9,
                            "windspeed": 1.5,
                            "temperature": 26,
                            "hour": 15,
                            "day": 6,
                            "month": 9,
                            "year": 2021
                        }
                    }
                }
            }
        )

        auth = ('ditto', 'ditto')

        try:
            requests.post(
                url=url,
                headers=headers,
                data=data,
                auth=auth,
                timeout=0.01
            )
        except requests.ReadTimeout:
            print("Value added correctly")

sensor = Sensor()

#sensor.create()
#sensor.update()
sensor.send_message()