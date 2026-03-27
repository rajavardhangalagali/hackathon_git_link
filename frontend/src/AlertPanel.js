import React from 'react';
import './AlertPanel.css';

function AlertPanel({ alerts }) {
  const getSeverityIcon = (severity) => {
    switch (severity) {
      case 'critical':
        return '🔴';
      case 'high':
        return '🟠';
      case 'medium':
        return '🟡';
      default:
        return '🟢';
    }
  };

  const getSeverityClass = (severity) => {
    return `alert-item severity-${severity}`;
  };

  return (
    <div className="alert-panel">
      {alerts && alerts.length > 0 ? (
        <div className="alerts-list">
          {alerts.map((alert, index) => (
            <div key={index} className={getSeverityClass(alert.severity)}>
              <div className="alert-header">
                <span className="alert-icon">{getSeverityIcon(alert.severity)}</span>
                <span className="alert-type">{alert.type}</span>
                <span className="alert-severity">{alert.severity.toUpperCase()}</span>
              </div>
              <div className="alert-description">{alert.description}</div>
              {alert.details && (
                <div className="alert-details">
                  <pre>{JSON.stringify(alert.details, null, 2)}</pre>
                </div>
              )}
            </div>
          ))}
        </div>
      ) : (
        <div className="no-alerts">
          <span className="no-alerts-icon">✅</span>
          <p>No security threats detected</p>
        </div>
      )}
    </div>
  );
}

export default AlertPanel;
