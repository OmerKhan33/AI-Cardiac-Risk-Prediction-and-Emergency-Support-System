import streamlit as st
import requests
import json

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Cardiac Risk AI",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- API CONFIG ---
API_URL = "http://api:8000"  # Docker network name, change to localhost for local dev

# --- SESSION STATE ---
if 'token' not in st.session_state:
    st.session_state.token = None
if 'username' not in st.session_state:
    st.session_state.username = None

# --- HELPER FUNCTIONS ---
def login(username, password):
    """Authenticate user and get JWT token"""
    try:
        response = requests.post(
            f"{API_URL}/token",
            data={"username": username, "password": password}
        )
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"Connection Error: {e}")
        return None

def register(username, password):
    """Register a new user"""
    try:
        response = requests.post(
            f"{API_URL}/register",
            json={"username": username, "password": password}
        )
        return response.status_code == 201, response.json()
    except Exception as e:
        return False, {"detail": str(e)}

def assess_patient(data, token):
    """Call the /assess endpoint with patient data"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(
            f"{API_URL}/assess",
            json=data,
            headers=headers
        )
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            st.session_state.token = None
            st.error("Session expired. Please login again.")
        return None
    except Exception as e:
        st.error(f"API Error: {e}")
        return None

# --- CUSTOM CSS ---
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #e74c3c;
        text-align: center;
        margin-bottom: 2rem;
    }
    .risk-high {
        background-color: #e74c3c;
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    .risk-moderate {
        background-color: #f39c12;
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    .risk-low {
        background-color: #27ae60;
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    .info-box {
        background-color: #3498db;
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .stButton>button {
        width: 100%;
        background-color: #e74c3c;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR: AUTH ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/heart-with-pulse.png", width=80)
    st.title("🏥 Cardiac Risk AI")
    
    if st.session_state.token:
        st.success(f"✅ Logged in as: {st.session_state.username}")
        if st.button("🚪 Logout"):
            st.session_state.token = None
            st.session_state.username = None
            st.rerun()
    else:
        auth_tab = st.radio("Choose Action", ["Login", "Register"])
        
        if auth_tab == "Login":
            st.subheader("🔐 Login")
            login_user = st.text_input("Username", key="login_user")
            login_pass = st.text_input("Password", type="password", key="login_pass")
            
            if st.button("Login"):
                if login_user and login_pass:
                    result = login(login_user, login_pass)
                    if result:
                        st.session_state.token = result['access_token']
                        st.session_state.username = login_user
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid credentials")
                else:
                    st.warning("Please enter both fields")
        
        else:  # Register
            st.subheader("📝 Register")
            reg_user = st.text_input("Username", key="reg_user")
            reg_pass = st.text_input("Password", type="password", key="reg_pass")
            reg_pass2 = st.text_input("Confirm Password", type="password", key="reg_pass2")
            
            if st.button("Register"):
                if reg_pass != reg_pass2:
                    st.error("Passwords don't match")
                elif len(reg_pass) < 4:
                    st.error("Password too short (min 4 chars)")
                elif reg_user and reg_pass:
                    success, msg = register(reg_user, reg_pass)
                    if success:
                        st.success("Registration successful! Please login.")
                    else:
                        st.error(msg.get('detail', 'Registration failed'))

# --- MAIN CONTENT ---
st.markdown('<p class="main-header">❤️ AI Cardiac Risk Assessment</p>', unsafe_allow_html=True)

if not st.session_state.token:
    st.info("👈 Please login or register using the sidebar to access the assessment.")
    
    # Show demo info
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        ### 🤖 AI-Powered
        Advanced XGBoost & Random Forest models trained on clinical data
        """)
    with col2:
        st.markdown("""
        ### 🌍 Live Environment
        Real-time weather & pollution data affects your risk score
        """)
    with col3:
        st.markdown("""
        ### 💊 Smart Advice
        Personalized recommendations based on your results
        """)
else:
    # --- ASSESSMENT FORM ---
    st.subheader("📋 Patient Information")
    
    with st.form("assessment_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### 👤 Demographics")
            age = st.number_input("Age", min_value=1, max_value=120, value=50)
            sex = st.selectbox("Sex", options=[(1, "Male"), (0, "Female")], format_func=lambda x: x[1])
            city = st.text_input("City (for weather data)", value="London")
        
        with col2:
            st.markdown("#### 🩺 Vital Signs")
            trestbps = st.number_input("Resting Blood Pressure (mm Hg)", 80, 220, 120)
            chol = st.number_input("Cholesterol (mg/dl)", 100, 600, 200)
            thalach = st.number_input("Max Heart Rate", 60, 220, 150)
            fbs = st.selectbox("Fasting Blood Sugar > 120mg/dl", 
                             options=[(0, "No (Normal)"), (1, "Yes (High)")],
                             format_func=lambda x: x[1])
        
        with col3:
            st.markdown("#### 📊 ECG & Tests")
            cp = st.selectbox("Chest Pain Type", options=[
                (0, "Typical Angina"),
                (1, "Atypical Angina"),
                (2, "Non-Anginal Pain"),
                (3, "Asymptomatic")
            ], format_func=lambda x: x[1])
            
            restecg = st.selectbox("Resting ECG", options=[
                (0, "Normal"),
                (1, "ST-T Wave Abnormality"),
                (2, "Left Ventricular Hypertrophy")
            ], format_func=lambda x: x[1])
            
            exang = st.selectbox("Exercise Induced Angina", 
                               options=[(0, "No"), (1, "Yes")],
                               format_func=lambda x: x[1])
        
        st.markdown("---")
        col4, col5 = st.columns(2)
        
        with col4:
            oldpeak = st.slider("ST Depression (oldpeak)", 0.0, 7.0, 1.0, 0.1)
            slope = st.selectbox("ST Slope", options=[
                (0, "Upsloping (Better)"),
                (1, "Flat"),
                (2, "Downsloping (Worse)")
            ], format_func=lambda x: x[1])
        
        with col5:
            ca = st.selectbox("Major Vessels Colored (0-4)", options=[0, 1, 2, 3, 4])
            thal = st.selectbox("Thalassemia", options=[
                (1, "Normal"),
                (2, "Fixed Defect"),
                (3, "Reversible Defect")
            ], format_func=lambda x: x[1])
        
        submitted = st.form_submit_button("🔬 Run Assessment", use_container_width=True)
    
    # --- PROCESS FORM ---
    if submitted:
        with st.spinner("🧠 AI is analyzing your data..."):
            patient_data = {
                "age": age,
                "sex": sex[0],
                "cp": cp[0],
                "trestbps": trestbps,
                "chol": chol,
                "fbs": fbs[0],
                "restecg": restecg[0],
                "thalach": thalach,
                "exang": exang[0],
                "oldpeak": oldpeak,
                "slope": slope[0],
                "ca": ca,
                "thal": thal[0],
                "city": city
            }
            
            result = assess_patient(patient_data, st.session_state.token)
        
        if result:
            st.markdown("---")
            st.subheader("📊 Assessment Results")
            
            # Risk Score Display
            risk_score = result['risk_score']
            risk_category = result['risk_category']
            
            if risk_category == "High Risk":
                risk_class = "risk-high"
                emoji = "🚨"
            elif risk_category == "Moderate":
                risk_class = "risk-moderate"
                emoji = "⚠️"
            else:
                risk_class = "risk-low"
                emoji = "✅"
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.markdown(f"""
                <div class="{risk_class}">
                    <h1>{emoji} {risk_score}%</h1>
                    <h3>{risk_category}</h3>
                </div>
                """, unsafe_allow_html=True)
            
            # Environment Data
            st.markdown("### 🌍 Environmental Factors")
            env = result['environment']
            env_col1, env_col2, env_col3, env_col4 = st.columns(4)
            
            with env_col1:
                st.metric("📍 City", env['city'])
            with env_col2:
                st.metric("🌡️ Temperature", f"{env['temp']}°C" if env['temp'] else "N/A")
            with env_col3:
                aqi_labels = {1: "Good", 2: "Fair", 3: "Moderate", 4: "Poor", 5: "Very Poor"}
                aqi_val = env['aqi'] if env['aqi'] else 1
                st.metric("💨 Air Quality", aqi_labels.get(aqi_val, "Unknown"))
            with env_col4:
                st.metric("📈 Env Stress", f"{env['stress_factor']}%")
            
            # Recommendations
            st.markdown("### 💊 Recommendations")
            for rec in result['recommendations']:
                st.info(f"• {rec}")
            
            # Warning for high risk
            if risk_category == "High Risk":
                st.error("⚠️ **IMPORTANT**: Your risk score is high. Please consult a healthcare professional immediately!")

# --- FOOTER ---
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>❤️ Cardiac Risk AI - MLOps Project | Built with FastAPI & Streamlit</p>
    <p>⚠️ This is for educational purposes only. Always consult a medical professional.</p>
</div>
""", unsafe_allow_html=True)
