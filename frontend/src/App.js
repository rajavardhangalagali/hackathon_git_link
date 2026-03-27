import React, { useState, useEffect } from 'react';
import './App.css';
import Dashboard from './Dashboard';
import Settings from './Settings';
import axios from 'axios';

const API_BASE = 'http://localhost:5000/api';

function App() {
  const [scanData, setScanData] = useState(null);
  const [scanning, setScanning] = useState(false);
  const [stats, setStats] = useState(null);
  const [showSettings, setShowSettings] = useState(false);

  useEffect(() => {
    // Auto-refresh every 30 seconds
    const interval = setInterval(() => {
      if (scanning) {
        fetchScanData();
        fetchStats();
      }
    }, 30000);

    return () => clearInterval(interval);
  }, [scanning]);

  const fetchScanData = async () => {
    try {
      const response = await axios.get(`${API_BASE}/scan-data`);
      setScanData(response.data);
    } catch (error) {
      console.error('Error fetching scan data:', error);
    }
  };

  const fetchStats = async () => {
    try {
      const response = await axios.get(`${API_BASE}/stats`);
      setStats(response.data);
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  const startScan = async () => {
    try {
      // Send Telegram credentials
      const botToken = localStorage.getItem('telegram_bot_token');
      const chatId = localStorage.getItem('telegram_chat_id');
      
      if (botToken && chatId) {
        await axios.post(`${API_BASE}/update-telegram`, {
          bot_token: botToken,
          chat_id: chatId
        });
      }
      
      await axios.post(`${API_BASE}/start-scan`);
      setScanning(true);
      fetchScanData();
      fetchStats();
    } catch (error) {
      console.error('Error starting scan:', error);
    }
  };

  const stopScan = async () => {
    try {
      await axios.post(`${API_BASE}/stop-scan`);
      setScanning(false);
    } catch (error) {
      console.error('Error stopping scan:', error);
    }
  };

  const generateReport = async () => {
    try {
      const response = await axios.post(`${API_BASE}/generate-report`, {}, {
        responseType: 'blob'
      });
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `wifi_security_report_${Date.now()}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      console.error('Error generating report:', error);
    }
  };

  return (
    <div className="App">
      <header className="app-header">
        <h1>🛡️ WiFi Security Auditor</h1>
        <div className="header-controls">
          <button className="btn btn-settings" onClick={() => setShowSettings(true)}>
            ⚙️ Settings
          </button>
          {!scanning ? (
            <button className="btn btn-start" onClick={startScan}>
              Start Scan
            </button>
          ) : (
            <button className="btn btn-stop" onClick={stopScan}>
              Stop Scan
            </button>
          )}
          <button className="btn btn-report" onClick={generateReport}>
            Generate Report
          </button>
          {scanning && <span className="scanning-indicator">● Scanning...</span>}
        </div>
      </header>

      {showSettings && <Settings onClose={() => setShowSettings(false)} />}

      {scanData && stats ? (
        <Dashboard scanData={scanData} stats={stats} />
      ) : (
        <div className="welcome-screen">
          <div className="welcome-icon">🛡️</div>
          <h2>WiFi Security Auditor</h2>
          <p className="welcome-subtitle">Real-time network monitoring and threat detection</p>
          
          <div className="welcome-features">
            <div className="feature-item">
              <span className="feature-icon">📡</span>
              <span>Scan WiFi Networks</span>
            </div>
            <div className="feature-item">
              <span className="feature-icon">🔍</span>
              <span>Detect Security Threats</span>
            </div>
            <div className="feature-item">
              <span className="feature-icon">📊</span>
              <span>Analyze Risk Levels</span>
            </div>
            <div className="feature-item">
              <span className="feature-icon">📱</span>
              <span>Get Instant Alerts</span>
            </div>
          </div>

          <div className="welcome-actions">
            <button className="btn btn-primary-large" onClick={startScan}>
              🚀 Start Scanning
            </button>
            <button className="btn btn-secondary-large" onClick={() => setShowSettings(true)}>
              ⚙️ Configure Alerts
            </button>
          </div>

          <p className="welcome-note">
            💡 Configure Telegram alerts to receive instant threat notifications
          </p>
        </div>
      )}
    </div>
  );
}

export default App;
