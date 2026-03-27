from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import json
import threading
import time
from scanner import WiFiScanner
from analyzer import SecurityAnalyzer
from detector import AttackDetector
from alerts import AlertSystem
from report_generator import ReportGenerator
from database import Database

app = Flask(__name__)
CORS(app)

# Default configuration (no config.json needed)
config = {
    'scan_interval': 30,  # seconds
    'database': {},  # Using SQLite by default
    'telegram': {}  # Configured via Settings UI
}

# Initialize components
scanner = WiFiScanner()
analyzer = SecurityAnalyzer()
detector = AttackDetector()
alert_system = AlertSystem(config)
report_gen = ReportGenerator()
db = Database(config.get('database', {}))

# Global state
current_scan_data = {
    'networks': [],
    'alerts': [],
    'devices': {},
    'environment_score': 100,
    'last_scan': None
}

scan_running = False

def background_scanner():
    """Background thread for continuous scanning"""
    global scan_running, current_scan_data
    
    while scan_running:
        try:
            # Scan networks
            networks = scanner.scan_networks()
            
            # Analyze each network
            analyzed_networks = []
            for network in networks:
                analysis = analyzer.analyze_network(network)
                network.update(analysis)
                analyzed_networks.append(network)
                
                # Save to database
                db.insert_network(network)
            
            # Sniff packets for attack detection
            packets = scanner.sniff_packets(duration=5)
            
            # Detect attacks
            alerts = detector.run_all_detections(analyzed_networks, packets)
            
            # Get connected devices
            devices = scanner.get_connected_devices(packets)
            
            # Calculate environment score
            env_score = analyzer.calculate_environment_score(analyzed_networks)
            
            # Update global state
            current_scan_data = {
                'networks': analyzed_networks,
                'alerts': alerts,
                'devices': devices,
                'environment_score': env_score,
                'last_scan': time.time()
            }
            
            # Save scan to database
            db.insert_scan(
                len(analyzed_networks),
                len(alerts),
                current_scan_data
            )
            
            # Send alerts
            for alert in alerts:
                db.insert_alert(
                    alert['type'],
                    alert['severity'],
                    alert['description'],
                    alert.get('details', {}).get('bssid', 'N/A'),
                    alert.get('details', {})
                )
                alert_system.send_threat_alert(alert)
            
            # Wait before next scan
            time.sleep(config.get('scan_interval', 30))
            
        except Exception as e:
            print(f"Scanner error: {e}")
            time.sleep(5)

@app.route('/api/update-telegram', methods=['POST'])
def update_telegram():
    """Update Telegram configuration"""
    try:
        data = request.json
        bot_token = data.get('bot_token')
        chat_id = data.get('chat_id')
        
        alert_system.update_telegram_config(bot_token, chat_id)
        
        return jsonify({
            'status': 'success',
            'message': 'Telegram configuration updated'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/start-scan', methods=['POST'])
def start_scan():
    """Start continuous scanning"""
    global scan_running
    
    if not scan_running:
        scan_running = True
        thread = threading.Thread(target=background_scanner, daemon=True)
        thread.start()
        return jsonify({'status': 'started', 'message': 'Scanning started'})
    
    return jsonify({'status': 'already_running', 'message': 'Scan already in progress'})

@app.route('/api/stop-scan', methods=['POST'])
def stop_scan():
    """Stop continuous scanning"""
    global scan_running
    scan_running = False
    return jsonify({'status': 'stopped', 'message': 'Scanning stopped'})

@app.route('/api/scan-data', methods=['GET'])
def get_scan_data():
    """Get current scan data"""
    return jsonify(current_scan_data)

@app.route('/api/networks', methods=['GET'])
def get_networks():
    """Get all detected networks"""
    networks = db.get_all_networks()
    return jsonify([dict(n) for n in networks])

@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    """Get recent alerts"""
    limit = request.args.get('limit', 50, type=int)
    alerts = db.get_recent_alerts(limit)
    return jsonify([dict(a) for a in alerts])

@app.route('/api/scan-history', methods=['GET'])
def get_scan_history():
    """Get scan history"""
    limit = request.args.get('limit', 10, type=int)
    scans = db.get_scan_history(limit)
    return jsonify([dict(s) for s in scans])

@app.route('/api/generate-report', methods=['POST'])
def generate_report():
    """Generate PDF report"""
    try:
        filename = f'wifi_security_report_{int(time.time())}.pdf'
        report_gen.generate_pdf_report(current_scan_data, filename)
        
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get statistics"""
    return jsonify({
        'total_networks': len(current_scan_data['networks']),
        'high_risk': len([n for n in current_scan_data['networks'] if n.get('risk_category') == 'high']),
        'medium_risk': len([n for n in current_scan_data['networks'] if n.get('risk_category') == 'medium']),
        'low_risk': len([n for n in current_scan_data['networks'] if n.get('risk_category') == 'low']),
        'total_alerts': len(current_scan_data['alerts']),
        'environment_score': current_scan_data['environment_score']
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'scanning': scan_running})

if __name__ == '__main__':
    print("Starting WiFi Security Auditor Backend...")
    print("Backend running on http://localhost:5000")
    app.run(debug=False, host='0.0.0.0', port=5000, threaded=True)
