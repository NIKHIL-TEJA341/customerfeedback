import streamlit as st

def load_css():
    """Injects premium dark theme CSS overrides into the Streamlit app."""
    st.markdown("""
        <style>

            [data-testid="stSidebar"] > div {
                display: flex;
                flex-direction: column;
            }
            
            [data-testid="stSidebarUserContent"] {
                order: -1 !important;
                padding-bottom: 0 !important;
                margin-bottom: 0 !important;
            }
            [data-testid="stSidebarUserContent"] .element-container {
                margin-bottom: 0 !important;
            }
            [data-testid="stSidebarUserContent"] [data-testid="stMarkdownContainer"] {
                margin-bottom: 0 !important;
                padding-bottom: 0 !important;
            }
            [data-testid="stSidebarNav"] {
                margin-top: 0 !important;
                padding-top: 0 !important;
            }
            
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
                margin-left: 0.5rem;
                margin-right: 0.5rem;
            }

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
            
            [data-testid="stSidebar"] {
                background-color: #0B1120 !important; /* Slightly lighter card-style background */
                border-right: 1px solid #1A2235 !important;
            }
            
            [data-testid="stSidebarNav"] {
                width: 100% !important;
            }
            [data-testid="stSidebarNav"] ul {
                padding-top: 0.5rem;
                padding-left: 0 !important;
                padding-right: 0 !important;
                width: 100% !important;
            }
            [data-testid="stSidebarNav"] li {
                width: 100% !important;
                display: block !important;
            }
            [data-testid="stSidebarNav"] a svg {
                display: none !important; /* Hide default streamlit page icon */
            }
            [data-testid="stSidebarNav"] a {
                background-color: transparent !important; /* Invisible by default */
                margin: 0.2rem 0.5rem !important; 
                padding: 0.6rem 0.5rem !important; 
                border-radius: 8px;
                border: none; /* No border for a cleaner look */
                transition: all 0.3s ease;
                display: flex;
                align-items: center;
                width: calc(100% - 1rem) !important; /* Force full width minus margins */
                box-sizing: border-box !important;
            }
            [data-testid="stSidebarNav"] a:hover {
                /* The beautiful purple/blue gradient from the image */
                background: linear-gradient(90deg, #4F46E5, #9333EA) !important;
                transform: translateX(5px);
                box-shadow: 0 4px 15px rgba(147, 51, 234, 0.3);
            }
            [data-testid="stSidebarNav"] a span {
                color: #94A3B8 !important; /* Light grey text by default */
                font-weight: 500;
                font-size: 0.9rem !important; /* Reduced for better sidebar proportions */
                transition: color 0.3s ease;
                display: flex;
                align-items: center;
                white-space: normal !important; /* Allow wrapping if needed */
                overflow: visible !important;
                text-overflow: clip !important;
                width: 100% !important; /* Ensure it takes full width to prevent premature wrap */
            }
            [data-testid="stSidebarNav"] a span * {
                white-space: normal !important;
                overflow: visible !important;
                text-overflow: clip !important;
                width: 100% !important;
            }
            [data-testid="stSidebarNav"] a:hover span, 
            [data-testid="stSidebarNav"] a[aria-current="page"] span {
                color: #FFFFFF !important; /* White text on hover */
                font-weight: 600;
            }
            [data-testid="stSidebarNav"] a[aria-current="page"] {
                background: linear-gradient(90deg, #4F46E5, #9333EA) !important;
                box-shadow: 0 4px 15px rgba(147, 51, 234, 0.3);
                border-radius: 8px;
            }

            [data-testid="stSidebarNav"] a span::before {
                content: '';
                display: inline-block;
                width: 24px !important;
                height: 24px !important;
                min-width: 24px !important;
                min-height: 24px !important;
                flex-shrink: 0 !important;
                margin-right: 12px;
                background-color: #94A3B8;
                -webkit-mask-size: contain;
                mask-size: contain;
                -webkit-mask-repeat: no-repeat;
                mask-repeat: no-repeat;
                -webkit-mask-position: center;
                mask-position: center;
                transition: background-color 0.3s ease;
            }
            [data-testid="stSidebarNav"] a:hover span::before,
            [data-testid="stSidebarNav"] a[aria-current="page"] span::before {
                background-color: #FFFFFF;
            }

            [data-testid="stSidebarNav"] ul li:nth-child(1) a span::before { -webkit-mask-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/></svg>'); }
            [data-testid="stSidebarNav"] ul li:nth-child(2) a span::before { -webkit-mask-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M3 3h8v8H3V3zm0 10h8v8H3v-8zm10-10h8v8h-8V3zm0 10h8v8h-8v-8z"/></svg>'); }
            
            [data-testid="stSidebarNav"] ul li:nth-child(3) a span::before { -webkit-mask-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zM6 9h12v2H6V9zm8 5H6v-2h8v2zm4-6H6V6h12v2z"/></svg>'); }
          
            [data-testid="stSidebarNav"] ul li:nth-child(4) a span::before { -webkit-mask-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M11.99 18.54l-7.37-5.73L3 14.07l9 7 9-7-1.63-1.27-7.38 5.74zM12 16l7.36-5.73L21 9l-9-7-9 7 1.63 1.27L12 16z"/></svg>'); }
            
            [data-testid="stSidebarNav"] ul li:nth-child(5) a span::before { -webkit-mask-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M13 3c-4.97 0-9 4.03-9 9H1l3.89 3.89.07.14L9 12H6c0-3.87 3.13-7 7-7s7 3.13 7 7-3.13 7-7 7c-1.93 0-3.68-.79-4.94-2.06l-1.42 1.42C8.27 19.99 10.51 21 13 21c4.97 0 9-4.03 9-9s-4.03-9-9-9zm-1 5v5l4.25 2.52.75-1.23-3.5-2.07V8h-1.5z"/></svg>'); }
            
            [data-testid="stSidebarNav"] ul li:nth-child(6) a span::before { -webkit-mask-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M11 2v20c-5.07-.5-9-4.79-9-10s3.93-9.5 9-10zm2.03 0v8.99H22c-.47-4.74-4.24-8.52-8.97-8.99zm0 11.01V22c4.74-.47 8.5-4.25 8.97-8.99h-8.97z"/></svg>'); }
           
            [data-testid="stSidebarNav"] ul li:nth-child(7) a span::before { -webkit-mask-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M16 6l2.29 2.29-4.88 4.88-4-4L2 16.59 3.41 18l6-6 4 4 6.3-6.29L22 12V6z"/></svg>'); }
            
            [data-testid="stSidebarNav"] ul li:nth-child(8) a span::before { -webkit-mask-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M19 3h-1V1h-2v2h-1c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h4c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16h-4V5h4v14zm-6.5-2h-2L9 10H7L5.5 17h-2l2.5-8h2z"/></svg>'); }
            
            [data-testid="stSidebarNav"] ul li:nth-child(9) a span::before { -webkit-mask-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M19.35 10.04C18.67 6.59 15.64 4 12 4 9.11 4 6.6 5.64 5.36 8.04 2.34 8.36 0 10.91 0 14c0 3.31 2.69 6 6 6h13c2.76 0 5-2.24 5-5 0-2.64-2.05-4.78-4.65-4.96z"/></svg>'); }
          
            [data-testid="stSidebarNav"] ul li:nth-child(10) a span::before { -webkit-mask-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/></svg>'); }
            
            [data-testid="stSidebarNav"] ul li:nth-child(11) a span::before { -webkit-mask-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/></svg>'); }
            
            
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
            
            [data-testid="stAlert"] {
                transition: all 0.3s ease;
                border: 1px solid transparent;
            }
            [data-testid="stAlert"]:hover {
                transform: translateY(-2px);
                border-color: #818CF8;
                box-shadow: 0 8px 12px -3px rgba(0, 0, 0, 0.3);
            }
            
            div[data-testid="stMetricValue"] {
                color: #FFFFFF;
                font-size: 3rem !important; /* Scaled up to be bigger than 1.6rem labels */
                font-weight: 700;
            }
            div[data-testid="stMetricLabel"] {
                color: #94A3B8;
                font-weight: 600;
                font-size: 1.6rem !important; /* Scaled to match decipher text */
            }
            div[data-testid="stMetricDelta"] {
                font-weight: 600;
                font-size: 1.2rem !important;
            }
            
            .stButton > button {
                background-color: #4F46E5;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-weight: 600;
                font-size: 1.4rem !important; /* Scaled up button text */
                transition: all 0.2s ease;
                box-shadow: 0 4px 6px -1px rgba(79, 70, 229, 0.2);
            }
            .stButton > button:hover {
                background-color: #4338CA;
                color: white;
                transform: translateY(-2px);
                box-shadow: 0 6px 10px -1px rgba(79, 70, 229, 0.4);
            }
            
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

    st.sidebar.markdown("""
        <!-- Top Logo -->
        <div class="top-sidebar-logo">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#A855F7" width="40" height="40" style="margin-right: 12px; flex-shrink: 0;">
                <path d="M12 2L14.26 8.74L21 11L14.26 13.26L12 20L9.74 13.26L3 11L9.74 8.74L12 2Z"/>
            </svg>
            <div style="overflow: hidden;">
                <div style="font-weight: 800; font-size: 1.8rem; color: #F8FAFC; letter-spacing: 0px; line-height: 1.1; white-space: nowrap; text-overflow: ellipsis;">Sentix AI</div>
                <div style="font-size: 0.85rem; color: #94A3B8; font-weight: 600; letter-spacing: 0px; white-space: nowrap; text-overflow: ellipsis;">Customer Sentiment</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
