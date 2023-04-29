import matplotlib.pyplot as plt
import pandas as pd

from data_loader import DataLoader

class DataExplorer(object):
    def __init__(self, path, label, numerical_values, categorical_values):
        """
        This class receives the dataset to work with and generates a set of
        diagrams to have a better view of how the data are distributed.
        """
        data_loader = DataLoader()
        data_loader.load_from_csv(path, label, numerical_values, categorical_values)
        self.label_set = data_loader.get_label()
        self.features_set = data_loader.get_features()

    def visualize_label(self, label):
        """
        This method generates a histogram and a box diagram to visualize the 
        distribution of the label being given. The diagrams will be saved as an 
        image on the data directory.
        """

        # Create a figure for 2 subplots (2 rows, 1 column)
        fig, ax = plt.subplots(2, 1, figsize = (9,12))

        # Plot the histogram   
        ax[0].hist(self.label_set, bins=100)
        ax[0].set_ylabel('Frequency')

        # Add lines for the mean, median, and mode
        ax[0].axvline(self.label_set.mean(), color='magenta', linestyle='dashed', linewidth=2)
        ax[0].axvline(self.label_set.median(), color='cyan', linestyle='dashed', linewidth=2)

        # Plot the boxplot   
        ax[1].boxplot(self.label_set, vert=False)
        ax[1].set_xlabel(label)

        # Add a title to the Figure
        fig.suptitle(label + ' Distribution')

        # Save the figure
        fig.savefig('diagrams/' + label + '_histogram-boxplot.png')
        plt.close(fig)

    def visualize_features(self, label, numeric_features, categorical_features):
        """
        This method generates a histogram and scatter diagram for each numeric 
        feature and a bar diagram and box diagram for each categorical feature.
        """

        # Plot a histogram for each numeric feature
        for col in numeric_features:
            fig = plt.figure(figsize=(9, 6))
            ax = fig.gca()
            feature = self.features_set[col]
            feature.hist(bins=100, ax = ax)
            ax.axvline(feature.mean(), color='magenta', linestyle='dashed', linewidth=2)
            ax.axvline(feature.median(), color='cyan', linestyle='dashed', linewidth=2)
            ax.set_title(col)

            # Save the figure
            fig.savefig('model_trainer/diagrams/' + col + '_histogram.png')
            plt.close(fig)

        for col in categorical_features:
            counts = self.features_set[col].value_counts().sort_index()
            fig = plt.figure(figsize=(9, 6))
            ax = fig.gca()
            counts.plot.bar(ax = ax, color='steelblue')
            ax.set_title(col + ' counts')
            ax.set_xlabel(col) 
            ax.set_ylabel("Frequency")

            # Save the figure
            fig.savefig('model_trainer/diagrams/' + col + '_histogram.png')
            plt.close(fig)


        # Now, let's scatter points intersecting a feature vs the label
        for col in numeric_features:
            fig = plt.figure(figsize=(9, 6))
            ax = fig.gca()
            feature = self.features_set[col]
            correlation = feature.corr(self.label_set)
            plt.scatter(x=feature, y=self.label_set)
            plt.xlabel(col)
            plt.ylabel(label)
            ax.set_title(label + ' vs ' + col + '- correlation: ' + str(correlation))

            # Save the figure
            fig.savefig('model_trainer/diagrams/' + col + '_scatter.png')
            plt.close(fig)

        for col in categorical_features:
            fig = plt.figure(figsize=(9, 6))
            ax = fig.gca()
            pd.concat([self.features_set, self.label_set], axis=1).boxplot(column = label, by = col, ax = ax)
            ax.set_title('Label by ' + col)
            ax.set_ylabel(label)

            # Save the figure
            fig.savefig('model_trainer/diagrams/' + col + '_boxplot.png')
            plt.close(fig)

numeric_features = ['et0', 'pluviometry', 'relativehumidity', 'soilmoisturetotal', 'soiltemperature', 'winddirection', 'windspeed', 'temperature']
categorical_features = ['hour', 'day', 'month', 'year']
label = 'temperature'
features = numeric_features + categorical_features

data_explorer = DataExplorer('./model_trainer/data/training.csv', label, numeric_features, categorical_features)
data_explorer.visualize_features(label, numeric_features, categorical_features)