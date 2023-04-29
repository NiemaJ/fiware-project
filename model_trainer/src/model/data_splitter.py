import pandas as pd

class DataSplitter():
    def load_from_csv(self, path):
        # load the training dataset
        input_data = pd.read_csv(path).dropna()

        training_data_set = input_data[input_data.timeinstant < '2021-09-10']
        visualization_data_set = input_data[input_data.timeinstant > '2021-04-01']

        training_data_set.to_csv('./model_trainer/data/training.csv')
        visualization_data_set.to_csv('./model_trainer/data/visualization.csv')

data_splitter = DataSplitter()
data_splitter.load_from_csv('./model_trainer/data/sensor_data_1.csv')