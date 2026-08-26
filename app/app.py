from pathlib import Path
from typing import Optional
import joblib
import sys
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field, computed_field
BASE_DIR = Path(__file__).parent.parent
SRC_DIR = BASE_DIR / "src"

sys.path.append(str(SRC_DIR))
from feature_engineering import FeatureEngineer

MODEL_PATH = (
    BASE_DIR
    / "model"
    / "credit_risk_model.joblib"
)

try:
    model = joblib.load(MODEL_PATH)
    print("Model loaded successfully!")

except Exception as e:
    model = None
    print("Could not load model:", e)

app = FastAPI(
    title="Credit Risk Prediction API",
    description="Predicts probability of serious delinquency within 2 years.",
    version="1.0",
)

class CreditApplication(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    revolving_utilization_of_unsecured_lines: float = Field(
        ...,
        alias="RevolvingUtilizationOfUnsecuredLines",
        ge=0,
        description="Credit utilization ratio."
    )

    age: int = Field(
        ...,
        ge=18,
        le=110,
        description="Applicant's age in years."
    )

    number_of_time_30_59_days_past_due_not_worse: int = Field(
        ...,
        alias="NumberOfTime30-59DaysPastDueNotWorse",
        ge=0,
        description="Number of times 30-59 days past due."
    )

    debt_ratio: float = Field(
        ...,
        alias="DebtRatio",
        ge=0,
        description="Debt ratio."
    )

    monthly_income: Optional[float] = Field(
        default=None,
        alias="MonthlyIncome",
        ge=0,
        description="Monthly income. Can be left blank."
    )

    number_of_open_credit_lines_and_loans: int = Field(
        ...,
        alias="NumberOfOpenCreditLinesAndLoans",
        ge=0,
        description="Number of open credit lines and loans."
    )

    number_of_times_90_days_late: int = Field(
        ...,
        alias="NumberOfTimes90DaysLate",
        ge=0,
        description="Number of times 90 or more days late."
    )

    number_real_estate_loans_or_lines: int = Field(
        ...,
        alias="NumberRealEstateLoansOrLines",
        ge=0,
        description="Number of real estate loans or lines."
    )

    number_of_time_60_89_days_past_due_not_worse: int = Field(
        ...,
        alias="NumberOfTime60-89DaysPastDueNotWorse",
        ge=0,
        description="Number of times 60-89 days past due."
    )

    number_of_dependents: Optional[int] = Field(
        default=None,
        alias="NumberOfDependents",
        ge=0,
        description="Number of dependents. Can be left blank."
    )

    def to_dataframe(self) -> pd.DataFrame:
        raw = self.model_dump(by_alias=True)
        raw = {key: (np.nan if value is None else value)for key, value in raw.items()}
        return pd.DataFrame([raw])

class PredictionResponse(BaseModel):
    default_probability: float = Field(...,description="Probability of serious delinquency.")
    prediction: int = Field(...,description="1 = likely default, 0 = likely safe.")
    
    @computed_field
    @property
    def risk_category(self) -> str:
        probability = self.default_probability
        if probability < 0.10:
            return "Low"
        elif probability < 0.20:
            return "Medium"
        else:
            return "High"

@app.get("/", tags=["Health"])
def root():
    return {"status": "ok","message": "Credit Risk Prediction API is running."}

@app.get("/health", tags=["Health"])
def health():
    return {"model_loaded": model is not None}

@app.post("/predict",
    response_model=PredictionResponse,
    tags=["Prediction"]
)
def predict(application: CreditApplication):
    if model is None:
        raise HTTPException(status_code=503,detail="Model is not loaded.")
    try:
        input_df = application.to_dataframe()
        probability = float(model.predict_proba(input_df)[0][1])
        prediction = int(probability >= 0.5)
    except Exception as exc:
        raise HTTPException(status_code=400,detail=f"Prediction failed: {exc}")
    return PredictionResponse(default_probability=probability,prediction=prediction)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app",host="0.0.0.0",port=8000,reload=True)