import pandas as pd
import numpy as np
from typing import Dict, List, Any
from datetime import datetime
import re


class DataProcessor:
    """Handles data cleaning, preprocessing, and analysis"""
    
    def __init__(self):
        self.df = None
        self.insights = []
        
    def load_csv(self, file_path: str) -> Dict[str, Any]:
        """Load and provide initial statistics about CSV file"""
        try:
            self.df = pd.read_csv(file_path)
            
            info = {
                "rows": len(self.df),
                "columns": len(self.df.columns),
                "column_names": self.df.columns.tolist(),
                "dtypes": {col: str(dtype) for col, dtype in self.df.dtypes.items()},
                "missing_values": self.df.isnull().sum().to_dict(),
                "preview": self.df.head(5).to_dict(orient='records')
            }
            
            return {"success": True, "data": info}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def clean_data(self) -> Dict[str, Any]:
        """Automatically clean the data"""
        if self.df is None:
            return {"success": False, "error": "No data loaded"}
        
        cleaning_steps = []
        
        # 1. Handle missing values
        initial_missing = self.df.isnull().sum().sum()
        
        # Fill numeric columns with median
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if self.df[col].isnull().any():
                self.df[col].fillna(self.df[col].median(), inplace=True)
                cleaning_steps.append(f"Filled missing values in '{col}' with median")
        
        # Fill categorical columns with mode
        categorical_cols = self.df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            if self.df[col].isnull().any():
                mode_val = self.df[col].mode()[0] if not self.df[col].mode().empty else "Unknown"
                self.df[col].fillna(mode_val, inplace=True)
                cleaning_steps.append(f"Filled missing values in '{col}' with mode")
        
        # 2. Remove duplicate rows
        initial_rows = len(self.df)
        self.df.drop_duplicates(inplace=True)
        duplicates_removed = initial_rows - len(self.df)
        if duplicates_removed > 0:
            cleaning_steps.append(f"Removed {duplicates_removed} duplicate rows")
        
        # 3. Parse date columns
        for col in self.df.columns:
            if self.df[col].dtype == 'object':
                try:
                    self.df[col] = pd.to_datetime(self.df[col])
                    cleaning_steps.append(f"Converted '{col}' to datetime format")
                except:
                    pass
        
        # 4. Remove outliers using IQR method
        for col in numeric_cols:
            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = ((self.df[col] < lower_bound) | (self.df[col] > upper_bound)).sum()
            if outliers > 0:
                self.df = self.df[(self.df[col] >= lower_bound) & (self.df[col] <= upper_bound)]
                cleaning_steps.append(f"Removed {outliers} outliers from '{col}'")
        
        return {
            "success": True,
            "steps": cleaning_steps,
            "final_shape": {"rows": len(self.df), "columns": len(self.df.columns)}
        }
    
    def detect_patterns(self) -> Dict[str, Any]:
        """Detect patterns and correlations in the data"""
        if self.df is None:
            return {"success": False, "error": "No data loaded"}
        
        patterns = []
        
        # Correlation analysis for numeric columns
        numeric_df = self.df.select_dtypes(include=[np.number])
        if len(numeric_df.columns) > 1:
            corr_matrix = numeric_df.corr()
            
            # Find strong correlations
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    corr_value = corr_matrix.iloc[i, j]
                    if abs(corr_value) > 0.7:
                        col1 = corr_matrix.columns[i]
                        col2 = corr_matrix.columns[j]
                        relationship = "positive" if corr_value > 0 else "negative"
                        patterns.append({
                            "type": "correlation",
                            "description": f"Strong {relationship} correlation between {col1} and {col2}",
                            "value": round(corr_value, 3),
                            "columns": [col1, col2]
                        })
        
        # Trend detection
        for col in numeric_df.columns:
            values = numeric_df[col].values
            if len(values) > 5:
                # Simple linear trend
                x = np.arange(len(values))
                slope = np.polyfit(x, values, 1)[0]
                
                if abs(slope) > 0.01 * values.std():
                    trend_type = "increasing" if slope > 0 else "decreasing"
                    patterns.append({
                        "type": "trend",
                        "description": f"{col} shows a {trend_type} trend",
                        "slope": round(slope, 4),
                        "column": col
                    })
        
        # Statistical summaries
        summary = {
            "statistics": {},
            "patterns": patterns
        }
        
        for col in numeric_df.columns:
            summary["statistics"][col] = {
                "mean": round(numeric_df[col].mean(), 2),
                "median": round(numeric_df[col].median(), 2),
                "std": round(numeric_df[col].std(), 2),
                "min": round(numeric_df[col].min(), 2),
                "max": round(numeric_df[col].max(), 2)
            }
        
        return {"success": True, "data": summary}
    
    def generate_insights(self) -> List[str]:
        """Generate natural language insights from the data"""
        if self.df is None:
            return []
        
        insights = []
        
        # Basic insights
        insights.append(f"📊 Dataset contains {len(self.df)} records across {len(self.df.columns)} variables")
        
        # Numeric column insights
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            mean_val = self.df[col].mean()
            std_val = self.df[col].std()
            
            if std_val / mean_val > 1 if mean_val != 0 else False:
                insights.append(f"⚠️ High variability detected in {col} (CV > 100%)")
            
            # Check for skewness
            skew = self.df[col].skew()
            if abs(skew) > 1:
                direction = "right" if skew > 0 else "left"
                insights.append(f"📈 {col} distribution is skewed to the {direction}")
        
        # Categorical insights
        categorical_cols = self.df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            unique_count = self.df[col].nunique()
            if unique_count <= 10:
                mode_val = self.df[col].mode()[0]
                mode_pct = (self.df[col] == mode_val).sum() / len(self.df) * 100
                insights.append(f"🎯 Most common {col}: '{mode_val}' ({mode_pct:.1f}% of records)")
        
        # Time-based insights
        date_cols = self.df.select_dtypes(include=['datetime64']).columns
        if len(date_cols) > 0:
            date_col = date_cols[0]
            duration = (self.df[date_col].max() - self.df[date_col].min()).days
            insights.append(f"📅 Data spans {duration} days from {self.df[date_col].min().date()} to {self.df[date_col].max().date()}")
        
        return insights
    
    def get_cleaned_data(self) -> pd.DataFrame:
        """Return the cleaned dataframe"""
        return self.df
    
    def get_data_for_charts(self) -> Dict[str, Any]:
        """Prepare data for visualization"""
        if self.df is None:
            return {}
        
        chart_data = {}
        
        # Line chart data for numeric trends
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            chart_data["line_chart"] = []
            for idx, row in self.df.head(50).iterrows():
                point = {"index": int(idx)}
                for col in numeric_cols[:3]:  # Limit to 3 numeric columns
                    point[col] = float(row[col])
                chart_data["line_chart"].append(point)
        
        # Bar chart data for categorical columns
        categorical_cols = self.df.select_dtypes(include=['object']).columns
        if len(categorical_cols) > 0:
            col = categorical_cols[0]
            value_counts = self.df[col].value_counts().head(10)
            chart_data["bar_chart"] = [
                {"name": str(name), "value": int(value)} 
                for name, value in value_counts.items()
            ]
        
        # Summary stats for gauge/number displays
        chart_data["summary"] = {}
        for col in numeric_cols:
            chart_data["summary"][col] = {
                "current": float(self.df[col].iloc[-1]) if len(self.df) > 0 else 0,
                "average": float(self.df[col].mean()),
                "trend": "up" if len(self.df) > 1 and self.df[col].iloc[-1] > self.df[col].iloc[0] else "down"
            }
        
        return chart_data
