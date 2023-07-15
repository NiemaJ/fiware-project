from model import model_trainer as md
import os
import json

class ModelCreator():
    "This class will be used as the main of the whole micro-service."

    def __init__(self, path):
        # Load config variables
        self.path = path
        self.model_trainer = md.ModelTrainer()

        # Load model data
        data = None
        with open(self.path + '/parameters.json') as file:
            data = json.load(file)

        self.numeric_features: list[str] = data['numeric_features']
        self.categorical_features: list[str] = data['categorical_features']
        self.labels: list[str] = self.numeric_features
        self.features: list[str] = self.numeric_features + self.categorical_features

    def _create_directories(self):
        "This method will create all the needed directories."

        try:
            os.mkdir(path='./diagrams')
            print('Created directory "diagrams"')
        except OSError as error:
            print('Directory "diagrams" already present')

        try:
            os.mkdir(path='./models')
            print('Created directory "models"')
        except OSError as error:
            print('Directory "models" already present')

        try:
            os.mkdir(path='./training_results')
            print('Created directory "training_results"')
        except OSError as error:
            print('Directory "training_results" already present')

    def train_models(self):
        "This method will train all the models."

        self._create_directories()

        for label in self.labels:
            current_numeric_features = self.numeric_features.copy()
            current_numeric_features.remove(label)

            print('Current label: ', label)
            print('Current features: ', current_numeric_features + self.categorical_features)

            self.model_trainer.load_dataset(label, current_numeric_features, self.categorical_features, path=self.path + '/training.csv')
            self.model_trainer.train_ensemble_model(label)

path = './model_trainer/data'
model_creator = ModelCreator(path)
model_creator.train_models()
