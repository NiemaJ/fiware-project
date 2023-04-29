from model import model_trainer as md
import os

path = './model_trainer/data/training.csv'
url = 'https://atdfiware.grayhats.com/quantum/v2/entities/urn:ngsi-ld:instation:in-sta3472/value'
headers = {
    'Fiware-Service': 'smarttrebol',
    'Fiware-ServicePath': '/rabanales'
}

numeric_features = ['et0', 'pluviometry', 'relativehumidity', 'soilmoisturetotal', 'soiltemperature', 'winddirection', 'windspeed', 'temperature']
# numeric_features = ['dirwind', 'humidity', 'humidity_in', 'press', 'temperature', 'temperature_in']
# numeric_features = ['dirwind', 'humidity', 'humidity_in', 'pluviometer', 'press', 'temperature', 'temperature_in', 'velwind']
categorical_features = ['hour', 'day', 'month', 'year']
labels = numeric_features
features = numeric_features + categorical_features

model_trainer = md.ModelTrainer()

# Create needed directories
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

for label in labels:
    current_numeric_features = numeric_features.copy()
    current_numeric_features.remove(label)

    print('Current label: ', label)
    print('Current features: ', current_numeric_features + categorical_features)

    model_trainer.load_dataset(label, current_numeric_features, categorical_features, path=path)
    model_trainer.train_ensemble_model(label)