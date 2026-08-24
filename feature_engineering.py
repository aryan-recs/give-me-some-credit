import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

class FeatureEngineer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()
        X = X.drop(columns=["Unnamed: 0"], errors="ignore")

        X["TotalPastDue"] = (
            X["NumberOfTime30-59DaysPastDueNotWorse"]
            + X["NumberOfTime60-89DaysPastDueNotWorse"]
            + X["NumberOfTimes90DaysLate"]
        )

        X["IncomePerCreditLine"] = X["MonthlyIncome"] / (
            X["NumberOfOpenCreditLinesAndLoans"] + 1
        )

        X["AgeGroup"] = pd.cut(
            X["age"],
            bins=[-1, 30, 40, 50, 60, 70, 120],
            labels=["20-30", "30-40", "40-50", "50-60", "60-70", "70+"],
        )
        return X
