import pandas as pd
import datetime
import time
import requests
import json
from database_connector import DatabaseConnector

class ExcelLoader():
    "This class will load excel files' data into the system."

    _FEATURES = [
        'et0', 'pluviometry', 'relativehumidity', 'soilmoisturetotal', 'soiltemperature', 
        'winddirection', 'windspeed', 'temperature', 'hour', 'day', 'month', 'year'
        ]
    
    def __init__(self):
        "Constructor."

        self.database = DatabaseConnector()

    def insert_into_database(self, data):
        "This method will insert the given data into the database"

        date_time = datetime.datetime(data[11], data[10], data[9], data[8], 0, 0)
        t_epoch = int(time.mktime(date_time.timetuple()))

        processed_data = {
            'temperature': data[7],
            'et0': data[0],
            'pluviometry': data[1],
            'relativehumidity': data[2],
            'soilmoisturetotal': data[3],
            'soiltemperature': data[4],
            'winddirection': data[5],
            'windspeed': data[6],
            't_hour': data[8],
            't_day': data[9],
            't_month': data[10],
            't_year': data[11],
            't_epoch': t_epoch
        }

        self.database.insert_into_real_values(processed_data)

    def notify_ditto(self, data):
        "This method will send a message to ditto to notify the other systems."
 
        url = 'http://localhost:8080/api/2/things/org.eclipse.ditto:f2c5c1cf-88c7-468c-93db-84393aab4e03/features/sensor/inbox/messages/update'

        headers = {
            'Content-Type': 'application/json'
        }

        json_data = json.dumps(
            {
                "definition": "digital-twin:sensor:2.1.0",
                "features": {
                    "sensor": {
                        "definition": [
                            "dtwin:sensor:1.0.0"
                        ],
                        "properties": {
                            'et0': data[0],
                            'pluviometry': data[1],
                            'relativehumidity': data[2],
                            'soilmoisturetotal': data[3],
                            'soiltemperature': data[4],
                            'winddirection': data[5],
                            'windspeed': data[6],
                            'temperature': data[7],
                            'hour': data[8],
                            'day': data[9],
                            'month': data[10],
                            'year': data[11]
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
                data=json_data,
                auth=auth,
                timeout=1
            )
        except:
            pass

    def load_from_excel(self):
        "This class will load the csv file and send the data to the other systems."

        input_data = pd.read_csv('./devices/visualization.csv').dropna()

        hour = pd.Series(pd.DatetimeIndex(pd.to_datetime(input_data['timeinstant'])).hour)
        day = pd.Series(pd.DatetimeIndex(pd.to_datetime(input_data['timeinstant'])).day)
        month = pd.Series(pd.DatetimeIndex(pd.to_datetime(input_data['timeinstant'])).month)
        year = pd.Series(pd.DatetimeIndex(pd.to_datetime(input_data['timeinstant'])).year)

        input_data = pd.concat([input_data, hour.rename('hour')], axis=1)
        input_data = pd.concat([input_data, day.rename('day')], axis=1)
        input_data = pd.concat([input_data, month.rename('month')], axis=1)
        input_data = pd.concat([input_data, year.rename('year')], axis=1)

        data = input_data[self._FEATURES]
        data = pd.DataFrame(data)

        print('Loading ' + str(len(data.index)) + ' values...')

        for index in data.itertuples():
            print(index[0])
            self.insert_into_database(list(index[1:13]))
            self.notify_ditto(list(index[1:13]))

excel_loader = ExcelLoader()
excel_loader.load_from_excel()