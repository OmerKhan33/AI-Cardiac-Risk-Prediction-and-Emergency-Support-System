# 🫀 AI Cardiac Risk Prediction & Emergency Support System

An end-to-end **MLOps project** that predicts cardiac risk from patient symptoms, adjusts risk using live weather/pollution data, and provides personalized health recommendations.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)
![ML](https://img.shields.io/badge/ML-XGBoost%20%7C%20Random%20Forest-orange.svg)

## 🌟 Features

- **🤖 AI-Powered Prediction**: XGBoost classifier + Random Forest regressor trained on clinical heart disease data
- **🌍 Live Environmental Context**: Real-time weather & air quality data affects risk assessment
- **🧠 Bayesian Reasoning**: Environmental stress factors calculated using probabilistic networks
- **🔐 Secure Authentication**: JWT-based auth with user registration and login
- **📊 Patient History**: All assessments saved to database for tracking
- **🎨 Web Frontend**: Beautiful Streamlit interface for easy interaction
- **🐳 Containerized**: Full Docker support for easy deployment
- **⚡ CI/CD Pipeline**: Automated testing and deployment with GitHub Actions

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND (Streamlit)                      │
│                         Port: 8501                               │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                         API (FastAPI)                            │
│                         Port: 8000                               │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │   Auth      │  │  Predict    │  │   Live Data Client      │  │
│  │  (JWT)      │  │  Endpoint   │  │   (Weather + AQI)       │  │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘  │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    ML MODELS                                 ││
│  │  • XGBoost Classifier (Disease Detection)                   ││
│  │  • Random Forest Regressor (Severity 0-4)                   ││
│  │  • Bayesian Network (Environmental Stress)                  ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DATABASE (SQLite)                           │
│              Users + Prediction History                          │
└─────────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/OmerKhan33/AI-Cardiac-Risk-Prediction-and-Emergency-Support-System.git
cd AI-Cardiac-Risk-Prediction-and-Emergency-Support-System

# 2. Create environment file
cp .env.example .env
# Edit .env with your API keys (get from https://openweathermap.org/api)

# 3. Run with Docker Compose
docker-compose up --build

# 4. Access the application
# Frontend: http://localhost:8501
# API Docs: http://localhost:8000/docs
```

### Option 2: Local Development

```bash
# 1. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 2. Install dependencies
pip install -r requirements.txt

# 3. Train models (if .pkl files don't exist)
python -m src.models.train

# 4. Run API
uvicorn src.api.main:app --reload

# 5. Run Frontend (new terminal)
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

## 📁 Project Structure

```
├── .github/
│   └── workflows/
│       └── ci-cd.yml          # GitHub Actions CI/CD
├── frontend/
│   ├── app.py                 # Streamlit frontend
│   ├── Dockerfile             # Frontend container
│   └── requirements.txt
├── src/
│   ├── api/
│   │   ├── main.py            # FastAPI application
│   │   ├── auth_routes.py     # Authentication endpoints
│   │   └── schemas.py         # Pydantic models
│   ├── auth/
│   │   └── security.py        # JWT & password hashing
│   ├── data/
│   │   └── raw/
│   │       ├── heart.csv      # Training data
│   │       └── advice_db.json # Recommendations database
│   ├── db/
│   │   └── database.py        # SQLite setup
│   ├── models/
│   │   ├── train.py           # Model training script
│   │   ├── *.pkl              # Trained models
│   │   ├── user_model.py      # User DB model
│   │   └── prediction_model.py# Prediction DB model
│   ├── pipelines/
│   │   └── training_pipeline.py # Prefect orchestration
│   └── utils/
│       ├── bayesian_network.py # Environmental stress calc
│       ├── live_data.py       # Weather/AQI API client
│       └── recommender.py     # Health recommendations
├── tests/
│   └── test_api.py            # API tests
├── docker-compose.yml         # Multi-container setup
├── Dockerfile                 # API container
├── requirements.txt           # Python dependencies
└── README.md
```

## 🔌 API Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/` | Health check | ❌ |
| POST | `/register` | Register new user | ❌ |
| POST | `/token` | Login & get JWT | ❌ |
| POST | `/assess` | Run cardiac assessment | ✅ |

### Example Assessment Request

```bash
curl -X POST "http://localhost:8000/assess" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "age": 55,
    "sex": 1,
    "cp": 0,
    "trestbps": 140,
    "chol": 250,
    "fbs": 0,
    "restecg": 0,
    "thalach": 150,
    "exang": 1,
    "oldpeak": 2.3,
    "slope": 2,
    "ca": 0,
    "thal": 2,
    "city": "London"
  }'
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=src --cov-report=html
```

## 🐳 Docker Commands

```bash
# Build and run
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop containers
docker-compose down

# Rebuild specific service
docker-compose build api
docker-compose build frontend
```

## 🔑 Environment Variables

Create a `.env` file based on `.env.example`:

| Variable | Description | Required |
|----------|-------------|----------|
| `WEATHER_API_KEY` | OpenWeatherMap API key | Yes |
| `OPENAQ_API_KEY` | OpenAQ API key (optional) | No |
| `SECRET_KEY` | JWT signing key | No (has default) |

## 📊 MLOps Features

- **Model Training**: Automated GridSearchCV hyperparameter tuning
- **Data Validation**: Pydantic schemas for input validation
- **Model Registry**: Trained models saved as `.pkl` files
- **Pipeline Orchestration**: Prefect flows for scheduled retraining
- **Monitoring**: Health checks and structured logging
- **CI/CD**: GitHub Actions for automated testing and deployment
- **Containerization**: Docker + Docker Compose for reproducibility

## 🚢 Deployment Options

### GitHub Container Registry (Automatic)
The CI/CD pipeline automatically pushes Docker images to GHCR on main branch pushes.

### Manual Deployment
```bash
# Pull images
docker pull ghcr.io/omerkhan33/ai-cardiac-risk-prediction-and-emergency-support-system-api:latest
docker pull ghcr.io/omerkhan33/ai-cardiac-risk-prediction-and-emergency-support-system-frontend:latest
```

### Cloud Deployment
The project can be deployed to:
- **Azure Container Apps** / Azure App Service
- **AWS ECS** / AWS App Runner
- **Google Cloud Run**
- **Railway** / **Render** / **Fly.io**

## 📈 Model Performance

| Model | Task | Metric | Score |
|-------|------|--------|-------|
| XGBoost | Classification | Accuracy | ~85% |
| Random Forest | Regression (Severity) | MAE | ~0.5 |

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is for educational purposes. Always consult medical professionals for health decisions.

## 👤 Author

**Omer Khan**
- GitHub: [@OmerKhan33](https://github.com/OmerKhan33)

---

⭐ Star this repo if you found it helpful!