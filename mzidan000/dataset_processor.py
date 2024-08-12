import pandas as pd
import numpy as np

class DatasetProcessor:
    """
    Class for processing the neighbour survey dataset.
    
    Class Example usage:
            df = pd.read_csv('neighbour_survey_data.csv')
            processor = DatasetProcessor(df)
            df_processed = processor.process_data(col_descr_115_dict,col_mapping_16_dict)
            print(df_processed)
    """
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def process_data(self, col_descr_115_dict: dict, col_mapping_16_dict: dict) -> pd.DataFrame:
        """
        Process all necessary columns of a DataFrame using the provided mappers.

        Parameters:
            self: The instance of DatasetProcessor containing the DataFrame as an attribute.
            col_descr_115_dict (dict): The mapper for processing 115 specific columns of the DataFrame
            col_mapping_16_dict (dict): The mapper for processing the other 16 columns of the DataFrame

        Returns:
            pd.DataFrame: The processed DataFrame with added columns for food security scores, statuses, and descriptions.
        """
        initial_row_count = len(self.df)
        print(f"Initial row count: {initial_row_count}")
        # Processing 115 columns
        for col_name in col_descr_115_dict:
            self.process_115_columns(col_name)
        print(f"Row count after processing 115 columns: {len(self.df)}")
        
        # Processing 16 columns
        for col_name, col_mapping in col_mapping_16_dict.items():
             self.process_16_columns(col_name, col_mapping)
        print(f"Row count after processing 16 columns: {len(self.df)}")
        
        # Adding 3 food security status-related columns
        self.df = self.get_food_security_status()
        print(f"Final row count after adding food security status columns: {len(self.df)}")
        return self.df

    def process_115_columns(self, col_name: str) -> None:
        """
        Function for processing 115 specific columns in a DataFrame:
        This function standardizes the formatting of text data in specified columns by stripping 
        extra spaces and capitalizing the first letter of each word.

        Parameters:
            self: The instance of DatasetProcessor containing the DataFrame as an attribute.
            col_name (str): The name of the column to process (i.e 'q001')

        Returns:
            None: The function modifies the DataFrame in place.
        """
        self.df[col_name] = self.df[col_name].apply(lambda s: s if pd.isna(s) else ' '.join(s.split()).capitalize())

    def process_16_columns(self, col_name: str, col_mapper: dict) -> None:
        """
        Function for processing 16 specific columns in a DataFrame:
        This function standardizes and maps the values of a specified column based on a provided mapping dictionary.

        Parameters:
            self: The instance of DatasetProcessor containing the DataFrame as an attribute.
            col_name (str): The name of the column to process (i.e 'q021f' , 'q011b')
            col_mapper (dict): A dictionary mapping the column's original values to standardized values or categories (i.e 'text_to_health_conditions', 'text_to_food_program_frequency')

        Returns:
            None: The function modifies the DataFrame in place.
  
        """ 
        if col_name != 'q012':
            self.df[col_name] = self.df[col_name].str.strip().str.lower().map(col_mapper)
        else:
            self.df[col_name] = self.df[col_name].str.strip().str.lower().replace(col_mapper)

    def get_food_security_status(self) -> pd.DataFrame:
        """
        Function to calculate food security scores, statuses, and descriptions based on survey responses in the DataFrame.

        Parameters:
            self: The instance of DatasetProcessor containing the DataFrame as an attribute.

        Returns:
            pd.DataFrame: The original DataFrame with added columns for food security scores, statuses, and descriptions.

        Food security status is assigned as follows:
            - Raw score 0-1: High or marginal food security
            - Raw score 2-4: Low food security.
            - Raw score 5-6: Very low food security.

        Food security description is assigned as follows:
            - Raw score 0-1 is described as food secure
            - Raw score 2-6 is described as food insecure

        """
        food_security_scores = []
        food_security_statuses = []
        food_security_status_descriptions = []

        for row_label, row_series in self.df.iterrows():
            affirmative_responses = 0 
            if row_series['q003'] == 'Often true' or row_series['q003'] == 'Sometimes true':
                affirmative_responses += 1
                
            if row_series['q004'] in ['Often true', 'Sometimes true']:
                affirmative_responses += 1
                
            if row_series['q005'] == 'Yes':
                affirmative_responses += 1
                
            if row_series['q006'] in ['Almost every month', 'Some months but not every month']:
                affirmative_responses += 1
            
            if row_series['q007'] == 'Yes':
                affirmative_responses += 1
            
            if row_series['q008'] == 'Yes':
                affirmative_responses += 1
        
            food_security_scores.append(affirmative_responses)
        
            if affirmative_responses == 0:
                food_security_statuses.append('High food security')
                food_security_status_descriptions.append('Food secure')
                
            elif affirmative_responses == 1:
                food_security_statuses.append('Marginal food security')
                food_security_status_descriptions.append('Food secure')
                
            elif 2 <= affirmative_responses <= 4:
                food_security_statuses.append('Low food security')
                food_security_status_descriptions.append('Food insecure')
        
            else:
                food_security_statuses.append('Very low food security')
                food_security_status_descriptions.append('Food insecure')
        
        new_columns_df = pd.DataFrame({
            'food_security_score': food_security_scores,
            'food_security_status': food_security_statuses,
            'food_security_status_description': food_security_status_descriptions
        }, index = self.df.index) # Ensure the index matches
   

        print (f'Are the concantenated df indexes aligned {new_columns_df.index == self.df.index}')
        
        self.df = pd.concat([self.df, new_columns_df], axis=1)
        return self.df


