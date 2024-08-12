import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats

from dataset_visualizer import DatasetVisualizer


class DatasetAnalyzer:
    """
    Class for analyzing the neighbour survey dataset, including performing chi-square tests (i.e., testing relationships between categorical columns),
    plotting, and analyzing significant relationships.
    Example usage:
            df = pd.read_csv('neighbour_survey_data.csv')
            analyzer = DatasetAnalyzer(df)
            variables_to_analyze = {
                "age": "q025",
                "household_size": "q026",
            }
            analyzer.perform_data_analysis(variables_to_analyze)
    """
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.visualizer = DatasetVisualizer(df)

    # Chi-square test function
    def chi_square_test(self, col1: str, col2: str):
        """
        Perform chi-square test between two categorical columns.
        
        Parameters:
            self: The instance of DatasetAnalyzer containing the DataFrame as an attribute.
            col1 (str): The first column for comparison.
            col2 (str): The second column for comparison.
            
        Returns:
            chi2 (float): The chi-square statistic.
            p (float): The p-value of the test.
            dof (int): The degrees of freedom.
            expected (ndarray): The expected frequencies.
        """
        contingency_table = pd.crosstab(self.df[col1], self.df[col2])
        chi2, p, dof, expected = stats.chi2_contingency(contingency_table)
        return chi2, p, dof, expected

    # Plot function for contingency tables
    def plot_contingency_table(self, col1: str, col2: str, title: str) -> None:
        """
        Plot heatmap of the contingency table between two categorical columns.
        
        Parameters:
            self: The instance of DatasetAnalyzer containing the DataFrame as an attribute.
            col1 (str): The first column for comparison.
            col2 (str): The second column for comparison.
            title (str): The title of the plot.
        """
        contingency_table = pd.crosstab(self.df[col1], self.df[col2])
        sns.heatmap(contingency_table, annot=True, fmt="d", cmap="YlGnBu")
        plt.title(title)
        plt.ylabel(col1)
        plt.xlabel(col2)
        plt.show()

    # Function to analyze significant relationships and visualize using counts and percentage-based plots
    def analyze_visualize_significant_relationships(self, results: dict) -> None:
        """
        Analyze significant relationships between food security status and other variables,
        and visualize the specifics through frequency analysis and bar plots (counts and percentage-based plots)
        
        Parameters:
            self: The instance of DatasetAnalyzer containing the DataFrame as an attribute.
            results (dict): Dictionary containing significant variables and their chi-square test results.
                            The keys are variable names, and the values are tuples with chi-square statistics and p-values.
        """
        for col in results.keys():
            self.visualizer.plot_frequency_distribution_stacked_unstacked_subplot(
                col1='food_security_status',
                col2=col,
                figsize=(25, 8),
                title1=f'Stacked Bar Plot: Food Security Status across {col}',
                title2=f'Bar Plot: Food Security Status across {col}',
                xlabel=col,
                ylabel='Count'
            )
            self.visualizer.plot_proportional_stacked_bar(
                col1=col,
                col2='food_security_status',
                title=f'Proportional Stacked Bar Plot: Food Security Status across {col}'
            )



    # Function to perform data analysis
    def perform_data_analysis(self, variables_to_analyze: dict) -> None:
        """
        Perform data analysis for the dataframe, including identification of variables (columns) related to the food security status,
        and analysis of those relationships.
        
        Parameters:
            self: The instance of DatasetAnalyzer containing the DataFrame as an attribute.
            variables_to_analyze (dict): Dictionary containing the variables to analyze
        
        Returns:
            None
        """
        # Perform chi-square tests, save and plot results
        results = {}
        for var_name, col in variables_to_analyze.items():
            if isinstance(col, list):
                for sub_col in col:
                    chi2, p, dof, expected = self.chi_square_test(sub_col, 'food_security_status')
                    if p < 0.05:  
                        results[sub_col] = (chi2, p)  # Save only significantly related variables
                        # self.plot_contingency_table(sub_col, 'food_security_status', f"{sub_col} {var_name} vs. Food Security Status")
            else:
                chi2, p, dof, expected = self.chi_square_test(col, 'food_security_status')
                if p < 0.05:
                    results[col] = (chi2, p)  # Save only significantly related variables
                    # self.plot_contingency_table(col, 'food_security_status', f"{col} {var_name} vs. Food Security Status")
        
        # Display results
        for col, (chi2, p) in results.items():
            print(f"Chi-square test for {col} vs. Food Security Status:")
            print(f"Chi-square statistic: {chi2}")
            print(f"P-value: {p}")
            print(f"Significant: {p < 0.05}")
            print("\n")
        
        # Analyze significant relationships
        self.analyze_visualize_significant_relationships(results)


    def visualize_participants_demographics(self):
        """
        Visualize participants' demographic information
        """
        # Use plot_grouped_columns_frequency for the specified columns
        
        pairs_income = [
            ('q041a', 'Employed at least 35 hours each week'),
            ('q041b', 'Employed less than 35 hours each week'),
            ('q041c', 'Ontario disability support program (odsp)'),
            ('q041d', 'Ontario works (ow)'),
            ('q041e', 'Canada emergency response benefit (cerb)'),
            ('q041f', 'Scholarship'),
            ('q041g', 'Student loans'),
            ('q041h', 'Employment insurance (ei)'),
            ('q041i', 'Family support'),
            ('q041j', 'Spousal support'),
            ('q041k', 'Canada child benefit (ccb)'),
            ('q041l', 'Ontario trillium benefit (otb)'),
            ('q041m', 'Canadian pension plan (cpp)'),
            ('q041n', 'Private pension'),
            ('q041o', 'Old age security (oas)'),
            ('q041p', 'Workplace safety and insurance board (wsib)'),
            ('q041q', 'Short/long term disability'),
            ('q041r', 'Other government programs'),
            ('q041s', 'No income'),
            ('q041t', 'Prefer not to answer')
        ]
        self.visualizer.plot_grouped_columns_frequency(pairs_income, 'Income Sources')

        pairs_ethnic_background = [
            ('q038a', 'Indigenous (Inuit/First Nations/Metis)'),
            ('q038b', 'White/European'),
            ('q038c', 'Black/african/caribbean (african, afro-caribbean, african-canadian descent)'),
            ('q038d', 'South east asian (filipino, vietnamese, cambodian, thai, other southeast asian descent)'),
            ('q038e', 'East asian (chinese, korean, japanese, taiwanese descent)'),
            ('q038f', 'South asian (e.g. east indian, pakistani, sri lankan, indo-caribbean, etc)'),
            ('q038g', 'Middle eastern (arab, persian, west asian descent, e.g. afghan, egyptian, iranian, etc)'),
            ('q038h', 'Latin american (latin american, hispanic descent)'),
            ('q038i', 'I don\'t know'),
            ('q038j', 'Prefer not to answer')
        ]

        self.visualizer.plot_grouped_columns_frequency(pairs_ethnic_background, 'Ethnic Background')

        pairs_education = [
            ('q033a', 'Some high school'),
            ('q033b', 'Completed high school'),
            ('q033c', 'Some college / university'),
            ('q033d', 'Completed college / university'),
            ('q033e', 'Apprenticeship training and trades'),
            ('q033f', 'Some graduate education'),
            ('q033g', 'Completed graduate education'),
            ('q033h', 'Professional degree'),
            ('q033i', 'Prefer not to answer')
        ]
        self.visualizer.plot_grouped_columns_frequency(pairs_education, 'Highest Level of Education')

        pairs_breastfeeding = [
            ('q028a', 'Yes'),
            ('q028b', 'No'),
            ('q028c', 'Not applicable'),
            ('q028d', 'Prefer not to answer')
        ]
        self.visualizer.plot_grouped_columns_frequency(pairs_breastfeeding, 'Breastfeeding')

        # Use plot_column_frequency for the remaining columns
        self.visualizer.plot_column_frequency('q025', 'How old are you?')
        self.visualizer.plot_column_frequency('q026', 'How many people live in your household, including yourself?')
        self.visualizer.plot_column_frequency('q027', 'Do you have any children living in your household?')
        self.visualizer.plot_column_frequency('q034', 'Did you complete your highest level of education outside of Canada?')
        self.visualizer.plot_column_frequency('q035a', 'What is your status in Canada?')
        self.visualizer.plot_column_frequency('q036a', 'What is your gender?')
        self.visualizer.plot_column_frequency('q037', 'How long have you lived in Canada?')
        self.visualizer.plot_column_frequency('q040a', 'Which of the following best describes where you currently live?')


    def visualize_participants_food_bank_info(self):
        """
        Visualize participants' food bank info
        """
        food_programs = self.df[['q009', 'q012', 'q010', 'q011a']]
        self.visualizer.plot_column_frequency('q009', 'First Food Bank Visit')
        self.visualizer.plot_column_frequency('q012', 'Most Visited Food Bank', top_n=5)
        self.visualizer.plot_column_frequency('q010', 'Food Bank Visit Frequency')
        self.visualizer.plot_column_frequency('q011a', 'Other Food Program Visit Frequency')

