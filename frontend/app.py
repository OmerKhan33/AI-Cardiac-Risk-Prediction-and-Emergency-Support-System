import streamlit as st
import requests
import os
import time

# --- PAGE CONFIG ---


st.set_page_config(
    page_title="CardioGuard AI",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- API CONFIG ---
API_URL = os.getenv("API_URL", "http://api:8000")

# --- SESSION STATE ---
if 'token' not in st.session_state:
    st.session_state.token = None
if 'username' not in st.session_state:
    st.session_state.username = None

# --- API FUNCTIONS ---
def login(username, password):
    try:
        response = requests.post(
            f"{API_URL}/token",
            data={"username": username, "password": password},
            timeout=10
        )
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, response.json().get('detail', 'Invalid credentials')
    except requests.exceptions.ConnectionError:
        return False, "Cannot connect to server. Please try again."
    except Exception as e:
        return False, str(e)

def register(username, password):
    try:
        response = requests.post(
            f"{API_URL}/register",
            json={"username": username, "password": password},
            timeout=10
        )
        if response.status_code == 201:
            return True, "Account created successfully!"
        else:
            return False, response.json().get('detail', 'Registration failed')
    except requests.exceptions.ConnectionError:
        return False, "Cannot connect to server. Please try again."
    except Exception as e:
        return False, str(e)

def assess_patient(data, token):
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(
            f"{API_URL}/assess",
            json=data,
            headers=headers,
            timeout=30
        )
        if response.status_code == 200:
            return True, response.json()
        elif response.status_code == 401:
            st.session_state.token = None
            st.session_state.username = None
            return False, "Session expired. Please login again."
        else:
            return False, response.json().get('detail', 'Assessment failed')
    except Exception as e:
        return False, str(e)

# --- PROFESSIONAL CSS - Medical Blue Theme ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
    
    :root {
        --primary: #0066CC;
        --primary-dark: #004C99;
        --primary-light: #E6F0FA;
        --secondary: #00A878;
        --accent: #FF6B6B;
        --dark: #1A1F36;
        --gray-900: #2D3748;
        --gray-700: #4A5568;
        --gray-500: #718096;
        --gray-300: #CBD5E0;
        --gray-100: #F7FAFC;
        --white: #FFFFFF;
        --success: #00A878;
        --warning: #F6AD55;
        --danger: #E53E3E;
    }
    
    * {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Hide Streamlit Elements */
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Main Container */
    .main .block-container {
        padding: 2rem 3rem;
        max-width: 1400px;
    }
    
    /* Auth Container */
    .auth-wrapper {
        min-height: 80vh;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .auth-card {
        background: var(--white);
        border-radius: 20px;
        padding: 3rem;
        box-shadow: 0 10px 40px rgba(0, 102, 204, 0.1);
        max-width: 440px;
        width: 100%;
        border: 1px solid var(--gray-100);
    }
    
    .brand-header {
        text-align: center;
        margin-bottom: 2.5rem;
    }
    
    .brand-icon {
        width: 70px;
        height: 70px;
        background: linear-gradient(135deg, var(--primary), var(--primary-dark));
        border-radius: 18px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 1.2rem;
        font-size: 2rem;
    }
    
    .brand-name {
        font-size: 1.75rem;
        font-weight: 700;
        color: var(--dark);
        margin: 0;
        letter-spacing: -0.5px;
    }
    
    .brand-tagline {
        color: var(--gray-500);
        font-size: 0.95rem;
        margin-top: 0.5rem;
    }
    
    /* Form Inputs */
    .stTextInput > div > div > input {
        background: var(--gray-100) !important;
        border: 2px solid transparent !important;
        border-radius: 12px !important;
        padding: 14px 18px !important;
        font-size: 1rem !important;
        color: var(--dark) !important;
        transition: all 0.2s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        background: var(--white) !important;
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 4px rgba(0, 102, 204, 0.1) !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: var(--gray-500) !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary), var(--primary-dark)) !important;
        color: var(--white) !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 14px 28px !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.3px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(0, 102, 204, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(0, 102, 204, 0.4) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0) !important;
    }
    
    /* Secondary Button */
    .secondary-btn > button {
        background: var(--gray-100) !important;
        color: var(--gray-700) !important;
        box-shadow: none !important;
    }
    
    .secondary-btn > button:hover {
        background: var(--gray-300) !important;
        box-shadow: none !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--gray-100);
        border-radius: 14px;
        padding: 6px;
        gap: 6px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 10px;
        color: var(--gray-700);
        font-weight: 500;
        padding: 12px 24px;
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--white) !important;
        color: var(--primary) !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    
    /* Dashboard Header */
    .dash-header {
        background: linear-gradient(135deg, var(--primary), var(--primary-dark));
        border-radius: 20px;
        padding: 2rem 2.5rem;
        margin-bottom: 2rem;
        color: var(--white);
    }
    
    .dash-title {
        font-size: 1.5rem;
        font-weight: 700;
        margin: 0;
    }
    
    .dash-subtitle {
        opacity: 0.9;
        margin-top: 0.25rem;
        font-size: 0.95rem;
    }
    
    /* Cards */
    .info-card {
        background: var(--white);
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.04);
        border: 1px solid var(--gray-100);
        height: 100%;
        transition: all 0.3s ease;
    }
    
    .info-card:hover {
        box-shadow: 0 8px 30px rgba(0,0,0,0.08);
        transform: translateY(-3px);
    }
    
    .card-icon {
        width: 48px;
        height: 48px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .card-icon.blue { background: var(--primary-light); }
    .card-icon.green { background: rgba(0, 168, 120, 0.1); }
    .card-icon.orange { background: rgba(246, 173, 85, 0.15); }
    
    .card-value {
        font-size: 1.75rem;
        font-weight: 700;
        color: var(--dark);
        line-height: 1.2;
    }
    
    .card-label {
        color: var(--gray-500);
        font-size: 0.875rem;
        margin-top: 0.25rem;
    }
    
    /* Form Sections */
    .form-section {
        background: var(--white);
        border-radius: 16px;
        padding: 1.75rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.04);
        border: 1px solid var(--gray-100);
    }
    
    .section-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1.25rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid var(--gray-100);
    }
    
    .section-icon {
        width: 36px;
        height: 36px;
        background: var(--primary-light);
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.1rem;
    }
    
    .section-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--dark);
        margin: 0;
    }
    
    /* Select boxes */
    .stSelectbox > div > div {
        background: var(--gray-100) !important;
        border: 2px solid transparent !important;
        border-radius: 12px !important;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: var(--primary) !important;
        background: var(--white) !important;
    }
    
    /* Number inputs */
    .stNumberInput > div > div > input {
        background: var(--gray-100) !important;
        border: 2px solid transparent !important;
        border-radius: 12px !important;
    }
    
    .stNumberInput > div > div > input:focus {
        background: var(--white) !important;
        border-color: var(--primary) !important;
    }
    
    /* Slider */
    .stSlider > div > div > div > div {
        background: var(--primary) !important;
    }
    
    /* Risk Results */
    .result-card {
        border-radius: 20px;
        padding: 3rem 2rem;
        text-align: center;
        margin: 2rem 0;
    }
    
    .result-card.high {
        background: linear-gradient(135deg, #E53E3E, #C53030);
        color: white;
    }
    
    .result-card.moderate {
        background: linear-gradient(135deg, #ED8936, #DD6B20);
        color: white;
    }
    
    .result-card.low {
        background: linear-gradient(135deg, #38A169, #2F855A);
        color: white;
    }
    
    .result-score {
        font-size: 4.5rem;
        font-weight: 700;
        line-height: 1;
    }
    
    .result-label {
        font-size: 1.25rem;
        margin-top: 0.75rem;
        opacity: 0.95;
        font-weight: 500;
    }
    
    /* Environment Cards */
    .env-card {
        background: var(--white);
        border-radius: 14px;
        padding: 1.25rem;
        text-align: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.04);
        border: 1px solid var(--gray-100);
    }
    
    .env-icon {
        font-size: 1.75rem;
        margin-bottom: 0.5rem;
    }
    
    .env-value {
        font-size: 1.25rem;
        font-weight: 700;
        color: var(--dark);
    }
    
    .env-label {
        font-size: 0.8rem;
        color: var(--gray-500);
        margin-top: 0.25rem;
    }
    
    /* Recommendations */
    .rec-item {
        background: var(--primary-light);
        border-left: 4px solid var(--primary);
        padding: 1rem 1.25rem;
        border-radius: 0 12px 12px 0;
        margin-bottom: 0.75rem;
        color: var(--dark);
        font-size: 0.95rem;
    }
    
    /* Alert box */
    .alert-box {
        background: rgba(229, 62, 62, 0.1);
        border: 1px solid rgba(229, 62, 62, 0.3);
        border-radius: 12px;
        padding: 1rem 1.25rem;
        color: #C53030;
        font-weight: 500;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem 0;
        margin-top: 3rem;
        border-top: 1px solid var(--gray-100);
        color: var(--gray-500);
        font-size: 0.875rem;
    }
    
    /* Feature Cards on Auth Page */
    .feature-card {
        background: var(--white);
        border-radius: 14px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 2px 12px rgba(0,0,0,0.04);
        border: 1px solid var(--gray-100);
    }
    
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 0.75rem;
    }
    
    .feature-title {
        font-weight: 600;
        color: var(--dark);
        margin-bottom: 0.25rem;
    }
    
    .feature-desc {
        font-size: 0.85rem;
        color: var(--gray-500);
    }
    
    /* Hide anchor links */
    .css-15zrgzn {display: none}
    .css-zt5igj {display: none}
    a[href^="#"] {display: none}
</style>
""", unsafe_allow_html=True)

# === AUTHENTICATION PAGE ===
def show_auth_page():
    st.markdown('<div class="auth-wrapper">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.5, 1])
    
    with col2:
        st.markdown("""
        <div class="auth-card">
            <div class="brand-header">
                <div class="brand-icon">🫀</div>
                <h1 class="brand-name">CardioGuard AI</h1>
                <p class="brand-tagline">Intelligent Cardiac Risk Assessment</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Sign In", "Create Account"])
        
        with tab1:
            with st.form("login_form", clear_on_submit=False):
                st.markdown("<div style='height: 0.5rem'></div>", unsafe_allow_html=True)
                username = st.text_input("Username", placeholder="Enter your username", key="login_user")
                password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_pass")
                st.markdown("<div style='height: 0.5rem'></div>", unsafe_allow_html=True)
                
                submitted = st.form_submit_button("Sign In", use_container_width=True)
                
                if submitted:
                    if not username or not password:
                        st.error("Please enter both username and password")
                    else:
                        with st.spinner("Signing in..."):
                            success, result = login(username, password)
                            if success:
                                st.session_state.token = result['access_token']
                                st.session_state.username = username
                                st.success("Welcome back!")
                                time.sleep(0.5)
                                st.rerun()
                            else:
                                st.error(f"Login failed: {result}")
        
        with tab2:
            with st.form("register_form", clear_on_submit=False):
                st.markdown("<div style='height: 0.5rem'></div>", unsafe_allow_html=True)
                new_username = st.text_input("Choose Username", placeholder="Pick a username", key="reg_user")
                new_password = st.text_input("Create Password", type="password", placeholder="Min 4 characters", key="reg_pass")
                confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter password", key="reg_pass2")
                st.markdown("<div style='height: 0.5rem'></div>", unsafe_allow_html=True)
                
                submitted = st.form_submit_button("Create Account", use_container_width=True)
                
                if submitted:
                    if not new_username or not new_password:
                        st.error("Please fill in all fields")
                    elif len(new_password) < 4:
                        st.error("Password must be at least 4 characters")
                    elif new_password != confirm_password:
                        st.error("Passwords do not match")
                    else:
                        with st.spinner("Creating account..."):
                            success, result = register(new_username, new_password)
                            if success:
                                st.success("Account created! Please sign in.")
                            else:
                                st.error(f"Registration failed: {result}")
        
        # Features
        st.markdown("<div style='height: 2rem'></div>", unsafe_allow_html=True)
        
        f1, f2, f3 = st.columns(3)
        with f1:
            st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">🤖</div>
                <div class="feature-title">AI Analysis</div>
                <div class="feature-desc">Machine Learning Models</div>
            </div>
            """, unsafe_allow_html=True)
        with f2:
            st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">🌍</div>
                <div class="feature-title">Live Data</div>
                <div class="feature-desc">Real-time Environment</div>
            </div>
            """, unsafe_allow_html=True)
        with f3:
            st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">💊</div>
                <div class="feature-title">Smart Advice</div>
                <div class="feature-desc">Personalized Care</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# === DASHBOARD PAGE ===
def show_dashboard():
    # Header
    col_header, col_logout = st.columns([5, 1])
    with col_header:
        st.markdown(f"""
        <div class="dash-header">
            <p class="dash-title">🫀 CardioGuard AI</p>
            <p class="dash-subtitle">Welcome, {st.session_state.username}</p>
        </div>
        """, unsafe_allow_html=True)
    with col_logout:
        st.markdown("<div style='height: 1.5rem'></div>", unsafe_allow_html=True)
        if st.button("Sign Out", key="logout_btn", use_container_width=True):
            st.session_state.token = None
            st.session_state.username = None
            st.rerun()
    
    # Assessment Form
    st.markdown("### 📋 Cardiac Risk Assessment")
    st.markdown("Complete the form below for your personalized risk evaluation.")
    st.markdown("<div style='height: 1rem'></div>", unsafe_allow_html=True)
    
    with st.form("assessment_form"):
        # Demographics Section
        st.markdown("""
        <div class="form-section">
            <div class="section-header">
                <div class="section-icon">👤</div>
                <h3 class="section-title">Demographics & Location</h3>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        d1, d2, d3 = st.columns(3)
        with d1:
            age = st.number_input("Age (years)", min_value=18, max_value=120, value=45, help="Your current age")
        with d2:
            sex = st.selectbox("Sex", options=["Male", "Female"], help="Biological sex")
        with d3:
            city = st.text_input("City", value="London", help="For weather & air quality data")
        
        st.markdown("<div style='height: 1rem'></div>", unsafe_allow_html=True)
        
        # Vital Signs Section
        st.markdown("""
        <div class="form-section">
            <div class="section-header">
                <div class="section-icon">🩺</div>
                <h3 class="section-title">Vital Signs & Blood Work</h3>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        v1, v2, v3, v4 = st.columns(4)
        with v1:
            trestbps = st.number_input("Blood Pressure (mm Hg)", min_value=80, max_value=220, value=120, help="Resting blood pressure")
        with v2:
            chol = st.number_input("Cholesterol (mg/dl)", min_value=100, max_value=600, value=200, help="Serum cholesterol level")
        with v3:
            thalach = st.number_input("Max Heart Rate", min_value=60, max_value=220, value=150, help="Maximum heart rate achieved")
        with v4:
            fbs = st.selectbox("Blood Sugar > 120", options=["No", "Yes"], help="Fasting blood sugar > 120 mg/dl")
        
        st.markdown("<div style='height: 1rem'></div>", unsafe_allow_html=True)
        
        # Symptoms Section
        st.markdown("""
        <div class="form-section">
            <div class="section-header">
                <div class="section-icon">📊</div>
                <h3 class="section-title">Symptoms & ECG Results</h3>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        s1, s2, s3 = st.columns(3)
        with s1:
            cp = st.selectbox("Chest Pain Type", options=[
                "Typical Angina",
                "Atypical Angina", 
                "Non-Anginal Pain",
                "Asymptomatic"
            ], help="Type of chest pain experienced")
        with s2:
            restecg = st.selectbox("Resting ECG", options=[
                "Normal",
                "ST-T Wave Abnormality",
                "Left Ventricular Hypertrophy"
            ], help="Resting ECG results")
        with s3:
            exang = st.selectbox("Exercise Angina", options=["No", "Yes"], help="Chest pain during exercise")
        
        st.markdown("<div style='height: 1rem'></div>", unsafe_allow_html=True)
        
        # Advanced Tests Section
        st.markdown("""
        <div class="form-section">
            <div class="section-header">
                <div class="section-icon">🔬</div>
                <h3 class="section-title">Advanced Cardiac Tests</h3>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        a1, a2, a3, a4 = st.columns(4)
        with a1:
            oldpeak = st.slider("ST Depression", min_value=0.0, max_value=6.0, value=1.0, step=0.1, help="ST depression induced by exercise")
        with a2:
            slope = st.selectbox("ST Slope", options=[
                "Upsloping",
                "Flat",
                "Downsloping"
            ], help="Slope of peak exercise ST segment")
        with a3:
            ca = st.selectbox("Vessels Colored", options=["0", "1", "2", "3", "4"], help="Major vessels colored by fluoroscopy")
        with a4:
            thal = st.selectbox("Thalassemia", options=[
                "Normal",
                "Fixed Defect",
                "Reversible Defect"
            ], help="Thalassemia status")
        
        st.markdown("<div style='height: 1.5rem'></div>", unsafe_allow_html=True)
        
        # Submit
        submitted = st.form_submit_button("🔬 Analyze Cardiac Risk", use_container_width=True)
    
    # Process Results
    if submitted:
        with st.spinner("Analyzing your cardiac data..."):
            # Convert values
            sex_val = 1 if sex == "Male" else 0
            cp_val = ["Typical Angina", "Atypical Angina", "Non-Anginal Pain", "Asymptomatic"].index(cp)
            fbs_val = 1 if fbs == "Yes" else 0
            restecg_val = ["Normal", "ST-T Wave Abnormality", "Left Ventricular Hypertrophy"].index(restecg)
            exang_val = 1 if exang == "Yes" else 0
            slope_val = ["Upsloping", "Flat", "Downsloping"].index(slope)
            ca_val = int(ca)
            thal_val = ["Normal", "Fixed Defect", "Reversible Defect"].index(thal) + 1
            
            patient_data = {
                "age": age,
                "sex": sex_val,
                "cp": cp_val,
                "trestbps": trestbps,
                "chol": chol,
                "fbs": fbs_val,
                "restecg": restecg_val,
                "thalach": thalach,
                "exang": exang_val,
                "oldpeak": oldpeak,
                "slope": slope_val,
                "ca": ca_val,
                "thal": thal_val,
                "city": city
            }
            
            success, result = assess_patient(patient_data, st.session_state.token)
        
        if success:
            st.markdown("---")
            st.markdown("## 📊 Assessment Results")
            
            risk_score = result['risk_score']
            risk_category = result['risk_category']
            
            # Determine risk class
            if risk_category == "High Risk":
                risk_class = "high"
                risk_emoji = "🚨"
            elif risk_category == "Moderate":
                risk_class = "moderate"
                risk_emoji = "⚠️"
            else:
                risk_class = "low"
                risk_emoji = "✅"
            
            # Display result
            r1, r2, r3 = st.columns([1, 2, 1])
            with r2:
                st.markdown(f"""
                <div class="result-card {risk_class}">
                    <div class="result-score">{risk_emoji} {risk_score}%</div>
                    <div class="result-label">{risk_category}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Environment
            st.markdown("### 🌍 Environmental Factors")
            env = result['environment']
            
            e1, e2, e3, e4 = st.columns(4)
            with e1:
                st.markdown(f"""
                <div class="env-card">
                    <div class="env-icon">📍</div>
                    <div class="env-value">{env['city']}</div>
                    <div class="env-label">Location</div>
                </div>
                """, unsafe_allow_html=True)
            with e2:
                temp = f"{env['temp']}°C" if env.get('temp') else "N/A"
                st.markdown(f"""
                <div class="env-card">
                    <div class="env-icon">🌡️</div>
                    <div class="env-value">{temp}</div>
                    <div class="env-label">Temperature</div>
                </div>
                """, unsafe_allow_html=True)
            with e3:
                aqi_map = {1: "Good", 2: "Fair", 3: "Moderate", 4: "Poor", 5: "Very Poor"}
                aqi = aqi_map.get(env.get('aqi'), "N/A")
                st.markdown(f"""
                <div class="env-card">
                    <div class="env-icon">💨</div>
                    <div class="env-value">{aqi}</div>
                    <div class="env-label">Air Quality</div>
                </div>
                """, unsafe_allow_html=True)
            with e4:
                stress = env.get('stress_factor', 0)
                st.markdown(f"""
                <div class="env-card">
                    <div class="env-icon">📈</div>
                    <div class="env-value">{stress}%</div>
                    <div class="env-label">Env. Stress</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Recommendations
            st.markdown("### 💊 Recommendations")
            for rec in result['recommendations']:
                st.markdown(f'<div class="rec-item">💡 {rec}</div>', unsafe_allow_html=True)
            
            # Warning for high risk
            if risk_category == "High Risk":
                st.markdown("""
                <div class="alert-box">
                    ⚠️ <strong>Important:</strong> Your assessment indicates elevated cardiac risk. 
                    Please consult a healthcare professional for comprehensive evaluation.
                </div>
                """, unsafe_allow_html=True)
        else:
            st.error(f"Assessment failed: {result}")
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p>🫀 <strong>CardioGuard AI</strong> — Intelligent Cardiac Risk Assessment</p>
        <p style="margin-top: 0.5rem; font-size: 0.8rem;">
            ⚠️ This tool is for educational purposes only. Always consult qualified healthcare professionals.
        </p>
    </div>
    """, unsafe_allow_html=True)

# === MAIN APP ===
if st.session_state.token:
    show_dashboard()
else:
    show_auth_page()
