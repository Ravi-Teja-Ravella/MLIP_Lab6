import pytest
import pandas as pd
import numpy as np
from prediction_demo import data_preparation, data_split, train_model, eval_model

@pytest.fixture
def housing_data_sample():
    return pd.DataFrame(
        data={
            'price': [13300000, 12250000],
            'area': [7420, 8960],
            'bedrooms': [4, 4],
            'bathrooms': [2, 4],
            'stories': [3, 4],
            'mainroad': ["yes", "yes"],
            'guestroom': ["no", "no"],
            'basement': ["no", "no"],
            'hotwaterheating': ["no", "no"],
            'airconditioning': ["yes", "yes"],
            'parking': [2, 3],
            'prefarea': ["yes", "no"],
            'furnishingstatus': ["furnished", "unfurnished"]
        }
    )

def test_data_preparation(housing_data_sample):
    feature_df, target_series = data_preparation(housing_data_sample)
    # Target and datapoints has same length
    assert feature_df.shape[0] == len(target_series)

    # Feature only has numerical values
    assert feature_df.shape[1] == feature_df.select_dtypes(include=(np.number, np.bool_)).shape[1]

@pytest.fixture
def feature_target_sample(housing_data_sample):
    feature_df, target_series = data_preparation(housing_data_sample)
    return (feature_df, target_series)

def test_data_split(feature_target_sample):
    return_tuple = data_split(*feature_target_sample)

    # Check that 4 elements are returned
    assert len(return_tuple) == 4, "data_split should return 4 values (X_train, X_test, y_train, y_test)"

    X_train, X_test, y_train, y_test = return_tuple

    # Check the types
    assert isinstance(X_train, pd.DataFrame)
    assert isinstance(X_test, pd.DataFrame)
    assert isinstance(y_train, pd.Series)
    assert isinstance(y_test, pd.Series)

    # Check that total rows match original input
    total_rows = len(feature_target_sample[0])
    assert len(X_train) + len(X_test) == total_rows
    assert len(y_train) + len(y_test) == total_rows

    # Optional: Check that indices of train and test sets do not overlap
    assert set(X_train.index).isdisjoint(X_test.index)
    assert set(y_train.index).isdisjoint(y_test.index)
