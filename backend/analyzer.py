class SecurityAnalyzer:
    def __init__(self):
        self.vulnerabilities = []
    
    def analyze_network(self, network):
        """Analyze network for security vulnerabilities"""
        risk_score = 0
        vulnerabilities = []
        
        # Check encryption type
        encryption = network['encryption']
        if encryption == 'Open':
            risk_score += 50
            vulnerabilities.append('Open network - No encryption')
        elif encryption == 'WEP':
            risk_score += 40
            vulnerabilities.append('WEP encryption - Outdated and easily crackable')
        elif 'WPA' in encryption and 'WPA2' not in encryption and 'WPA3' not in encryption:
            risk_score += 30
            vulnerabilities.append('WPA encryption - Vulnerable to attacks')
        elif 'WPA2' in encryption:
            risk_score += 10
            vulnerabilities.append('WPA2 - Acceptable but WPA3 recommended')
        
        # Check for hidden network
        if network.get('hidden', False):
            risk_score += 15
            vulnerabilities.append('Hidden SSID - Security through obscurity')
        
        # Check signal strength (weak signals might indicate rogue AP)
        if network['signal_strength'] < -80:
            risk_score += 5
            vulnerabilities.append('Weak signal - Possible rogue AP or distance issue')
        
        # Determine risk level
        if risk_score >= 60:
            risk_level = 'High Risk 🔴'
            risk_category = 'high'
        elif risk_score >= 30:
            risk_level = 'Medium Risk 🟡'
            risk_category = 'medium'
        else:
            risk_level = 'Low Risk 🟢'
            risk_category = 'low'
        
        return {
            'risk_score': min(risk_score, 100),
            'risk_level': risk_level,
            'risk_category': risk_category,
            'vulnerabilities': vulnerabilities,
            'recommendations': self._get_recommendations(vulnerabilities)
        }
    
    def _get_recommendations(self, vulnerabilities):
        """Generate security recommendations"""
        recommendations = []
        
        for vuln in vulnerabilities:
            if 'Open network' in vuln:
                recommendations.append('Enable WPA3 or WPA2 encryption immediately')
            elif 'WEP' in vuln:
                recommendations.append('Upgrade to WPA3 or at minimum WPA2-PSK')
            elif 'WPA ' in vuln and 'WPA2' not in vuln:
                recommendations.append('Upgrade to WPA2 or WPA3 for better security')
            elif 'Hidden SSID' in vuln:
                recommendations.append('Consider unhiding SSID and use strong encryption instead')
            elif 'Weak signal' in vuln:
                recommendations.append('Verify AP legitimacy and check for rogue access points')
        
        if not recommendations:
            recommendations.append('Network appears secure - Continue monitoring')
        
        return recommendations
    
    def calculate_environment_score(self, networks):
        """Calculate overall environment security score"""
        if not networks:
            return 100
        
        total_score = sum(n.get('risk_score', 0) for n in networks)
        avg_risk = total_score / len(networks)
        
        # Invert score (lower risk = higher security)
        environment_score = max(0, 100 - avg_risk)
        
        return round(environment_score, 2)
