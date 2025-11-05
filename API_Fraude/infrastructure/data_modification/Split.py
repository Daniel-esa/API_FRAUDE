
import pandas as pd
from API_Fraude.config import settings

def split_data(df_input, date_var: str, split_date: str, target_var: str) :
    """
    Splits a dataset into training and testing sets based on a date threshold.

    The data is divided into two subsets depending on whether the value in the 
    `date_var` column is before or after the given `split_date`. Both feature 
    matrices and target vectors are returned for training and testing.

    Parameters
    ----------
    df_input : pandas.DataFrame
        Full dataset containing features, target, and a date column.
    date_var : str
        Name of the column containing date values used for splitting.
    split_date : str
        The cutoff date (in a parseable string format) used to split the data.
        Rows with a date < `split_date` go to the training set; the rest go to the test set.
    target_var : str
        Name of the target column to be predicted.

    Returns
    -------
    tuple
        A tuple containing:
        - x_train (pandas.DataFrame): Training features.
        - y_train (pandas.Series): Training target.
        - x_test (pandas.DataFrame): Testing features.
        - y_test (pandas.Series): Testing target.

    Notes
    -----
    The `date_var` column is dropped from the output feature sets.
    Ensure the date column is in a datetime-compatible format or string.
    """
    df = df_input.copy()

    split_date = pd.to_datetime(split_date)

    train_df = df[df[date_var] < split_date]
    test_df = df[df[date_var] >= split_date]

    x_train = train_df.drop(columns=[target_var, date_var])
    y_train= train_df[target_var]

    x_test= test_df.drop(columns=[target_var, date_var])
    y_test = test_df[target_var]

    return x_train, y_train, x_test, y_test
