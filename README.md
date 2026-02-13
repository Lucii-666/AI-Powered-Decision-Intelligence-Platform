# AI-Powered Decision Intelligence Platform

**Theme:** Data Analytics & Decision Intelligence / AI for Everyday Life

## Concept

A web platform that transforms messy CSV data into actionable insights.

### Features
- 📊 Automatic data cleaning
- 🔍 Pattern detection
- 📈 Future trend prediction
- 💬 Natural language insights
- 📉 Interactive visual dashboards

**Upload data. Get clarity.**

## Tech Stack

- **Frontend:** React + Tailwind CSS
- **Backend:** FastAPI
- **ML:** Scikit-learn
- **Charts:** Recharts
- **Deployment:** Vercel (Frontend) + Render (Backend)

## Project Structure

```
CircuitBreak/
├── backend/              # FastAPI backend
│   ├── main.py          # Main API server
│   ├── ml_models.py     # ML prediction models
│   ├── data_processor.py # Data cleaning & analysis
│   └── requirements.txt
├── frontend/            # React frontend
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── services/    # API services
│   │   └── App.jsx
│   └── package.json
└── README.md
```

## Setup Instructions

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Backend runs at: `http://localhost:8000`

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at: `http://localhost:5173`

## API Endpoints

- `POST /upload` - Upload CSV file
- `POST /analyze` - Analyze data and get insights
- `POST /predict` - Generate predictions
- `GET /dashboard/{file_id}` - Get dashboard data

## Features

### 1. Smart Data Cleaning
- Handles missing values
- Detects and removes outliers
- Normalizes data formats

### 2. Pattern Detection
- Correlation analysis
- Trend identification
- Anomaly detection

### 3. Predictive Analytics
- Time series forecasting
- Regression analysis
- Trend extrapolation

### 4. Natural Language Insights
- Plain English summaries
- Key findings extraction
- Actionable recommendations

### 5. Visual Dashboards
- Interactive charts
- Real-time updates
- Customizable views

## Deployment

### Frontend (Vercel)
```bash
cd frontend
vercel --prod
```

### Backend (Render)
- Connect GitHub repository
- Set up Python environment
- Deploy with `uvicorn main:app --host 0.0.0.0 --port $PORT`

## License

MIT License - Built for CircuitBreak Hackathon 2026
