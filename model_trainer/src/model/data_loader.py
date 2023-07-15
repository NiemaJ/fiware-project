import os
import pandas as pd
import matplotlib.pyplot as plt

class DataLoader(object):
    def __init__(self):
        self.features_set: pd.DataFrame = None

    def load_from_csv(self, path: str, label: str, numeric_features: list[str], categorical_features: list[str]) -> None:
        """
            This method loads data contained on a csv file into a pandas dataframe.
        """
        # load the training dataset
        input_data = pd.read_csv(path).dropna()

        hour = pd.Series(pd.DatetimeIndex(pd.to_datetime(input_data['timeinstant'])).hour)
        day = pd.Series(pd.DatetimeIndex(pd.to_datetime(input_data['timeinstant'])).day)
        month = pd.Series(pd.DatetimeIndex(pd.to_datetime(input_data['timeinstant'])).month)
        year = pd.Series(pd.DatetimeIndex(pd.to_datetime(input_data['timeinstant'])).year)

        input_data = pd.concat([input_data, hour.rename('hour')], axis=1)
        input_data = pd.concat([input_data, day.rename('day')], axis=1)
        input_data = pd.concat([input_data, month.rename('month')], axis=1)
        input_data = pd.concat([input_data, year.rename('year')], axis=1)

        self.label: str = label
        self.features: list[str] = numeric_features + categorical_features
        self.numeric_features: list[str] = numeric_features
        self.categorical_features: list[str] = categorical_features

        self.features_set = input_data[self.features]

    def get_label_set(self) -> pd.DataFrame:
        """
        This function retrieves the label set being loaded.
        """

        return self.features_set[self.label]

    def get_features_set(self) -> pd.DataFrame:
        """
        This function retrieves the features being loaded.
        """
        return self.features_set

    def visualize_label(self, folder: str) -> None:
        """
        This method generates a histogram and a box diagram to visualize the 
        distribution of the label being given. The diagrams will be saved as an 
        image on the data directory.
        """

        # Create a figure for 2 subplots (2 rows, 1 column)
        fig, ax = plt.subplots(2, 1, figsize = (9,12))

        # Plot the histogram   
        ax[0].hist(self.get_label_set(), bins=100)
        ax[0].set_ylabel('Frequency')

        # Add lines for the mean, median, and mode
        ax[0].axvline(self.get_label_set().mean(), color='magenta', linestyle='dashed', linewidth=2)
        ax[0].axvline(self.get_label_set().median(), color='cyan', linestyle='dashed', linewidth=2)

        # Plot the boxplot   
        ax[1].boxplot(self.get_label_set(), vert=False)
        ax[1].set_xlabel(self.label)

        # Add a title to the Figure
        fig.suptitle(self.label + ' Distribution')

        # # Save the figure
        try:
            os.mkdir(path='./diagrams/' + self.label + '/' + folder)
            print('Created directory "' + self.label + '/' + folder)
        except OSError:
            print('Directory "' + folder + '" already present')

        fig.savefig('diagrams/' + self.label + "/" + folder + "/" + self.label + '_histogram-boxplot.png')
        plt.close(fig)

    def visualize_features(self, folder: str) -> None:
        """
        This method generates a histogram and scatter diagram for each numeric 
        feature and a bar diagram and box diagram for each categorical feature.
        """

        try:
            os.mkdir(path='./diagrams/' + self.label + '/' + folder)
            print('Created directory ' + folder)
        except OSError:
            print('Directory "' + folder + '" already present')

        # Plot a histogram for each numeric feature
        for col in self.numeric_features:
            fig = plt.figure(figsize=(9, 6))
            ax = fig.gca()
            feature = self.features_set[col]
            feature.hist(bins=100, ax = ax)
            ax.axvline(feature.mean(), color='magenta', linestyle='dashed', linewidth=2)
            ax.axvline(feature.median(), color='cyan', linestyle='dashed', linewidth=2)
            ax.set_title(col)

            # Save the figure
            fig.savefig('diagrams/' + self.label + '/' + folder + "/" + col + '_histogram.png')
            plt.close(fig)

        for col in self.categorical_features:
            counts = self.features_set[col].value_counts().sort_index()
            fig = plt.figure(figsize=(9, 6))
            ax = fig.gca()
            counts.plot.bar(ax = ax, color='steelblue')
            ax.set_title(col + ' counts')
            ax.set_xlabel(col) 
            ax.set_ylabel("Frequency")

            # Save the figure
            fig.savefig('diagrams/' + self.label + '/'+ folder + "/" + col + '_histogram.png')
            plt.close(fig)


        # Now, let's scatter points intersecting a feature vs the label
        for col in self.numeric_features:
            fig = plt.figure(figsize=(9, 6))
            ax = fig.gca()
            feature = self.features_set[col]
            correlation = feature.corr(self.get_label_set())
            plt.scatter(x=feature, y=self.get_label_set())
            plt.xlabel(col)
            plt.ylabel(self.label)
            ax.set_title(self.label + ' vs ' + col + '- correlation: ' + str(correlation))

            # Save the figure
            fig.savefig('diagrams/' + self.label + '/' + folder + "/" + col + '_scatter.png')
            plt.close(fig)

        for col in self.categorical_features:
            fig = plt.figure(figsize=(9, 6))
            ax = fig.gca()
            pd.concat([self.features_set[col], self.get_label_set()], axis=1).boxplot(column = self.label, by = col, ax = ax)
            ax.set_title('Label by ' + col)
            ax.set_ylabel(self.label)

            # Save the figure
            fig.savefig('diagrams/' + self.label + '/' + folder + "/" + col + '_boxplot.png')
            plt.close(fig)
