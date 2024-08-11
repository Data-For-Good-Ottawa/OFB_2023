import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
def load_data(file_path):
    return pd.read_csv(file_path)

# Restructure income data
def restructure_income_data(df):

    # Ensure column names are lowercase for consistency
    df.columns = df.columns.str.lower()
    df['id'] = df.index

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
def create_stacked_bar_chart(df, id_column='id', output_file='food_security_chart.png'):
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
def analyze_income_types_per_person(df, id_column='id'):
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
    
    # Analyze multiple income sources
    income_sources_count = df.groupby(id_column)['income_type'].nunique()
    multiple_sources = (income_sources_count > 1).sum()
    multiple_sources_percentage = (multiple_sources / total_persons) * 100

    # Plot a bar chart of income types
    plt.figure(figsize=(12, 6))
    income_analysis['Count'].plot(kind='bar')
    plt.title('Number of People with Each Income Type')
    plt.xlabel('Income Type')
    plt.ylabel('Number of People')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('income_types_per_person.png')

    return income_analysis, multiple_sources, multiple_sources_percentage, total_persons

# Main execution
if __name__ == "__main__":
    df = load_data('neighbour_survey_clean-2024-08-11.csv')
    restructured_df = restructure_income_data(df)
    pivot_percentage = create_stacked_bar_chart(restructured_df, output_file='food_security_by_income_source.png')
    income_analysis, multiple_sources, multiple_sources_percentage, total_persons = analyze_income_types_per_person(restructured_df)
    
    print(f"Total number of unique persons: {total_persons}")
    print(f"Number of people with multiple income sources: {multiple_sources}")
    print(f"Percentage of people with multiple income sources: {multiple_sources_percentage:.2f}%")
    print("\nIncome type analysis per person:")
    print(income_analysis)