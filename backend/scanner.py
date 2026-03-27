try:
    import pywifi
    from pywifi import const
    PYWIFI_AVAILABLE = True
except:
    PYWIFI_AVAILABLE = False
    print("ERROR: pywifi not available. Install with: pip install pywifi")

from scapy.all import *
import time
from collections import defaultdict
import subprocess
import platform

class WiFiScanner:
    def __init__(self):
        if not PYWIFI_AVAILABLE:
            raise Exception("pywifi library is required for WiFi scanning")
        
        try:
            self.wifi = pywifi.PyWiFi()
            self.iface = self.wifi.interfaces()[0] if self.wifi.interfaces() else None
            if not self.iface:
                raise Exception("No WiFi interface found")
            print(f"WiFi interface initialized: {self.iface.name()}")
        except Exception as e:
            raise Exception(f"Failed to initialize WiFi interface: {e}")
        
        self.networks = []
        self.devices = defaultdict(dict)
        self.os_type = platform.system()
    
    def get_connected_network_windows(self):
        """Get connected network on Windows using netsh"""
        try:
            result = subprocess.run(
                ['netsh', 'wlan', 'show', 'interfaces'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                output = result.stdout
                for line in output.split('\n'):
                    if 'SSID' in line and 'BSSID' not in line:
                        # Extract SSID
                        ssid = line.split(':', 1)[1].strip()
                        if ssid:
                            print(f"Detected connected network (Windows): {ssid}")
                            return ssid
        except Exception as e:
            print(f"Windows netsh detection failed: {e}")
        return None
    
    def get_connected_network_linux(self):
        """Get connected network on Linux using iwgetid"""
        try:
            result = subprocess.run(
                ['iwgetid', '-r'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                ssid = result.stdout.strip()
                if ssid:
                    print(f"Detected connected network (Linux): {ssid}")
                    return ssid
        except Exception as e:
            print(f"Linux iwgetid detection failed: {e}")
        return None
    
    def get_connected_network(self):
        """Get currently connected WiFi network (cross-platform)"""
        connected_ssid = None
        
        # Try OS-specific methods first
        if self.os_type == 'Windows':
            connected_ssid = self.get_connected_network_windows()
        elif self.os_type == 'Linux':
            connected_ssid = self.get_connected_network_linux()
        
        # Fallback to pywifi method
        if not connected_ssid:
            try:
                if self.iface.status() == const.IFACE_CONNECTED:
                    profile = self.iface.network_profiles()
                    if profile:
                        connected_ssid = profile[0].ssid
                        print(f"Detected connected network (pywifi): {connected_ssid}")
            except Exception as e:
                print(f"pywifi detection failed: {e}")
        
        return connected_ssid
        
    def scan_networks(self):
        """Scan for WiFi networks using pywifi - REAL DATA ONLY"""
        if not self.iface:
            raise Exception("WiFi interface not available")
        
        try:
            print("Starting WiFi scan...")
            
            # Get currently connected network using multiple methods
            connected_ssid = self.get_connected_network()
            
            if connected_ssid:
                print(f"✅ Currently connected to: {connected_ssid}")
            else:
                print("⚠️ No connected network detected")
            
            self.iface.scan()
            time.sleep(3)  # Wait for scan to complete
            scan_results = self.iface.scan_results()
            
            if not scan_results:
                print("No networks found in scan")
                return []
            
            networks = []
            for network in scan_results:
                try:
                    encryption = self._get_encryption_type(network)
                    
                    # Check if this network is the connected one
                    is_connected = False
                    if connected_ssid:
                        # Match by SSID (case-insensitive)
                        is_connected = (network.ssid.lower() == connected_ssid.lower()) if network.ssid else False
                    
                    network_info = {
                        'ssid': network.ssid if network.ssid else '<Hidden Network>',
                        'bssid': network.bssid,
                        'signal_strength': network.signal,
                        'channel': self._freq_to_channel(network.freq),
                        'encryption': encryption,
                        'hidden': not bool(network.ssid),
                        'connected': is_connected
                    }
                    networks.append(network_info)
                    
                    status = "⭐ CONNECTED" if is_connected else ""
                    print(f"Found network: {network_info['ssid']} ({network_info['encryption']}) {status}")
                except Exception as e:
                    print(f"Error processing network: {e}")
                    continue
            
            self.networks = networks
            print(f"Scan complete: {len(networks)} networks found")
            return networks
            
        except Exception as e:
            print(f"Scan error: {e}")
            raise Exception(f"WiFi scan failed: {e}")
    
    def _get_encryption_type(self, network):
        """Determine encryption type from real network data"""
        try:
            akm = network.akm
            
            if not akm or akm == [const.AKM_TYPE_NONE]:
                return 'Open'
            elif const.AKM_TYPE_WPA3PSK in akm or const.AKM_TYPE_WPA3 in akm:
                return 'WPA3'
            elif const.AKM_TYPE_WPA2PSK in akm or const.AKM_TYPE_WPA2 in akm:
                return 'WPA2-PSK'
            elif const.AKM_TYPE_WPAPSK in akm or const.AKM_TYPE_WPA in akm:
                return 'WPA-PSK'
            else:
                return 'WEP'
        except:
            return 'Unknown'
    
    def _freq_to_channel(self, freq):
        """Convert frequency to channel number"""
        if freq >= 2412 and freq <= 2484:
            return (freq - 2412) // 5 + 1
        elif freq >= 5170 and freq <= 5825:
            return (freq - 5170) // 5 + 34
        return 0
    
    def sniff_packets(self, duration=10, interface=None):
        """Sniff network packets for attack detection - REAL DATA ONLY"""
        packets = []
        
        def packet_handler(pkt):
            packets.append(pkt)
        
        try:
            print(f"Starting packet capture for {duration} seconds...")
            if interface:
                sniff(iface=interface, prn=packet_handler, timeout=duration, store=False)
            else:
                # Try to sniff on default interface
                sniff(prn=packet_handler, timeout=duration, store=False, count=100)
            print(f"Captured {len(packets)} packets")
        except Exception as e:
            print(f"Packet sniffing error: {e}")
            print("Note: Packet sniffing requires administrator/root privileges")
        
        return packets
    
    def get_connected_devices(self, packets):
        """Extract connected devices from captured packets - REAL DATA ONLY"""
        devices = {}
        
        if not packets:
            print("No packets to analyze for devices")
            return devices
        
        for pkt in packets:
            try:
                if pkt.haslayer(Dot11):
                    if pkt.type == 0 and pkt.subtype == 8:  # Beacon frame
                        bssid = pkt.addr2
                        try:
                            ssid = pkt.info.decode()
                        except:
                            ssid = '<Hidden>'
                        
                        if bssid not in devices:
                            devices[bssid] = {
                                'type': 'AP',
                                'ssid': ssid,
                                'packets': 0
                            }
                        devices[bssid]['packets'] += 1
                    
                    elif pkt.type == 2:  # Data frame
                        src = pkt.addr2
                        dst = pkt.addr1
                        
                        for addr in [src, dst]:
                            if addr and addr not in devices:
                                devices[addr] = {
                                    'type': 'Client',
                                    'ssid': 'Unknown',
                                    'packets': 0
                                }
                            if addr:
                                devices[addr]['packets'] += 1
            except Exception as e:
                continue
        
        print(f"Identified {len(devices)} devices from packet capture")
        return devices
