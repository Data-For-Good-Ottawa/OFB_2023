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
from income_source_analysis import restructure_income_data, create_stacked_bar_chart, analyze_income_types_per_person

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
# Grouped Bar Plot function
visualizer.plot_column_frequency('food_security_score', 'Food security scores')
# Grouped Bar Plot function
pairs =[('q014a', 'None of the above'),  ('q014b', 'Language barriers'),  ('q014c', 'Physical inaccessibility'),  ('q014d', 'Safety concerns'),  ('q014e', 'Transportation barriers'),  ('q014f', 'Program hours of operation'),  ('q014g', 'Prefer not to answer')]
question_category = "Food Programs Access Barrier"
visualizer.plot_grouped_columns_frequency(pairs, question_category)
# Stacked bar plot function:
pairs =[('q014a', 'None of the above'),  ('q014b', 'Language barriers'),  ('q014c', 'Physical inaccessibility'),  ('q014d', 'Safety concerns'),  ('q014e', 'Transportation barriers'),  ('q014f', 'Program hours of operation'),  ('q014g', 'Prefer not to answer')]
question_category = "Food Programs Access Barrier"
visualizer.plot_stacked_columns_frequency(pairs, "Title", question_category)
#Heatmap function:
cols = ['q014a', 'q014b', 'q014c', 'q014d', 'q014e', 'q014f', 'q014g']
question_category = "Food Programs Access Barrier"
visualizer.plot_heatmap_columns_frequency(cols, question_category)
# plot proportional stack bar plot
visualizer.plot_proportional_stacked_bar('q040a','food_security_status','Proportional Bar Plot: Food Security Status across Housing Situations')






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
analyzer.perform_data_analysis(variables_to_analyze)

analyzer. visualize_participants_demographics() # Chapter 1 
analyzer.visualize_participants_food_bank_info() # Chapter 1 

# Visualize income source data
restructured_df = restructure_income_data(processed_data)
create_stacked_bar_chart(restructured_df, output_file='food_security_by_income_source.png')
analyze_income_types_per_person(restructured_df)
