from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Dict, Any
import os
import uuid
from pathlib import Path
import pandas as pd

from data_processor import DataProcessor
from ml_models import MLPredictor

app = FastAPI(
    title="AI Decision Intelligence API",
    description="Transform messy CSV data into actionable insights",
    version="1.0.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Storage for uploaded files and processors
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Session storage (in production, use Redis or database)
sessions = {}


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "AI Decision Intelligence API",
        "status": "running",
        "version": "1.0.0"
    }


@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Upload a CSV file for analysis
    Returns a session ID and basic file information
    """
    try:
        # Validate file type
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="Only CSV files are supported")
        
        # Generate unique session ID
        session_id = str(uuid.uuid4())
        
        # Save file
        file_path = UPLOAD_DIR / f"{session_id}.csv"
        
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
        
        # Initialize processor
        processor = DataProcessor()
        load_result = processor.load_csv(str(file_path))
        
        if not load_result["success"]:
            raise HTTPException(status_code=400, detail=load_result["error"])
        
        # Store session
        sessions[session_id] = {
            "processor": processor,
            "file_path": str(file_path),
            "filename": file.filename
        }
        
        return {
            "success": True,
            "session_id": session_id,
            "filename": file.filename,
            "data_info": load_result["data"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


@app.post("/api/analyze/{session_id}")
async def analyze_data(session_id: str) -> Dict[str, Any]:
    """
    Clean and analyze the uploaded data
    Returns cleaning steps, patterns, and insights
    """
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    try:
        processor = sessions[session_id]["processor"]
        
        # Clean data
        clean_result = processor.clean_data()
        if not clean_result["success"]:
            raise HTTPException(status_code=400, detail=clean_result["error"])
        
        # Detect patterns
        pattern_result = processor.detect_patterns()
        if not pattern_result["success"]:
            raise HTTPException(status_code=400, detail=pattern_result["error"])
        
        # Generate insights
        insights = processor.generate_insights()
        
        # Get chart data
        chart_data = processor.get_data_for_charts()
        
        return {
            "success": True,
            "cleaning": clean_result,
            "patterns": pattern_result["data"],
            "insights": insights,
            "chart_data": chart_data
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing data: {str(e)}")


@app.post("/api/predict/{session_id}")
async def predict_trends(
    session_id: str,
    target_column: str,
    steps: int = 5
) -> Dict[str, Any]:
    """
    Generate predictions for a specific column
    Returns predictions, trend analysis, and recommendations
    """
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    try:
        processor = sessions[session_id]["processor"]
        df = processor.get_cleaned_data()
        
        if df is None:
            raise HTTPException(status_code=400, detail="Data not yet analyzed. Call /analyze first")
        
        # Initialize ML predictor
        ml_predictor = MLPredictor()
        
        # Train model
        model_result = ml_predictor.train_regression_model(df, target_column)
        
        # Predict future values
        prediction_result = ml_predictor.predict_next_values(df, target_column, steps)
        
        # Detect anomalies
        anomaly_result = ml_predictor.detect_anomalies(df, target_column)
        
        # Get patterns for recommendations
        pattern_result = processor.detect_patterns()
        patterns = pattern_result["data"]["patterns"] if pattern_result["success"] else []
        
        # Generate recommendations
        recommendations = ml_predictor.generate_recommendations(patterns, prediction_result)
        
        return {
            "success": True,
            "model_info": model_result,
            "predictions": prediction_result,
            "anomalies": anomaly_result,
            "recommendations": recommendations
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating predictions: {str(e)}")


@app.get("/api/dashboard/{session_id}")
async def get_dashboard_data(session_id: str) -> Dict[str, Any]:
    """
    Get comprehensive dashboard data for visualization
    Returns all analysis, predictions, and insights in one call
    """
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    try:
        processor = sessions[session_id]["processor"]
        df = processor.get_cleaned_data()
        
        if df is None:
            # If not analyzed yet, do it now
            analyze_result = await analyze_data(session_id)
            df = processor.get_cleaned_data()
        
        # Get numeric columns for prediction
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        
        dashboard = {
            "success": True,
            "filename": sessions[session_id]["filename"],
            "data_shape": {
                "rows": len(df),
                "columns": len(df.columns)
            },
            "columns": df.columns.tolist(),
            "numeric_columns": numeric_cols,
            "chart_data": processor.get_data_for_charts(),
            "insights": processor.generate_insights()
        }
        
        return dashboard
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching dashboard data: {str(e)}")


@app.get("/api/columns/{session_id}")
async def get_columns(session_id: str) -> Dict[str, Any]:
    """Get list of columns in the dataset"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    try:
        processor = sessions[session_id]["processor"]
        df = processor.get_cleaned_data() or processor.df
        
        if df is None:
            raise HTTPException(status_code=400, detail="No data loaded")
        
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        return {
            "success": True,
            "all_columns": df.columns.tolist(),
            "numeric_columns": numeric_cols,
            "categorical_columns": categorical_cols
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching columns: {str(e)}")


@app.delete("/api/session/{session_id}")
async def delete_session(session_id: str) -> Dict[str, Any]:
    """Delete a session and clean up files"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    try:
        # Delete file
        file_path = Path(sessions[session_id]["file_path"])
        if file_path.exists():
            file_path.unlink()
        
        # Remove session
        del sessions[session_id]
        
        return {"success": True, "message": "Session deleted"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting session: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
