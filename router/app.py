from flask import Flask, request, jsonify
from sklearn.ensemble import RandomForestRegressor
from sklearn import preprocessing
import numpy as np
import joblib
import pandas as pd

app = Flask(__name__)

class Model():
    """
        This class will be used to load the models.
    """

    _NUMERIC_FEATURES = ['et0', 'pluviometry', 'relativehumidity', 'soilmoisturetotal', 'soiltemperature', 'winddirection', 'windspeed', 'temperature']
    _CATEGORICAL_FEATURES = ['hour', 'day', 'month', 'year']

    def __init__(self):
        "Load the models and the scaler"
        self.temperature_model: RandomForestRegressor = joblib.load('./models/temperature.pkl')
        self.et0_model: RandomForestRegressor = joblib.load('./models/et0.pkl')
        self.pluviometry_model: RandomForestRegressor = joblib.load('./models/pluviometry.pkl')
        self.relativehumidity_model: RandomForestRegressor = joblib.load('./models/relativehumidity.pkl')
        self.soilmoisturetotal_model: RandomForestRegressor = joblib.load('./models/soilmoisturetotal.pkl')
        self.soiltemperature_model: RandomForestRegressor = joblib.load('./models/soiltemperature.pkl')
        self.winddirection_model: RandomForestRegressor = joblib.load('./models/winddirection.pkl')
        self.windspeed_model: RandomForestRegressor = joblib.load('./models/windspeed.pkl')

        self.scaler: preprocessing.MinMaxScaler = joblib.load('./models/scaler.pkl')

    def predict_all_values(self, features_set: pd.DataFrame):
        numeric_features = features_set[self._NUMERIC_FEATURES].values#[[value] for value in features_set[self._NUMERIC_FEATURES].values]
        categorical_features = features_set[self._CATEGORICAL_FEATURES]

        # return {'cosa': numeric_features}

        scaled_numeric_features = self.scaler.fit_transform(numeric_features)
        prepared_features = pd.concat([pd.DataFrame(scaled_numeric_features, columns=self._NUMERIC_FEATURES), categorical_features], axis=1)

        temperature = self.predict_temperature(prepared_features)
        et0 = self.predict_et0(prepared_features)
        pluviometry = self.predict_pluviometry(prepared_features)
        relativehumidity = self.predict_relativehumidity(prepared_features)
        soilmoisturetotal = self.predict_soilmoisturetotal(prepared_features)
        soiltemperature = self.predict_soiltemperature(prepared_features)
        winddirection = self.predict_winddirection(prepared_features)
        windspeed = self.predict_windspeed(prepared_features)

        # predictions = np.ndarray([temperature, et0, pluviometry, relativehumidity, soilmoisturetotal, soiltemperature, winddirection, windspeed])

        predictions = pd.DataFrame(data=[[temperature, et0, pluviometry, relativehumidity, soilmoisturetotal, soiltemperature, winddirection, windspeed]], columns=self._NUMERIC_FEATURES)

        unscaled_prediction = list(self.scaler.inverse_transform(predictions.values)[0])

        result = {
            'temperature': unscaled_prediction[7],
            'et0': unscaled_prediction[0],
            'pluviometry': unscaled_prediction[1],
            'relativehumidity': unscaled_prediction[2],
            'soilmoisturetotal': unscaled_prediction[3],
            'soiltemperature': unscaled_prediction[4],
            'winddirection': unscaled_prediction[5],
            'windspeed': unscaled_prediction[6]
        }

        return result


    def predict_temperature(self, features_set: pd.DataFrame):
        scaled_prediction = self.temperature_model.predict(features_set.drop('temperature', axis=1))
        return list(scaled_prediction)[0]
    
    def predict_et0(self, features_set: pd.DataFrame):
        scaled_prediction = self.et0_model.predict(features_set.drop('et0', axis=1))
        return list(scaled_prediction)[0]
    
    def predict_pluviometry(self, features_set: pd.DataFrame):
        scaled_prediction = self.pluviometry_model.predict(features_set.drop('pluviometry', axis=1))
        return list(scaled_prediction)[0]
    
    def predict_relativehumidity(self, features_set: pd.DataFrame):
        scaled_prediction = self.relativehumidity_model.predict(features_set.drop('relativehumidity', axis=1))
        return list(scaled_prediction)[0]
    
    def predict_soilmoisturetotal(self, features_set: pd.DataFrame):
        scaled_prediction = self.soilmoisturetotal_model.predict(features_set.drop('soilmoisturetotal', axis=1))
        return list(scaled_prediction)[0]
    
    def predict_soiltemperature(self, features_set: pd.DataFrame):
        scaled_prediction = self.soiltemperature_model.predict(features_set.drop('soiltemperature', axis=1))
        return list(scaled_prediction)[0]
    
    def predict_winddirection(self, features_set: pd.DataFrame):
        scaled_prediction = self.winddirection_model.predict(features_set.drop('winddirection', axis=1))
        return list(scaled_prediction)[0]
    
    def predict_windspeed(self, features_set: pd.DataFrame):
        scaled_prediction = self.windspeed_model.predict(features_set.drop('windspeed', axis=1))
        return list(scaled_prediction)[0]
    
predictor = Model()

@app.post("/prediction")
def predict_all_values():
    if request.is_json:
        input_parameters = dict(request.get_json())
        dataframe_parameters = pd.DataFrame(data=[list(input_parameters.values())], columns=list(input_parameters.keys()))
        result = predictor.predict_all_values(dataframe_parameters)
        return result
    return {"error": "Request must be JSON"}, 415

