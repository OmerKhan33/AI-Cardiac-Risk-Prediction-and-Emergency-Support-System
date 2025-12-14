import pandas as pd
import numpy as np
import joblib
import os
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, mean_absolute_error, classification_report
from src.config import settings

def train_models():
    print(" Starting High-Performance Training Pipeline...")

    # 1. Load Data
    data_path = os.path.join(settings.DATA_PATH, "raw", "heart.csv")
    if not os.path.exists(data_path):
        print(f"Error: Data file not found at {data_path}")
        return

    df = pd.read_csv(data_path)
    
    # Rename target
    df.rename(columns={df.columns[-1]: 'target'}, inplace=True)

    # 2. SEPARATE FEATURES
    X = df.drop('target', axis=1)
    y = df['target']

    # 3. ADVANCED PREPROCESSING
    # A. One-Hot Encoding for Categorical variables
    # (cp=chest pain, thal=thalassemia, slope=peak exercise ST segment)
    cat_cols = ['cp', 'restecg', 'slope', 'thal']
    X = pd.get_dummies(X, columns=cat_cols, drop_first=True)

    # B. Scaling for Numerical variables (CRITICAL for higher accuracy)
    # We fit the scaler on ALL data for consistency, then split.
    num_cols = ['age', 'trestbps', 'chol', 'thalach', 'oldpeak']
    scaler = StandardScaler()
    X[num_cols] = scaler.fit_transform(X[num_cols])

    print(f"Features processed: {X.shape[1]} columns (Scaled + Encoded)")

    # 4. DEFINE TARGETS
    y_class = y.apply(lambda x: 1 if x > 0 else 0) # 0=Healthy, 1=Sick
    y_reg = y # 0-4 scale

    # 5. SPLIT DATA
    # random_state=42 is standard. 
    # stratify=y_class ensures we don't accidentally get all sick people in the test set.
    X_train, X_test, y_class_train, y_class_test, y_reg_train, y_reg_test = train_test_split(
        X, y_class, y_reg, test_size=0.2, random_state=42, stratify=y_class
    )

    # ---------------------------------------------------------
    # MODEL 1: XGBoost (Tuned)
 
    print("\nTraining Tuned XGBoost Classifier...")
    
    xgb_param_grid = {
        'n_estimators': [50, 80, 100],
        'max_depth': [2, 3, 4],
        'learning_rate': [0.01, 0.025, 0.05],
        'subsample': [0.6, 0.7, 0.8]
    }

    xgb_base = XGBClassifier(use_label_encoder=False, reg_alpha=0.1, eval_metric='logloss', random_state=42)

    xgb_grid_search = GridSearchCV(
        xgb_base, xgb_param_grid, cv=5, scoring='f1', n_jobs=-1, verbose=1
    )

    xgb_grid_search.fit(X_train, y_class_train)
    clf = xgb_grid_search.best_estimator_
    # Detailed Evaluation
    y_pred_class = clf.predict(X_test)
    acc = accuracy_score(y_class_test, y_pred_class)
    print(f"XGBoost Accuracy: {acc:.2%}")
    
    # Print a mini report to see WHERE it is failing (optional debugging)
    # print(classification_report(y_class_test, y_pred_class))

    # ---------------------------------------------------------
    #MODEL 2: Random Forest Regressor(Tuned)
    rf_param_grid = {
        'n_estimators': [100, 150, 200],
        'max_depth': [5, 7, 10],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4]
    }

    rf_base = RandomForestRegressor(random_state=42)

    rf_grid_search = GridSearchCV(
        rf_base, rf_param_grid, cv=5, scoring='neg_mean_absolute_error', n_jobs=-1, verbose=1
    )

    rf_grid_search.fit(X_train, y_reg_train)
    print("\nTraining Random Forest Regressor...")
    reg = rf_grid_search.best_estimator_

    y_pred_reg = reg.predict(X_test)
    mae = mean_absolute_error(y_reg_test, y_pred_reg)
    print(f"Regression MAE: {mae:.2f} / 4.0")

    # ---------------------------------------------------------
    #SAVE EVERYTHING (Including the Scaler!)

    save_path = settings.MODEL_PATH
    os.makedirs(save_path, exist_ok=True)
    
    joblib.dump(clf, os.path.join(save_path, "model_classification.pkl"))
    joblib.dump(reg, os.path.join(save_path, "model_regression.pkl"))
    joblib.dump(X.columns.tolist(), os.path.join(save_path, "model_columns.pkl"))
    
    # Save the Scaler. The API needs this to scale the user's input!
    joblib.dump(scaler, os.path.join(save_path, "model_scaler.pkl"))

    print(f"\n Models + Scaler saved to {save_path}")

if __name__ == "__main__":
    train_models()