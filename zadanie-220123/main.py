import pandas as pd

INPUT_DATA_FILENAME = 'sampledatafoodinfo.csv'
CLEAN_DATA_FILENAME = 'cleandata.csv'
EXTENDED_DATA_FILENAME = 'extendeddata.csv'
LOW_CARB_FOODS_FILENAME = 'lowcarbfoods.csv'
LOW_CARB_FOODS_VS_CATEGORY_FILENAME = 'lowcarbfoodsvscategory.csv'


def load_and_parse_data(filename: str) -> pd.DataFrame:
    return pd.read_csv(filename, sep=';')


def clean_up_data(raw_data: pd.DataFrame) -> pd.DataFrame:
    dataframe_clean: pd.DataFrame = raw_data.iloc[:, :-2]  # drop last two columns (empty and notes)
    dataframe_clean['Fibre'] = dataframe_clean['Fibre'].str.replace(',', '.').astype(float)
    # ^ Fibre column uses different decimal separators.
    dataframe_clean.fillna(0.0, inplace=True)  # change NaNs to 0s
    return dataframe_clean


def get_carb_calorie_content(data: pd.DataFrame, index: int) -> float:
    row = data.iloc[index]
    calories = row['Calories']
    carb_calories = row['Carbs'] * 4  # 1 g of carbs has 4 kcal

    if calories == 0 or carb_calories == 0:
        return 0

    carb_calorie_content = carb_calories / calories

    return carb_calorie_content


def get_extended_data(data: pd.DataFrame) -> pd.DataFrame:
    """Creates a dataframe with 'Carb Calorie Content' column"""
    row_count = len(data.index)
    carb_calorie_content_column = [get_carb_calorie_content(data, x) for x in range(row_count)]
    data['Carb Calorie Content'] = carb_calorie_content_column
    return data


def get_low_carb_foods_data(data: pd.DataFrame, threshold: float):
    result = data[data['Carb Calorie Content'] <= threshold]
    return result


def get_low_carb_category_count(data: pd.DataFrame):
    low_carb_food_counts = data.groupby('Category', as_index=False).size()

    return low_carb_food_counts


if __name__ == '__main__':
    raw_data = load_and_parse_data(INPUT_DATA_FILENAME)
    clean_data = clean_up_data(raw_data)
    clean_data.to_csv(CLEAN_DATA_FILENAME, index=False)

    extended_data = get_extended_data(clean_data)
    extended_data.to_csv(EXTENDED_DATA_FILENAME, index=False)

    low_carb_foods = get_low_carb_foods_data(extended_data, .5)
    low_carb_foods.to_csv(LOW_CARB_FOODS_FILENAME, index=False)

    low_carb_foods_vs_category = get_low_carb_category_count(low_carb_foods)
    low_carb_foods_vs_category.to_csv(LOW_CARB_FOODS_VS_CATEGORY_FILENAME, index=False)



