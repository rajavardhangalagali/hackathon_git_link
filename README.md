# 🛡️ WiFi Security Auditor

<div align="center">

![WiFi Security](https://img.shields.io/badge/WiFi-Security-green?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**Advanced WiFi Security Auditor with Real-time Attack Detection & Professional Dashboard**

[Features](#-features) • [Demo](#-demo) • [Installation](#-installation) • [Usage](#-usage) • [Tech Stack](#-tech-stack) • [License](#-license)

</div>

---

## 📺 Demo

### 🎥 Video Demo


https://github.com/user-attachments/assets/a9b5f5e9-651e-4980-a708-ff3617dfcddc




## ✨ Features

### 🔍 Network Scanning
- **Real-time WiFi scanning** using pywifi
- Detects SSID, BSSID, encryption type, signal strength, and channel
- Identifies hidden networks
- Shows currently connected network with visual indicators
- Auto-refresh every 30 seconds

### 🛡️ Security Analysis
- **Risk scoring system** (0-100 for each network)
- Color-coded risk levels: 🔴 High Risk, 🟡 Medium Risk, 🟢 Low Risk
- Flags open networks and outdated encryption (WEP/WPA)
- Environment security score calculation
- Comprehensive vulnerability assessment

### 🚨 Attack Detection
- **Evil Twin Attack** - Detects duplicate SSIDs with different MAC addresses
- **Deauthentication Attack** - Identifies devices being kicked off networks
- **MITM Detection** - Man-in-the-Middle attack indicators
- **Rogue Access Point** - Unauthorized AP detection
- **ARP Spoofing** - Network poisoning attempts
- **Packet Injection** - Abnormal packet rate detection

### 📊 Professional Dashboard
- **Interactive Network Map** - D3.js visualization with drag-and-drop nodes
- **Real-time Charts** - Plotly.js powered analytics
  - Encryption type distribution (pie chart)
  - Signal strength comparison (bar chart)
  - Risk heatmap
- **Live Alert Panel** - Real-time threat notifications
- **Responsive Design** - Works on desktop, tablet, and mobile
- **Dark Mode UI** - Professional cybersecurity aesthetic

### 📱 Telegram Alerts
- Real-time threat notifications via Telegram
- Configurable through Settings UI
- No email or SMS dependencies
- Instant alerts for critical threats

### 📄 PDF Reports
- One-click report generation
- Comprehensive scan summary
- Risk assessment tables
- Attack findings
- Security recommendations
- Overall environment security score

### 💾 Database Logging
- SQLite database for all events
- Timestamped alerts and scans
- Historical scan comparison
- Network tracking over time
- Persistent data storage

---

## 🚀 Installation

### Prerequisites

- **Python 3.8+**
- **Node.js 16+**
- **WiFi adapter** with monitor mode support (for packet sniffing)
- **Administrator/Root privileges** (required for WiFi scanning)

### 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/wifi-security-auditor.git
cd wifi-security-auditor
```

### 2. Backend Setup

```bash
cd backend
pip install -r requirements.txt
```

**Dependencies:**
- Flask 3.0.0 - Web framework
- Flask-CORS 4.0.0 - Cross-origin support
- Scapy 2.5.0 - Packet analysis
- pywifi 1.1.12 - WiFi scanning
- ReportLab 4.0.7 - PDF generation
- python-telegram-bot 20.7 - Telegram integration

### 3. Frontend Setup

```bash
cd frontend
npm install
```

**Dependencies:**
- React 18.2.0 - UI framework
- D3.js 7.8.5 - Network visualization
- Plotly.js 2.27.1 - Charts and graphs
- Axios 1.6.2 - HTTP client

### 4. Configuration

**No configuration file needed!** All settings are configured through the web interface.

**Telegram Alerts (Optional):**
1. Click "⚙️ Settings" in the app
2. Get bot token from [@BotFather](https://t.me/botfather)
3. Get chat ID from [@userinfobot](https://t.me/userinfobot)
4. Enter credentials and save

**Database:**
- Uses SQLite by default (`wifi_auditor.db`)
- Automatically created on first run
- No setup required

---

## 🎯 Usage

### Quick Start

**Terminal 1 - Start Backend:**
```bash
cd backend
sudo python app.py  # Requires admin for WiFi scanning
```

**Terminal 2 - Start Frontend:**
```bash
cd frontend
npm start
```

**Access the app:**
```
http://localhost:3000
```

### Step-by-Step Guide

1. **Start the application** (both backend and frontend)
2. **Configure Telegram alerts** (optional) via Settings
3. **Click "Start Scan"** to begin monitoring
4. **View real-time data:**
   - Network map visualization
   - Security analytics
   - Live threat alerts
5. **Generate PDF report** when needed
6. **Click "Stop Scan"** when finished

### Important Notes

⚠️ **Administrator Privileges Required**
- Backend needs root/admin access for WiFi scanning
- Run backend with `sudo` (Linux/Mac) or as Administrator (Windows)

⚠️ **WiFi Adapter Required**
- Physical WiFi adapter needed for scanning
- Monitor mode capability recommended for packet sniffing
- Cannot run on cloud platforms (AWS, Heroku, etc.)

⚠️ **Legal & Ethical Use**
- Only scan networks you own or have permission to audit
- Unauthorized network scanning may be illegal
- Use responsibly and ethically

---

## 🏗️ Tech Stack

### Backend
- **Python 3.8+** - Core language
- **Flask** - REST API framework
- **Scapy** - Packet analysis and sniffing
- **pywifi** - WiFi network scanning
- **SQLite** - Database
- **ReportLab** - PDF generation
- **python-telegram-bot** - Alert system

### Frontend
- **React 18** - UI framework
- **D3.js** - Network map visualization
- **Plotly.js** - Interactive charts
- **Axios** - API communication
- **CSS3** - Responsive styling

### Architecture
```
┌─────────────────┐         ┌──────────────────┐
│  React Frontend │ ◄─────► │  Flask Backend   │
│  (Port 3000)    │  HTTP   │  (Port 5000)     │
└─────────────────┘         └──────────────────┘
                                     │
                    ┌────────────────┼────────────────┐
                    │                │                │
              ┌─────▼─────┐   ┌─────▼─────┐   ┌─────▼─────┐
              │  pywifi   │   │   Scapy   │   │  SQLite   │
              │  Scanner  │   │  Detector │   │  Database │
              └───────────┘   └───────────┘   └───────────┘
```

---

## 📁 Project Structure

```
wifi-security-auditor/
├── backend/
│   ├── app.py                 # Flask API server
│   ├── scanner.py             # WiFi scanning logic
│   ├── analyzer.py            # Security analysis
│   ├── detector.py            # Attack detection
│   ├── alerts.py              # Telegram alerts
│   ├── report_generator.py   # PDF reports
│   ├── database.py            # SQLite operations
│   ├── requirements.txt       # Python dependencies
│   └── wifi_auditor.db        # SQLite database (auto-created)
│
├── frontend/
│   ├── public/
│   │   └── index.html         # HTML template
│   ├── src/
│   │   ├── App.js             # Main app component
│   │   ├── Dashboard.js       # Dashboard view
│   │   ├── NetworkMap.js      # D3.js network visualization
│   │   ├── Charts.js          # Plotly charts
│   │   ├── AlertPanel.js      # Live alerts
│   │   ├── Settings.js        # Settings modal
│   │   └── *.css              # Component styles
│   ├── package.json           # Node dependencies
│   └── .env                   # Environment variables
│
├── .gitignore                 # Git ignore rules
└── README.md                  # This file
```

---

## 🔒 Security Considerations

### Legal Notice
This tool is designed for:
- ✅ Auditing your own networks
- ✅ Educational purposes in controlled environments
- ✅ Authorized security assessments with proper permissions

**⚠️ WARNING:** Unauthorized network scanning, packet sniffing, or attack detection on networks you don't own may be illegal in your jurisdiction. Always obtain proper authorization before use.

### Ethical Use Guidelines
- Only scan networks you own or have explicit permission to audit
- Packet sniffing requires elevated privileges (root/admin)
- Some features may require WiFi adapter in monitor mode
- Respect privacy and legal boundaries
- Use for defensive security purposes only

### Data Privacy
- All data stored locally in SQLite database
- No data sent to external servers (except Telegram alerts if configured)
- Telegram credentials stored in browser localStorage
- No cloud dependencies

---

## 🎨 Features Showcase

### Dashboard Stats
- 📡 Networks Found
- ⭐ Connected Network (with security score)
- 🔴 High Risk Networks
- 🟡 Medium Risk Networks
- 🟢 Low Risk Networks
- ⚠️ Active Alerts
- 🛡️ Environment Security Score

### Network Map
- Interactive D3.js force-directed graph
- Drag-and-drop nodes
- Color-coded by risk level
- Shows your device connection
- Real-time updates
- Responsive design

### Analytics Charts
- **Encryption Distribution** - Pie chart showing encryption types
- **Signal Strength** - Bar chart comparing network signals
- **Risk Heatmap** - Visual risk assessment across networks

### Alert System
- Real-time threat notifications
- Severity-based color coding (Critical, High, Medium, Low)
- Detailed alert information
- Telegram integration for remote alerts

---

## 🐛 Troubleshooting

### Permission Issues
```bash
# Linux/Mac - Run with sudo
sudo python app.py

# Windows - Run PowerShell as Administrator
```

### WiFi Adapter Not Found
```bash
# Check available interfaces
ip link show  # Linux
ifconfig      # Mac
ipconfig      # Windows
```

### Port Already in Use
```bash
# Kill process on port 5000 (backend)
lsof -ti:5000 | xargs kill  # Mac/Linux
netstat -ano | findstr :5000  # Windows

# Kill process on port 3000 (frontend)
lsof -ti:3000 | xargs kill  # Mac/Linux
netstat -ano | findstr :3000  # Windows
```

### Database Issues
```bash
# Delete and recreate database
rm backend/wifi_auditor.db
# Restart backend - database will be recreated
```

### Frontend Build Issues
```bash
# Clear cache and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install
```

---

## 🚧 Roadmap

- [ ] User authentication system
- [ ] Multi-user support
- [ ] Historical data visualization
- [ ] Export data to CSV/JSON
- [ ] Custom alert rules
- [ ] Email alert integration
- [ ] Advanced packet analysis
- [ ] Network performance metrics
- [ ] Scheduled scanning
- [ ] API documentation

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Use ESLint for JavaScript code
- Write meaningful commit messages
- Add comments for complex logic
- Test thoroughly before submitting

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 WiFi Security Auditor

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## ⚠️ Disclaimer

This tool is provided for educational and authorized security testing purposes only. The developers are not responsible for any misuse or damage caused by this tool. Always obtain proper authorization before scanning or testing networks.

**Use at your own risk. Always comply with local laws and regulations.**

---

## 📧 Contact & Support

- **Issues:** [GitHub Issues](https://github.com/YOUR_USERNAME/wifi-security-auditor/issues)
- **Discussions:** [GitHub Discussions](https://github.com/YOUR_USERNAME/wifi-security-auditor/discussions)
- **Email:** your.email@example.com

---

## 🌟 Acknowledgments

- [Scapy](https://scapy.net/) - Packet manipulation library
- [pywifi](https://github.com/awkman/pywifi) - WiFi scanning library
- [D3.js](https://d3js.org/) - Data visualization
- [Plotly](https://plotly.com/) - Interactive charts
- [React](https://reactjs.org/) - UI framework
- [Flask](https://flask.palletsprojects.com/) - Web framework

---

## 📊 Stats

![GitHub stars](https://img.shields.io/github/stars/YOUR_USERNAME/wifi-security-auditor?style=social)
![GitHub forks](https://img.shields.io/github/forks/YOUR_USERNAME/wifi-security-auditor?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/YOUR_USERNAME/wifi-security-auditor?style=social)

---

<div align="center">

**Made with ❤️ for Cybersecurity**

**⭐ Star this repo if you find it useful!**

[⬆ Back to Top](#️-wifi-security-auditor)

</div>
