import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Area, AreaChart } from 'recharts';

const PredictionView = ({ predictionData, columnName }) => {
  if (!predictionData || !predictionData.success) {
    return (
      <div className="bg-white rounded-xl shadow-lg p-6">
        <p className="text-gray-500">No prediction data available</p>
      </div>
    );
  }

  const { predictions, trend, trend_strength, current_value, predicted_change, percent_change, model_info, anomalies, recommendations } = predictionData;

  // Prepare chart data
  const chartData = predictions?.predictions?.map((pred, idx) => ({
    step: `T+${pred.step}`,
    predicted: pred.predicted_value,
    lower: pred.lower_bound,
    upper: pred.upper_bound,
  })) || [];

  return (
    <div className="w-full max-w-7xl mx-auto p-6 space-y-6">
      {/* Prediction Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white rounded-lg shadow p-4 border-l-4 border-blue-500">
          <p className="text-sm text-gray-600 font-medium">Current Value</p>
          <p className="text-2xl font-bold text-gray-800 mt-1">{current_value}</p>
        </div>

        <div className="bg-white rounded-lg shadow p-4 border-l-4 border-purple-500">
          <p className="text-sm text-gray-600 font-medium">Predicted Change</p>
          <p className={`text-2xl font-bold mt-1 ${predicted_change >= 0 ? 'text-green-600' : 'text-red-600'}`}>
            {predicted_change >= 0 ? '+' : ''}{predicted_change}
          </p>
        </div>

        <div className="bg-white rounded-lg shadow p-4 border-l-4 border-green-500">
          <p className="text-sm text-gray-600 font-medium">Percent Change</p>
          <p className={`text-2xl font-bold mt-1 ${percent_change >= 0 ? 'text-green-600' : 'text-red-600'}`}>
            {percent_change >= 0 ? '+' : ''}{percent_change}%
          </p>
        </div>

        <div className="bg-white rounded-lg shadow p-4 border-l-4 border-orange-500">
          <p className="text-sm text-gray-600 font-medium">Trend</p>
          <p className="text-xl font-bold text-gray-800 mt-1 capitalize flex items-center gap-2">
            {trend === 'increasing' ? '📈' : trend === 'decreasing' ? '📉' : '➡️'}
            {trend}
          </p>
        </div>
      </div>

      {/* Prediction Chart */}
      {chartData.length > 0 && (
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-xl font-bold text-gray-800 mb-4">
            Future Predictions for {columnName}
          </h3>
          <ResponsiveContainer width="100%" height={350}>
            <AreaChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="step" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Area
                type="monotone"
                dataKey="upper"
                stackId="1"
                stroke="none"
                fill="#93c5fd"
                fillOpacity={0.3}
              />
              <Area
                type="monotone"
                dataKey="predicted"
                stackId="2"
                stroke="#0ea5e9"
                fill="#0ea5e9"
                strokeWidth={3}
              />
              <Area
                type="monotone"
                dataKey="lower"
                stackId="3"
                stroke="none"
                fill="#93c5fd"
                fillOpacity={0.3}
              />
            </AreaChart>
          </ResponsiveContainer>
          <p className="text-sm text-gray-500 mt-2 text-center">
            Shaded area represents 95% confidence interval
          </p>
        </div>
      )}

      {/* Model Information */}
      {model_info && model_info.success && (
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-xl font-bold text-gray-800 mb-4">Model Performance</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <p className="text-sm text-gray-600 mb-2">Model Type</p>
              <p className="text-lg font-semibold text-gray-800">{model_info.model_type}</p>
              
              <div className="mt-4 space-y-2">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">R² Score</span>
                  <span className="font-bold text-gray-800">{model_info.r2_score}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">RMSE</span>
                  <span className="font-bold text-gray-800">{model_info.rmse}</span>
                </div>
              </div>
            </div>

            <div>
              <p className="text-sm text-gray-600 mb-2">Feature Importance (Top 5)</p>
              <div className="space-y-2">
                {model_info.feature_importance?.slice(0, 5).map((item, idx) => (
                  <div key={idx}>
                    <div className="flex justify-between text-sm mb-1">
                      <span className="text-gray-700">{item.feature}</span>
                      <span className="font-semibold">{(item.importance * 100).toFixed(1)}%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-primary-600 h-2 rounded-full"
                        style={{ width: `${item.importance * 100}%` }}
                      ></div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Anomalies */}
      {anomalies && anomalies.success && anomalies.total_anomalies > 0 && (
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-xl font-bold text-gray-800 mb-4">⚠️ Anomalies Detected</h3>
          <p className="text-gray-600 mb-4">
            Found {anomalies.total_anomalies} anomalies ({anomalies.anomaly_percentage}% of data)
          </p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {anomalies.anomalies?.slice(0, 6).map((anomaly, idx) => (
              <div
                key={idx}
                className={`p-3 rounded-lg border-2 ${
                  anomaly.type === 'high' 
                    ? 'bg-red-50 border-red-200' 
                    : 'bg-yellow-50 border-yellow-200'
                }`}
              >
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Index {anomaly.index}</span>
                  <span className={`text-xs px-2 py-1 rounded font-semibold ${
                    anomaly.type === 'high' 
                      ? 'bg-red-200 text-red-800' 
                      : 'bg-yellow-200 text-yellow-800'
                  }`}>
                    {anomaly.type}
                  </span>
                </div>
                <p className="text-lg font-bold text-gray-800 mt-1">{anomaly.value}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Recommendations */}
      {recommendations && recommendations.length > 0 && (
        <div className="bg-gradient-to-r from-purple-50 to-blue-50 rounded-xl shadow-lg p-6">
          <h3 className="text-xl font-bold text-gray-800 mb-4">🎯 Recommendations</h3>
          <div className="space-y-3">
            {recommendations.map((rec, idx) => (
              <div key={idx} className="flex items-start gap-3 p-4 bg-white rounded-lg shadow-sm">
                <span className="text-primary-600 font-bold text-lg">{idx + 1}.</span>
                <p className="text-gray-700">{rec}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default PredictionView;
