import datetime
import time
import websocket
import json
import pandas as pd
from predictor import Predictor
from database_connector import DatabaseConnector

class PredictorWebSocket():
    "This class will listen to Eclipse Ditto's messages and respond to them."

    def __init__(self):
        "Constructor."

        print('Initializing database connector...')

        self.database = DatabaseConnector()

        print('Initializing predictor...')

        self.predictor = Predictor()

        print('Connecting web socket...')

        def on_message(webSocketApp, message):
            try:
                input_parameters = dict(json.loads(message)['value']['features']['sensor']['properties'])
                dataframe_parameters = pd.DataFrame(data=[list(input_parameters.values())], columns=list(input_parameters.keys()))
                result = self.predictor.predict_all_values(dataframe_parameters)
                self.insert_into_database(result)
                print(result)
            except Exception as e:
                print(message)

        def on_open(webSocketApp):
            webSocketApp.send('START-SEND-MESSAGES')

        self.webSocket = websocket.WebSocketApp('ws://localhost:8080/ws/2', 
            header=[
                'User-Agent: predictor',
                'Authorization: Basic ZGl0dG86ZGl0dG8='
            ],
            on_open=on_open,
            on_message=on_message
        )

        self.webSocket.run_forever()

    def insert_into_database(self, data):
        "This method will insert the given data into the database"

        year = data['t_year']
        month = data['t_month']
        day = data['t_day']
        hour = data['t_hour']

        date_time = datetime.datetime(year, month, day, hour, 0, 0)
        t_epoch = int(time.mktime(date_time.timetuple()))

        data['t_epoch'] = t_epoch

        self.database.insert_into_predicted_values(data)

predictor_web_socket = PredictorWebSocket()