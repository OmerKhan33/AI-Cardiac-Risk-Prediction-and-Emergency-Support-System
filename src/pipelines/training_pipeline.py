from prefect import flow, task
from src.models.train import train_models
from src.config import settings
import os

# 1. Define the Task (The Worker)
@task(name="Train XGBoost & Random Forest", retries=3, retry_delay_seconds=60)
def run_training_task():
    """
    Executes the training logic we built in Day 2.
    If it fails, Prefect will automatically retry 3 times.
    """
    print("PREFECT WORKER: Starting training job...")
    
    # We call the function directly from your existing script
    # This ensures we use the EXACT same logic as before
    try:
        train_models()
        return "Success"
    except Exception as e:
        print(f"Training Failed: {e}")
        raise e

# 2. Define the Flow (The Manager)
@flow(name="Weekly Cardiac Model Update", log_prints=True)
def cardiac_retraining_flow():
    """
    The Master Pipeline.
    1. Checks if data exists.
    2. Runs training.
    3. Notifications (Future step).
    """
    print(f"Starting Pipeline for {settings.APP_NAME}...")
    
    # Check Data
    data_path = os.path.join(settings.DATA_PATH, "raw", "heart.csv")
    if not os.path.exists(data_path):
        print("CRITICAL: No data found. Skipping training.")
        return

    # Run Training
    state = run_training_task()
    
    print(f"Pipeline Finished. Status: {state}")

if __name__ == "__main__":
    # Run the flow immediately (Manual Trigger)
    cardiac_retraining_flow()