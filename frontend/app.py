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
if 'just_registered' not in st.session_state:
    st.session_state.just_registered = False
if 'show_welcome' not in st.session_state:
    st.session_state.show_welcome = False

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

# --- PROFESSIONAL CSS - Dark Medical Theme ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    :root {
        --bg-primary: #0a0f1a;
        --bg-secondary: #111827;
        --bg-card: #1f2937;
        --bg-input: #374151;
        --accent-blue: #3b82f6;
        --accent-blue-hover: #2563eb;
        --accent-green: #10b981;
        --accent-orange: #f59e0b;
        --accent-red: #ef4444;
        --text-primary: #f9fafb;
        --text-secondary: #9ca3af;
        --text-muted: #6b7280;
        --border-color: #374151;
        --gradient-start: #3b82f6;
        --gradient-end: #8b5cf6;
    }
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Hide Streamlit defaults */
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display: none;}
    div[data-testid="stToolbar"] {display: none;}
    div[data-testid="stDecoration"] {display: none;}
    
    /* Main background */
    .stApp {
        background: var(--bg-primary);
    }
    
    .main .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    
    /* ========== NAVBAR ========== */
    .navbar {
        background: var(--bg-secondary);
        border-bottom: 1px solid var(--border-color);
        padding: 0.75rem 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        position: sticky;
        top: 0;
        z-index: 1000;
    }
    
    .nav-brand {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .nav-logo {
        width: 40px;
        height: 40px;
        background: linear-gradient(135deg, var(--gradient-start), var(--gradient-end));
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.25rem;
    }
    
    .nav-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: var(--text-primary);
        letter-spacing: -0.5px;
    }
    
    /* Hamburger Menu */
    .menu-toggle {
        display: flex;
        flex-direction: column;
        gap: 5px;
        cursor: pointer;
        padding: 8px;
    }
    
    .menu-toggle span {
        width: 24px;
        height: 3px;
        background: var(--text-primary);
        border-radius: 2px;
        transition: 0.3s;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: var(--bg-secondary) !important;
        border-right: 1px solid var(--border-color);
    }
    
    [data-testid="stSidebar"] > div {
        background: var(--bg-secondary) !important;
    }
    
    [data-testid="stSidebarContent"] {
        background: var(--bg-secondary) !important;
    }
    
    .nav-profile {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .user-info {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        background: var(--bg-card);
        padding: 0.5rem 1rem;
        border-radius: 50px;
        border: 1px solid var(--border-color);
    }
    
    .user-avatar {
        width: 32px;
        height: 32px;
        background: linear-gradient(135deg, var(--accent-green), #059669);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.875rem;
        font-weight: 600;
        color: white;
    }
    
    .user-name {
        color: var(--text-primary);
        font-weight: 500;
        font-size: 0.9rem;
    }
    
    .user-role {
        color: var(--text-muted);
        font-size: 0.75rem;
    }
    
    /* ========== AUTH PAGE ========== */
    .auth-container {
        min-height: 100vh;
        display: flex;
        background: var(--bg-primary);
    }
    
    .auth-left {
        flex: 1;
        background: linear-gradient(135deg, #1e3a5f 0%, #0a0f1a 100%);
        display: flex;
        flex-direction: column;
        justify-content: center;
        padding: 4rem;
    }
    
    .auth-hero-title {
        font-size: 3rem;
        font-weight: 800;
        color: var(--text-primary);
        line-height: 1.2;
        margin-bottom: 1.5rem;
    }
    
    .auth-hero-title span {
        background: linear-gradient(135deg, var(--gradient-start), var(--gradient-end));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .auth-hero-desc {
        color: var(--text-secondary);
        font-size: 1.125rem;
        line-height: 1.7;
        max-width: 500px;
    }
    
    .auth-features {
        display: flex;
        gap: 2rem;
        margin-top: 3rem;
    }
    
    .auth-feature {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .auth-feature-icon {
        width: 44px;
        height: 44px;
        background: rgba(59, 130, 246, 0.15);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.25rem;
    }
    
    .auth-feature-text {
        color: var(--text-secondary);
        font-size: 0.9rem;
    }
    
    .auth-right {
        width: 480px;
        background: var(--bg-secondary);
        display: flex;
        flex-direction: column;
        justify-content: center;
        padding: 3rem;
    }
    
    .auth-card {
        background: var(--bg-card);
        border-radius: 20px;
        padding: 2.5rem;
        border: 1px solid var(--border-color);
    }
    
    .auth-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .auth-logo {
        width: 64px;
        height: 64px;
        background: linear-gradient(135deg, var(--gradient-start), var(--gradient-end));
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.75rem;
        margin: 0 auto 1rem;
    }
    
    .auth-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 0.25rem;
    }
    
    .auth-subtitle {
        color: var(--text-muted);
        font-size: 0.9rem;
    }
    
    /* ========== FORM INPUTS ========== */
    .stTextInput > label, .stSelectbox > label, .stNumberInput > label {
        color: var(--text-secondary) !important;
        font-weight: 500 !important;
        font-size: 0.875rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    .stTextInput > div > div > input {
        background: var(--bg-input) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 10px !important;
        padding: 0.875rem 1rem !important;
        font-size: 0.95rem !important;
        color: var(--text-primary) !important;
        transition: all 0.2s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--accent-blue) !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15) !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: var(--text-muted) !important;
    }
    
    .stNumberInput > div > div > input {
        background: var(--bg-input) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 10px !important;
        color: var(--text-primary) !important;
    }
    
    .stSelectbox > div > div {
        background: var(--bg-input) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 10px !important;
    }
    
    .stSelectbox > div > div > div {
        color: var(--text-primary) !important;
    }
    
    /* ========== BUTTONS ========== */
    .stButton > button {
        background: linear-gradient(135deg, var(--gradient-start), var(--gradient-end)) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.875rem 1.5rem !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4) !important;
    }
    
    /* Logout button */
    .logout-btn button {
        background: transparent !important;
        border: 1px solid var(--border-color) !important;
        color: var(--text-secondary) !important;
        box-shadow: none !important;
        padding: 0.5rem 1rem !important;
        font-size: 0.85rem !important;
    }
    
    .logout-btn button:hover {
        background: rgba(239, 68, 68, 0.1) !important;
        border-color: var(--accent-red) !important;
        color: var(--accent-red) !important;
        transform: none !important;
        box-shadow: none !important;
    }
    
    /* ========== TABS ========== */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--bg-input);
        border-radius: 12px;
        padding: 4px;
        gap: 4px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        color: var(--text-muted);
        font-weight: 500;
        padding: 0.75rem 1.5rem;
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--accent-blue) !important;
        color: white !important;
    }
    
    /* ========== FEATURE CARDS ========== */
    .feature-card {
        background: var(--bg-card);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid var(--border-color);
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        border-color: var(--accent-blue);
        transform: translateY(-3px);
    }
    
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 0.75rem;
    }
    
    .feature-title {
        font-weight: 600;
        color: var(--text-primary);
        font-size: 0.95rem;
        margin-bottom: 0.25rem;
    }
    
    .feature-desc {
        font-size: 0.8rem;
        color: var(--text-muted);
    }
    
    /* ========== WELCOME BANNER PRO ========== */
    .welcome-banner-pro {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(139, 92, 246, 0.1));
        border: 1px solid rgba(59, 130, 246, 0.2);
        border-radius: 20px;
        padding: 3rem 2rem;
        text-align: center;
        margin: 2rem 0;
    }
    
    .welcome-icon-row {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        display: flex;
        justify-content: center;
        gap: 0.5rem;
    }
    
    .welcome-title-pro {
        font-size: 2rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 1rem;
        background: linear-gradient(135deg, var(--gradient-start), var(--gradient-end));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .welcome-desc-pro {
        color: var(--text-secondary);
        font-size: 1.1rem;
        line-height: 1.7;
        max-width: 600px;
        margin: 0 auto;
    }
    
    /* ========== WELCOME BANNER ========== */
    .welcome-banner {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(59, 130, 246, 0.15));
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 16px;
        padding: 2rem;
        margin: 2rem;
        text-align: center;
    }
    
    .welcome-emoji {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    .welcome-title {
        font-size: 1.75rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }
    
    .welcome-message {
        color: var(--text-secondary);
        font-size: 1rem;
        max-width: 500px;
        margin: 0 auto;
        line-height: 1.6;
    }
    
    /* ========== CONTENT AREA ========== */
    .content-area {
        padding: 2rem 3rem;
        max-width: 1400px;
        margin: 0 auto;
    }
    
    .page-header {
        margin-bottom: 2rem;
    }
    
    .page-title {
        font-size: 1.75rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }
    
    .page-desc {
        color: var(--text-secondary);
        font-size: 1rem;
    }
    
    /* ========== FORM SECTIONS ========== */
    .form-section {
        background: var(--bg-card);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        border: 1px solid var(--border-color);
    }
    
    .section-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1.25rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid var(--border-color);
    }
    
    .section-icon {
        width: 40px;
        height: 40px;
        background: rgba(59, 130, 246, 0.15);
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.1rem;
    }
    
    .section-title {
        font-size: 1rem;
        font-weight: 600;
        color: var(--text-primary);
    }
    
    /* ========== RESULT CARDS ========== */
    .result-card {
        border-radius: 20px;
        padding: 3rem 2rem;
        text-align: center;
        margin: 2rem 0;
    }
    
    .result-card.high {
        background: linear-gradient(135deg, #dc2626, #991b1b);
    }
    
    .result-card.moderate {
        background: linear-gradient(135deg, #d97706, #b45309);
    }
    
    .result-card.low {
        background: linear-gradient(135deg, #059669, #047857);
    }
    
    .result-score {
        font-size: 4rem;
        font-weight: 800;
        color: white;
        line-height: 1;
    }
    
    .result-label {
        font-size: 1.25rem;
        color: rgba(255,255,255,0.9);
        margin-top: 0.75rem;
        font-weight: 500;
    }
    
    /* ========== ENV CARDS ========== */
    .env-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin: 1.5rem 0;
    }
    
    .env-card {
        background: var(--bg-card);
        border-radius: 14px;
        padding: 1.25rem;
        text-align: center;
        border: 1px solid var(--border-color);
    }
    
    .env-icon {
        font-size: 1.75rem;
        margin-bottom: 0.5rem;
    }
    
    .env-value {
        font-size: 1.25rem;
        font-weight: 700;
        color: var(--text-primary);
    }
    
    .env-label {
        font-size: 0.8rem;
        color: var(--text-muted);
        margin-top: 0.25rem;
    }
    
    /* ========== RECOMMENDATIONS ========== */
    .rec-item {
        background: rgba(59, 130, 246, 0.1);
        border-left: 4px solid var(--accent-blue);
        padding: 1rem 1.25rem;
        border-radius: 0 12px 12px 0;
        margin-bottom: 0.75rem;
        color: var(--text-primary);
        font-size: 0.95rem;
    }
    
    /* ========== ALERT ========== */
    .alert-box {
        background: rgba(239, 68, 68, 0.15);
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-radius: 12px;
        padding: 1rem 1.25rem;
        color: #fca5a5;
        font-weight: 500;
        margin-top: 1.5rem;
    }
    
    /* ========== SUCCESS MESSAGE ========== */
    .success-msg {
        background: rgba(16, 185, 129, 0.15);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 12px;
        padding: 1rem;
        color: #6ee7b7;
        text-align: center;
        margin: 1rem 0;
    }
    
    /* ========== FOOTER ========== */
    .footer {
        text-align: center;
        padding: 2rem;
        margin-top: 2rem;
        border-top: 1px solid var(--border-color);
        color: var(--text-muted);
        font-size: 0.875rem;
    }
    
    /* Slider */
    .stSlider > div > div > div > div {
        background: var(--accent-blue) !important;
    }
    
    .stSlider > div > div > div > div > div {
        background: var(--accent-blue) !important;
    }
    
    /* Hide anchor links */
    .css-15zrgzn, .css-zt5igj, a[href^="#"] {display: none !important;}
    
    /* Markdown text color */
    .stMarkdown, .stMarkdown p, .stMarkdown li {
        color: var(--text-primary) !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-primary) !important;
    }
</style>
""", unsafe_allow_html=True)

# === AUTHENTICATION PAGE ===
def show_auth_page():
    # Centered layout
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding-top: 2rem;">
            <div class="auth-logo">🫀</div>
            <h2 class="auth-title">CardioGuard AI</h2>
            <p class="auth-subtitle">Intelligent Cardiac Risk Assessment</p>
        </div>
        """, unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["🔐 Sign In", "✨ Create Account"])
        
        with tab1:
            with st.form("login_form", clear_on_submit=False):
                username = st.text_input("Username", placeholder="Enter your username", key="login_user")
                password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_pass")
                
                st.markdown("<div style='height: 0.5rem'></div>", unsafe_allow_html=True)
                submitted = st.form_submit_button("Sign In →", use_container_width=True)
                
                if submitted:
                    if not username or not password:
                        st.error("⚠️ Please enter both username and password")
                    else:
                        with st.spinner("Signing in..."):
                            success, result = login(username, password)
                            if success:
                                st.session_state.token = result['access_token']
                                st.session_state.username = username
                                st.session_state.show_welcome = True
                                time.sleep(0.5)
                                st.rerun()
                            else:
                                st.error(f"❌ {result}")
        
        with tab2:
            with st.form("register_form", clear_on_submit=False):
                new_username = st.text_input("Choose Username", placeholder="Pick a unique username", key="reg_user")
                new_password = st.text_input("Create Password", type="password", placeholder="Min 4 characters", key="reg_pass")
                confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter password", key="reg_pass2")
                
                st.markdown("<div style='height: 0.5rem'></div>", unsafe_allow_html=True)
                submitted = st.form_submit_button("Create Account →", use_container_width=True)
                
                if submitted:
                    if not new_username or not new_password:
                        st.error("⚠️ Please fill in all fields")
                    elif len(new_password) < 4:
                        st.error("⚠️ Password must be at least 4 characters")
                    elif new_password != confirm_password:
                        st.error("⚠️ Passwords do not match")
                    else:
                        with st.spinner("Creating your account..."):
                            success, result = register(new_username, new_password)
                            if success:
                                st.markdown("""
                                <div class="success-msg">
                                    ✅ <strong>Account created successfully!</strong><br>
                                    Please sign in with your credentials.
                                </div>
                                """, unsafe_allow_html=True)
                                st.balloons()
                            else:
                                st.error(f"❌ {result}")
        
        # Features below form
        st.markdown("<div style='height: 2rem'></div>", unsafe_allow_html=True)
        f1, f2, f3 = st.columns(3)
        with f1:
            st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">🤖</div>
                <div class="feature-title">ML-Powered Analysis</div>
                <div class="feature-desc">Advanced Machine Learning Models</div>
            </div>
            """, unsafe_allow_html=True)
        with f2:
            st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">🌍</div>
                <div class="feature-title">Real-time Environment</div>
                <div class="feature-desc">Live Weather & Air Quality Data</div>
            </div>
            """, unsafe_allow_html=True)
        with f3:
            st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">💊</div>
                <div class="feature-title">Personalized Advice</div>
                <div class="feature-desc">Smart Health Recommendations</div>
            </div>
            """, unsafe_allow_html=True)

# === DASHBOARD PAGE ===
def show_dashboard():
    # Professional Header with Profile & Logout inline
    header_col1, header_col2 = st.columns([6, 4])
    
    with header_col1:
        st.markdown("""
        <div style="display: flex; align-items: center; gap: 12px; padding: 1rem 0;">
            <div style="width: 45px; height: 45px; background: linear-gradient(135deg, #3b82f6, #8b5cf6); 
                        border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 1.5rem;">
                🫀
            </div>
            <div>
                <div style="font-size: 1.25rem; font-weight: 700; color: #f9fafb;">CardioGuard AI</div>
                <div style="font-size: 0.75rem; color: #6b7280;">Cardiac Risk Assessment</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with header_col2:
        profile_col, logout_col = st.columns([3, 1])
        with profile_col:
            st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 10px; justify-content: flex-end; padding: 1rem 0;">
                <div style="width: 36px; height: 36px; background: linear-gradient(135deg, #10b981, #059669); 
                            border-radius: 50%; display: flex; align-items: center; justify-content: center; 
                            font-size: 0.9rem; color: white; font-weight: 600;">
                    {st.session_state.username[0].upper()}
                </div>
                <div style="text-align: left;">
                    <div style="font-size: 0.9rem; font-weight: 500; color: #f9fafb;">{st.session_state.username}</div>
                    <div style="font-size: 0.7rem; color: #6b7280;">Patient</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with logout_col:
            st.markdown("<div style='padding-top: 1rem;'>", unsafe_allow_html=True)
            if st.button("🚪", key="logout_btn", help="Logout"):
                st.session_state.token = None
                st.session_state.username = None
                st.session_state.show_welcome = False
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<hr style='border: none; border-top: 1px solid #374151; margin: 0 0 1.5rem 0;'>", unsafe_allow_html=True)
    
    # Welcome Banner (shown only once after login)
    if st.session_state.show_welcome:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(59, 130, 246, 0.15), rgba(139, 92, 246, 0.15));
                    border: 1px solid rgba(59, 130, 246, 0.3); border-radius: 16px; padding: 2.5rem; 
                    text-align: center; margin-bottom: 2rem;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">👋🫀✨</div>
            <h2 style="font-size: 1.75rem; font-weight: 700; color: #f9fafb; margin-bottom: 0.75rem;">
                Welcome to CardioGuard, {st.session_state.username}!
            </h2>
            <p style="color: #9ca3af; font-size: 1rem; max-width: 600px; margin: 0 auto; line-height: 1.6;">
                We're excited to have you! Complete the cardiac assessment form below to receive your 
                personalized risk evaluation powered by AI and real-time environmental data.
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.session_state.show_welcome = False
    
    # Tabs for Assessment and History
    tab_assess, tab_history = st.tabs(["📋 New Assessment", "📊 My History"])
    
    with tab_assess:
        show_assessment_form()
    
    with tab_history:
        show_history()

def get_history(token):
    """Fetch user's assessment history"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{API_URL}/history", headers=headers, timeout=10)
        if response.status_code == 200:
            return True, response.json()
        return False, "Failed to load history"
    except Exception as e:
        return False, str(e)

def show_history():
    """Display user's assessment history"""
    success, data = get_history(st.session_state.token)
    
    if success and data.get('history'):
        st.markdown(f"""
        <div style="margin-bottom: 1.5rem;">
            <h3 style="color: #f9fafb; font-size: 1.25rem;">Your Assessment History</h3>
            <p style="color: #6b7280;">You have {data['count']} previous assessments</p>
        </div>
        """, unsafe_allow_html=True)
        
        for item in data['history']:
            # Use percentage-based logic (>=60% = High Risk)
            score = item['risk_score']
            if score >= 60:
                risk_color = "#ef4444"
                risk_label = "High Risk"
            elif score >= 30:
                risk_color = "#f59e0b"
                risk_label = "Moderate"
            else:
                risk_color = "#10b981"
                risk_label = "Low Risk"
            
            st.markdown(f"""
            <div style="background: #1f2937; border-radius: 12px; padding: 1.25rem; margin-bottom: 1rem; 
                        border-left: 4px solid {risk_color};">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="color: #f9fafb; font-weight: 600; font-size: 1rem;">
                            Risk Score: {item['risk_score']}%
                        </div>
                        <div style="color: #6b7280; font-size: 0.85rem; margin-top: 0.25rem;">
                            {item['date']} • Age: {item['age']} • BP: {item['trestbps']} • Chol: {item['chol']}
                        </div>
                    </div>
                    <div style="background: {risk_color}; color: white; padding: 0.5rem 1rem; 
                                border-radius: 20px; font-size: 0.8rem; font-weight: 600;">
                        {risk_label}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align: center; padding: 3rem; background: #1f2937; border-radius: 16px;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">📭</div>
            <h3 style="color: #f9fafb; margin-bottom: 0.5rem;">No History Yet</h3>
            <p style="color: #6b7280;">Complete your first assessment to see your history here.</p>
        </div>
        """, unsafe_allow_html=True)

def show_assessment_form():
    """The main assessment form"""
    # Page Header
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h1 style="font-size: 1.5rem; font-weight: 700; color: #f9fafb; margin-bottom: 0.25rem;">📋 Cardiac Risk Assessment</h1>
        <p style="color: #9ca3af; font-size: 0.95rem;">Complete the form below for your personalized AI-powered risk evaluation.</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("assessment_form"):
        # Section 1: Demographics
        st.markdown("""
        <div class="form-section">
            <div class="section-header">
                <div class="section-icon">👤</div>
                <span class="section-title">Demographics & Location</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        d1, d2, d3 = st.columns(3)
        with d1:
            age = st.number_input("Age (years)", min_value=18, max_value=120, value=45)
        with d2:
            sex = st.selectbox("Biological Sex", options=["Male", "Female"])
        with d3:
            city = st.text_input("City (for weather data)", value="London")
        
        # Section 2: Vital Signs
        st.markdown("""
        <div class="form-section">
            <div class="section-header">
                <div class="section-icon">🩺</div>
                <span class="section-title">Vital Signs & Blood Work</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        v1, v2, v3, v4 = st.columns(4)
        with v1:
            trestbps = st.number_input("Blood Pressure (mm Hg)", min_value=80, max_value=220, value=120)
        with v2:
            chol = st.number_input("Cholesterol (mg/dl)", min_value=100, max_value=600, value=200)
        with v3:
            thalach = st.number_input("Max Heart Rate", min_value=60, max_value=220, value=150)
        with v4:
            fbs = st.selectbox("Blood Sugar > 120 mg/dl", options=["No", "Yes"])
        
        # Section 3: Symptoms
        st.markdown("""
        <div class="form-section">
            <div class="section-header">
                <div class="section-icon">📊</div>
                <span class="section-title">Symptoms & ECG Results</span>
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
            ])
        with s2:
            restecg = st.selectbox("Resting ECG Result", options=[
                "Normal",
                "ST-T Wave Abnormality",
                "Left Ventricular Hypertrophy"
            ])
        with s3:
            exang = st.selectbox("Exercise-Induced Angina", options=["No", "Yes"])
        
        # Section 4: Advanced Tests
        st.markdown("""
        <div class="form-section">
            <div class="section-header">
                <div class="section-icon">🔬</div>
                <span class="section-title">Advanced Cardiac Tests</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        a1, a2, a3, a4 = st.columns(4)
        with a1:
            oldpeak = st.slider("ST Depression", min_value=0.0, max_value=6.0, value=1.0, step=0.1)
        with a2:
            slope = st.selectbox("ST Slope", options=["Upsloping", "Flat", "Downsloping"])
        with a3:
            ca = st.selectbox("Vessels Colored", options=["0", "1", "2", "3", "4"])
        with a4:
            thal = st.selectbox("Thalassemia", options=["Normal", "Fixed Defect", "Reversible Defect"])
        
        st.markdown("<div style='height: 1rem'></div>", unsafe_allow_html=True)
        submitted = st.form_submit_button("🔬 Analyze My Cardiac Risk", use_container_width=True)
    
    # Process Results
    if submitted:
        with st.spinner("🧠 AI is analyzing your cardiac data..."):
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
                "age": age, "sex": sex_val, "cp": cp_val,
                "trestbps": trestbps, "chol": chol, "fbs": fbs_val,
                "restecg": restecg_val, "thalach": thalach, "exang": exang_val,
                "oldpeak": oldpeak, "slope": slope_val, "ca": ca_val,
                "thal": thal_val, "city": city
            }
            
            success, result = assess_patient(patient_data, st.session_state.token)
        
        if success:
            st.markdown("---")
            st.markdown("## 📊 Your Assessment Results")
            
            risk_score = result['risk_score']
            risk_category = result['risk_category']
            
            # Determine risk class based on percentage (>60% = high risk with red)
            if risk_score >= 60:
                risk_class = "high"
                risk_emoji = "🚨"
                risk_category = "High Risk"
            elif risk_score >= 30:
                risk_class = "moderate"
                risk_emoji = "⚠️"
                risk_category = "Moderate Risk"
            else:
                risk_class = "low"
                risk_emoji = "✅"
                risk_category = "Low Risk"
            
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
            st.markdown("### 💊 Personalized Recommendations")
            for rec in result['recommendations']:
                st.markdown(f'<div class="rec-item">{rec}</div>', unsafe_allow_html=True)
            
            # Warning for high risk
            if risk_category == "High Risk":
                st.markdown("""
                <div class="alert-box">
                    🚨 <strong>IMPORTANT:</strong> Your assessment indicates elevated cardiac risk. 
                    Please consult a healthcare professional immediately for comprehensive evaluation.
                </div>
                """, unsafe_allow_html=True)
        else:
            st.error(f"❌ Assessment failed: {result}")
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p>🫀 <strong>CardioGuard AI</strong> — Intelligent Cardiac Risk Assessment System</p>
        <p style="margin-top: 0.5rem; font-size: 0.8rem; color: #6b7280;">
            ⚠️ This tool is for educational purposes only. Always consult qualified healthcare professionals for medical advice.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# === MAIN APP ===
if st.session_state.token:
    show_dashboard()
else:
    show_auth_page()
