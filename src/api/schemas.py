from pydantic import BaseModel, Field
from enum import IntEnum

# --- PATIENT-FRIENDLY DROPDOWNS (ENUMS) ---

class SexType(IntEnum):
    FEMALE = 0
    MALE = 1

class ChestPainType(IntEnum):
    # Mapping to dataset values 0-3
    TYPICAL_ANGINA_HEART_RELATED = 0
    ATYPICAL_ANGINA_NOT_HEART_RELATED = 1
    NON_ANGINAL_PAIN = 2
    ASYMPTOMATIC_NO_PAIN = 3

class FastingBloodSugarType(IntEnum):
    NORMAL_LESS_THAN_120 = 0
    HIGH_DIABETIC_GREATER_THAN_120 = 1

class RestingECGType(IntEnum):
    NORMAL = 0
    ABNORMAL_ST_T_WAVE = 1
    LEFT_VENTRICULAR_HYPERTROPHY = 2

class ExerciseAnginaType(IntEnum):
    NO_PAIN_DURING_EXERCISE = 0
    YES_PAIN_DURING_EXERCISE = 1

class SlopeType(IntEnum):
    UPSLOPING_BETTER = 0
    FLAT_AVERAGE = 1
    DOWNSLOPING_WORSE = 2

class ThalassemiaType(IntEnum):
    NORMAL = 1
    FIXED_DEFECT_PERMANENT = 2
    REVERSIBLE_DEFECT_TEMPORARY = 3
    # Note: 0 is sometimes null/unknown in this dataset, usually treated as Normal or dropped.

class VesselsType(IntEnum):
    ZERO_BLOCKED = 0
    ONE_BLOCKED = 1
    TWO_BLOCKED = 2
    THREE_BLOCKED = 3
    FOUR_BLOCKED = 4

# --- THE DATA MODEL ---

class PatientData(BaseModel):
    # 1. Manual Inputs (Continuous Numbers)
    age: int = Field(..., example=65, description="Patient Age")
    trestbps: int = Field(..., example=120, description="Resting Blood Pressure (mm Hg)")
    chol: int = Field(..., example=240, description="Cholesterol Level (mg/dl)")
    thalach: int = Field(..., example=150, description="Maximum Heart Rate Achieved")
    oldpeak: float = Field(..., example=1.5, description="ST Depression (Number usually between 0.0 and 6.0)")
    
    # 2. Dropdown Inputs (Categorical)
    sex: SexType = Field(..., description="Biological Sex")
    cp: ChestPainType = Field(..., description="Chest Pain Type")
    fbs: FastingBloodSugarType = Field(..., description="Fasting Blood Sugar > 120 mg/dl?")
    restecg: RestingECGType = Field(..., description="Resting Electrocardiographic Results")
    exang: ExerciseAnginaType = Field(..., description="Exercise Induced Angina")
    slope: SlopeType = Field(..., description="Slope of the peak exercise ST segment")
    ca: VesselsType = Field(..., description="Number of major vessels colored by flourosopy")
    thal: ThalassemiaType = Field(..., description="Thalassemia Blood Disorder Status")

    # 3. Context (Manual Entry as requested)
    city: str = Field(..., example="London", description="Enter your city for live environmental analysis")

class AssessmentResponse(BaseModel):
    risk_score: float
    risk_category: str
    environment: dict
    recommendations: list