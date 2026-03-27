import sqlite3
import json
from datetime import datetime

class Database:
    def __init__(self, config=None):
        self.config = config or {}
        self.conn = None
        self.connect()
        self.init_tables()
    
    def connect(self):
        try:
            # Use SQLite for simplicity
            self.conn = sqlite3.connect('wifi_auditor.db', check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
        except Exception as e:
            print(f"Database connection error: {e}")
    
    def init_tables(self):
        cursor = self.conn.cursor()
        
        # Networks table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS networks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ssid TEXT,
                bssid TEXT UNIQUE,
                encryption TEXT,
                channel INTEGER,
                signal_strength INTEGER,
                risk_score INTEGER,
                risk_level TEXT,
                first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Alerts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                alert_type TEXT,
                severity TEXT,
                description TEXT,
                network_bssid TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                details TEXT
            )
        """)
        
        # Scans table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scan_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                networks_found INTEGER,
                threats_detected INTEGER,
                scan_data TEXT
            )
        """)
        
        self.conn.commit()
        cursor.close()
    
    def insert_network(self, network_data):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO networks (ssid, bssid, encryption, channel, signal_strength, risk_score, risk_level)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(bssid) DO UPDATE SET
                signal_strength = excluded.signal_strength,
                last_seen = CURRENT_TIMESTAMP
        """, (
            network_data['ssid'],
            network_data['bssid'],
            network_data['encryption'],
            network_data['channel'],
            network_data['signal_strength'],
            network_data['risk_score'],
            network_data['risk_level']
        ))
        self.conn.commit()
        cursor.close()
    
    def insert_alert(self, alert_type, severity, description, bssid, details):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO alerts (alert_type, severity, description, network_bssid, details)
            VALUES (?, ?, ?, ?, ?)
        """, (alert_type, severity, description, bssid, json.dumps(details)))
        self.conn.commit()
        cursor.close()
    
    def insert_scan(self, networks_found, threats_detected, scan_data):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO scans (networks_found, threats_detected, scan_data)
            VALUES (?, ?, ?)
        """, (networks_found, threats_detected, json.dumps(scan_data)))
        self.conn.commit()
        cursor.close()
    
    def get_recent_alerts(self, limit=50):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM alerts ORDER BY timestamp DESC LIMIT ?
        """, (limit,))
        alerts = [dict(row) for row in cursor.fetchall()]
        cursor.close()
        return alerts
    
    def get_scan_history(self, limit=10):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM scans ORDER BY scan_timestamp DESC LIMIT ?
        """, (limit,))
        scans = [dict(row) for row in cursor.fetchall()]
        cursor.close()
        return scans
    
    def get_all_networks(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM networks ORDER BY last_seen DESC")
        networks = [dict(row) for row in cursor.fetchall()]
        cursor.close()
        return networks
