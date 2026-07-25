import streamlit as st

def load_css():
    """Injects premium dark theme CSS overrides into the Streamlit app."""
    st.markdown("""
        <style>
            /* Sidebar background */
            [data-testid="stSidebar"] {
                background-color: #0B1120 !important;
                border-right: 1px solid #1A2235 !important;
            }
            
            /* Custom Logo Box */
            .top-sidebar-logo {
                display: flex; 
                align-items: center;
                margin-top: 0;
                margin-bottom: 1rem;
                padding: 1.25rem 1rem;
                background-color: #050810;
                border: 1px solid #1E293B;
                border-radius: 16px;
                box-shadow: 0 8px 16px -4px rgba(0, 0, 0, 0.4);
            }
            
            /* Style st.navigation active link (Purple Gradient) */
            [data-testid="stSidebarNavItems"] a[aria-current="page"] {
                background: linear-gradient(90deg, #4F46E5, #9333EA) !important;
                border-radius: 8px !important;
                box-shadow: 0 4px 15px rgba(147, 51, 234, 0.3) !important;
            }
            
            /* Make text white on active link */
            [data-testid="stSidebarNavItems"] a[aria-current="page"] span {
                color: #FFFFFF !important;
                font-weight: 600 !important;
            }
            
            /* Style inactive links */
            [data-testid="stSidebarNavItems"] a {
                border-radius: 8px !important;
                margin: 0.2rem 0.5rem !important;
                padding: 0.6rem 0.5rem !important;
                transition: all 0.3s ease !important;
            }
            
            [data-testid="stSidebarNavItems"] a:hover {
                background-color: rgba(255, 255, 255, 0.05) !important;
                transform: translateX(3px);
            }
            
            [data-testid="stSidebarNavItems"] span {
                color: #94A3B8 !important;
                font-size: 0.95rem !important;
                font-weight: 500;
            }
            
            /* Subtitles / Headers */
            [data-testid="stMarkdownContainer"] p, 
            [data-testid="stMarkdownContainer"] li {
                color: #E2E8F0;
                line-height: 1.6;
            }
            
            .hero-subtitle {
                color: #94A3B8 !important;
                font-weight: 400;
                line-height: 1.6;
                margin-bottom: 2rem;
            }
            
            /* Metrics Cards */
            [data-testid="stMetric"] {
                background-color: #0F1626; 
                padding: 20px;
                border-radius: 12px;
                border: 1px solid #1A2235;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
                transition: all 0.3s ease;
            }
            
            [data-testid="stMetric"]:hover {
                transform: translateY(-4px);
                border-color: #4F46E5;
                box-shadow: 0 10px 15px -3px rgba(79, 70, 229, 0.2);
            }
            
            div[data-testid="stMetricValue"] {
                color: #FFFFFF;
                font-size: 3rem !important;
                font-weight: 700;
            }
            div[data-testid="stMetricLabel"] {
                color: #94A3B8;
                font-weight: 600;
                font-size: 1.6rem !important;
            }
            div[data-testid="stMetricDelta"] {
                font-weight: 600;
                font-size: 1.2rem !important;
            }
            
            /* Custom Buttons */
            .stButton > button {
                background-color: #4F46E5;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-weight: 600;
                font-size: 1.4rem !important;
                transition: all 0.2s ease;
                box-shadow: 0 4px 6px -1px rgba(79, 70, 229, 0.2);
            }
            .stButton > button:hover {
                background-color: #4338CA;
                color: white;
                transform: translateY(-2px);
                box-shadow: 0 6px 10px -1px rgba(79, 70, 229, 0.4);
            }
            
            /* General App Layout */
            .main .block-container {
                max-width: 1400px !important;
                padding-top: 1rem !important;
                padding-bottom: 1rem !important;
            }
            
            h1, h2, h3 {
                font-family: 'Inter', sans-serif;
            }
            .accent-text {
                color: #818CF8 !important;
            }
        </style>
    """, unsafe_allow_html=True)