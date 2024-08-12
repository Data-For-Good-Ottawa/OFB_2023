from constants import PathNeighbourSurvey, PathHungerCount
from Lib import data_loader as dl


def main():

    # Example: Load the CSV file into a pandas DataFrame using the function
    df_neighbour_survey = dl.get_data_as_pandas_data_frame(PathNeighbourSurvey)
    df_hunger_count = dl.get_data_as_pandas_data_frame(PathHungerCount)

    # Display the first few rows of the DataFrame to verify the load
    if not df_neighbour_survey.empty:
        print(df_neighbour_survey.head())
    else:
        print("Failed to load [Neighbour Survey] data.")

    if not df_hunger_count.empty:
        print(df_hunger_count.head())
    else:
        print("Failed to load [Hunger Count] data.")


if __name__ == "__main__":
    main()