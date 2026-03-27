import React, { useState } from 'react';
import './Settings.css';
import axios from 'axios';

const API_BASE = 'http://localhost:5000/api';

function Settings({ onClose }) {
  const [botToken, setBotToken] = useState(localStorage.getItem('telegram_bot_token') || '');
  const [chatId, setChatId] = useState(localStorage.getItem('telegram_chat_id') || '');
  const [saved, setSaved] = useState(false);

  const handleSave = async () => {
    localStorage.setItem('telegram_bot_token', botToken);
    localStorage.setItem('telegram_chat_id', chatId);
    
    // Send to backend
    try {
      await axios.post(`${API_BASE}/update-telegram`, {
        bot_token: botToken,
        chat_id: chatId
      });
      setSaved(true);
      setTimeout(() => setSaved(false), 3000);
    } catch (error) {
      console.error('Error saving settings:', error);
    }
  };

  return (
    <div className="settings-overlay">
      <div className="settings-modal">
        <div className="settings-header">
          <h2>⚙️ Telegram Alert Settings</h2>
          <button className="close-btn" onClick={onClose}>✕</button>
        </div>
        
        <div className="settings-content">
          <div className="settings-info">
            <h3>📱 How to get your Telegram credentials:</h3>
            <ol>
              <li>Open Telegram and search for <strong>@BotFather</strong></li>
              <li>Send <code>/newbot</code> and follow instructions</li>
              <li>Copy the <strong>Bot Token</strong> provided</li>
              <li>Search for <strong>@userinfobot</strong> in Telegram</li>
              <li>Send <code>/start</code> to get your <strong>Chat ID</strong></li>
            </ol>
          </div>

          <div className="form-group">
            <label>Telegram Bot Token</label>
            <input
              type="text"
              placeholder="1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"
              value={botToken}
              onChange={(e) => setBotToken(e.target.value)}
            />
          </div>

          <div className="form-group">
            <label>Telegram Chat ID</label>
            <input
              type="text"
              placeholder="123456789"
              value={chatId}
              onChange={(e) => setChatId(e.target.value)}
            />
          </div>

          <button className="save-btn" onClick={handleSave}>
            💾 Save Settings
          </button>

          {saved && (
            <div className="success-message">
              ✅ Settings saved successfully!
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Settings;
