import pandas as pd

FOOD_DATA_FILENAME = 'sampledatafoodinfo.csv'


def load_food_data(filename: str) -> pd.DataFrame:
    """
    Reads data from `filename`.csv file, assuming that it has the same columns as sampledatafoodinfo.csv.
    Also changes nans into 0s.
    """

    dataframe_raw: pd.DataFrame = pd.read_csv(filename, sep=';')
    dataframe_clean: pd.DataFrame = dataframe_raw.iloc[:, :-2]  # drop last two columns

    rows = [x[1] for x in dataframe_clean.iterrows()]  # my god, I hate pandas

    for row in rows:
        row: pd.Series
        columns = row.axes[0].values
        for column in columns:
            if row[column] == 'nan':
                row[column] = 0.0

    return dataframe_clean


if __name__ == '__main__':
    data = load_food_data(FOOD_DATA_FILENAME)