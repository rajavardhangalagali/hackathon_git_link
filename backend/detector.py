from scapy.all import *
from collections import defaultdict
import time

class AttackDetector:
    def __init__(self):
        self.known_networks = {}
        self.deauth_count = defaultdict(int)
        self.arp_table = {}
        self.packet_injection_count = defaultdict(int)
        self.alerts = []
    
    def detect_evil_twin(self, networks):
        """Detect Evil Twin attacks (same SSID, different MAC)"""
        ssid_map = defaultdict(list)
        alerts = []
        
        for network in networks:
            ssid = network['ssid']
            if ssid and ssid != '<Hidden Network>':
                ssid_map[ssid].append(network['bssid'])
        
        for ssid, bssids in ssid_map.items():
            if len(bssids) > 1:
                alerts.append({
                    'type': 'Evil Twin Attack',
                    'severity': 'high',
                    'description': f'Multiple APs with same SSID "{ssid}" detected',
                    'details': {
                        'ssid': ssid,
                        'bssids': bssids,
                        'count': len(bssids)
                    }
                })
        
        return alerts
    
    def detect_deauth_attack(self, packets):
        """Detect Deauthentication attacks"""
        alerts = []
        deauth_threshold = 5
        
        for pkt in packets:
            if pkt.haslayer(Dot11Deauth):
                bssid = pkt.addr2
                self.deauth_count[bssid] += 1
                
                if self.deauth_count[bssid] >= deauth_threshold:
                    alerts.append({
                        'type': 'Deauthentication Attack',
                        'severity': 'critical',
                        'description': f'Multiple deauth frames from {bssid}',
                        'details': {
                            'bssid': bssid,
                            'deauth_count': self.deauth_count[bssid]
                        }
                    })
        
        return alerts
    
    def detect_rogue_ap(self, networks):
        """Detect Rogue Access Points"""
        alerts = []
        
        for network in networks:
            # Check for suspicious characteristics
            suspicious = False
            reasons = []
            
            # Very strong signal might indicate unauthorized AP nearby
            if network['signal_strength'] > -30:
                suspicious = True
                reasons.append('Unusually strong signal')
            
            # Open network in enterprise environment
            if network['encryption'] == 'Open':
                suspicious = True
                reasons.append('Open network detected')
            
            # Hidden network with weak encryption
            if network.get('hidden') and network['encryption'] in ['Open', 'WEP']:
                suspicious = True
                reasons.append('Hidden network with weak encryption')
            
            if suspicious:
                alerts.append({
                    'type': 'Rogue Access Point',
                    'severity': 'high',
                    'description': f'Suspicious AP detected: {network["ssid"]}',
                    'details': {
                        'ssid': network['ssid'],
                        'bssid': network['bssid'],
                        'reasons': reasons
                    }
                })
        
        return alerts
    
    def detect_mitm_attack(self, packets):
        """Detect Man-in-the-Middle attacks"""
        alerts = []
        
        # Look for ARP spoofing indicators
        arp_packets = [pkt for pkt in packets if pkt.haslayer(ARP)]
        
        for pkt in arp_packets:
            if pkt[ARP].op == 2:  # ARP reply
                ip = pkt[ARP].psrc
                mac = pkt[ARP].hwsrc
                
                if ip in self.arp_table and self.arp_table[ip] != mac:
                    alerts.append({
                        'type': 'MITM Attack (ARP Spoofing)',
                        'severity': 'critical',
                        'description': f'ARP spoofing detected for IP {ip}',
                        'details': {
                            'ip': ip,
                            'old_mac': self.arp_table[ip],
                            'new_mac': mac
                        }
                    })
                
                self.arp_table[ip] = mac
        
        return alerts
    
    def detect_arp_spoofing(self, packets):
        """Detect ARP Spoofing attacks"""
        alerts = []
        arp_replies = defaultdict(list)
        
        for pkt in packets:
            if pkt.haslayer(ARP) and pkt[ARP].op == 2:
                src_ip = pkt[ARP].psrc
                src_mac = pkt[ARP].hwsrc
                arp_replies[src_ip].append(src_mac)
        
        for ip, macs in arp_replies.items():
            unique_macs = set(macs)
            if len(unique_macs) > 1:
                alerts.append({
                    'type': 'ARP Spoofing',
                    'severity': 'critical',
                    'description': f'Multiple MAC addresses for IP {ip}',
                    'details': {
                        'ip': ip,
                        'mac_addresses': list(unique_macs)
                    }
                })
        
        return alerts
    
    def detect_packet_injection(self, packets):
        """Detect Packet Injection attacks"""
        alerts = []
        injection_threshold = 100
        
        for pkt in packets:
            if pkt.haslayer(Dot11):
                src = pkt.addr2
                if src:
                    self.packet_injection_count[src] += 1
                    
                    # High packet rate from single source
                    if self.packet_injection_count[src] > injection_threshold:
                        alerts.append({
                            'type': 'Packet Injection',
                            'severity': 'high',
                            'description': f'High packet rate from {src}',
                            'details': {
                                'source': src,
                                'packet_count': self.packet_injection_count[src]
                            }
                        })
        
        return alerts
    
    def run_all_detections(self, networks, packets):
        """Run all attack detection methods"""
        all_alerts = []
        
        all_alerts.extend(self.detect_evil_twin(networks))
        all_alerts.extend(self.detect_deauth_attack(packets))
        all_alerts.extend(self.detect_rogue_ap(networks))
        all_alerts.extend(self.detect_mitm_attack(packets))
        all_alerts.extend(self.detect_arp_spoofing(packets))
        all_alerts.extend(self.detect_packet_injection(packets))
        
        return all_alerts
