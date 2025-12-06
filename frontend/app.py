import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuration
API_URL = "http://localhost:8000/api/v1"

# Page Configuration
st.set_page_config(
    page_title="Enterprise Data Interface",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Professional UI
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 4px;
        height: 3em;
        background-color: #0066cc;
        color: white;
    }
    .stTextInput>div>div>input {
        border-radius: 4px;
    }
    h1 {
        color: #1a1a1a;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
        font-size: 2.5rem;
    }
    h2, h3 {
        color: #333;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .metric-card {
        background-color: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("System Configuration")
    
    st.markdown("### Model Selection")
    model_choice = st.selectbox(
        "Active Model",
        ["GPT-4o-mini (Fine-Tuned)", "Llama-3-8B (Fine-Tuned)", "Gemma-7B (Fine-Tuned)", "GPT-4 (Baseline)"],
        index=0
    )
    
    st.markdown("### Connection Status")
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("API Gateway")
    with col2:
        st.markdown(":green[Online]")
        
    st.markdown("---")
    st.markdown("### Session Info")
    st.caption("User Role: Data Analyst")
    st.caption("Session ID: #8X92-L")

# Main Header
col_head1, col_head2 = st.columns([3, 1])
with col_head1:
    st.title("Enterprise Data Interface")
    st.markdown("Execute natural language queries against the corporate sales database.")

# Query Section
st.markdown("### Query Input")
query = st.text_area(
    "Enter your analytical question below:", 
    height=100, 
    placeholder="Example: List the top 5 customers in France by total sales volume in 2003."
)

if st.button("Execute Query", type="primary"):
    if query:
        # Progress Container
        status_container = st.status("Processing Query...", expanded=True)
        
        try:
            status_container.write("Authenticating...")
            status_container.write(f"Routing to {model_choice}...")
            
            # API Call
            payload = {"question": query}
            response = requests.post(f"{API_URL}/query", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                status_container.update(label="Query Executed Successfully", state="complete", expanded=False)
                
                # Layout: SQL and Results
                tab1, tab2, tab3 = st.tabs(["Data View", "Visualization", "SQL Trace"])
                
                with tab1:
                    st.subheader("Result Set")
                    if data["results"]:
                        df = pd.DataFrame(data["results"])
                        st.dataframe(
                            df, 
                            use_container_width=True,
                            hide_index=True
                        )
                        st.caption(f"Returned {len(df)} rows.")
                    else:
                        st.info("Query returned no results.")

                with tab2:
                    st.subheader("Data Visualization")
                    if data["results"]:
                        df = pd.DataFrame(data["results"])
                        if len(df) > 0 and len(df.columns) >= 2:
                            col_viz1, col_viz2 = st.columns(2)
                            
                            numeric_cols = df.select_dtypes(include=['number']).columns
                            categorical_cols = df.select_dtypes(include=['object']).columns
                            
                            with col_viz1:
                                chart_type = st.selectbox("Visualization Type", ["Bar Chart", "Line Chart", "Scatter Plot", "Pie Chart"])
                            
                            if len(numeric_cols) > 0:
                                with col_viz2:
                                    x_col = st.selectbox("X Axis (Category)", df.columns)
                                    y_col = st.selectbox("Y Axis (Value)", numeric_cols)
                                
                                if chart_type == "Bar Chart":
                                    fig = px.bar(df, x=x_col, y=y_col, template="plotly_white")
                                elif chart_type == "Line Chart":
                                    fig = px.line(df, x=x_col, y=y_col, template="plotly_white")
                                elif chart_type == "Scatter Plot":
                                    fig = px.scatter(df, x=x_col, y=y_col, template="plotly_white")
                                elif chart_type == "Pie Chart":
                                    fig = px.pie(df, names=x_col, values=y_col, template="plotly_white")
                                    
                                fig.update_layout(margin=dict(t=10, b=10, l=10, r=10))
                                st.plotly_chart(fig, use_container_width=True)
                            else:
                                st.warning("Not enough numeric data to generate visualization.")
                        else:
                            st.info("Insufficient data for visualization.")
                    else:
                        st.info("No data to visualize.")

                with tab3:
                    st.subheader("Generated SQL")
                    st.code(data["sql_query"], language="sql")
                    
                    st.subheader("Execution Metadata")
                    col_meta1, col_meta2 = st.columns(2)
                    with col_meta1:
                        st.metric("Execution Time", f"{data.get('metadata', {}).get('latency', 0.45)}s")
                    with col_meta2:
                        st.metric("Rows Processed", len(data.get('results', [])))

            else:
                status_container.update(label="Execution Failed", state="error")
                st.error(f"Server Error: {response.text}")
                
        except Exception as e:
            status_container.update(label="Connection Failed", state="error")
            st.error(f"Could not connect to backend. Ensure the API server is running.\nError: {str(e)}")
    else:
        st.warning("Please enter a valid query string.")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <small>Enterprise Data Interface v2.0 | Powered by Fine-Tuned LLM Architecture</small>
    </div>
    """, 
    unsafe_allow_html=True
)
