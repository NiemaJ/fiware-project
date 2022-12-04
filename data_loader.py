import pandas as pd

class DataLoader(object):
    def __init__(self, path, label, features):
        """
        This class receives the path of the file being loaded,
        the label to be predicted and the features used to predict the label.
        """

        # load the training dataset
        input_data = pd.read_csv(path).dropna()

        day = pd.Series(pd.DatetimeIndex(pd.to_datetime(input_data['timeinstant'])).day)
        month = pd.Series(pd.DatetimeIndex(pd.to_datetime(input_data['timeinstant'])).month)
        year = pd.Series(pd.DatetimeIndex(pd.to_datetime(input_data['timeinstant'])).year)

        # sensor_data = input_data['windspeed']
        # sensor_data = pd.concat([sensor_data, input_data['winddirection']], axis=1)
        # sensor_data = pd.concat([sensor_data, input_data['pluviometry']], axis=1)
        # sensor_data = pd.concat([sensor_data, input_data['relativehumidity']], axis=1)
        # sensor_data = pd.concat([sensor_data, input_data['temperature']], axis=1)
        # sensor_data = pd.concat([sensor_data, input_data['et0']], axis=1)
        # sensor_data = pd.concat([sensor_data, input_data['soiltemperature']], axis=1)
        # sensor_data = pd.concat([sensor_data, input_data['soilmoisturetotal']], axis=1)
        input_data = pd.concat([input_data, day.rename('day')], axis=1)
        input_data = pd.concat([input_data, month.rename('month')], axis=1)
        input_data = pd.concat([input_data, year.rename('year')], axis=1)

        self.features = input_data[features]
        self.label = input_data[label]

    def get_label(self):
        """
        This function retrieves the label set being loaded.
        """
        return self.label

    def get_features(self):
        """
        This function retrieves the features being loaded.
        """
        return self.features