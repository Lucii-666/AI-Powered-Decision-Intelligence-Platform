import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from typing import Dict, List, Any, Tuple
import warnings
warnings.filterwarnings('ignore')


class MLPredictor:
    """Machine Learning models for prediction and forecasting"""
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.feature_names = []
        
    def prepare_features(self, df: pd.DataFrame, target_col: str) -> Tuple[np.ndarray, np.ndarray]:
        """Prepare features for training"""
        # Select numeric columns only
        numeric_df = df.select_dtypes(include=[np.number])
        
        if target_col not in numeric_df.columns:
            raise ValueError(f"Target column '{target_col}' not found or not numeric")
        
        # Separate features and target
        X = numeric_df.drop(columns=[target_col])
        y = numeric_df[target_col]
        
        # Handle missing values
        X = X.fillna(X.mean())
        y = y.fillna(y.mean())
        
        self.feature_names = X.columns.tolist()
        
        return X.values, y.values
    
    def train_regression_model(self, df: pd.DataFrame, target_col: str) -> Dict[str, Any]:
        """Train a regression model for prediction"""
        try:
            X, y = self.prepare_features(df, target_col)
            
            if len(X) < 5:
                return {
                    "success": False,
                    "error": "Insufficient data for training (need at least 5 samples)"
                }
            
            # Scale features
            X_scaled = self.scaler.fit_transform(X)
            
            # Train model
            self.model = RandomForestRegressor(n_estimators=100, random_state=42)
            self.model.fit(X_scaled, y)
            
            # Calculate model performance
            train_score = self.model.score(X_scaled, y)
            predictions = self.model.predict(X_scaled)
            mse = np.mean((predictions - y) ** 2)
            rmse = np.sqrt(mse)
            
            # Feature importance
            feature_importance = dict(zip(
                self.feature_names,
                self.model.feature_importances_
            ))
            
            # Sort by importance
            sorted_features = sorted(
                feature_importance.items(),
                key=lambda x: x[1],
                reverse=True
            )
            
            return {
                "success": True,
                "model_type": "Random Forest Regression",
                "r2_score": round(train_score, 4),
                "rmse": round(rmse, 4),
                "feature_importance": [
                    {"feature": feat, "importance": round(imp, 4)}
                    for feat, imp in sorted_features
                ],
                "target_column": target_col
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def predict_next_values(self, df: pd.DataFrame, target_col: str, steps: int = 5) -> Dict[str, Any]:
        """Predict future values using time series forecasting"""
        try:
            if target_col not in df.columns:
                return {"success": False, "error": f"Column '{target_col}' not found"}
            
            # Get the target column data
            data = df[target_col].values
            
            if len(data) < 10:
                return {
                    "success": False,
                    "error": "Insufficient data for prediction (need at least 10 points)"
                }
            
            # Simple time series prediction using linear regression
            X = np.arange(len(data)).reshape(-1, 1)
            y = data
            
            # Remove NaN values
            mask = ~np.isnan(y)
            X_clean = X[mask]
            y_clean = y[mask]
            
            # Train simple linear model
            model = LinearRegression()
            model.fit(X_clean, y_clean)
            
            # Predict future values
            future_X = np.arange(len(data), len(data) + steps).reshape(-1, 1)
            predictions = model.predict(future_X)
            
            # Calculate trend
            slope = model.coef_[0]
            trend = "increasing" if slope > 0 else "decreasing" if slope < 0 else "stable"
            
            # Calculate confidence intervals (simple approximation)
            residuals = y_clean - model.predict(X_clean)
            std_error = np.std(residuals)
            
            prediction_list = []
            for i, pred in enumerate(predictions):
                prediction_list.append({
                    "step": i + 1,
                    "predicted_value": round(float(pred), 2),
                    "lower_bound": round(float(pred - 1.96 * std_error), 2),
                    "upper_bound": round(float(pred + 1.96 * std_error), 2)
                })
            
            return {
                "success": True,
                "predictions": prediction_list,
                "trend": trend,
                "trend_strength": round(abs(slope), 4),
                "current_value": round(float(data[-1]), 2),
                "predicted_change": round(float(predictions[-1] - data[-1]), 2),
                "percent_change": round(float((predictions[-1] - data[-1]) / data[-1] * 100), 2) if data[-1] != 0 else 0
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def detect_anomalies(self, df: pd.DataFrame, column: str) -> Dict[str, Any]:
        """Detect anomalies in a specific column"""
        try:
            if column not in df.columns:
                return {"success": False, "error": f"Column '{column}' not found"}
            
            data = df[column].dropna()
            
            if len(data) < 5:
                return {"success": False, "error": "Insufficient data for anomaly detection"}
            
            # Use IQR method for anomaly detection
            Q1 = data.quantile(0.25)
            Q3 = data.quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            # Find anomalies
            anomalies = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
            
            anomaly_list = []
            for idx, row in anomalies.iterrows():
                anomaly_list.append({
                    "index": int(idx),
                    "value": float(row[column]),
                    "type": "high" if row[column] > upper_bound else "low"
                })
            
            return {
                "success": True,
                "total_anomalies": len(anomalies),
                "anomaly_percentage": round(len(anomalies) / len(data) * 100, 2),
                "anomalies": anomaly_list[:20],  # Limit to 20 anomalies
                "thresholds": {
                    "lower_bound": round(float(lower_bound), 2),
                    "upper_bound": round(float(upper_bound), 2)
                }
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def generate_recommendations(self, patterns: List[Dict], predictions: Dict) -> List[str]:
        """Generate actionable recommendations based on analysis"""
        recommendations = []
        
        # Based on predictions
        if predictions.get("success"):
            trend = predictions.get("trend", "")
            change_pct = predictions.get("percent_change", 0)
            
            if trend == "increasing" and change_pct > 10:
                recommendations.append(
                    f"📈 Strong upward trend detected. Expected increase of {change_pct}% - consider scaling operations"
                )
            elif trend == "decreasing" and abs(change_pct) > 10:
                recommendations.append(
                    f"📉 Declining trend observed. Expected decrease of {abs(change_pct)}% - investigate root causes"
                )
            elif abs(change_pct) < 5:
                recommendations.append(
                    "➡️ Stable trend detected. Focus on maintaining current performance"
                )
        
        # Based on patterns
        if patterns:
            for pattern in patterns[:3]:
                if pattern.get("type") == "correlation":
                    cols = pattern.get("columns", [])
                    if len(cols) == 2:
                        recommendations.append(
                            f"🔗 {cols[0]} and {cols[1]} are strongly correlated - changes in one affect the other"
                        )
        
        # General recommendations
        recommendations.append("💡 Review outliers and anomalies for data quality issues")
        recommendations.append("🎯 Focus on high-importance features identified by the model")
        recommendations.append("📊 Set up monitoring for key metrics to track changes over time")
        
        return recommendations[:5]  # Return top 5 recommendations
