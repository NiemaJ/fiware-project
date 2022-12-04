from data_loader import DataLoader
from data_explorer import DataExplorer
from model_trainer import ModelTrainer







path = 'data/sensor_data_1.csv'
numeric_features = ['et0', 'pluviometry', 'relativehumidity', 'soilmoisturetotal', 'soiltemperature', 'winddirection', 'windspeed']
categorical_features = ['day', 'month', 'year']
label = 'temperature'
features = numeric_features + categorical_features

# data_explorer = DataExplorer(path, label, features)
# data_explorer.visualize_label(label)
# data_explorer.visualize_features(label, numeric_features, categorical_features)

model = ModelTrainer()
model.load_dataset(path, label, features)
# model.train_lineal_model('lineal')
# model.train_lasso_model('lasso')
# model.train_tree_model('tree')
model.train_ensemble_model('ensemble')
# model.train_gradient_boost_model('gradient_boost')

# params = {
#  'learning_rate': [0.1, 0.5, 1.0],
#  'n_estimators' : [50, 100, 150]
# }

# model.train_gradient_boost_model('gradient_boost', params)