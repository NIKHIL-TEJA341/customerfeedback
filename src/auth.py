import os
import streamlit as st
import urllib.parse
import requests
from dotenv import load_dotenv
from streamlit_cookies_controller import CookieController

load_dotenv()

def get_cookie_controller():
    if 'cookie_controller' not in st.session_state:
        st.session_state['cookie_controller'] = CookieController()
    return st.session_state['cookie_controller']

try:
    CLIENT_ID = st.secrets["GOOGLE_CLIENT_ID"]
    CLIENT_SECRET = st.secrets["GOOGLE_CLIENT_SECRET"]
    REDIRECT_URI = st.secrets["REDIRECT_URI"]
except Exception:
    CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    REDIRECT_URI = os.getenv("REDIRECT_URI", "http://localhost:8501")

def init_session_state():
    # Try to load from cookie first
    cookie_controller = get_cookie_controller()
    saved_email = cookie_controller.get('sentix_user_email')
    saved_name = cookie_controller.get('sentix_user_name')
    
    if 'connected' not in st.session_state:
        if saved_email and saved_name:
            st.session_state['connected'] = True
            st.session_state['demo_mode'] = False
            st.session_state['user_info'] = {
                "name": saved_name,
                "email": saved_email,
                "picture": ""
            }
        else:
            st.session_state['connected'] = False
    
    if 'demo_mode' not in st.session_state:
        st.session_state['demo_mode'] = False

def get_login_url():
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "online",
        "prompt": "select_account"
    }
    url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode(params)
    return url

def check_authentification():
    # Use st.query_params to parse the URL for a Google Auth code
    query_params = st.query_params
    if "code" in query_params and not st.session_state.get('connected'):
        code = query_params["code"]
        
        # Exchange the code for an access token directly with Google
        token_url = "https://oauth2.googleapis.com/token"
        data = {
            "code": code,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "redirect_uri": REDIRECT_URI,
            "grant_type": "authorization_code"
        }
        res = requests.post(token_url, data=data)
        
        if res.status_code == 200:
            tokens = res.json()
            access_token = tokens.get("access_token")
            
            # Fetch user info using the access token
            user_info_url = "https://www.googleapis.com/oauth2/v1/userinfo"
            user_res = requests.get(user_info_url, headers={"Authorization": f"Bearer {access_token}"})
            
            if user_res.status_code == 200:
                user_info = user_res.json()
                st.session_state['connected'] = True
                st.session_state['demo_mode'] = False
                st.session_state['user_info'] = {
                    "name": user_info.get("name"),
                    "email": user_info.get("email"),
                    "picture": user_info.get("picture")
                }
                
                # Persist to cookie (7 day expiry)
                cookie_controller = get_cookie_controller()
                cookie_controller.set('sentix_user_email', user_info.get("email"), max_age=604800)
                cookie_controller.set('sentix_user_name', user_info.get("name"), max_age=604800)
                
                # Clear query parameters so a refresh doesn't trigger auth again
                st.query_params.clear()
                st.rerun()

def login():
    """Renders the Google Login button"""
    st.markdown(f'<a href="{get_login_url()}" target="_self" style="display:inline-flex; align-items:center; justify-content:center; gap:8px; padding:0.6rem 1.2rem; background-color:white; color:#334155; border:1px solid #CBD5E1; border-radius:8px; text-decoration:none; font-weight:600; font-size:1.05rem; width:100%; box-shadow:0 1px 2px rgba(0,0,0,0.05); transition:background-color 0.2s;"><svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.73 17.74 9.5 24 9.5z"/><path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/><path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"/><path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/></svg>Continue with Google</a>', unsafe_allow_html=True)

def logout():
    """Logs the user out"""
    st.session_state['connected'] = False
    st.session_state.pop('user_info', None)
    st.session_state['demo_mode'] = False
    try:
        cookie_controller = get_cookie_controller()
        cookie_controller.remove('sentix_user_email')
    except KeyError:
        pass
    try:
        cookie_controller = get_cookie_controller()
        cookie_controller.remove('sentix_user_name')
    except KeyError:
        pass
    st.rerun()

def check_auth():
    """Checks if the user is authenticated (Google) or in Demo Mode."""
    init_session_state()
    check_authentification()
    is_demo = st.session_state.get('demo_mode', False)
    is_logged_in = st.session_state.get('connected', False)
    return is_demo or is_logged_in

def require_auth():
    """Stops execution if the user is not authenticated."""
    if not check_auth():
        st.warning("🔒 Please log in with Google or select Demo Mode from the Home page to view this.")
        st.stop()

def get_current_user_email():
    """Returns the email of the logged-in user, or None if in Demo Mode."""
    if st.session_state.get('connected') and 'user_info' in st.session_state:
        return st.session_state['user_info'].get('email')
    return None
