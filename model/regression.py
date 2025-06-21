import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

class RegressionPricingModel:
    def __init__(self):
        self.model = LinearRegression()

    def train(self, X, y):
        self.model.fit(X, y)

    def predict(self, X):
        return self.model.predict(X)

# Example usage:
# features = pd.DataFrame({'demand': [...], 'time': [...], 'competitor_price': [...]})
# target = pd.Series([...])  # actual prices
# model = RegressionPricingModel()
# model.train(features, target)
# suggested_prices = model.predict(features)
