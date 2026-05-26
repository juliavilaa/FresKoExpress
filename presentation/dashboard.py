import streamlit as st
import requests
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="FresKoExpress MVP", layout="wide", initial_sidebar_state="collapsed")

API_URL = "http://127.0.0.1:8000"

# --- 2. SESSION MANAGEMENT (SIMULATED AUTH SERVICE) ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    # LOGIN SCREEN
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.5, 1])
    
    with col2:
        st.markdown("""
            <div style="text-align: center; margin-bottom: 20px;">
                <h1 style="color: #047857; margin-bottom: 0;">FresKoExpress</h1>
                <p style="color: #64748B; font-size: 1.2rem;">Logistics Management Platform</p>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            st.markdown("**Administrative Access**")
            usuario = st.text_input("Username", placeholder="Username")
            password = st.text_input("Password", type="password", placeholder="password")
            submit = st.form_submit_button("Login")
            
            if submit:
                # Real authentication against FastAPI Auth Service
                auth_payload = {"username": usuario, "password": password}
                auth_res = requests.post(f"{API_URL}/token", data=auth_payload)
                
                if auth_res.status_code == 200:
                    st.session_state.logged_in = True
                    st.session_state.token = auth_res.json().get("access_token")
                    st.rerun()
                else:
                    st.error("Invalid credentials. Please try again.")

else:
    # --- 3. MAIN DASHBOARD ---
    
    # Logout button in the sidebar
    with st.sidebar:
        st.markdown("""
            <div style='text-align: center; padding: 10px 0; background-color: #064E3B; border-radius: 10px; margin-bottom: 20px;'>
                <h1 style='color: #34D399; margin:0; font-size: 2.2rem; font-weight: 900;'>🛒 FresKo</h1>
                <p style='color: #A7F3D0; margin:0; font-size: 0.9rem; letter-spacing: 2px;'>EXPRESS LOGISTICS</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 👨‍💻 Profile")
        st.markdown("**User:** Administrator")
        st.markdown("**Role:** Operations")
        st.divider()
        st.markdown("### 🔔 Live System Events")
        try:
            notif_res = requests.get(f"{API_URL}/api/notifications")
            if notif_res.status_code == 200:
                events = notif_res.json()
                if not events:
                    st.info("No recent events.")
                for ev in events:
                    st.toast(f"{ev['event']}: {ev['details']['product']}", icon="🔔") # Toast flotante
                    st.markdown(f"**{ev['time']}** - {ev['event']}<br><small>{ev['details']}</small>", unsafe_allow_html=True)
                    st.divider()
        except Exception:
            st.error("Event bus offline.")
    

    # Custom CSS for headers
    
    st.markdown("""
        <style>
            /* Fondo sutil con puntitos tipo blueprint */
            .stApp {
                background-color: #F8FAFC;
                background-image: radial-gradient(#CBD5E1 1px, transparent 1px);
                background-size: 24px 24px;
            }
            
            /* Títulos principales */
            .main-header { 
                font-size: 2.5rem; 
                color: #0F172A; 
                font-weight: 900; 
                margin-bottom: 0rem; 
                text-transform: uppercase;
                letter-spacing: -1px;
            }
            .section-header { 
                color: #047857; 
                font-weight: 700; 
                font-size: 1.4rem; 
                border-bottom: 3px solid #10B981; 
                padding-bottom: 0.5rem; 
                margin-bottom: 1.5rem; 
                margin-top: 2rem;
            }
            
            /* Darle estilo oscuro a la barra lateral (Sidebar) */
            [data-testid="stSidebar"] {
                background-color: #0F172A;
                border-right: 1px solid #1E293B;
            }
            [data-testid="stSidebar"] .css-17lntkn, [data-testid="stSidebar"] p, [data-testid="stSidebar"] div {
                color: #F8FAFC !important;
            }
            
            /* Estilizar los botones para que parezcan de una App nativa */
            .stButton > button {
                background-color: #10B981 !important;
                color: white !important;
                border-radius: 8px !important;
                border: none !important;
                font-weight: bold !important;
                padding: 0.5rem 1rem !important;
                transition: all 0.3s ease;
            }
            .stButton > button:hover {
                background-color: #059669 !important;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06) !important;
                transform: translateY(-2px);
            }
            
            /* Mejorar el formulario de inputs */
            .stTextInput>div>div>input, .stNumberInput>div>div>input, .stSelectbox>div>div>select {
                border-radius: 6px;
                border: 1px solid #CBD5E1;
            }
        </style>
    """, unsafe_allow_html=True)

    # 4. Fetch data from backend
    stock_data = []
    try:
        response = requests.get(f"{API_URL}/api/inventory/stock")
        if response.status_code == 200:
            stock_data = response.json()
    except Exception:
        pass

    # 5. KPI Cards Section
    df_stock = pd.DataFrame(stock_data) if stock_data else pd.DataFrame(columns=['quantity', 'expires_in_days'])
    total_lotes = len(df_stock)
    total_unidades = df_stock['quantity'].sum() if total_lotes > 0 else 0
    lotes_criticos = len(df_stock[df_stock['expires_in_days'] <= 3]) if total_lotes > 0 else 0

    # Color logic for the critical card
    color_alerta = "#DC2626" if lotes_criticos > 0 else "#047857" # Red if danger, green if ok
    texto_alerta = "ACTION REQUIRED" if lotes_criticos > 0 else "STABLE"

    # HTML for cards
    st.markdown(f"""
        <div style="display: flex; gap: 20px; margin-bottom: 20px;">
            <div style="flex: 1; background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); border-left: 5px solid #3B82F6;">
                <p style="color: #64748B; font-size: 14px; margin: 0; font-weight: 600;">Active Batches</p>
                <h2 style="color: #0F172A; margin: 0; font-size: 32px;">{total_lotes}</h2>
            </div>
            <div style="flex: 1; background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); border-left: 5px solid #8B5CF6;">
                <p style="color: #64748B; font-size: 14px; margin: 0; font-weight: 600;">Total Units</p>
                <h2 style="color: #0F172A; margin: 0; font-size: 32px;">{total_unidades}</h2>
            </div>
            <div style="flex: 1; background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); border-left: 5px solid {color_alerta};">
                <p style="color: #64748B; font-size: 14px; margin: 0; font-weight: 600;">At-Risk Batches (≤ 3 days)</p>
                <h2 style="color: {color_alerta}; margin: 0; font-size: 32px;">{lotes_criticos} <span style="font-size: 12px; vertical-align: middle; background-color: {color_alerta}20; padding: 3px 8px; border-radius: 10px;">{texto_alerta}</span></h2>
            </div>
        </div>
    """, unsafe_allow_html=True)


    # 6. Split screen for actions and visualization
    col1, col_space, col2 = st.columns([1, 0.1, 1.5])

    with col1:
        st.markdown('<div class="section-header">Inbound Registration</div>', unsafe_allow_html=True)
        with st.form("lote_form", clear_on_submit=True):
            nombre = st.text_input("Product Reference", placeholder="e.g., Gala Apples")
            categoria = st.selectbox("Category", ["Fruits", "Vegetables", "Dairy", "Meat"])
            cantidad = st.number_input("Volume (Units)", min_value=1, value=100)
            dias_vencimiento = st.number_input("Days to Expiration", min_value=1, value=7)
            
            if st.form_submit_button("Process Inbound", use_container_width=True):
                payload = {"product_name": nombre, "category": categoria, "quantity": cantidad, "days_to_expire": dias_vencimiento}
                headers = {"Authorization": f"Bearer {st.session_state.token}"}
                try:
                    res = requests.post(f"{API_URL}/api/inventory/batches", params=payload,headers=headers)
                    if res.status_code == 200:
                        st.success("Transaction recorded. Please refresh the view.")
                except Exception:
                    st.error("Backend communication error.")

    with col2:
        st.markdown('<div class="section-header">FEFO Traceability</div>', unsafe_allow_html=True)
        if stock_data:
            df_display = df_stock.rename(columns={"batch_id": "Batch ID", "product": "Product", "quantity": "Qty.", "expires_in_days": "Days Remaining"})
            st.dataframe(df_display, use_container_width=True, hide_index=True)
        else:
            st.info("No records in the system.")
            
        if st.button("Synchronize Data"):
            st.rerun()