import numpy as np
from dataset_mappers import text_to_number 

class DatasetValidator:
    '''
    Remove or Update Inconsistent Rows in the neighbour survey dataset: 
        - Results in maintaining the integrity and reliability of the data for subsequent analysis.
    '''
    def __init__(self, df):
        self.df = df


    def get_number_of_rows(self):
        """Get the number of rows in a DataFrame"""
        return len(self.df)
    
    def drop_all_na_rows(self):
        """Drop rows where all values are NA"""
        initial_rows = self.get_number_of_rows()
        self.df = self.df[~self.df.isnull().all(axis=1)]
        print(f"drop_all_na_rows: Deleted {initial_rows - self.get_number_of_rows()} rows. Current number of rows: {self.get_number_of_rows()}")

    def remove_duplicates(self):
        """Remove all duplicate rows"""
        initial_rows = self.get_number_of_rows()
        self.df = self.df[~self.df.duplicated()]
        print(f"remove_duplicates: Deleted {initial_rows - self.get_number_of_rows()} rows. Current number of rows: {self.get_number_of_rows()}")

    
    def validate_income_sources(self):
        """Validate income sources to ensure mutually exclusive conditions are respected."""
        initial_rows = self.get_number_of_rows()
        conditions = [
            (self.df['q041a'].notna() & self.df['q041b'].notna()),
            (self.df['q041c'].notna() & self.df['q041d'].notna()),
            (self.df['q041e'].notna() & self.df['q041h'].notna()),
            (self.df['q041q'].notna() & self.df['q041p'].notna()),
            (self.df['q041q'].notna() & self.df['q041c'].notna()),
        ]
        for condition in conditions:
            self.df = self.df[~condition]
        print(f"validate_income_sources: Deleted {initial_rows - self.get_number_of_rows()} rows. Current number of rows: {self.get_number_of_rows()}")

    def validate_health_conditions(self):
        """Validate health conditions to ensure mutually exclusive conditions are respected."""
        initial_rows = self.get_number_of_rows()
        condition = self.df['q039a'].notna() & (self.df[['q039b', 'q039c', 'q039d', 'q039e', 'q039f', 'q039g']].any(axis=1))
        self.df = self.df[~condition]
        print(f"validate_health_conditions: Deleted {initial_rows - self.get_number_of_rows()} rows. Current number of rows: {self.get_number_of_rows()}")

    def validate_ethnicity(self):
        """Validate ethnicity responses to ensure mutually exclusive conditions are respected."""
        initial_rows = self.get_number_of_rows()
        conditions = [
            (self.df['q038j'].notna() & (self.df[['q038a', 'q038b', 'q038c', 'q038d', 'q038e', 'q038f', 'q038g', 'q038h', 'q038i', 'q038k']].any(axis=1))), # prefer not to answer
            (self.df['q038i'].notna() & (self.df[['q038a', 'q038b', 'q038c', 'q038d', 'q038e', 'q038f', 'q038g', 'q038h', 'q038k']].any(axis=1))) # I do not know
        ]
        for condition in conditions:
            self.df = self.df[~condition]
        print(f"validate_ethnicity: Deleted {initial_rows - self.get_number_of_rows()} rows. Current number of rows: {self.get_number_of_rows()}")

    def validate_education(self):
        """Validate education responses to ensure mutually exclusive conditions are respected."""
        initial_rows = self.get_number_of_rows()
        condition = self.df['q033i'].notna() & (self.df[['q033a', 'q033b', 'q033c', 'q033d', 'q033e', 'q033f', 'q033g', 'q033h']].any(axis=1))
        self.df = self.df[~condition]
        print(f"validate_education: Deleted {initial_rows - self.get_number_of_rows()} rows. Current number of rows: {self.get_number_of_rows()}")


    def validate_children_in_household(self): #No rows discarded , but specific column(s) updated
        """Validate children in household responses to ensure consistency with the reported number of children."""
        initial_rows = self.get_number_of_rows() 
        # Transform values in columns 'q029', 'q030','q031', 'q032 using text_to_number mapper
        for col in ['q029', 'q030','q031', 'q032']:
             self.df[col] = self.df[col].str.strip().str.lower().map(text_to_number)

        # Define conditions for logical consistency
        condition_no_children = (self.df['q027'] == 'No') & (self.df[['q029', 'q030', 'q031', 'q032']].fillna(0).sum(axis=1) > 0)
        condition_prefer_not = (self.df['q027'] == 'Prefer not to answer') & self.df[['q029', 'q030', 'q031', 'q032']].notna().any(axis=1)
        condition_yes_children = (self.df['q027'] == 'Yes') & (self.df[['q029', 'q030', 'q031', 'q032']].fillna(0).sum(axis=1) == 0)

        # New conditions for child benefit inconsistencies
        condition_no_children_1 = (self.df['q027'] == 'No') & (self.df['q041k'].notna())
        condition_skipped_q027 = (self.df['q027'].isna()) & (self.df['q041k'].notna())

        # Update the inconsistent values
        self.df.loc[condition_no_children, ['q029', 'q030', 'q031', 'q032']] = 0  # maintain respondent's original intent
        self.df.loc[condition_prefer_not, ['q029', 'q030', 'q031', 'q032']] = np.nan  # maintain respondent's original intent
        self.df.loc[condition_yes_children, ['q029', 'q030', 'q031', 'q032']] = np.nan # maintain respondent's original intent and reflect non-disclosure.
        
        # Update the child benefit inconsistencies
        self.df.loc[condition_no_children_1, 'q041k'] = np.nan  # maintain respondent's original intent
        self.df.loc[condition_skipped_q027, 'q041k'] = np.nan # maintain respondent's original intent

        print(f"validate_children_in_household: Deleted {initial_rows - self.get_number_of_rows()} rows. Current number of rows: {self.get_number_of_rows()}")



    def validate_breastfeeding(self):
        """Validate breastfeeding responses to ensure only one option is selected."""
        initial_rows = self.get_number_of_rows()
        self.df = self.df[
            ~(
                (self.df[['q028a', 'q028b', 'q028c', 'q028d']].count(axis=1) > 1)
            )
        ]
        print(f"validate_breastfeeding: Deleted {initial_rows - self.get_number_of_rows()} rows. Current number of rows: {self.get_number_of_rows()}")

    
    def validate_unique_food_needs(self):
        """Validate unique food needs responses to ensure 'none of the above' is not selected with any other options."""
        initial_rows = self.get_number_of_rows()
        # Condition where 'none of the above' is selected with any other options
        condition_none_of_above = self.df['q023a'].notna() & (self.df[['q023b', 'q023c', 'q023d', 'q023e', 'q023f']].notna().any(axis=1))
    
        # Remove rows with 'none of the above' selected alongside any other options
        self.df = self.df[~condition_none_of_above]
        print(f"validate_unique_food_needs: Deleted {initial_rows - self.get_number_of_rows()} rows. Current number of rows: {self.get_number_of_rows()}")
        

    def validate_special_food_needs(self): # No rows discarded , but specific column(s) updated 
        """Validate special food needs responses to ensure 'no special food' is not selected with any other options."""
        initial_rows = self.get_number_of_rows()
        # Identify rows with inconsistencies in special food needs
        condition_no_special = self.df['q024g'].notna() & self.df[['q024a', 'q024b', 'q024c', 'q024d', 'q024e', 'q024f', 'q024h', 'q024i']].any(axis=1)
        # Replace 'no special food' with np.nan for those rows
        self.df.loc[condition_no_special, 'q024g'] = np.nan
        print(f"validate_special_food_needs: Deleted {initial_rows - self.get_number_of_rows()} rows. Current number of rows: {self.get_number_of_rows()}")

 

    def validate_health_conditions_detailed(self):  # No rows discarded , but specific column(s) updated 
        """Validate detailed health conditions responses to ensure mutually exclusive conditions are respected."""
        initial_rows = self.get_number_of_rows()
        condition_no_health = self.df['q021e'].notna() & (self.df[['q021a', 'q021b', 'q021c', 'q021d']].any(axis=1))
        condition_prefer_not = self.df['q021a'].notna() & (self.df[['q021b', 'q021c', 'q021d', 'q021e', 'q021f']].any(axis=1))

        # Update the 'q021e' column to NaN for the rows that meet the condition.
        self.df.loc[condition_no_health, 'q021e'] = np.nan
        # Update the 'q021a' column to NaN for the rows that meet the condition
        self.df.loc[condition_prefer_not, 'q021a'] = np.nan
        print(f"validate_health_conditions_detailed: Deleted {initial_rows - self.get_number_of_rows()} rows. Current number of rows: {self.get_number_of_rows()}")
        
        

    def validate_other_food_program_services(self): # No rows discarded , but specific column(s) updated
        """Validate other food program services responses to ensure 'None' is not selected with any other options."""
        initial_rows = self.get_number_of_rows()
        condition_none = self.df['q017i'].notna() & (self.df[['q017a', 'q017b', 'q017c', 'q017d', 'q017e', 'q017f', 'q017g', 'q017h']].any(axis=1))
        # Set 'q017i' to NaN for the identified rows
        self.df.loc[condition_none, 'q017i'] = np.nan
        print(f"validate_other_food_program_services: Deleted {initial_rows - self.get_number_of_rows()} rows. Current number of rows: {self.get_number_of_rows()}")
        

    def validate_food_program_access(self): # No rows discarded , but specific column(s) updated
        """Validate food program access responses to ensure 'None' is not selected with any other options."""
        initial_rows = self.get_number_of_rows()
        condition_none = self.df['q014a'].notna() & (self.df[['q014b', 'q014c', 'q014d', 'q014e', 'q014f']].any(axis=1))
        self.df.loc[condition_none,'q014a'] = np.nan
        print(f"validate_food_program_access: Deleted {initial_rows - self.get_number_of_rows()} rows. Current number of rows: {self.get_number_of_rows()}")



    def validate_exercise(self):
        """Validate exercise responses to ensure logical consistency with the reported exercise frequency."""
        initial_rows = self.get_number_of_rows()
        # Define conditions for logical consistency
        condition_no_exercise = (self.df['q019'] == 'No') & self.df['q020'].isin([
            '2-4 times a week', '5 or more times a week', 'Daily', 'daily', 'less than 1 time a week', 'Less than 1 time a week','Prefer not to answer',
        ])
        condition_prefer_not = (self.df['q019'] == 'Prefer not to answer') & self.df['q020'].isin([
            '2-4 times a week', '5 or more times a week', 'Daily', 'daily', 'do not exercise',  'Do not exercise', 'less than 1 time a week', 'Less than 1 time a week'
        ])
        condition_yes_exercise = (self.df['q019'] == 'Yes') & self.df['q020'].isin(['do not exercise', 'Do not exercise'])

        # Update the inconsistent values
        self.df.loc[condition_no_exercise, 'q020'] = 'Do not exercise' # maintain respondent's original intent
        self.df.loc[condition_prefer_not, 'q020'] = 'Prefer not to answer' # maintain respondent's original intent
        self.df.loc[condition_yes_exercise, 'q020'] = np.nan # maintain respondent's original intent
        print(f"validate_exercise: Deleted {initial_rows - self.get_number_of_rows()} rows. Current number of rows: {self.get_number_of_rows()}")
    


    def validate_food_security_score_fields(self):  # No rows discarded , but specific column(s) updated 
        """Validate food security score fields to ensure logical consistency."""
        initial_rows = self.get_number_of_rows()
        # Define conditions for logical consistency
        condition_yes = (self.df['q005'] == 'Yes') & (self.df['q006'] =='Never true')
        condition_prefer_not = (self.df['q005'] == 'Prefer not to answer') & self.df['q006'].isin([ 'Almost every month', 'Never true', "don't know", "Don't know" , 'Only 1 or 2 months', 'Some months but not every month'])
        condition_no = (self.df['q005'] == 'No') & self.df['q006'].isin(['Almost every month', "don't know", "Don't know", 'Only 1 or 2 months', 'Prefer not to answer', 'Some months but not every month'])
        condition_dont_know = (self.df['q005'].isin(["Don't know", "don't know"]) & self.df['q006'].isin(['Almost every month', 'Did not happen', 'Only 1 or 2 months', 'Prefer not to answer', 'Some months but not every month']))
        
        # Update the inconsistent values
        self.df.loc[condition_yes, 'q006'] = np.nan # maintain respondent's original intent
        self.df.loc[condition_prefer_not, 'q006'] = 'Prefer not to answer' # # maintain respondent's original intent  (np.nan is also valid here)
        self.df.loc[condition_no, 'q006'] = 'Never true' # maintain respondent's original intent
        self.df.loc[condition_dont_know, 'q006'] = "don't know" # maintain respondent's original intent
        print(f"validate_food_security_score_fields: Deleted {initial_rows - self.get_number_of_rows()} rows. Current number of rows: {self.get_number_of_rows()}")



    def run_all_validations(self):
        self.drop_all_na_rows()
        self.remove_duplicates()
        self.validate_income_sources()
        self.validate_health_conditions()
        self.validate_ethnicity()
        self.validate_education()
        self.validate_children_in_household()
        self.validate_breastfeeding()
        self.validate_unique_food_needs()
        self.validate_special_food_needs()
        self.validate_health_conditions_detailed()
        self.validate_exercise()
        self.validate_other_food_program_services()
        self.validate_food_program_access()
        self.validate_food_security_score_fields()

