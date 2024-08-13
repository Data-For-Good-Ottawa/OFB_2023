from constants import PathNeighbourSurvey, PathHungerCount, PathMemberAssetInventory
from Lib import data_loader as dl
import pandas as pd

df_neighbour_survey = dl.get_data_as_pandas_data_frame(PathNeighbourSurvey)
df_hunger_count = dl.get_data_as_pandas_data_frame(PathHungerCount)
df_member_asset_inventory = dl.get_data_as_pandas_data_frame(PathMemberAssetInventory)

#MAI calculations - how many days of food are provided per visitor and per month?

df_slice = df_member_asset_inventory[["id", "MAI_Q004_002", "MAI_Q004_003", "MAI_Q004_004", "MAI_Q004_005", "MAI_Q004_006", "MAI_Q004_007", "MAI_Q004_008", "MAI_Q004_009", "MAI_Q004_010", "MAI_Q004_011", "MAI_Q004_012", "MAI_Q004_013", "MAI_Q004_014", "MAI_Q004_015", "MAI_Q004_016", "MAI_Q004_017", "MAI_Q004_018", "MAI_Q004_019", "MAI_Q004_020", "MAI_Q004_021", "MAI_Q004_022", "MAI_Q004_023", "MAI_Q004_024", "MAI_Q031_001", "MAI_Q031_002", "MAI_Q031_003", "MAI_Q031_004", "MAI_Q031_005", "MAI_Q031_006", "MAI_Q031_007", "MAI_Q031_008", "MAI_Q031_009", "MAI_Q031_010", "MAI_Q031_011", "MAI_Q048", "MAI_Q051", "MAI_Q053_001", "MAI_Q053_002", "MAI_Q053_003", "MAI_Q053_004", "MAI_Q053_005", "MAI_Q053_006", "MAI_Q053_007", "MAI_Q053_008", "MAI_Q008"]]

num_rows = len(df_slice)
num_supports = 0
num_between_1_and_3_days = 0
num_over_3_days = 0
num_at_least_1_weekend_day = 0
num_over_500 = 0
num_over_5_days = 0
num_atypical_grocery_answer = 0
Food_bank_IDs = ["A005", "A011", "A020", "A024", "A028", "A029", "A031", "A032", "A037", "A038", "A039", "A041", "A046", "A047", "A050", "A057", "A058", "A060", "A062", "A064", "A065", "A076", "A082"]

df_slice.insert(21, "Number of wrap-around supports provided", "Empty")
df_slice.insert(22,"Hours of service per month","Empty")
df_slice.insert(23,"Visitors served per hour","Empty")
df_slice.insert(24,"Days of food provided per visitor","Empty")
df_slice.insert(25,"Days of food provided per month","Empty")
df_slice.insert(26, "Type of agency", "Empty")
df_slice.insert(27, "Effective number of staff/volunteers", "Empty")

x = 0

while x < num_rows:
    if pd.isna(df_slice.at[x, 'MAI_Q004_002']) == False:
        num_supports += 1
    if pd.isna(df_slice.at[x, 'MAI_Q004_003']) == False:
        num_supports += 1
    if pd.isna(df_slice.at[x, 'MAI_Q004_004']) == False:
        num_supports += 1
    if pd.isna(df_slice.at[x, 'MAI_Q004_005']) == False:
        num_supports += 1
    if pd.isna(df_slice.at[x, 'MAI_Q004_006']) == False:
        num_supports += 1
    if pd.isna(df_slice.at[x, 'MAI_Q004_007']) == False:
        num_supports += 1
    if pd.isna(df_slice.at[x, 'MAI_Q004_008']) == False:
        num_supports += 1
    if pd.isna(df_slice.at[x, 'MAI_Q004_009']) == False:
        num_supports += 1
    if pd.isna(df_slice.at[x, 'MAI_Q004_010']) == False:
        num_supports += 1
    if pd.isna(df_slice.at[x, 'MAI_Q004_011']) == False:
        num_supports += 1
    if pd.isna(df_slice.at[x, 'MAI_Q004_012']) == False:
        num_supports += 1
    if pd.isna(df_slice.at[x, 'MAI_Q004_013']) == False:
        num_supports += 1
    if pd.isna(df_slice.at[x, 'MAI_Q004_014']) == False:
        num_supports += 1 
    if pd.isna(df_slice.at[x, 'MAI_Q004_015']) == False:
        num_supports += 1 
    if pd.isna(df_slice.at[x, 'MAI_Q004_016']) == False:
        num_supports += 1 
    if pd.isna(df_slice.at[x, 'MAI_Q004_017']) == False:
        num_supports += 1
    if pd.isna(df_slice.at[x, 'MAI_Q004_018']) == False:
        num_supports += 1 
    if pd.isna(df_slice.at[x, 'MAI_Q004_019']) == False:
        num_supports += 1 
    if pd.isna(df_slice.at[x, 'MAI_Q004_020']) == False:
        num_supports += 1 
    if pd.isna(df_slice.at[x, 'MAI_Q004_021']) == False:
        num_supports += 1 
    if pd.isna(df_slice.at[x, 'MAI_Q004_022']) == False:
        num_supports += 1 
    if pd.isna(df_slice.at[x, 'MAI_Q004_023']) == False:
        num_supports += 1 
    if pd.isna(df_slice.at[x, 'MAI_Q004_024']) == False:
        num_supports += 1 
    
    if num_supports > 0:
        df_slice.loc[x, 'Number of wrap-around supports provided'] = num_supports
    else:
        df_slice.loc[x, 'Number of wrap-around supports provided'] = "NA"

    num_supports = 0
    x += 1
    


x = 0

while x < num_rows:
    if pd.isna(df_slice.at[x,'MAI_Q031_003']) == False:
        df_slice.loc[x,'Hours of service per month'] = 64
        num_between_1_and_3_days += 1
    elif pd.isna(df_slice.at[x,'MAI_Q031_004']) == False:
        df_slice.loc[x,'Hours of service per month'] = 128
        num_over_3_days += 1
    elif pd.isna(df_slice.at[x,'MAI_Q031_007']) == False:
        df_slice.loc[x, 'Hours of service per month'] = 48
        num_at_least_1_weekend_day += 1
    elif pd.isna(df_slice.at[x,'MAI_Q031_008']) == False:
        df_slice.loc[x, 'Hours of service per month'] = 16
    elif pd.isna(df_slice.at[x,'MAI_Q031_002']) == False:
        df_slice.loc[x, 'Hours of service per month'] = 16
    elif pd.isna(df_slice.at[x,'MAI_Q031_005']) == False:
        df_slice.loc[x, 'Hours of service per month'] = 48
    elif pd.isna(df_slice.at[x,'MAI_Q031_006']) == False:
        df_slice.loc[x, 'Hours of service per month'] = 8
    elif pd.isna(df_slice.at[x,'MAI_Q031_009']) == False:
        df_slice.loc[x, 'Hours of service per month'] = 28
    elif pd.isna(df_slice.at[x,'MAI_Q031_010']) == False:
        df_slice.loc[x, 'Hours of service per month'] = 28
    elif pd.isna(df_slice.at[x,'MAI_Q031_011']) == False:
        df_slice.loc[x, 'Hours of service per month'] = 28
    else:
        df_slice.loc[x, 'Hours of service per month'] = "NA"


    if df_slice.loc[x, 'MAI_Q051'] == "1-10 visitors":
        df_slice.loc[x, 'Visitors served per hour'] = 5
    elif df_slice.loc[x, 'MAI_Q051'] == "11-25 visitors":
        df_slice.loc[x, 'Visitors served per hour'] = 18
    elif df_slice.loc[x, 'MAI_Q051'] == "26-50 visitors":
        df_slice.loc[x, 'Visitors served per hour'] = 38
    elif df_slice.loc[x, 'MAI_Q051'] == "51-100 visitors":
        df_slice.loc[x, 'Visitors served per hour'] = 76
    elif df_slice.loc[x, 'MAI_Q051'] == "101-200 visitors":
        df_slice.loc[x, 'Visitors served per hour'] = 151
    elif df_slice.loc[x, 'MAI_Q051'] == "201-500 visitors":
        df_slice.loc[x, 'Visitors served per hour'] = 350
    elif df_slice.loc[x, 'MAI_Q051'] == "500+ visitors":
        df_slice.loc[x, 'Visitors served per hour'] = 500
        num_over_500 += 1
    else:
        df_slice.loc[x, 'Visitors served per hour'] = "NA"


    if df_slice.loc[x, 'MAI_Q053_001'] == "We provide enough for a meal's worth on average":
        df_slice.loc[x, 'Days of food provided per visitor'] = 0.3
    elif df_slice.loc[x, 'MAI_Q053_002'] == "We provide 1-2 days of food on average":
        df_slice.loc[x, 'Days of food provided per visitor'] = 1.5
    elif df_slice.loc[x, 'MAI_Q053_003'] == "We provide 3 days of food on average":
        df_slice.loc[x, 'Days of food provided per visitor'] = 3
    elif df_slice.loc[x, 'MAI_Q053_004'] == "We are able to provide 4 days of food on average":
        df_slice.loc[x, 'Days of food provided per visitor'] = 4
    elif df_slice.loc[x, 'MAI_Q053_005'] == "We are able to provide 5 days of food on average":
        df_slice.loc[x, 'Days of food provided per visitor'] = 5
    elif df_slice.loc[x, 'MAI_Q053_006'] == "We are able to provide more than 5 days of food on average":
        df_slice.loc[x, 'Days of food provided per visitor'] = 7
        num_over_5_days += 1
    else:
        df_slice.loc[x, 'Days of food provided per visitor'] = "NA"
        num_atypical_grocery_answer += 1
    
    if (isinstance(df_slice.loc[x, 'Hours of service per month'], int) == True) and (isinstance(df_slice.loc[x, 'Visitors served per hour'], int) == True) and (isinstance(df_slice.loc[x, 'Days of food provided per visitor'], int) == True):
        df_slice.loc[x, 'Days of food provided per month'] = df_slice.loc[x, 'Hours of service per month']*df_slice.loc[x, 'Visitors served per hour']*df_slice.loc[x, 'Days of food provided per visitor']
    else:
        df_slice.loc[x, 'Days of food provided per month'] = "NA"

    if (df_slice.loc[x, 'id'] in Food_bank_IDs) == True:
        df_slice.loc[x, 'Type of agency'] = 'Food bank'
    else:
        df_slice.loc[x, 'Type of agency'] = 'Other food program'
    
    x += 1

food_bank_dataframe_for_food_per_month = pd.DataFrame()
food_bank_dataframe_for_food_per_visitor = pd.DataFrame()
food_program_dataframe_for_food_per_month = pd.DataFrame()
food_program_dataframe_for_food_per_visitor = pd.DataFrame()

food_bank_dataframe_for_food_per_month.insert(0,"Days of food provided per month","Empty")
food_bank_dataframe_for_food_per_visitor.insert(0,"Days of food provided per visitor","Empty")
food_program_dataframe_for_food_per_month.insert(0, "Days of food provided per month", "Empty")
food_program_dataframe_for_food_per_visitor.insert(0, "Days of food provided per visitor", "Empty")

x = 0
x_food_bank = 0
x_food_program = 0

while x < num_rows:
    
    if isinstance(df_slice.loc[x, 'Days of food provided per month'], int) == True:
        if df_slice.loc[x, 'Type of agency'] == 'Food bank':
            food_bank_dataframe_for_food_per_month.loc[x_food_bank, 'Days of food provided per month'] = df_slice.loc[x, 'Days of food provided per month']
            x_food_bank += 1
        else:
            food_program_dataframe_for_food_per_month.loc[x_food_program, 'Days of food provided per month'] = df_slice.loc[x, 'Days of food provided per month']
            x_food_program += 1
    
    x += 1

x = 0
x_food_bank = 0
x_food_program = 0

while x < num_rows:
    
    if isinstance(df_slice.loc[x, 'Days of food provided per visitor'], int) == True:
        if df_slice.loc[x, 'Type of agency'] == 'Food bank':
            food_bank_dataframe_for_food_per_visitor.loc[x_food_bank, 'Days of food provided per visitor'] = df_slice.loc[x, 'Days of food provided per visitor']
            x_food_bank += 1
        else:
            food_program_dataframe_for_food_per_visitor.loc[x_food_program, 'Days of food provided per visitor'] = df_slice.loc[x, 'Days of food provided per visitor']
            x_food_program += 1
    
    x += 1

food_bank_food_per_month_lower_quartile = food_bank_dataframe_for_food_per_month.quantile([0.25])
food_bank_food_per_month_upper_quartile = food_bank_dataframe_for_food_per_month.quantile([0.75])
food_bank_food_per_visitor_lower_quartile = food_bank_dataframe_for_food_per_visitor.quantile([0.25])
food_bank_food_per_visitor_upper_quartile = food_bank_dataframe_for_food_per_visitor.quantile([0.75])

food_program_food_per_month_lower_quartile = food_program_dataframe_for_food_per_month.quantile([0.25])
food_program_food_per_month_upper_quartile = food_program_dataframe_for_food_per_month.quantile([0.75])
food_program_food_per_visitor_lower_quartile = food_program_dataframe_for_food_per_visitor.quantile([0.25])
food_program_food_per_visitor_upper_quartile = food_program_dataframe_for_food_per_visitor.quantile([0.75])

x = 0

while x < num_rows:
    if pd.isna(df_slice.at[x,'MAI_Q008']) == False:
        if df_slice.loc[x, 'MAI_Q008'] == "We have enough staff and/or volunteers to run our food programming effectively":
            df_slice.loc[x, 'Effective number of staff/volunteers'] = 1
        else:
            df_slice.loc[x, 'Effective number of staff/volunteers'] = 0
    else:
        df_slice.loc[x, 'Effective number of staff/volunteers'] = "NA"

    x += 1


print("Food provided per month by a food bank at the lower quartile:")
print(food_bank_food_per_month_lower_quartile)
print("\n")

print("Food provided per month by a food bank at the upper quartile:")
print(food_bank_food_per_month_upper_quartile)
print("\n")

print("Food provided per month by a food program at the lower quartile:")
print(food_program_food_per_month_lower_quartile)
print("\n")

print("Food provided per month by a food program at the upper quartile:")
print(food_program_food_per_month_upper_quartile)
print("\n")

print("Food provided per visitor by a food bank at the lower quartile:")
print(food_bank_food_per_visitor_lower_quartile)
print("\n")

print("Food provided per visitor by a food bank at the upper quartile:")
print(food_bank_food_per_visitor_upper_quartile)
print("\n")

print("Food provided per visitor by a food program at the lower quartile:")
print(food_program_food_per_visitor_lower_quartile)
print("\n")

print("Food provided per visitor by a food program at the upper quartile:")
print(food_program_food_per_visitor_upper_quartile)
print("\n")

print("\n")
print("\n")
print("\n")
print("\n")
print("\n")
print("\n")
print("\n")
print("\n")

df_slice = df_slice.drop(columns=["MAI_Q004_002", "MAI_Q004_003", "MAI_Q004_004", "MAI_Q004_005", "MAI_Q004_006", "MAI_Q004_007", "MAI_Q004_008", "MAI_Q004_009", "MAI_Q004_010", "MAI_Q004_011", "MAI_Q004_012", "MAI_Q004_013", "MAI_Q004_014", "MAI_Q004_015", "MAI_Q004_016", "MAI_Q004_017", "MAI_Q004_018", "MAI_Q004_019", "MAI_Q004_020", "MAI_Q004_021", "MAI_Q004_022", "MAI_Q004_023", "MAI_Q004_024", "MAI_Q031_001", "MAI_Q031_002", "MAI_Q031_003", "MAI_Q031_004", "MAI_Q031_005", "MAI_Q031_006", "MAI_Q031_007", "MAI_Q031_008", "MAI_Q031_009", "MAI_Q031_010", "MAI_Q031_011", "MAI_Q048", "MAI_Q051", "MAI_Q053_001", "MAI_Q053_002", "MAI_Q053_003", "MAI_Q053_004", "MAI_Q053_005", "MAI_Q053_006", "MAI_Q053_007", "MAI_Q053_008", "MAI_Q008"])

df_slice.to_csv("MAI calculations.csv", na_rep="NA")

#Neighbour Survey Calculations - how many visitors work 35hrs a week? and how frequently do visitors visit?

df_slice = df_neighbour_survey[["q002", "q033c", "q033d", "q033f", "q033g", "q033h", "q041a", "q010", "q011a"]]

num_rows = len(df_slice)
num_cant_meet_food_needs = 0
num_some_university_education = 0
num_employed_35hs = 0
num_food_bank_visits = 0
num_food_program_visits = 0

df_slice.insert(9,"Can't meet food needs","Empty")
df_slice.insert(10,"At least some post-secondary education","Empty")
df_slice.insert(11,"At least 35hrs of employment a week","Empty")
df_slice.insert(12,"Food bank visits a month","Empty")
df_slice.insert(13,"Food program visits a month","Empty")

x = 0

while x < num_rows:
    if df_slice.loc[x, 'q002'] == "No":
        df_slice.loc[x, "Can't meet food needs"] = 1
        num_cant_meet_food_needs += 1
    else:
        df_slice.loc[x, "Can't meet food needs"] = "NA"
    
    if df_slice.loc[x, 'q033c'] == 'Some college / university' and df_slice.loc[x, 'q002'] == 'No':
        df_slice.loc[x, 'At least some post-secondary education'] = 1
        num_some_university_education += 1
    elif df_slice.loc[x, 'q033d'] == 'Completed college / university' and df_slice.loc[x, 'q002'] == 'No':
        df_slice.loc[x, 'At least some post-secondary education'] = 1
        num_some_university_education += 1
    elif df_slice.loc[x, 'q033f'] == 'Some graduate education' and df_slice.loc[x, 'q002'] == 'No':
        df_slice.loc[x, 'At least some post-secondary education'] = 1
        num_some_university_education += 1
    elif df_slice.loc[x, 'q033g'] == 'Completed graduate education' and df_slice.loc[x, 'q002'] == 'No':
        df_slice.loc[x, 'At least some post-secondary education'] = 1
        num_some_university_education += 1
    elif df_slice.loc[x, 'q033h'] == 'Professional degree' and df_slice.loc[x, 'q002'] == 'No':
        df_slice.loc[x, 'At least some post-secondary education'] = 1
        num_some_university_education += 1
    else:
        df_slice.loc[x, 'At least some post-secondary education'] = "NA"
    
    if df_slice.loc[x, 'q041a'] == 'Employed at least 35 hours each week' and df_slice.loc[x, 'q002'] == 'No':
        df_slice.loc[x, 'At least 35hrs of employment a week'] = 1
        num_employed_35hs += 1
    else:
        df_slice.loc[x, 'At least 35hrs of employment a week'] = "NA"
    
    if df_slice.loc[x, 'q010'] == 'Every 6 months':
        df_slice.loc[x, 'Food bank visits a month'] = 0.17
    elif df_slice.loc[x, 'q010'] == 'Every two months':
        df_slice.loc[x, 'Food bank visits a month'] = 0.5
    elif df_slice.loc[x, 'q010'] == 'Less than twice a year':
        df_slice.loc[x, 'Food bank visits a month'] = 0
    elif df_slice.loc[x, 'q010'] == 'Once per month':
        df_slice.loc[x, 'Food bank visits a month'] = 1
    elif df_slice.loc[x, 'q010'] == 'Two times per month':
        df_slice.loc[x, 'Food bank visits a month'] = 2
    else:
        df_slice.loc[x, 'Food bank visits a month'] = "NA"
    
    if df_slice.loc[x, 'q011a'] == 'Daily':
        df_slice.loc[x, 'Food program visits a month'] = 30
    elif df_slice.loc[x, 'q011a'] == "don't visit every month":
        df_slice.loc[x, 'Food program visits a month'] = 0.33
    elif df_slice.loc[x, 'q011a'] == 'I do not visit other food programs':
        df_slice.loc[x, 'Food program visits a month'] = 0
    elif df_slice.loc[x, 'q011a'] == 'Less than every 6 months':
        df_slice.loc[x, 'Food program visits a month'] = 0.22
    elif df_slice.loc[x, 'q011a'] == 'More than once a week but less than daily':
        df_slice.loc[x, 'Food program visits a month'] = 12
    elif df_slice.loc[x, 'q011a'] == 'Once a week':
        df_slice.loc[x, 'Food program visits a month'] = 4
    elif df_slice.loc[x, 'q011a'] == 'Two times a month':
        df_slice.loc[x, 'Food program visits a month'] = 2
    else:
        df_slice.loc[x, 'Food program visits a month'] = "NA"
    
    x += 1

print("Share of respondents who don't have enough income to meet food needs:")
print(num_cant_meet_food_needs/num_rows)
print("\n")

print("Share of respondents who don't have enough income who have at least some post-secondary education:")
print(num_some_university_education/num_cant_meet_food_needs)
print("\n")

print("Share of respondents who don't have enough income who work at least 35hrs a week:")
print(num_employed_35hs/num_cant_meet_food_needs)
print("\n")

visitor_dataframe_for_food_bank_visits_a_month = pd.DataFrame()
visitor_dataframe_for_food_program_visits_a_month = pd.DataFrame()

visitor_dataframe_for_food_bank_visits_a_month.insert(0, "Food bank visits a month", "Empty")
visitor_dataframe_for_food_program_visits_a_month.insert(0, "Food program visits a month", "Empty")

x = 0
x_food_bank = 0
x_food_program = 0

while x < num_rows:

    if isinstance(df_slice.loc[x, 'Food bank visits a month'], int) == True:
        visitor_dataframe_for_food_bank_visits_a_month.loc[x_food_bank, 'Food bank visits a month'] = df_slice.loc[x, 'Food bank visits a month']
        x_food_bank += 1

    if isinstance(df_slice.loc[x, 'Food program visits a month'], int) == True:
        visitor_dataframe_for_food_program_visits_a_month.loc[x_food_program, 'Food program visits a month'] = df_slice.loc[x, 'Food program visits a month']
        x_food_program += 1
    
    x += 1

visitor_food_bank_visits_a_month_lower_quartile = visitor_dataframe_for_food_bank_visits_a_month.quantile([0.25])
visitor_food_bank_visits_a_month_upper_quartile = visitor_dataframe_for_food_bank_visits_a_month.quantile([0.75])
visitor_food_program_visits_a_month_lower_quartile = visitor_dataframe_for_food_program_visits_a_month.quantile([0.25])
visitor_food_program_visits_a_month_upper_quartile = visitor_dataframe_for_food_program_visits_a_month.quantile([0.75])

print("Number of visits per month to a food bank at the lower quartile:")
print(visitor_food_bank_visits_a_month_lower_quartile)
print("\n")

print("Number of visits per month to a food bank at the upper quartile:")
print(visitor_food_bank_visits_a_month_upper_quartile)
print("\n")

print("Number of visits per month to a food program at the lower quartile:")
print(visitor_food_program_visits_a_month_lower_quartile)
print("\n")

print("Number of visits per month to a food program at the upper quartile:")
print(visitor_food_program_visits_a_month_upper_quartile)
print("\n")

df_slice.to_csv("Neighbour Survey calculations.csv", na_rep="NA")

