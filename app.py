import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from prophet import Prophet
import warnings
warnings.filterwarnings('ignore')
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from snowflake_utils import SnowflakeConnection  # Import our custom SnowflakeConnection class

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Cultural Tourism Dashboard - India",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.html("""
<style>
    .main-header {
        font-size: 3rem;
        color: #FF6B35;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #FF6B35, #F7931E);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    }
    .metric-card {
        background: #FFFFFF;
        padding: 1rem;
        border-radius: 10px;
        color: #2C2C2E;
        text-align: center;
        margin: 0.5rem 0;
    }
    .matric-card-h3 {
        font-size: 1rem;  
        margin-block: 0.4rem;
    }
    .matric-card-p {
        font-size: 1.5rem;  
        margin-block: 0.4rem;
    }
    .culture-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #FF6B35;
        margin: 0.5rem 0;
        height: 100%;
        display: flex;
        flex-direction: column;
    }
    .culture-card h4 {
        color: #FF6B35;
        margin-bottom: 1rem;
        font-size: 1.2rem;
    }
    .culture-card p {
        color: #2c3e50;
        margin: 0.5rem 0;
    }
    .culture-card strong {
        color: #34495e;
    }
    .culture-card ul {
        color: #2c3e50;
        padding-left: 1.2rem;
        margin: 0.5rem 0;
    }
    .culture-card li {
        margin: 0.5rem 0;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    /* Add styles for the columns to ensure equal height */
    [data-testid="column"] {
        display: flex;
        flex-direction: column;
    }
    [data-testid="column"] > div {
        flex: 1;
    }
</style>
""")

@st.cache_data
def load_data():
    """Load data from Snowflake database"""
    try:
        # Initialize Snowflake connection
        sf = SnowflakeConnection()
        if not sf.connect():
            st.error("Failed to connect to Snowflake database")
            return None
        
        # Load data with filters
        df = sf.load_cultural_data()
        
        if df is None or df.empty:
            st.error("No data retrieved from Snowflake")
            return None
            
        # Ensure date column is datetime and rename if needed
        if 'DATE' in df.columns:
            df['Date'] = pd.to_datetime(df['DATE'])
            df = df.drop('DATE', axis=1)
        elif 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])
        
        # Add derived columns if not present in Snowflake
        if 'MONTH' not in df.columns:
            df['MONTH'] = df['Date'].dt.month
        if 'YEAR' not in df.columns:
            df['YEAR'] = df['Date'].dt.year
        if 'QUARTER' not in df.columns:
            df['QUARTER'] = df['Date'].dt.quarter.apply(lambda x: f'Q{x}')
        if 'REGION' not in df.columns:
            df['REGION'] = df['STATE'].apply(get_region)
        
        # Close Snowflake connection
        sf.disconnect()
        
        return df
        
    except Exception as e:
        st.error(f"Error loading data from Snowflake: {str(e)}")
        return None

def get_region(state):
    """Map states to regions"""
    regions = {
        'North': ['Punjab', 'Himachal Pradesh', 'Uttar Pradesh'],
        'South': ['Kerala', 'Karnataka', 'Tamil Nadu'],
        'West': ['Rajasthan', 'Gujarat', 'Maharashtra', 'Goa'],
        'East': ['West Bengal', 'Odisha', 'Assam'],
        'Northeast': ['Meghalaya', 'Manipur']
    }
    
    for region, states in regions.items():
        if state in states:
            return region
    return 'Other'

@st.cache_data
def prepare_forecast_data(df, state=None, event=None):
    """Prepare data for Prophet forecasting"""
    # Filter data if specified
    forecast_df = df.copy()
    if state and state != 'All':
        forecast_df = forecast_df[forecast_df['STATE'] == state]
    if event and event != 'All':
        forecast_df = forecast_df[forecast_df['EVENT'] == event]
    
    # Aggregate by date
    daily_visitors = forecast_df.groupby('Date')['VISITORS'].sum().reset_index()
    daily_visitors.columns = ['ds', 'y']
    
    return daily_visitors

def create_forecast(df, periods=365):
    """Create Prophet forecast"""
    try:
        model = Prophet(
            yearly_seasonality=True,
            weekly_seasonality=True,
            daily_seasonality=False,
            changepoint_prior_scale=0.05
        )
        
        # Add custom seasonalities
        model.add_seasonality(name='monthly', period=30.5, fourier_order=5)
        
        model.fit(df)
        
        # Create future dataframe
        future = model.make_future_dataframe(periods=periods)
        forecast = model.predict(future)
        
        return model, forecast
    except Exception as e:
        st.error(f"Error creating forecast: {str(e)}")
        return None, None

def main():
    # Header
    st.html('<h1 class="main-header">🏛️ Cultural Tourism Dashboard - India</h1>')
    
    # Load data
    with st.spinner('Loading cultural tourism data from Snowflake...'):
        df = load_data()
        
    if df is None:
        st.error("""
        Failed to load data from Snowflake. Please check:
        1. Your Snowflake credentials in .env file
        2. Network connectivity
        3. Database and table permissions
        """)
        return
    
    # Sidebar
    st.sidebar.image("https://upload.wikimedia.org/wikipedia/en/4/41/Flag_of_India.svg", width=100)
    st.sidebar.markdown("## 🎭 Cultural Tourism Analytics")
    
    # Filters
    selected_state = st.sidebar.selectbox(
        "Select State",
        ['All'] + sorted(df['STATE'].unique().tolist())
    )
    
    selected_event = st.sidebar.selectbox(
        "Select Event Type",
        ['All'] + sorted(df['EVENT'].unique().tolist())
    )
    
    selected_year = st.sidebar.selectbox(
        "Select Year",
        ['All'] + sorted(df['YEAR'].unique().tolist())
    )
    
    # Filter data
    filtered_df = df.copy()
    if selected_state != 'All':
        filtered_df = filtered_df[filtered_df['STATE'] == selected_state]
    if selected_event != 'All':
        filtered_df = filtered_df[filtered_df['EVENT'] == selected_event]
    if selected_year != 'All':
        filtered_df = filtered_df[filtered_df['YEAR'] == selected_year]
    
    if filtered_df.empty:
        st.warning("No data available for the selected filters. Please try different filter combinations.")
        return
    
    # Main dashboard
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_visitors = filtered_df['VISITORS'].sum()
        st.html(f"""
        <div class="metric-card">
            <h3 class="matric-card-h3">👥 Total Visitors</h3>
            <p class="matric-card-p">{total_visitors:,}</p>
        </div>
        """)
    
    with col2:
        total_events = len(filtered_df)
        st.html(f"""
        <div class="metric-card">
            <h3 class="matric-card-h3">🎪 Total Events</h3>
            <p class="matric-card-p">{total_events:,}</p>
        </div>
        """)
    
    with col3:
        total_revenue = filtered_df['REVENUE_INR'].sum()
        st.html(f"""
        <div class="metric-card">
            <h3 class="matric-card-h3">💰 Revenue (₹)</h3>
            <p class="matric-card-p">{total_revenue/1000000:.1f}M</p>
        </div>
        """)
    
    with col4:
        employment = filtered_df['LOCAL_EMPLOYMENT'].sum()
        st.html(f"""
        <div class="metric-card">
            <h3 class="matric-card-h3">👷 Employment</h3>
            <p class="matric-card-p">{employment:,}</p>
        </div>
        """)
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Overview", "📅 Cultural Calendar", "🔮 Forecasting", "🗺️ Regional Analysis", "📈 Insights"])
    
    with tab1:
        st.subheader("Tourism Trends Overview")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Monthly visitors trend
            monthly_data = filtered_df.groupby(['YEAR', 'MONTH'])['VISITORS'].sum().reset_index()
            monthly_data['Date'] = pd.to_datetime(monthly_data[['YEAR', 'MONTH']].assign(day=1))
            
            fig = px.line(monthly_data, x='Date', y='VISITORS', 
                         title='Monthly Visitor Trends',
                         color_discrete_sequence=['#FF6B35'])
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Top events by visitors
            event_stats = filtered_df.groupby('EVENT')['VISITORS'].sum().sort_values(ascending=False).head(10)
            
            fig = px.bar(x=event_stats.values, y=event_stats.index, 
                        orientation='h',
                        title='Top Events by Visitors',
                        color_discrete_sequence=['#F7931E'])
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # State-wise analysis
        st.subheader("State-wise Cultural Tourism")
        state_stats = filtered_df.groupby('STATE').agg({
            'VISITORS': 'sum',
            'REVENUE_INR': 'sum',
            'LOCAL_EMPLOYMENT': 'sum',
            'EVENT': 'count'
        }).round(2)
        state_stats.columns = ['Total Visitors', 'Revenue (₹)', 'Employment', 'Total Events']
        st.dataframe(state_stats.sort_values('Total Visitors', ascending=False), use_container_width=True)
    
    with tab2:
        st.subheader("Cultural Calendar & Seasonality")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Seasonal patterns
            seasonal_data = filtered_df.groupby('MONTH')['VISITORS'].mean().reset_index()
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                     'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            seasonal_data['Month_Name'] = [months[i-1] for i in seasonal_data['MONTH']]
            
            fig = px.bar(seasonal_data, x='Month_Name', y='VISITORS',
                        title='Average Visitors by Month',
                        color='VISITORS',
                        color_continuous_scale='Oranges')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Weekly patterns
            filtered_df['Weekday'] = filtered_df['Date'].dt.day_name()
            weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            weekly_data = filtered_df.groupby('Weekday')['VISITORS'].mean().reindex(weekday_order)
            
            fig = px.bar(x=weekly_data.index, y=weekly_data.values,
                        title='Average Visitors by Day of Week',
                        color_discrete_sequence=['#764ba2'])
            st.plotly_chart(fig, use_container_width=True)
        
        # Cultural event calendar heatmap
        st.subheader("Event Calendar Heatmap")
        
        # Create a more detailed calendar view
        filtered_df['Day'] = filtered_df['Date'].dt.day
        heatmap_data = filtered_df.groupby(['MONTH', 'Day'])['VISITORS'].sum().reset_index()
        heatmap_pivot = heatmap_data.pivot(index='MONTH', columns='Day', values='VISITORS').fillna(0)
        
        fig = px.imshow(heatmap_pivot, 
                       title="Cultural Tourism Intensity Calendar",
                       color_continuous_scale='Oranges',
                       aspect='auto')
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("Tourism Forecasting with Prophet")
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            forecast_state = st.selectbox("Forecast State", ['All'] + sorted(df['STATE'].unique().tolist()), key='forecast_state')
            forecast_event = st.selectbox("Forecast Event", ['All'] + sorted(df['EVENT'].unique().tolist()), key='forecast_event')
            forecast_days = st.slider("Forecast Days", 30, 365, 180)
        
        with col2:
            with st.spinner('Generating forecast...'):
                forecast_data = prepare_forecast_data(df, forecast_state, forecast_event)
                
                if len(forecast_data) > 30:  # Minimum data points for forecasting
                    model, forecast = create_forecast(forecast_data, forecast_days)
                    
                    if model and forecast is not None:
                        # Plot forecast
                        fig = go.Figure()
                        
                        # Historical data
                        fig.add_trace(go.Scatter(
                            x=forecast_data['ds'],
                            y=forecast_data['y'],
                            mode='markers',
                            name='Historical',
                            marker=dict(color='#FF6B35', size=4)
                        ))
                        
                        # Forecast
                        future_data = forecast[forecast['ds'] > forecast_data['ds'].max()]
                        fig.add_trace(go.Scatter(
                            x=future_data['ds'],
                            y=future_data['yhat'],
                            mode='lines',
                            name='Forecast',
                            line=dict(color='#F7931E', width=2)
                        ))
                        
                        # Confidence intervals
                        fig.add_trace(go.Scatter(
                            x=future_data['ds'],
                            y=future_data['yhat_upper'],
                            fill=None,
                            mode='lines',
                            line_color='rgba(0,0,0,0)',
                            showlegend=False
                        ))
                        
                        fig.add_trace(go.Scatter(
                            x=future_data['ds'],
                            y=future_data['yhat_lower'],
                            fill='tonexty',
                            mode='lines',
                            line_color='rgba(0,0,0,0)',
                            name='Confidence Interval',
                            fillcolor='rgba(247, 147, 30, 0.2)'
                        ))
                        
                        fig.update_layout(
                            title=f'Tourism Forecast - {forecast_state} - {forecast_event}',
                            xaxis_title='Date',
                            yaxis_title='Visitors',
                            height=500
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Forecast summary
                        future_sum = future_data['yhat'].sum()
                        avg_daily = future_sum / len(future_data)
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Predicted Total Visitors", f"{future_sum:,.0f}")
                        with col2:
                            st.metric("Average Daily Visitors", f"{avg_daily:,.0f}")
                        with col3:
                            growth_rate = ((future_data['yhat'].iloc[-1] - forecast_data['y'].iloc[-1]) / forecast_data['y'].iloc[-1]) * 100
                            st.metric("Growth Rate", f"{growth_rate:.1f}%")
                    
                else:
                    st.warning("Not enough data for forecasting. Please select different filters.")
    
    with tab4:
        st.subheader("Regional Cultural Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Regional distribution
            regional_data = filtered_df.groupby('REGION')['VISITORS'].sum().reset_index()
            
            fig = px.pie(regional_data, values='VISITORS', names='REGION',
                        title='Visitors by Region',
                        color_discrete_sequence=px.colors.qualitative.Set3)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Art forms popularity
            art_data = filtered_df.groupby('ART_FORM')['VISITORS'].sum().sort_values(ascending=False).head(8)
            
            fig = px.bar(x=art_data.index, y=art_data.values,
                        title='Popular Art Forms',
                        color_discrete_sequence=['#667eea'])
            fig.update_layout(xaxis_tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
        
        # Regional insights
        st.subheader("Regional Tourism Insights")
        
        regional_insights = filtered_df.groupby('REGION').agg({
            'VISITORS': ['sum', 'mean'],
            'REVENUE_INR': 'sum',
            'LOCAL_EMPLOYMENT': 'sum',
            'TOURISM_LEVEL': lambda x: (x == 'High').sum()
        }).round(2)
        
        regional_insights.columns = ['Total Visitors', 'Avg Visitors/Event', 'Total Revenue', 'Employment', 'High Tourism Events']
        st.dataframe(regional_insights, use_container_width=True)
    
    with tab5:
        st.subheader("Cultural Tourism Insights & Recommendations")
        
        # Key insights
        st.markdown("### 🔍 Key Insights")
        
        # Calculate insights
        peak_month = filtered_df.groupby('MONTH')['VISITORS'].sum().idxmax()
        peak_state = filtered_df.groupby('STATE')['VISITORS'].sum().idxmax()
        peak_event = filtered_df.groupby('EVENT')['VISITORS'].sum().idxmax()
        
        underperforming = filtered_df[filtered_df['TOURISM_LEVEL'] == 'Low']
        underperforming_states = underperforming['STATE'].value_counts().head(3)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.html(f"""
            <div class="culture-card">
                <h4>🏆 Peak Tourism</h4>
                <p><strong>Month:</strong> {calendar.month_name[peak_month]}</p>
                <p><strong>State:</strong> {peak_state}</p>
                <p><strong>Event:</strong> {peak_event}</p>
            </div>
            """)
        
        with col2:
            st.html(f"""
            <div class="culture-card">
                <h4>📊 Tourism Distribution</h4>
                <p><strong>High Tourism Events:</strong> {len(filtered_df[filtered_df['TOURISM_LEVEL'] == 'High'])}</p>
                <p><strong>Medium Tourism Events:</strong> {len(filtered_df[filtered_df['TOURISM_LEVEL'] == 'Medium'])}</p>
                <p><strong>Low Tourism Events:</strong> {len(filtered_df[filtered_df['TOURISM_LEVEL'] == 'Low'])}</p>
            </div>
            """)
        
        # ''' Will be used if required '''
        # with col2:
        #     st.markdown("""
        #     <div class="culture-card">
        #         <h4>💡 Recommendations</h4>
        #         <ul>
        #             <li>Focus marketing efforts during off-peak months</li>
        #             <li>Promote lesser-known cultural events</li>
        #             <li>Develop cultural tourism packages</li>
        #             <li>Invest in infrastructure for high-potential regions</li>
        #             <li>Create cultural exchange programs</li>
        #         </ul>
        #     </div>
        #     """, unsafe_allow_html=True)
            
        #     st.markdown(f"""
        #     <div class="culture-card">
        #         <h4>🎯 Focus Areas</h4>
        #         <p>States with untapped potential:</p>
        #         <ul>
        #             {"".join([f"<li>{state} ({count} low-tourism events)</li>" for state, count in underperforming_states.head(3).items()])}
        #         </ul>
        #     </div>
        #     """, unsafe_allow_html=True)
        
        # Economic impact
        st.markdown("### 💰 Economic Impact Analysis")
        
        economic_data = filtered_df.groupby('STATE').agg({
            'REVENUE_INR': 'sum',
            'LOCAL_EMPLOYMENT': 'sum',
            'VISITORS': 'sum'
        }).reset_index()
        
        economic_data['Revenue_per_Visitor'] = economic_data['REVENUE_INR'] / economic_data['VISITORS']
        economic_data['Employment_per_1000_Visitors'] = (economic_data['LOCAL_EMPLOYMENT'] / economic_data['VISITORS']) * 1000
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.scatter(economic_data, x='VISITORS', y='REVENUE_INR', 
                           size='LOCAL_EMPLOYMENT', hover_name='STATE',
                           title='Economic Impact by State',
                           color_discrete_sequence=['#FF6B35'])
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(economic_data.nlargest(10, 'Revenue_per_Visitor'), 
                        x='STATE', y='Revenue_per_Visitor',
                        title='Revenue per Visitor by State',
                        color_discrete_sequence=['#F7931E'])
            fig.update_layout(xaxis_tickangle=45)
            st.plotly_chart(fig, use_container_width=True)

    # Footer
    st.markdown("---")
    st.html("""
    <div style='text-align: center; color: #666;'>
        <p>🏛️ Cultural Tourism Dashboard | Promoting India's Rich Heritage | Data-Driven Tourism Insights</p>
        <p>Built with Streamlit • Prophet • Plotly</p>
    </div>
    """)

if __name__ == "__main__":
    import calendar
    main()