import os
import pandas as pd
import numpy as np
import joblib
from sklearn import preprocessing
from .data_loader import DataLoader

class DataProcessor(DataLoader):

    def __init__(self, path: str, label: str, numeric_features: list[str], categorical_features: list[str]):
        self.load_from_csv(path, label, numeric_features, categorical_features)
        
        try:
            os.mkdir(path='./diagrams/' + label)
            print('Created directory "training_results"')
        except OSError as error:
            print('Directory ' + label + ' already present')
        
        self.visualize_label('raw_data')
        self.visualize_features('raw_data')

    def remove_outliers(self) -> None:
        """
            This method will filter out outliers values.
        """

        q_low = self.features_set[self.label].quantile(0.01)
        q_hi  = self.features_set[self.label].quantile(0.99)
        self.features_set = self.features_set[(self.features_set[self.label] < q_hi) & (self.features_set[self.label] > q_low)]

        self.visualize_label('filtered_data')
        self.visualize_features('filtered_data')

    def normalize(self) -> None:
        """
            This method will normalize the data.
        """

        numeric_features = self.features_set[self.numeric_features].values
        categorical_features_set = self.features_set[self.categorical_features]

        # The scaler will be the same for all the models, so if there is no one created yet, create one and save it.
        try:
            min_max_scaler = joblib.load('./models/scaler.pkl')
        except Exception:
            min_max_scaler = preprocessing.MinMaxScaler()
            joblib.dump(min_max_scaler, './models/' + 'scaler.pkl')

        x_scaled = min_max_scaler.fit_transform(numeric_features)
        numeric_features_set = pd.DataFrame(x_scaled, columns=self.numeric_features)
        self.features_set = pd.concat([numeric_features_set, categorical_features_set], axis=1).dropna()

        self.visualize_label('normalized_data')
        self.visualize_features('normalized_data')
