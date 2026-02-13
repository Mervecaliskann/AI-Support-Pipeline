"""
AI SUPPORT SYSTEM - BUSINESS INTELLIGENCE DASHBOARD
Description: A real-time monitoring interface built with Streamlit and Plotly. 
             It fetches data directly from PostgreSQL to visualize support trends, 
             departmental ticket distribution, and critical priority alerts.
Features: Real-time SQL fetching, Data Visualization, Priority Alerting.
"""

import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
from dotenv import load_dotenv
import os

load_dotenv()

# Page configuration
st.set_page_config(page_title="AI Support Analytics", layout="wide")

# Database connection
engine = create_engine(os.getenv("DB_URL"))

def get_data():
    query = """
    SELECT t.*, u.full_name, u.email 
    FROM support_tickets t
    JOIN users u ON t.user_id = u.user_id
    ORDER BY t.created_at DESC
    """
    return pd.read_sql(query, engine)

st.title("🚀 AI Support Dashboard")
st.markdown("Real-time AI-Powered Ticket Analysis System")

# Fetch data
df = get_data()

# --- CRITICAL ALERT SYSTEM ---
if not df.empty:
    critical_tickets = df[df['priority'] == 5]
    if not critical_tickets.empty:
        st.error(f"🚨 ALERT: {len(critical_tickets)} CRITICAL (P5) ticket(s) require immediate attention!", icon="⚠️")
        with st.expander("View Critical Tickets"):
            st.dataframe(critical_tickets[['created_at', 'full_name', 'message_text']], use_container_width=True)

if not df.empty:
    # Top Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Tickets", len(df))
    col2.metric("Critical (P5) Issues", len(df[df['priority'] == 5]))
    
    # Calculate negative sentiment rate
    neg_rate = round(len(df[df['sentiment'] == 'Negative']) / len(df) * 100)
    col3.metric("Negative Sentiment Rate", f"{neg_rate}%")

    st.divider()

    # Visualizations
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("Ticket Distribution by Category")
        fig_cat = px.pie(df, names='category', hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_cat, use_container_width=True)

    with c2:
        st.subheader("Priority Level Breakdown")
        fig_prio = px.bar(df, x='priority', color='priority', 
                          labels={'priority': 'Priority Level', 'count': 'Ticket Count'},
                          color_continuous_scale='Reds')
        st.plotly_chart(fig_prio, use_container_width=True)

    st.divider()

    # Detailed Data Table
    st.subheader("📋 Support Ticket Logs")
    # Mapping for display
    display_df = df[['created_at', 'full_name', 'category', 'sentiment', 'priority', 'message_text']].copy()
    display_df.columns = ['Date', 'Customer', 'Category', 'Sentiment', 'Priority', 'Message']
    st.dataframe(display_df, use_container_width=True)
else:
    st.warning("No tickets found in the database. Please send data via FastAPI.")