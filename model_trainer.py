import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import mean_squared_error, r2_score, make_scorer
import joblib

from data_loader import DataLoader

class ModelTrainer(object):
    def __init__(self):
        """
        This class receives the processed dataset and uses it to train a lineal
        regression model to predict values.
        """

        self.model = None

        self.x_train = None
        self.y_train = None

        self.x_test = None
        self.y_test = None

    def load_dataset(self, path, label, features):
        """
        This method loads a dataset given a file path and generates the sets of
        data needed for training and testing.
        """

        # Load the data
        data_loader = DataLoader(path, label, features)
        features = data_loader.get_features()
        label = data_loader.get_label()  

        # Split data 70%-30% into training set and test set
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(features, label, test_size=0.30, random_state=0)

        print ('Training Set: %d rows\nTest Set: %d rows' % (self.x_train.shape[0], self.x_test.shape[0]))

    def train_lineal_model(self, name='model'):
        """
        This method trains a Linear Regression model with the dataset being loaded.
        """
        # Fit a linear regression model on the training set
        self.model = LinearRegression().fit(self.x_train, self.y_train)
        print('The model has been trained')
        self.get_model_metrics(name)

    def train_lasso_model(self, name='model'):
        """
        This method trains a Linear Lasso Regression model with the dataset being loaded.
        """
        # Fit a linear regression model on the training set
        self.model = Lasso().fit(self.x_train, self.y_train)
        print('The model has been trained')
        self.get_model_metrics(name)

    def train_tree_model(self, name='model'):
        """
        This method trains a Decision Tree Regression model with the dataset being loaded.
        """
        # Fit a linear regression model on the training set
        self.model = DecisionTreeRegressor().fit(self.x_train, self.y_train)
        print('The model has been trained')
        self.get_model_metrics(name)

    def train_ensemble_model(self, name='model', hiperparameters=None):
        """
        This method trains a Random Forest Regression model with the dataset being loaded.
        """

        if hiperparameters == None:
    
            # Fit a linear regression model on the training set
            self.model = RandomForestRegressor().fit(self.x_train, self.y_train)
            print('The model has been trained')

            # Get the metrics
            self.get_model_metrics(name)

            # Save the model
            self.save_model(name)

    def train_gradient_boost_model(self, name='model', hiperparameters=None):
        """
        This method trains a Linear Regression model with the dataset being loaded.
        """
        if hiperparameters == None:
            
            # Fit a linear regression model on the training set
            self.model = RandomForestRegressor().fit(self.x_train, self.y_train)
            print('The model has been trained')

            # Get the metrics
            self.get_model_metrics(name)

            # Save the model
            self.save_model(name)
        else:
            # Use a Gradient Boosting algorithm
            alg = GradientBoostingRegressor()

            # Find the best hyperparameter combination to optimize the R2 metric
            score = make_scorer(r2_score)
            gridsearch = GridSearchCV(alg, hiperparameters, scoring=score, cv=3, return_train_score=True)
            gridsearch.fit(self.x_train, self.y_train)
            print("Best parameter combination:", gridsearch.best_params_, "\n")

            # Get the best model
            self.model=gridsearch.best_estimator_
            print('The model has been trained')

            # Get the metrics
            self.get_model_metrics(name)

    def load_model(self, path):
        """
        This method loads the specified model.
        """
        self.model = joblib.load(path)

    def save_model(self, name):
        """
        This method saves the currently loaded model.
        """
        joblib.dump(self.model, 'models/' + name + '.pkl')

    def get_model_metrics(self, name='model'):
        """
        This method returns diagrams showing the model fitness.
        """

        predictions = self.model.predict(self.x_test)
        np.set_printoptions(suppress=True)
        print('Predicted labels: ', np.round(predictions, 1)[:10])
        print('Actual labels   : ' ,self.y_test.to_numpy()[:10])

        plt.scatter(self.y_test, predictions)
        plt.xlabel('Actual Labels')
        plt.ylabel('Predicted Labels')
        plt.title('Predictions')
        
        # overlay the regression line
        z = np.polyfit(self.y_test, predictions, 1)
        p = np.poly1d(z)
        plt.plot(self.y_test,p(self.y_test), color='magenta')
        plt.savefig('diagrams/' + name + '_prediction_diagram.png')
        plt.close()

        mse = mean_squared_error(self.y_test, predictions)
        print("MSE:", mse)

        rmse = np.sqrt(mse)
        print("RMSE:", rmse)

        r2 = r2_score(self.y_test, predictions)
        print("R2:", r2)

    def predict_value(self, features_set):
        return self.model.predict(features_set)

