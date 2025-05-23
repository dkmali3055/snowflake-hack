# 🏛️ Cultural Tourism Dashboard - India

An interactive web application built with Streamlit that showcases India's traditional art forms, cultural experiences, and promotes responsible tourism through data-driven insights and forecasting.

## 🎯 Project Overview

This dashboard provides comprehensive analysis of cultural tourism in India, featuring:

- **Cultural Calendar**: Interactive mapping of festivals, fairs, and traditional art events
- **Tourism Forecasting**: Prophet-based forecasting for tourism planning
- **Regional Analysis**: State-wise and region-wise cultural tourism insights
- **Seasonality Analysis**: Understanding tourism patterns and trends
- **Economic Impact**: Revenue and employment generation analysis

## 🚀 Features

### 📊 Dashboard Components

1. **Overview Tab**
   - Key performance metrics (visitors, events, revenue, employment)
   - Monthly visitor trends
   - Top events by visitor count
   - State-wise performance analysis

2. **Cultural Calendar Tab**
   - Seasonal tourism patterns
   - Weekly visitor distribution
   - Event calendar heatmap
   - Festival timing optimization

3. **Forecasting Tab**
   - Prophet-based time series forecasting
   - Customizable forecast periods (30-365 days)
   - Confidence intervals
   - Growth rate predictions

4. **Regional Analysis Tab**
   - Regional tourism distribution
   - Popular art forms analysis
   - Regional insights and comparisons
   - Economic impact by region

5. **Insights & Recommendations Tab**
   - Key tourism insights
   - Economic impact analysis
   - Actionable recommendations
   - Focus areas for development

### 🎨 Interactive Features

- **Dynamic Filtering**: Filter by state, event type, and year
- **Real-time Updates**: Responsive charts and metrics
- **Export Capabilities**: Download insights and forecasts
- **Mobile Responsive**: Optimized for all devices

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly, Altair
- **Forecasting**: Prophet (Facebook's time series forecasting tool)
- **Database**: Snowflake (optional)
- **Environment**: Python 3.8+

## 📁 Project Structure

```
cultural-tourism-app/
├── app.py                 # Main Streamlit application
├── data/
│   └── dummy_data.csv     # Sample cultural tourism data
├── .env                   # Environment configuration
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
└── utils/
    ├── data_loader.py    # Data loading utilities
    ├── forecasting.py    # Prophet forecasting functions
    └── visualizations.py # Custom visualization functions
```

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/cultural-tourism-app.git
cd cultural-tourism-app
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Copy the `.env.example` file to `.env` and update with your configurations:

```bash
cp .env.example .env
```

Edit the `.env` file with your Snowflake credentials (if using Snowflake):

```env
SNOWFLAKE_ACCOUNT=your_account_identifier
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_WAREHOUSE=your_warehouse
SNOWFLAKE_DATABASE=CULTURAL_TOURISM_DB
SNOWFLAKE_SCHEMA=PUBLIC
```

### 5. Run the Application

```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## 📊 Data Sources

### Government Data Sources (data.gov.in)

The application is designed to work with data from:

- Ministry of Tourism, Government of India
- Archaeological Survey of India
- Ministry of Culture
- State Tourism Departments
- Festival and Fair organizers

### Data Structure

The application expects data with the following columns:

- `Date`: Event date
- `State`: Indian state
- `Event`: Event name
- `Art_Form`: Type of traditional art
- `Visitors`: Number of visitors
- `Tourism_Level`: High/Medium/Low classification
- `Revenue_INR`: Revenue in Indian Rupees
- `Local_Employment`: Jobs created
- `Region`: Geographical region

## 🔮 Forecasting Capabilities

### Prophet Integration

The application uses Facebook's Prophet for time series forecasting:

- **Seasonality Detection**: Automatically detects yearly, weekly, and custom seasonal patterns
- **Holiday Effects**: Accounts for festival and holiday impacts
- **Trend Analysis**: Identifies long-term growth patterns
- **Uncertainty Intervals**: Provides confidence bounds for predictions

### Forecasting Features

- Customizable forecast horizons (30-365 days)
- State-specific and event-specific forecasting
- Growth rate calculations
- Seasonal decomposition
- Interactive forecast visualization

## 📈 Analytics & Insights

### Key Performance Indicators

- **Total Visitors**: Aggregate visitor count
- **Revenue Generation**: Economic impact in INR
- **Employment Creation**: Jobs generated
- **Event Distribution**: Geographic spread of events

### Regional Analysis

- **Tourism Intensity**: Visitor density by region
- **Art Form Popularity**: Most engaging traditional arts
- **Seasonal Patterns**: Peak and off-peak periods
- **Economic Efficiency**: Revenue per visitor metrics

## 🎯 Use Cases

### For Tourism Boards

- **Marketing Strategy**: Identify peak seasons and popular events
- **Resource Allocation**: Optimize infrastructure and staff deployment
- **Event Planning**: Schedule events to maximize attendance
- **Budget Planning**: Forecast revenue and visitor numbers

### For Cultural Organizations

- **Event Promotion**: Understand audience preferences
- **Collaboration Opportunities**: Identify complementary events
- **Impact Assessment**: Measure cultural and economic impact
- **Grant Applications**: Provide data-driven justifications

### For Researchers

- **Cultural Studies**: Analyze trends in traditional arts
- **Tourism Research**: Study visitor behavior patterns
- **Economic Analysis**: Assess tourism's economic contribution
- **Policy Development**: Inform cultural tourism policies

## 🌟 Advanced Features

### Machine Learning Integration

- **Visitor Prediction**: ML models for attendance forecasting
- **Sentiment Analysis**: Social media sentiment about events
- **Recommendation Engine**: Personalized event suggestions
- **Anomaly Detection**: Identify unusual tourism patterns

### Data Integration

- **API Connectivity**: Connect to external data sources
- **Real-time Updates**: Live data streaming capabilities
- **Multi-format Support**: CSV, Excel, JSON, API data
- **Cloud Storage**: Integration with cloud databases

## 🔧 Configuration

### Environment Variables

```env
# Application Settings
APP_TITLE=Cultural Tourism Dashboard - India
APP_DESCRIPTION=Interactive dashboard for cultural tourism analysis

# Data Configuration
DATA_SOURCE=local  # Options: local, snowflake, api
CSV_FILE_PATH=data/dummy_data.csv

# Forecasting Settings
DEFAULT_FORECAST_DAYS=180
MIN_DATA_POINTS=30

# UI Settings
THEME=light
COLOR_PALETTE=orange
```

### Customization Options

- **Themes**: Light/Dark mode support
- **Color Schemes**: Customizable color palettes
- **Layout**: Flexible dashboard layout options
- **Metrics**: Configurable KPIs and metrics

## 📱 Deployment

### Local Development

```bash
streamlit run app.py --server.port 8501
```

### Cloud Deployment

#### Streamlit Cloud

1. Push code to GitHub repository
2. Connect repository to Streamlit Cloud
3. Configure environment variables
4. Deploy application

#### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

#### Heroku Deployment

1. Create `Procfile`:
```
web: sh setup.sh && streamlit run app.py
```

2. Create `setup.sh`:
```bash
mkdir -p ~/.streamlit/
echo "[server]
port = $PORT
enableCORS = false
headless = true
" > ~/.streamlit/config.toml
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## 🙏 Acknowledgments

- **Prophet**: Facebook's open-source forecasting tool
- **Streamlit**: For the amazing web app framework
- **Government of India**: For providing open cultural tourism data
- **Indian Cultural Organizations**: For preserving and promoting traditional arts

## 📞 Support

For support and questions:

- 📧 Email: support@cultural-tourism-dashboard.com
- 🐛 Issues: [GitHub Issues](https://github.com/your-username/cultural-tourism-app/issues)
- 📖 Documentation: [Wiki](https://github.com/your-username/cultural-tourism-app/wiki)

## 🚀 Future Enhancements

- [ ] Real-time data integration
- [ ] Mobile app development
- [ ] AI-powered recommendations
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] API for third-party integrations
- [ ] Offline mode capabilities
- [ ] Enhanced security features

---

**Built with ❤️ for promoting India's rich cultural heritage**