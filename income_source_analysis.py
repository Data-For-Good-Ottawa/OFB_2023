import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Restructure income data
def restructure_income_data(df):
    """
    Restructure the income data in a DataFrame from a wide format to a long format.

    This function takes a DataFrame where different income categories are spread across multiple columns,
    and converts it into a long format where there is a single column for income source and multiple rows
    per person if they have multiple income sources. The function also handles entries in the 'other' column
    that might match existing income categories.

    Args:
        df (pandas.DataFrame): Input DataFrame containing income data with columns for various income sources
                               and an 'other' column for additional income sources.

    Returns:
        pandas.DataFrame: A long-format DataFrame where each row represents a single income source for a person,
                          with columns for the person ID, any additional non-income columns, and the income type.
                          
    Raises:
        ValueError: If the DataFrame does not contain an 'id' column or if any of the expected income columns
                    or the 'other' column are missing.
    """

    # Ensure column names are lowercase for consistency
    df.columns = df.columns.str.lower()

    # Add id column 

    df['id'] = range(1, len(df) + 1)

    # Find the ID column
    id_column = next((col for col in df.columns if 'id' in col.lower()), None)
    if id_column is None:
        raise ValueError("No column containing 'id' found in the DataFrame")

    # Define income columns and other column
    income_columns = [f'q041{chr(c)}' for c in range(ord('a'), ord('t')+1)]
    other_column = 'q041u'
    
    # Ensure all expected columns are present
    missing_columns = [col for col in income_columns + [other_column] if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing expected columns: {', '.join(missing_columns)}")
    
    # Define the correct mapping of keywords to income columns
    keyword_mapping = {
        'Employed at least 35 hours each week': 'q041a',
        'Employed less than 35 hours each week': 'q041b',
        'Ontario disability support program (odsp)': 'q041c',
        'Ontario works (ow)': 'q041d',
        'Canada emergency response benefit (cerb)': 'q041e',
        'Scholarship': 'q041f',
        'Student loans': 'q041g',
        'Employment insurance (ei)': 'q041h',
        'Family support': 'q041i',
        'Spousal support': 'q041j',
        'Canada child benefit (ccb)': 'q041k',
        'Ontario trillium benefit (otb)': 'q041l',
        'Canadian pension plan (cpp)': 'q041m',
        'Private pension': 'q041n',
        'Old age security (oas)': 'q041o',
        'Workplace safety and insurance board (wsib)': 'q041p',
        'Short/long term disability': 'q041q',
        'Other government programs': 'q041r',
        'No income': 'q041s',
        'Prefer not to answer': 'q041t'
    }
    
    # Identify non-income columns to preserve
    non_income_columns = [col for col in df.columns if col not in income_columns and col != other_column and col != id_column]
    
    # Create a long DataFrame for regular income columns
    long_df = df.melt(id_vars=[id_column] + non_income_columns, value_vars=income_columns, var_name='income_column', value_name='has_income')
    long_df = long_df[long_df['has_income'].notna()]
    
    # Map income columns to their descriptions
    reverse_mapping = {v: k for k, v in keyword_mapping.items()}
    long_df['income_type'] = long_df['income_column'].map(reverse_mapping)
    
    # Process the "Other" column
    other_df = df[df[other_column].notna()][[id_column] + non_income_columns + [other_column]]
    other_income_types = []
    
    for _, row in other_df.iterrows():
        other_incomes = [keyword for keyword in keyword_mapping.keys() if keyword.lower() in str(row[other_column]).lower()]
        other_income_types.extend([(row[id_column], *[row[col] for col in non_income_columns], income) for income in other_incomes])
    
    other_long_df = pd.DataFrame(other_income_types, columns=[id_column] + non_income_columns + ['income_type'])
    
    # Combine regular and "Other" income data
    final_df = pd.concat([long_df[[id_column] + non_income_columns + ['income_type']], other_long_df])
    final_df = final_df.drop_duplicates().reset_index(drop=True)
    
    return final_df

# Create a stacked bar chart
def create_stacked_bar_chart(df, id_column='id', output_file='food_security_by_income_source.png'):
    """
    Create and save a stacked bar chart displaying the percentage distribution of food security status by income type.

    This function generates a horizontal stacked bar chart to visualize the proportion of different food security statuses
    within each income type. It calculates the percentage of each food security status relative to the total for each income type.

    Args:
        df (pandas.DataFrame): Input DataFrame containing columns for 'income_type', 'food_security_status', and the id column.
        id_column (str): The name of the column containing unique identifiers for individuals (default is 'id').
        output_file (str): The filename for saving the generated chart (default is 'food_security_by_income_source.png').

    Returns:
        pandas.DataFrame: A DataFrame with the percentage distribution of food security status by income type, suitable for
                          further analysis or visualization.

    Raises:
        ValueError: If the DataFrame does not contain the required columns.
    """
    print(df.columns)
    # Create a pivot table of income types and food security status
    pivot = pd.pivot_table(df, values=id_column, index='income_type', columns='food_security_status', aggfunc='count', fill_value=0)
    
    # Calculate percentages
    pivot_percentage = pivot.div(pivot.sum(axis=1), axis=0) * 100
    
    # Define the correct order of food security status
    correct_order = ['High food security', 'Marginal food security', 'Low food security', 'Very low food security']
    
    # Define a color palette (colorblind-friendly)
    colors = ['#1a9850', '#91cf60', '#fee08b', '#fc8d59']
    
    # Reorder the columns and sort the rows
    pivot_percentage = pivot_percentage[correct_order]
    pivot_percentage = pivot_percentage.sort_values(by='Very low food security', ascending=False)
    
    # Set up the plot
    fig, ax = plt.subplots(figsize=(20, 10))
    
    # Plot the bars
    pivot_percentage.plot(kind='barh', stacked=True, width=0.7, ax=ax, color=colors)
    
    # Customize the plot
    ax.set_title('Food Security Status by Income Type', fontsize=18, fontweight='bold')
    ax.set_xlabel('Percentage', fontsize=14)
    ax.set_ylabel('Income Type', fontsize=14)
    ax.legend(title='Food Security Status', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=12)
    
    # Add percentage labels on the bars
    for c in ax.containers:
        ax.bar_label(c, fmt='%.1f%%', label_type='center', fontsize=10, fontweight='bold')
    
    # Adjust y-axis to add space between labels
    num_categories = len(pivot_percentage)
    y_positions = range(num_categories)
    ax.set_yticks(y_positions)
    ax.set_yticklabels(pivot_percentage.index, fontsize=12)
    
    # Increase spacing between y-axis ticks
    ax.set_ylim(-1, num_categories)
    
    # Increase font size for tick labels
    ax.tick_params(axis='x', which='major', labelsize=12)
    
    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Add a grid for better readability
    ax.grid(axis='x', linestyle='--', alpha=0.7)
    
    # Adjust layout
    plt.tight_layout()
    
    # Save the plot as a PNG file
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    
    # Close the figure to free up memory
    plt.close(fig)
    
    print(f"Chart saved as {output_file}")
    
    return pivot_percentage

# Analyze income types per person

import pandas as pd
import matplotlib.pyplot as plt

def analyze_income_types_per_person(df, id_column='id'):
    """
    Analyze and visualize the distribution of income types per person.

    This function calculates and visualizes the number of unique people associated with each income type. It computes
    both the count and percentage of people with each income type and generates a bar chart showing the distribution.

    Args:
        df (pandas.DataFrame): Input DataFrame containing the income types and a unique identifier column.
        id_column (str): The name of the column containing unique identifiers for individuals (default is 'id').

    Returns:
        pandas.DataFrame: A DataFrame with the count and percentage of people associated with each income type,
                          sorted by the count in descending order.

    Raises:
        KeyError: If the specified id_column does not exist in the DataFrame.
    """
    # Ensure we're working with unique persons
    unique_persons = df.drop_duplicates(subset=[id_column])
    total_persons = len(unique_persons)

    # Count how many people have each income type
    income_counts = df.groupby(id_column)['income_type'].apply(set).apply(list).explode().value_counts()
    
    # Calculate the percentage of people with each income type
    income_percentages = (income_counts / total_persons) * 100
    
    # Combine counts and percentages into a single DataFrame
    income_analysis = pd.DataFrame({
        'Count': income_counts,
        'Percentage of People': income_percentages
    }).sort_values('Count', ascending=False)

    multiple_income_sources_percentage = (df.groupby(id_column)['income_type'].nunique() > 1).mean() * 100
    print(f'{multiple_income_sources_percentage:.2f}% of people reported multiple income sources.')
    
    # Plot a bar chart of income types
    plt.figure(figsize=(12, 6))
    ax = income_analysis['Count'].plot(kind='bar')
    plt.title('Number of People with Each Income Type')
    plt.xlabel('Income Type')
    plt.ylabel('Number of People')
    plt.xticks(rotation=45, ha='right')

    # Remove the top and right spines (bounding box lines)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    
    # Annotate each bar with the percentage of total unique people
    for p, percentage in zip(ax.patches, income_analysis['Percentage of People']):
        height = p.get_height()
        ax.annotate(f'{percentage:.1f}%', 
                    (p.get_x() + p.get_width() / 2, height),
                    xytext=(0, 5), 
                    textcoords='offset points',
                    ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig('income_source_counts.png')

    return income_analysis