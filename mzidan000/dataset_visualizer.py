import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class DatasetVisualizer:
    """
    Class for visualizing the neighbour survey dataset.

    Example usage:
            df = pd.read_csv('neighbour_survey_data.csv')
            visualizer = DatasetVisualizer(df)
            visualizer.plot_column_frequency('q001', 'Question 1 Frequency')
            visualizer.plot_grouped_columns_frequency(pairs, 'Food Programs Access Barriers')
            visualizer.plot_stacked_columns_frequency(pairs, 'Stacked Bar Plot Title', 'Food Programs Access Barriers')
            visualizer.plot_heatmap_columns_frequency(cols, 'Food Programs Access Barriers')
            visualizer.plot_proportional_stacked_bar('q040a','food_security_status','Proportional Bar Plot: Food Security Status across Housing Situations')

    """
    def __init__(self, df: pd.DataFrame):
        self.df = df



    def plot_column_frequency(self, col_name: str, plot_title: str, top_n: int = None, df: pd.DataFrame = None) -> None:
        """
        Bar plot function: Make a bar plot to visualize the frequency of unique values in a specified column of a DataFrame.

        Parameters:
            self: The instance of DatasetVisualizer containing the DataFrame as an attribute.
            col_name (str): The name of the column to plot.
            plot_title (str): The title of the plot.
            top_n (int, optional): Number of top entries to plot. If None, plots all entries.
            df (pd.DataFrame, optional): The DataFrame to use for plotting. Defaults to the instance's DataFrame.
        """

        # If no DataFrame is provided, use self.df
        if df is None:
            df = self.df

        df[col_name].value_counts(dropna=False).head(top_n).plot(kind='bar', title=plot_title, xlabel=col_name, ylabel='Count')
        plt.show()



    def plot_column_frequency_unstacked_proportion(self, col_name: str, plot_title: str, df: pd.DataFrame = None, top_n: int = None) -> None:
        """
        Bar plot function: Make a proportional unstacked bar plot to visualize the frequency of unique values
        in a specified column of a DataFrame as percentages.

        Parameters:
            self: The instance of DatasetVisualizer containing the DataFrame as an attribute.
            col_name (str): The name of the column to plot.
            plot_title (str): The title of the plot.
            df (pd.DataFrame, optional): The DataFrame to use for plotting.
            top_n (int, optional): Number of top entries to plot. If None, plots all entries.
        """

        # If no DataFrame is provided, use self.df
        if df is None:
            df = self.df

        # Calculate the proportional value counts
        value_counts = df[col_name].value_counts(normalize=True, dropna=False).head(top_n)

        # Plot the proportional stacked bar plot
        ax = value_counts.plot(kind='bar', stacked=True, figsize=(10, 7))

        # Add percentages on the bars
        for c in ax.containers:
            labels = [f'{v.get_height()*100:.1f}%' if v.get_height() > 0 else '' for v in c]
            ax.bar_label(c, labels=labels, label_type='center', fontsize=7, color='white')

        plt.title(plot_title)
        plt.ylabel('Proportion')
        plt.xlabel(col_name)
        plt.show()




    def plot_column_frequency_stacked_proportion(self, col_name: str, xlabel: str, plot_title: str, df: pd.DataFrame = None, top_n: int = None) -> None:
        """
        Bar plot function: Make a proportional stacked bar plot to visualize the frequency of unique values
        in a specified column of a DataFrame as percentages.

        Parameters:
            self: The instance of DatasetVisualizer containing the DataFrame as an attribute.
            col_name (str): The name of the column to plot.
            xlabel (str): The label for the x-axis.
            plot_title (str): The title of the plot.
            df (pd.DataFrame, optional): The DataFrame to use for plotting. Defaults to the instance's DataFrame.
            top_n (int, optional): Number of top entries to plot. If None, plots all entries.
        """

        # If no DataFrame is provided, use self.df
        if df is None:
            df = self.df

        # Example data with top_n filtering
        col_data = df[col_name].value_counts(normalize=True, dropna=False).head(top_n)

        # Convert column data to list to stack
        values = col_data.values
        labels = col_data.index

        # Plot a single stacked bar
        fig, ax = plt.subplots()
        ax.bar(xlabel, values[0], label=labels[0])
        bottom_value = values[0]
        for i in range(1, len(values)):
            ax.bar(xlabel, values[i], bottom=bottom_value, label=labels[i])
            bottom_value += values[i]

        # Add percentages on the bars
        for c in ax.containers:
            labels = [f'{v.get_height()*100:.1f}%' if v.get_height() > 0 else '' for v in c]
            ax.bar_label(c, labels=labels, label_type='center', fontsize=7, color='white')

        # Add labels
        ax.set_ylabel('Proportion')
        ax.set_title(plot_title)
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

        # Show the plot
        plt.tight_layout()
        plt.show()








    def plot_grouped_columns_frequency(self, pairs: list, question_category: str) -> None:
        """
        Grouped Bar Plot function: Plots the frequency of related values across multiple columns in a DataFrame.

        Parameters:
            self: The instance of DatasetVisualizer containing the DataFrame as an attribute.
            pairs (list): A list of tuples where each tuple contains a sub-question column name and a corresponding choice.
                        Each tuple should be in the format (sub_question_column, choice).
            question_category (str): The question category (e.g., "Food Programs Access Barriers").
        
            Example:
            question_category = "Food Programs Access Barriers"
            pairs = [
                ('q014a', 'None of the above'),
                ('q014b', 'Language barriers'),
                ('q014c', 'Physical inaccessibility'),
                ('q014d', 'Safety concerns'),
                ('q014e', 'Transportation barriers'),
                ('q014f', 'Program hours of operation'),
                ('q014g', 'Prefer not to answer')
            ]
        """

        boolean_df = pd.DataFrame()

        for col, choice in pairs:
            boolean_df[choice] = self.df[col].str.contains(choice, na=False, regex = False)

        summed_data = boolean_df.sum().reset_index()
        summed_data.columns = [question_category, 'Count']

        values = summed_data['Count']
        labels = summed_data[question_category]

        sorted_indices = np.argsort(values)
        sorted_values = values[sorted_indices]
        sorted_labels = labels[sorted_indices]

        plt.barh(sorted_labels, sorted_values)
        plt.xlabel('Count')
        plt.ylabel('Choices')
        plt.title(question_category)
        plt.show()

    def plot_stacked_columns_frequency(self, pairs: list, plot_title: str, question_category: str) -> None:
        """
        Stacked bar plot function: Plots the frequency of related values across multiple columns in a DataFrame 
                                   by stacking bars on top of each other for each choice.

        Parameters:
            self: The instance of DatasetVisualizer containing the DataFrame as an attribute.
            pairs (list): A list of tuples where each tuple contains a sub-question column name and a corresponding choice.
                        Each tuple should be in the format (sub_question_column, choice).
            plot_title (str): The title of the plot.
            question_category (str): The question category (e.g., "Food Programs Access Barriers").

            Example:
            question_category = "Food Programs Access Barriers"
            pairs = [
                ('q014a', 'None of the above'),
                ('q014b', 'Language barriers'),
                ('q014c', 'Physical inaccessibility'),
                ('q014d', 'Safety concerns'),
                ('q014e', 'Transportation barriers'),
                ('q014f', 'Program hours of operation'),
                ('q014g', 'Prefer not to answer')
            ]
        """
        boolean_df = pd.DataFrame()

        for col, choice in pairs:
            boolean_df[choice] = self.df[col].str.contains(choice, na=False)

        summed_data = boolean_df.sum().reset_index()
        summed_data.columns = [question_category, 'Count']

        summed_data.set_index(question_category).T.plot(kind='bar', stacked=True)
        plt.title(plot_title)
        plt.xlabel('Choices')
        plt.ylabel('Count')
        plt.show()

    def plot_heatmap_columns_frequency(self, cols: list, question_category: str) -> None:
        """
        Heatmap function: Plots the frequency of related values across multiple columns in a DataFrame 
                          by stacking bars on top of each other for each choice.

        Parameters:
            self: The instance of DatasetVisualizer containing the DataFrame as an attribute.
            cols (list): A list of column names belonging to the sub-question of the question category.
            question_category (str): The question category (e.g., "Food Programs Access Barriers").
            Example:
            question_category = "Food Programs Access Barriers"
            cols = ['q014a', 'q014b', 'q014c', 'q014d', 'q014e', 'q014f', 'q014g']
        """
        data = self.df[cols].apply(pd.Series.value_counts)
        sns.heatmap(data, annot=True, cmap="YlGnBu")
        plt.title(f'{question_category} Heatmap')
        plt.show()




    
    def plot_proportional_stacked_bar(self, col1: str, col2: str, title: str, df: pd.DataFrame = None) -> None:
        """
        Plot proportional stacked bar plot to show food security status distribution within each category
        with percentages displayed on the bars.

        Parameters:
            self: The instance of DatasetVisualizer containing the DataFrame as an attribute.
            col1 (str): The first column to plot.
            col2 (str): The second column to plot.
            title (str): The title of the plot.
            df (pd.DataFrame, optional): The DataFrame to use for plotting. Defaults to the instance's DataFrame.
        """

        # If no DataFrame is provided, use self.df
        if df is None:
            df = self.df

        contingency_table = pd.crosstab(df[col1], df[col2], normalize='index')

        ax = contingency_table.plot(kind='bar', stacked=True, figsize=(10, 7))

        # Add percentages on the bars
        for c in ax.containers:
            labels = [f'{v.get_height()*100:.1f}%' if v.get_height() > 0 else '' for v in c]
            ax.bar_label(c, labels=labels, label_type='center', fontsize=7, color='white')

        plt.title(title)
        plt.ylabel('Proportion')
        plt.xlabel(col1)
        plt.legend(title=col2, bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.show()




    def plot_frequency_distribution_stacked_unstacked_subplot(
        self, 
        col1: str,  
        col2: str, 
        figsize: tuple = (12, 6),  # Size of the figure
        title1: str = "Stacked Bar Plot", 
        title2: str = "Unstacked Bar Plot", 
        xlabel: str = "Categories",  
        ylabel: str = "Frequency",  
        df: pd.DataFrame = None  
        ) -> None:
    
        """
        Plot frequency distribution with stacked and unstacked bar plots in a 1x2 subplot grid.

        Parameters:
            col1 (str): The first column to plot.
            col2 (str): The second column to plot.
            figsize (tuple): Size of the figure. Default is (12, 6).
            title1 (str): Title for the stacked bar plot. Default is "Stacked Bar Plot".
            title2 (str): Title for the unstacked bar plot. Default is "Unstacked Bar Plot".
            xlabel (str): Label for the x-axis. Default is "Categories".
            ylabel (str): Label for the y-axis. Default is "Frequency".
            df (pd.DataFrame, optional): The DataFrame to use for plotting. Defaults to the instance's DataFrame.
        """
        
        # If no DataFrame is provided, use self.df
        if df is None:
            df = self.df

        # Calculate the frequency of the two variables
        contingency_table = pd.crosstab(df[col1], df[col2])

        # Create a figure with subplots in a 1x2 layout
        fig, axes = plt.subplots(nrows=1, ncols=2, figsize=figsize)

        # Plot a stacked bar plot to show the distribution of col2 across the groups in col1
        contingency_table.T.plot(kind='bar', stacked=True, ax=axes[0])
        axes[0].set_title(title1)
        axes[0].set_xlabel(xlabel)
        axes[0].set_ylabel(ylabel)

        # Plot an unstacked bar plot to show the distribution of col2 across the groups in col1
        contingency_table.T.plot(kind='bar', stacked=False, ax=axes[1])
        axes[1].set_title(title2)
        axes[1].set_xlabel(xlabel)
        axes[1].set_ylabel(ylabel)

        # Adjust the layout to prevent overlapping elements
        plt.tight_layout()
        plt.show()
