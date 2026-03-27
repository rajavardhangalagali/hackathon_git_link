from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.platypus import Image as RLImage
from datetime import datetime
import io

class ReportGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=1
        )
    
    def generate_pdf_report(self, scan_data, filename='wifi_security_report.pdf'):
        """Generate comprehensive PDF security report"""
        doc = SimpleDocTemplate(filename, pagesize=letter)
        story = []
        
        # Title
        title = Paragraph("WiFi Security Audit Report", self.title_style)
        story.append(title)
        story.append(Spacer(1, 0.2*inch))
        
        # Scan Summary
        scan_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        summary_data = [
            ['Scan Date/Time:', scan_time],
            ['Networks Found:', str(len(scan_data.get('networks', [])))],
            ['Threats Detected:', str(len(scan_data.get('alerts', [])))],
            ['Environment Score:', f"{scan_data.get('environment_score', 0)}/100"]
        ]
        
        summary_table = Table(summary_data, colWidths=[2.5*inch, 3*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e0e0e0')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(Paragraph("<b>Scan Summary</b>", self.styles['Heading2']))
        story.append(Spacer(1, 0.1*inch))
        story.append(summary_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Networks Risk Table
        story.append(Paragraph("<b>Network Risk Assessment</b>", self.styles['Heading2']))
        story.append(Spacer(1, 0.1*inch))
        
        network_data = [['SSID', 'Encryption', 'Risk Score', 'Risk Level']]
        for network in scan_data.get('networks', []):
            network_data.append([
                network.get('ssid', 'N/A')[:20],
                network.get('encryption', 'N/A'),
                str(network.get('risk_score', 0)),
                network.get('risk_level', 'N/A')
            ])
        
        network_table = Table(network_data, colWidths=[2*inch, 1.5*inch, 1*inch, 1.5*inch])
        network_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4a4a4a')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(network_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Attack Findings
        if scan_data.get('alerts'):
            story.append(Paragraph("<b>Security Threats Detected</b>", self.styles['Heading2']))
            story.append(Spacer(1, 0.1*inch))
            
            alert_data = [['Type', 'Severity', 'Description']]
            for alert in scan_data.get('alerts', []):
                alert_data.append([
                    alert.get('type', 'N/A')[:25],
                    alert.get('severity', 'N/A'),
                    alert.get('description', 'N/A')[:40]
                ])
            
            alert_table = Table(alert_data, colWidths=[2*inch, 1.5*inch, 2.5*inch])
            alert_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#d32f2f')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ffebee')),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(alert_table)
            story.append(Spacer(1, 0.3*inch))
        
        # Security Recommendations
        story.append(Paragraph("<b>Security Recommendations</b>", self.styles['Heading2']))
        story.append(Spacer(1, 0.1*inch))
        
        recommendations = self._generate_recommendations(scan_data)
        for i, rec in enumerate(recommendations, 1):
            story.append(Paragraph(f"{i}. {rec}", self.styles['Normal']))
            story.append(Spacer(1, 0.1*inch))
        
        # Build PDF
        doc.build(story)
        return filename
    
    def _generate_recommendations(self, scan_data):
        """Generate security recommendations based on scan data"""
        recommendations = []
        
        networks = scan_data.get('networks', [])
        alerts = scan_data.get('alerts', [])
        
        # Check for open networks
        open_networks = [n for n in networks if n.get('encryption') == 'Open']
        if open_networks:
            recommendations.append(
                f"Found {len(open_networks)} open network(s). Enable WPA3 or WPA2 encryption immediately."
            )
        
        # Check for WEP
        wep_networks = [n for n in networks if n.get('encryption') == 'WEP']
        if wep_networks:
            recommendations.append(
                f"Found {len(wep_networks)} network(s) using WEP. Upgrade to WPA2 or WPA3 immediately."
            )
        
        # Check for attacks
        if alerts:
            recommendations.append(
                f"Detected {len(alerts)} security threat(s). Investigate and mitigate immediately."
            )
        
        # General recommendations
        recommendations.append("Regularly update router firmware to patch security vulnerabilities.")
        recommendations.append("Use strong, unique passwords for WiFi networks (minimum 12 characters).")
        recommendations.append("Enable MAC address filtering for additional security layer.")
        recommendations.append("Disable WPS (WiFi Protected Setup) as it's vulnerable to brute force attacks.")
        recommendations.append("Monitor network regularly for unauthorized devices and rogue access points.")
        
        return recommendations
