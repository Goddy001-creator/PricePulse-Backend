import pandas as pd
from sklearn.impute import SimpleImputer


def preprocess_products(products):
    if not products:
        return []

    dataframe = pd.DataFrame(products)

    if "rating" not in dataframe.columns:
        return products

    imputer = SimpleImputer(strategy="mean")

    dataframe["rating"] = imputer.fit_transform(
        dataframe[["rating"]]
    ).ravel()

    dataframe["rating"] = dataframe["rating"].round(1)

    return dataframe.to_dict(orient="records")
