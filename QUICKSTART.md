# Quick Start Guide

## Prerequisites

- Python 3.11+
- Node.js 18+
- npm or yarn

## Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment (recommended):
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Start the server:
```bash
uvicorn main:app --reload
```

Backend will run at: `http://localhost:8000`

**API Documentation:** Visit `http://localhost:8000/docs` for interactive API documentation

## Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start development server:
```bash
npm run dev
```

Frontend will run at: `http://localhost:5173`

## Testing the Application

1. Open `http://localhost:5173` in your browser
2. Upload one of the sample CSV files from `SAMPLE_DATA.md`
3. Explore the dashboard with insights and visualizations
4. Click "Predict Future Trends" to see ML predictions

## Sample Use Cases

### 📚 College Attendance Analysis
- Upload student attendance CSV
- See attendance patterns and correlations with grades
- Predict future performance trends

### 💰 Expense Tracking
- Upload monthly expenses CSV
- Identify spending patterns by category
- Forecast future expenses

### ⚡ Productivity Insights
- Upload daily productivity logs
- Discover what affects your focus score
- Get recommendations to boost productivity

### 🔌 Energy Usage Optimization
- Upload utility consumption data
- Detect usage anomalies
- Predict costs and optimize consumption

## Features Demonstrated

✅ **Automatic Data Cleaning**
- Missing value imputation
- Outlier detection and removal
- Date parsing and normalization

✅ **Pattern Detection**
- Correlation analysis
- Trend identification
- Statistical summaries

✅ **ML Predictions**
- Random Forest regression models
- Time series forecasting
- Confidence intervals

✅ **Natural Language Insights**
- Plain English summaries
- Key findings extraction
- Actionable recommendations

✅ **Interactive Visualizations**
- Line charts for trends
- Bar charts for distributions
- Prediction plots with uncertainty

## Deployment

### Backend (Render)

1. Push code to GitHub
2. Create new Web Service on Render
3. Connect repository
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Deploy

### Frontend (Vercel)

1. Push code to GitHub
2. Import project on Vercel
3. Set root directory to `frontend`
4. Update API URL in `src/services/api.js` to your Render backend URL
5. Deploy

## Troubleshooting

**Backend won't start:**
- Make sure Python 3.11+ is installed
- Check if port 8000 is available
- Verify all dependencies are installed

**Frontend won't start:**
- Make sure Node.js 18+ is installed
- Delete `node_modules` and run `npm install` again
- Check if port 5173 is available

**CORS errors:**
- Make sure backend is running
- Check CORS configuration in `backend/main.py`
- Update frontend API URL if backend is on different port

**File upload fails:**
- Ensure CSV file is properly formatted
- Check file size (keep under 10MB for best performance)
- Verify backend `uploads/` directory exists

## Tech Stack Details

### Backend
- **FastAPI**: Modern, fast web framework
- **Pandas**: Data manipulation and analysis
- **Scikit-learn**: ML models and preprocessing
- **NumPy**: Numerical computing

### Frontend
- **React 18**: UI library
- **Vite**: Build tool and dev server
- **Tailwind CSS**: Utility-first CSS framework
- **Recharts**: Charting library
- **Axios**: HTTP client

## API Endpoints

- `POST /api/upload` - Upload CSV file
- `POST /api/analyze/{session_id}` - Analyze and clean data
- `POST /api/predict/{session_id}` - Generate predictions
- `GET /api/dashboard/{session_id}` - Get dashboard data
- `GET /api/columns/{session_id}` - Get column information
- `DELETE /api/session/{session_id}` - Delete session

## Project Structure

```
CircuitBreak/
├── backend/
│   ├── main.py              # FastAPI app
│   ├── data_processor.py    # Data cleaning & analysis
│   ├── ml_models.py         # ML prediction models
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   │   ├── FileUpload.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   └── PredictionView.jsx
│   │   ├── services/
│   │   │   └── api.js       # API client
│   │   ├── App.jsx          # Main app component
│   │   └── main.jsx         # Entry point
│   └── package.json         # Node dependencies
└── README.md
```

## Support

For issues or questions:
1. Check the API documentation at `/docs`
2. Review sample data in `SAMPLE_DATA.md`
3. Ensure both backend and frontend are running

Built for **CircuitBreak Hackathon 2026** 🚀
