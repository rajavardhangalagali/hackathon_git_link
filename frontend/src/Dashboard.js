import React from 'react';
import './Dashboard.css';
import NetworkMap from './NetworkMap';
import Charts from './Charts';
import AlertPanel from './AlertPanel';

function Dashboard({ scanData, stats }) {
  return (
    <div className="dashboard">
      {/* Stats Cards */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">📡</div>
          <div className="stat-content">
            <h3>Networks Found</h3>
            <p className="stat-value">{stats.total_networks}</p>
          </div>
        </div>
        
        <div className="stat-card connected">
          <div className="stat-icon">⭐</div>
          <div className="stat-content">
            <h3>Connected Network</h3>
            <div className="stat-value connected-name">
              {(() => {
                const connectedNet = scanData.networks.find(n => n.connected);
                if (!connectedNet) return 'None';
                
                const riskEmoji = connectedNet.risk_category === 'high' ? '🔴' : 
                                 connectedNet.risk_category === 'medium' ? '🟡' : '🟢';
                
                return (
                  <>
                    <div>{connectedNet.ssid}</div>
                    <div className="connected-score">
                      {riskEmoji} Score: {connectedNet.risk_score}/100
                    </div>
                  </>
                );
              })()}
            </div>
          </div>
        </div>
        
        <div className="stat-card high-risk">
          <div className="stat-icon">🔴</div>
          <div className="stat-content">
            <h3>High Risk</h3>
            <p className="stat-value">{stats.high_risk}</p>
          </div>
        </div>
        
        <div className="stat-card medium-risk">
          <div className="stat-icon">🟡</div>
          <div className="stat-content">
            <h3>Medium Risk</h3>
            <p className="stat-value">{stats.medium_risk}</p>
          </div>
        </div>
        
        <div className="stat-card low-risk">
          <div className="stat-icon">🟢</div>
          <div className="stat-content">
            <h3>Low Risk</h3>
            <p className="stat-value">{stats.low_risk}</p>
          </div>
        </div>
        
        <div className="stat-card alerts">
          <div className="stat-icon">⚠️</div>
          <div className="stat-content">
            <h3>Active Alerts</h3>
            <p className="stat-value">{stats.total_alerts}</p>
          </div>
        </div>
        
        <div className="stat-card score">
          <div className="stat-icon">🛡️</div>
          <div className="stat-content">
            <h3>Security Score</h3>
            <p className="stat-value">{stats.environment_score.toFixed(1)}/100</p>
          </div>
        </div>
      </div>

      {/* Main Content Grid */}
      <div className="content-grid">
        <div className="panel network-map-panel">
          <h2>Network Map</h2>
          <NetworkMap networks={scanData.networks} devices={scanData.devices} />
        </div>

        <div className="panel charts-panel">
          <h2>Analytics</h2>
          <Charts networks={scanData.networks} />
        </div>

        <div className="panel alerts-panel">
          <h2>Live Alerts</h2>
          <AlertPanel alerts={scanData.alerts} />
        </div>
      </div>

      {/* Networks Table */}
      <div className="panel networks-table-panel">
        <h2>Detected Networks</h2>
        <div className="table-container">
          <table className="networks-table">
            <thead>
              <tr>
                <th>SSID</th>
                <th>BSSID</th>
                <th>Encryption</th>
                <th>Channel</th>
                <th>Signal</th>
                <th>Risk Score</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {scanData.networks.map((network, index) => (
                <tr key={index} className={`risk-${network.risk_category} ${network.connected ? 'connected-row' : ''}`}>
                  <td>
                    {network.connected && <span className="connected-badge">⭐ </span>}
                    {network.ssid}
                  </td>
                  <td className="monospace">{network.bssid}</td>
                  <td>{network.encryption}</td>
                  <td>{network.channel}</td>
                  <td>{network.signal_strength} dBm</td>
                  <td>{network.risk_score}</td>
                  <td>{network.risk_level}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
