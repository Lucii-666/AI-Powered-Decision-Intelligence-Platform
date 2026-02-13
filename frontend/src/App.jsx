import React, { useState } from 'react';
import './index.css';
import FileUpload from './components/FileUpload';
import Dashboard from './components/Dashboard';
import PredictionView from './components/PredictionView';
import { apiService } from './services/api';

function App() {
  const [sessionId, setSessionId] = useState(null);
  const [filename, setFilename] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [analysisData, setAnalysisData] = useState(null);
  const [predictionData, setPredictionData] = useState(null);
  const [availableColumns, setAvailableColumns] = useState([]);
  const [selectedColumn, setSelectedColumn] = useState('');
  const [currentView, setCurrentView] = useState('upload'); // upload, dashboard, prediction

  const handleFileSelect = async (file) => {
    setIsLoading(true);
    try {
      // Upload file
      const uploadResult = await apiService.uploadFile(file);
      if (uploadResult.success) {
        setSessionId(uploadResult.session_id);
        setFilename(uploadResult.filename);
        
        // Automatically analyze data
        const analyzeResult = await apiService.analyzeData(uploadResult.session_id);
        if (analyzeResult.success) {
          setAnalysisData(analyzeResult);
          
          // Get available columns
          const columnsResult = await apiService.getColumns(uploadResult.session_id);
          if (columnsResult.success && columnsResult.numeric_columns.length > 0) {
            setAvailableColumns(columnsResult.numeric_columns);
            setSelectedColumn(columnsResult.numeric_columns[0]);
          }
          
          setCurrentView('dashboard');
        }
      }
    } catch (error) {
      console.error('Error processing file:', error);
      alert('Error processing file. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handlePredict = async () => {
    if (!sessionId || !selectedColumn) {
      alert('Please select a column for prediction');
      return;
    }

    setIsLoading(true);
    try {
      const predictionResult = await apiService.predict(sessionId, selectedColumn, 5);
      if (predictionResult.success) {
        setPredictionData(predictionResult);
        setCurrentView('prediction');
      }
    } catch (error) {
      console.error('Error generating predictions:', error);
      alert('Error generating predictions. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    if (sessionId) {
      apiService.deleteSession(sessionId).catch(console.error);
    }
    setSessionId(null);
    setFilename('');
    setAnalysisData(null);
    setPredictionData(null);
    setAvailableColumns([]);
    setSelectedColumn('');
    setCurrentView('upload');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50">
      {/* Header */}
      <header className="bg-white shadow-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                AI Decision Intelligence
              </h1>
              <p className="text-gray-600 mt-1">Transform data into actionable insights</p>
            </div>
            
            {sessionId && (
              <button
                onClick={handleReset}
                className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors font-medium"
              >
                ← New Analysis
              </button>
            )}
          </div>
        </div>
      </header>

      {/* Navigation Tabs */}
      {sessionId && (
        <div className="bg-white border-b">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex gap-8">
              <button
                onClick={() => setCurrentView('dashboard')}
                className={`px-4 py-4 font-medium transition-colors border-b-2 ${
                  currentView === 'dashboard'
                    ? 'text-primary-600 border-primary-600'
                    : 'text-gray-500 border-transparent hover:text-gray-700'
                }`}
              >
                📊 Dashboard
              </button>
              <button
                onClick={() => setCurrentView('prediction')}
                className={`px-4 py-4 font-medium transition-colors border-b-2 ${
                  currentView === 'prediction'
                    ? 'text-primary-600 border-primary-600'
                    : 'text-gray-500 border-transparent hover:text-gray-700'
                }`}
              >
                🔮 Predictions
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Main Content */}
      <main className="py-12 px-4 sm:px-6 lg:px-8">
        {currentView === 'upload' && (
          <div className="space-y-8">
            <div className="text-center mb-8">
              <h2 className="text-4xl font-bold text-gray-800 mb-4">
                Upload Data. Get Clarity.
              </h2>
              <p className="text-xl text-gray-600">
                Automatically clean, analyze, and predict trends from your CSV data
              </p>
            </div>
            
            <FileUpload onFileSelect={handleFileSelect} isLoading={isLoading} />
            
            {/* Features */}
            <div className="max-w-5xl mx-auto grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-16">
              <div className="bg-white rounded-lg p-6 shadow-md">
                <div className="text-3xl mb-3">🧹</div>
                <h3 className="text-lg font-semibold text-gray-800 mb-2">Auto Cleaning</h3>
                <p className="text-gray-600 text-sm">Handles missing values, outliers, and formatting automatically</p>
              </div>
              
              <div className="bg-white rounded-lg p-6 shadow-md">
                <div className="text-3xl mb-3">🔍</div>
                <h3 className="text-lg font-semibold text-gray-800 mb-2">Pattern Detection</h3>
                <p className="text-gray-600 text-sm">Discovers correlations and trends in your data</p>
              </div>
              
              <div className="bg-white rounded-lg p-6 shadow-md">
                <div className="text-3xl mb-3">📈</div>
                <h3 className="text-lg font-semibold text-gray-800 mb-2">Future Predictions</h3>
                <p className="text-gray-600 text-sm">ML-powered forecasting for data-driven decisions</p>
              </div>
              
              <div className="bg-white rounded-lg p-6 shadow-md">
                <div className="text-3xl mb-3">💬</div>
                <h3 className="text-lg font-semibold text-gray-800 mb-2">Plain English Insights</h3>
                <p className="text-gray-600 text-sm">No technical jargon, just clear actionable insights</p>
              </div>
              
              <div className="bg-white rounded-lg p-6 shadow-md">
                <div className="text-3xl mb-3">📊</div>
                <h3 className="text-lg font-semibold text-gray-800 mb-2">Visual Dashboards</h3>
                <p className="text-gray-600 text-sm">Interactive charts and graphs for easy understanding</p>
              </div>
              
              <div className="bg-white rounded-lg p-6 shadow-md">
                <div className="text-3xl mb-3">⚡</div>
                <h3 className="text-lg font-semibold text-gray-800 mb-2">Instant Results</h3>
                <p className="text-gray-600 text-sm">Get insights in seconds, not hours</p>
              </div>
            </div>
          </div>
        )}

        {currentView === 'dashboard' && analysisData && (
          <>
            <Dashboard
              data={{
                data_shape: {
                  rows: analysisData.cleaning?.final_shape?.rows || 0,
                  columns: analysisData.cleaning?.final_shape?.columns || 0,
                },
              }}
              insights={analysisData.insights || []}
              chartData={analysisData.chart_data}
            />
            
            {/* Action Button */}
            {availableColumns.length > 0 && (
              <div className="max-w-7xl mx-auto px-6 mt-8">
                <div className="bg-white rounded-xl shadow-lg p-6">
                  <h3 className="text-xl font-bold text-gray-800 mb-4">
                    Generate Predictions
                  </h3>
                  <div className="flex flex-col sm:flex-row gap-4 items-end">
                    <div className="flex-1">
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Select Column for Prediction
                      </label>
                      <select
                        value={selectedColumn}
                        onChange={(e) => setSelectedColumn(e.target.value)}
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                      >
                        {availableColumns.map((col) => (
                          <option key={col} value={col}>
                            {col}
                          </option>
                        ))}
                      </select>
                    </div>
                    <button
                      onClick={handlePredict}
                      disabled={isLoading}
                      className="px-6 py-2 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:from-blue-700 hover:to-purple-700 transition-all font-medium disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      {isLoading ? 'Generating...' : '🔮 Predict Future Trends'}
                    </button>
                  </div>
                </div>
              </div>
            )}
          </>
        )}

        {currentView === 'prediction' && predictionData && (
          <PredictionView
            predictionData={{
              ...predictionData.predictions,
              model_info: predictionData.model_info,
              anomalies: predictionData.anomalies,
              recommendations: predictionData.recommendations,
            }}
            columnName={selectedColumn}
          />
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center text-gray-600">
            <p className="font-semibold text-gray-800 mb-2">
              Built for CircuitBreak Hackathon 2026
            </p>
            <p className="text-sm">
              AI-Powered Decision Intelligence Platform • Data Analytics & AI for Everyday Life
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
