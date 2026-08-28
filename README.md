# Credit Risk Prediction

An end-to-end machine learning project that predicts whether a borrower is likely to experience financial distress using the **Give Me Some Credit** dataset.

The project focuses on building a reliable classification pipeline for an imbalanced financial dataset and taking the trained model from **data preprocessing to deployment**.

## Project Overview

Credit risk prediction is a classification problem where the goal is to identify borrowers who may be at higher risk of financial distress.

This project implements a complete ML workflow:

**Data → Preprocessing → Feature Engineering → Imbalance Handling → Model Training → Hyperparameter Optimization → Evaluation → API → Web Interface → Docker**

## Dataset

The project uses the **Give Me Some Credit** dataset, which contains financial and demographic information about borrowers.

The target variable indicates whether a borrower experienced financial distress.

### Important Features

Some of the features include:

* Revolving utilization of unsecured lines
* Age
* Number of times 30–59 days past due
* Debt ratio
* Monthly income
* Number of open credit lines and loans
* Number of times 90 days late
* Number of real estate loans
* Number of dependents

## Machine Learning Approach

### 1. Data Preprocessing

* Missing value analysis and treatment
* Data type validation
* Outlier analysis
* Duplicate checking
* Feature preparation
* Train-test split

### 2. Feature Engineering

Relevant borrower and financial features were prepared to improve the model's ability to identify patterns associated with financial distress.

### 3. Handling Class Imbalance

The dataset contains significantly fewer high-risk cases than low-risk cases.

**SMOTE (Synthetic Minority Over-sampling Technique)** was used to address class imbalance during model training.

### 4. Model Training

Multiple classification approaches were explored, with **CatBoost** selected as the primary model.

CatBoost is well suited for structured/tabular data and can capture nonlinear relationships between financial features.

### 5. Hyperparameter Optimization

**Optuna** was used for automated hyperparameter optimization.

The objective was to find a better-performing model configuration rather than relying only on default model parameters.

## Model Evaluation

Because this is an imbalanced classification problem, accuracy alone is not sufficient.

The model is evaluated using:

* **ROC-AUC**
* **Precision**
* **Recall**
* **F1-score**
* **Confusion Matrix**

Particular attention is given to **Recall**, since correctly identifying borrowers at risk is important in a credit-risk application.

### Results

Add your final model results here:

| Metric    |    Score  |
| --------- | --------: |
| ROC-AUC   | **0.863** |
| Accuracy  | **0.935** |
| Precision | **0.537** |
| Recall    | **0.241** |
| F1-Score  | **0.333** |


## Deployment

The trained model is exposed through a **FastAPI** backend and an interactive **Streamlit** frontend.

### Architecture

```text
User
  ↓
Streamlit Interface
  ↓
FastAPI
  ↓
Preprocessing Pipeline
  ↓
Trained CatBoost Model
  ↓
Risk Prediction
```

The application is containerized using **Docker** for reproducible deployment.

## Project Structure

```text
credit-risk-prediction/
│
├── app/
│   ├── app.py
│   └── frontend.py
│
├── src/
│   └── ...
│
├── notebooks/
│   └── ...
│
├── models/
│   └── ...
│
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
└── README.md
```

## Running Locally

### Clone the Repository

```bash
git clone https://github.com/aryan-recs/credit-risk-prediction.git
cd credit-risk-prediction
```

### Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run FastAPI

```bash
uvicorn app.app:app --reload
```

The API will run at:

```text
http://localhost:8000
```

FastAPI documentation:

```text
http://localhost:8000/docs
```

### Run Streamlit

Open another terminal and run:

```bash
streamlit run app/frontend.py
```

## Running with Docker

Build the image:

```bash
docker build -t credit-risk-prediction .
```

Run the container:

```bash
docker run -p 8501:8501 credit-risk-prediction
```

## Key Skills Demonstrated

* End-to-end machine learning workflow
* Binary classification
* Imbalanced dataset handling
* SMOTE
* Feature engineering
* CatBoost
* Hyperparameter optimization with Optuna
* Model evaluation
* FastAPI model serving
* Streamlit application development
* Docker containerization
* Git and GitHub

## Future Improvements

* Add model explainability using SHAP
* Add model monitoring
* Implement automated model retraining
* Improve input validation
* Add automated testing
* Deploy the application to a cloud platform
