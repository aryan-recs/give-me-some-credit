# Credit Risk Prediction App

Serves your CatBoost pipeline (`pipe4` from the notebook) via FastAPI, with a Streamlit frontend.

## Files
- `app.py` — FastAPI backend, loads the pipeline and exposes `/predict`
- `frontend.py` — Streamlit UI that calls the API
- `feature_engineering.py` — the `FeatureEngineer` transformer class, needed so the pickled pipeline can be unpickled
- `requirements.txt` — dependencies

## 1. Add your trained model file
Place your saved pipeline in this folder as **`credit_risk_pipeline.joblib`** (same folder as `app.py`).

If you haven't saved it yet, in your notebook run:
```python
import joblib
joblib.dump(pipe4, "credit_risk_pipeline.joblib")
```

⚠️ **Important:** `pipe4`'s first step is your custom `FeatureEngineer` class. Pickle needs to resolve that
class from the same import path used when it was saved. If your notebook defined `FeatureEngineer` inline
(so pickle recorded it as coming from `__main__`), loading it via `app.py`'s `from feature_engineering import
FeatureEngineer` may fail. If you hit an `AttributeError`/`ModuleNotFoundError` on load, the safest fix is to
re-save the model after importing the class from `feature_engineering.py` first:
```python
from feature_engineering import FeatureEngineer
import joblib
# rebuild pipe4 with this FeatureEngineer (re-run the pipeline definition + .fit(x_train, y_train))
joblib.dump(pipe4, "credit_risk_pipeline.joblib")
```

If you already have a saved file and it loads fine as-is, no action needed.

## 2. Install dependencies
```bash
pip install -r requirements.txt
```

## 3. Run the API
```bash
uvicorn app:app --reload --port 8000
```
Check it's up at http://127.0.0.1:8000/docs

## 4. Run the frontend (in a separate terminal)
```bash
streamlit run frontend.py
```

## API contract
`POST /predict`
```json
{
  "RevolvingUtilizationOfUnsecuredLines": 0.5,
  "age": 45,
  "NumberOfTime30-59DaysPastDueNotWorse": 0,
  "DebtRatio": 0.3,
  "MonthlyIncome": 6000,
  "NumberOfOpenCreditLinesAndLoans": 8,
  "NumberOfTimes90DaysLate": 0,
  "NumberRealEstateLoansOrLines": 1,
  "NumberOfTime60-89DaysPastDueNotWorse": 0,
  "NumberOfDependents": 2
}
```
`MonthlyIncome` and `NumberOfDependents` can be `null` — the model's built-in imputers handle missing values.

Response:
```json
{
  "default_probability": 0.0421,
  "prediction": 0,
  "risk_category": "Low"
}
```
