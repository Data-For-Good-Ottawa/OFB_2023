# Income Source Analysis

## Overview

My analysis consists of two Python files: `income_analysis.py` and `main.py`. The `income_analysis.py` file contains functions to restructure the income data and analyze the relationship between income source and food security status. The `main.py` file is adapted from Mohammed's code. I added statements to import and run the functions in `income_analysis.py`.

The analysis depends on Mohammed's scripts for preprocessing and cleaning the data (`dataset_mappers`, `dataset_analyzer`, `dataset_validator`, `dataset_visualizer` and `dataset_processor`).

The lines I added to Mohammed's main.py file are:

```python
# Visualize income source data
from income_source_analysis import restructure_income_data, create_stacked_bar_chart, analyze_income_types_per_person
restructured_df = restructure_income_data(processed_data)
create_stacked_bar_chart(restructured_df, output_file='food_security_by_income_source.png')
analyze_income_types_per_person(restructured_df)
```

## Functions

These functions are as follows:

- `restructure_income_data`: Since the different income categories are divided across columns this function converts it into a long format with a single column for income source and multiple rows per person if they have multiple income sources. It also handles entries in the 'other' column that match existing categories. 

- `create_stacked_bar_chart`: This function generates a horizontal stacked bar chart to visualize the proportion of different food security statuses within each income type. It calculates the percentage of each food security status relative to the total for each income type. The chart is exported as `food_security_by_income_source.png`.

- `analyze_income_types_per_person`: This function calculates and visualizes the number of unique people associated with each income type. It computes both the count and percentage of people with each income type and generates a bar chart showing the distribution. This is exported as `income_source_counts.png`.

## Results and Interpretation

The bar chart shown `income_source_counts.png` shows that the most common reported income was 'Employed at least 35 hours each week', which was reported by 26.2% of food bank users. The second most common income source was 'Employed less than 35 hours each week', reported by 24.1%. This was followed by 'Ontario works' at 15.2% and Ontario disability support program at 10.3%. A quarter of respondents (23.50%) reported having more than one income source. Overall, this implies that around half of food bank users are employed. However, this may be slightly higher as 4.8% selected 'Prefer not to answer'.

The stacked bar chart `food_security_by_income_source.png` shows that the percentage of people living with Very low food security varies depending on the income source. The most extreme levels of very low food security are seen in people who are Ontario Disability Support Program (75.3%), Family support (74.3%), Ontario Trillium Benefit (72.3%), those employed less than 35 hours each week (71.6%) and those with short/long term disability (69.6%). The extremely high percentages of very low food security in these groups suggest that current social assistance programs may not be sufficient to ensure basic nutritional needs. The data indicates that living with a disability is associated with experiencing very low food security. 

Reduced levels of very low food security were reported by people who preferred not to share their income (34.4%). People in this group had much higher food security than other respondents with 24% reporting high food security. It could suggest that some in this category have higher incomes but are reluctant to disclose them.

Overall, the majority of recipients of all income sources reported having very low food security.




