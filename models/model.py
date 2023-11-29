from typing import List
import numpy as np
import pandas as pd
import pickle

from api.models import Items

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler


class Model:
    """Модель линейной регрессии, выполняющая предсказания стоимости автомобиля на основе его признаков (свойств) """
    imputer: SimpleImputer
    one_hot_encoder: OneHotEncoder
    scaler: StandardScaler

    def __init__(self):
        with open('models/imputer.pickle', 'rb') as f:
            self.imputer = pickle.load(f)
        with open('models/one_hot_encoder.pickle', 'rb') as f:
            self.one_hot_encoder = pickle.load(f)
        with open('models/scaler.pickle', 'rb') as f:
            self.scaler = pickle.load(f)
        with open('models/model.pickle', 'rb') as f:
            self.model = pickle.load(f)

    def predict(self, items: Items) -> List[float]:
        """Выполняет предсказание целевой переменной (стоимости автомобиля) для объектов в items и возвращает
        предсказанные значения в виде списка"""
        df = self.predict_and_return_raw(items)
        result = df['selling_price'].to_list()
        return result

    def predict_and_return_raw(self, items: Items) -> pd.DataFrame:
        """Выполняет предсказание целевой переменной (стоимости автомобиля) для объектов в items и возвращает
        результат в виде DataFrame, содержащего как признаки, так и целевую переменную"""
        df = pd.DataFrame(items.to_dict())
        self._fill_predictions_in_dataframe(df)
        return df

    def _fill_predictions_in_dataframe(self, data: pd.DataFrame) -> None:
        df = data.copy()
        self.clean(df)
        self.impute(df)
        self.transform_features(df)
        X = self.get_X(df)
        X = self.encode(X)
        X_scaled = self.scale(X)

        y_predicted = np.exp(self.model.predict(X_scaled))
        data['selling_price'] = y_predicted

    def clean(self, df: pd.DataFrame):
        unit_names = ['bhp', 'kmpl', 'km/kg', 'CC']
        col_names = ['mileage', 'engine', 'max_power']
        for col_name in col_names:
            df[col_name] = pd.to_numeric(df[col_name].replace("|".join(unit_names), '', regex=True).str.strip())

        df.drop(['torque'], axis=1, inplace=True, errors='ignore')

    def impute(self, df: pd.DataFrame):
        col_names = ['mileage', 'engine', 'max_power', 'seats']
        df[col_names] = self.imputer.transform(df[col_names])

        col_names = ['engine', 'seats']
        for col_name in col_names:
            df[col_name] = df[col_name].astype('int64')

    def transform_features(self, df: pd.DataFrame):
        # берем первые два слова от наименования
        df['name'] = df['name'].apply(lambda name: " ".join(str(name).split()[:2]))
        # вычисляем количество л.с. на единицу объема двигателя
        df['power_per_engine'] = df['max_power'] / df['engine']
        # заменяем год на квадрат года
        df['year'] = df['year'] ** 2

    def get_X(self, df: pd.DataFrame):
        X = df.drop(['selling_price'], axis=1, errors='ignore')
        return X

    def encode(self, X: pd.DataFrame):
        cat_columns = ['fuel', 'owner', 'seller_type', 'transmission', 'seats', 'name']
        encoded_cat_columns = self.one_hot_encoder.get_feature_names_out(cat_columns)
        return pd.concat(
            [
                X.drop(cat_columns, axis=1),
                pd.DataFrame(self.one_hot_encoder.transform(X[cat_columns]), columns=encoded_cat_columns)
            ],
            axis=1
        )

    def scale(self, X: pd.DataFrame):
        return self.scaler.transform(X)