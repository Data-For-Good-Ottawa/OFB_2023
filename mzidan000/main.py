import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats

from dataset_validator import DatasetValidator
from dataset_processor import DatasetProcessor
from dataset_visualizer import DatasetVisualizer
from dataset_analyzer import DatasetAnalyzer
import dataset_mappers

# Read the data
df = pd.read_csv('neighbour_survey_clean-2024-06-14.csv', usecols=lambda col: col != 'id')

# Initialize the validator with the dataframe
validator = DatasetValidator(df)
# Run all validations
validator.run_all_validations()
# Get the validated data
validated_data = validator.df

# Porcessing the dataset using mappers
processor = DatasetProcessor(validated_data)
processed_data = processor.process_data(dataset_mappers.col_descr_115_dict, dataset_mappers.col_mapping_16_dict)


visualizer = DatasetVisualizer(processed_data)



# Perfom data analysis: Find a relationship between food security status and health/demographics/needs in the data sample
variables_to_analyze = {
    "age": "q025",
    "household_size": "q026",
    "household_children": [ "q029", "q030", "q031", "q032"], 
    "education_level": ["q033a", "q033b", "q033c", "q033d", "q033e", "q033f", "q033g", "q034"],
    "status_in_canada": ["q035a", "q035b"],
    "gender": ["q036a", "q036b"],
    "time_in_canada": "q037",
    "ethnic_background": ["q038a", "q038b", "q038c", "q038d", "q038e", "q038f", "q038g", "q038h", "q038i", "q038j", "q038k"],
    "housing_situation": ["q040a", "q040b"],
    "employment": ["q041a", "q041b", "q041c", "q041d", "q041e", "q041f", "q041g", "q041h", "q041i", "q041j", "q041k", "q041l", "q041m", "q041n", "q041o", "q041p", "q041q", "q041r", "q041s", "q041t", "q041u"],
    "health_conditions": ["q021a", "q021b", "q021c", "q021d", "q021e", "q021f"],
    "additional_health_conditions": ["q039a", "q039b", "q039c", "q039d", "q039e", "q039f", "q039g", "q039h", "q039i"],
    "exercise_habits": ["q019", "q020"],
    "pregnancy": "q022",
    "breastfeeding": [ "q028a", "q028b", "q028c", "q028d"],
    "income": "q002",
    "food_programs_access_barriers": ["q014a", "q014b", "q014c", "q014d", "q014e", "q014f", "q014g", "q014h"],
    "non_food_services": ["q017a", "q017b", "q017c", "q017d", "q017e", "q017f", "q017g", "q017h", "q017i", "q017j"], # OK
    "special_food_needs": ["q023a", "q023b", "q023c", "q023d", "q023e", "q024a", "q024b", "q024c", "q024d", "q024e", "q024f", "q024g", "q024h", "q024i"] # OK
}


analyzer = DatasetAnalyzer(processed_data)

#---------------------------------------------------- CHAPTER 1 -----------------------------------------------------------
analyzer. visualize_participants_demographics()
analyzer.visualize_participants_food_bank_info()

#------------------------------------------------- CHAPTER 3 & CHAPTER 5 -------------------------------------------------
analyzer.perform_data_analysis(variables_to_analyze)


#---------------------------------------------------- CHAPTER 4 -----------------------------------------------------------
# Define columns
social_assistance_cols = ['q041c', 'q041d', 'q041h'] 
health_condition_1_cols = ['q021b', 'q021c', 'q021d', 'q021f'] 
health_condition_2_cols = ['q039b', 'q039c', 'q039d', 'q039e', 'q039f', 'q039g', 'q039i']

# Select the rows where at least one of the social assistance columns is not null
df_x = processed_data.loc[processed_data[social_assistance_cols].any(axis=1)].copy()
# Combine all the non-null values in the social assistance columns into a single string separated by commas
df_x['social_assistance'] = df_x[social_assistance_cols].apply(lambda row: " / ".join(row.dropna().astype(str)), axis=1)
# Count the number of non-null values in health_condition_2_cols for each row
df_x['health_condition_2_counts'] = df_x[health_condition_2_cols[:-1]].count(axis=1) + df_x[health_condition_2_cols[-1]].apply(lambda x: 0 if pd.isna(x) else int(x))
# Count the number of non-null values in health_condition_1_cols for each row
df_x['health_condition_1_counts'] = df_x[health_condition_1_cols[:-1]].count(axis=1) + df_x[health_condition_1_cols[-1]].apply(lambda x: 0 if pd.isna(x) else int(x))


# Plot Health Condition 2 (q39a-i)
visualizer.plot_frequency_distribution_stacked_unstacked_subplot(
    col1='health_condition_2_counts', 
    col2='social_assistance', 
    figsize=(15, 11), 
    title1='Stacked Bar Plot: Health Conditions Status across Social Assistance (q39a-i)', 
    title2='Bar Plot: Health Conditions Status across Social Assistance (q39a-i)', 
    xlabel='social_assistance', 
    ylabel='Count',
    df = df_x
)
visualizer.plot_proportional_stacked_bar(
    col1='health_condition_2_counts',
    col2='social_assistance',
    title='Proportional Stacked Bar Plot: Health Conditions Status across Social Assistance (q39a-i)',

    df = df_x
)

# Plot Health Condition 1 (q21b-f)
visualizer.plot_frequency_distribution_stacked_unstacked_subplot(
    col1='health_condition_1_counts', 
    col2='social_assistance', 
    figsize=(15, 11), 
    title1='Stacked Bar Plot: Health Conditions Status across Social Assistance (q21b-f)', 
    title2='Bar Plot: Health Conditions Status across Social Assistance (q21b-f)', 
    xlabel='social_assistance', 
    ylabel='Count',
    df = df_x
)
visualizer.plot_proportional_stacked_bar(
    col1='health_condition_1_counts',
    col2='social_assistance',
    title='Proportional Stacked Bar Plot: Health Conditions Status across Social Assistance (q21b-f)',
    df = df_x
)



#---------------------------------------------------- CHAPTER 6 -----------------------------------------------------------


visualizer.plot_proportional_stacked_bar( 'q025','food_security_status', 'Proportional Bar Plot: Food Security Status across age groups')
# Income Sufficiency across Age Groups
visualizer.plot_proportional_stacked_bar( 'q025','q002', 'Income Sufficiency across Age Groups')
# Health across Age Groups - A
visualizer.plot_proportional_stacked_bar('q025','q021f', ' Health across Age Groups - A')
# Health across Age Groups - B
visualizer.plot_proportional_stacked_bar( 'q025','q039i', ' Health across Age Groups - B')

# # Income sources vs age groups
income_sources_cols = ['q041a', 'q041b', 'q041c', 'q041d', 'q041e', 'q041f', 'q041g', 'q041h', 'q041i', 'q041j', 'q041k', 'q041l', 'q041m', 'q041n', 'q041o', 'q041p', 'q041q', 'q041r', 'q041u']
processed_data ['income_sources_counts'] = processed_data[income_sources_cols].count(axis=1)
visualizer.plot_proportional_stacked_bar('q025','income_sources_counts', ' Income sources across Age Groups ')

# Housuing types across Age Groups 
visualizer.plot_proportional_stacked_bar( 'q025','q040a', ' Housing types across Age Groups - A')



#---------------------------------------------------- CHAPTER 7 -----------------------------------------------------------
# Define the sub-dataframes with meaningful names
families_receiving_child_benefits = processed_data[
    (processed_data['q041k'] == 'Canada child benefit (ccb)') & (processed_data['q027'] == 'Yes')
]
families_not_receiving_child_benefits = processed_data[
    (processed_data['q041k'].isna()) & (processed_data['q027'] == 'Yes')
]

# Visualize food security status for families receiving child benefits
visualizer.plot_proportional_stacked_bar(
    col1='q041k',
    col2='food_security_status',
    title='Food Security Status for Families Receiving Child Benefits',
    df=families_receiving_child_benefits
)
# Visualize food security status for families NOT receiving child benefits
visualizer.plot_column_frequency_stacked_proportion(
    col_name='food_security_status', 
    xlabel='Food Security', 
    plot_title='Food Security Status for Families Not Receiving Child Benefits (Stacked)', 
    df=families_not_receiving_child_benefits
)



# Visualize Food Security Status for Families with Reported Children (rc)

# Identify families that reported having children
has_reported_children_condition = processed_data[['q029', 'q030', 'q031', 'q032']].sum(axis=1) > 0

df_rc = processed_data.loc[has_reported_children_condition].copy()
# Visualize food security status for respondents with Reported Children
visualizer.plot_column_frequency_stacked_proportion(
    col_name='food_security_status', 
    xlabel='Food Security', 
    plot_title='Food Security Status for Families With Reported Children', 
    df=df_rc
)


# Calculate Percentage of Children in Food-Insecure Households

# Total number of children across all families
df_rc['number_of_children'] = df_rc[['q029', 'q030', 'q031', 'q032']].count(axis=1)
total_reported_children = df_rc['number_of_children'].sum()
# Condition to filter families with insecure food security status
food_insecure_condition = df_rc['food_security_status'].isin(['Very low food security', 'Low food security', 'Marginal food security'])
# Total number of children in food-insecure households
total_children_in_food_insecure_households = df_rc[food_insecure_condition]['number_of_children'].sum()
# Calculate the percentage
percentage_children_in_food_insecure_households = (total_children_in_food_insecure_households / total_reported_children) * 100
# Create a bar chart to visualize the percentage
labels = ['Kids in Food-Insecure Households', 'Kids in Food-Secure Households']
percentages = [percentage_children_in_food_insecure_households, 100 - percentage_children_in_food_insecure_households]
plt.bar(labels, percentages, color=['red', 'green'])
plt.title('Percentage of Children in Food-Insecure Households')
plt.ylabel('Percentage')
plt.ylim(0, 100)
# Add text labels on the bars
for i in range(len(labels)):
    plt.text(i, percentages[i] +1 , f'{percentages[i]:.2f}%', ha='center', fontsize=12)
plt.show()
