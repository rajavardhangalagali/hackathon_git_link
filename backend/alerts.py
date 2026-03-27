import asyncio
from telegram import Bot

class AlertSystem:
    def __init__(self, config):
        self.config = config
        self.telegram_bot = None
        self.bot_token = None
        self.chat_id = None
        
        if config.get('telegram'):
            self.update_telegram_config(
                config['telegram'].get('bot_token'),
                config['telegram'].get('chat_id')
            )
    
    def update_telegram_config(self, bot_token, chat_id):
        """Update Telegram configuration"""
        self.bot_token = bot_token
        self.chat_id = chat_id
        
        if bot_token and chat_id:
            try:
                self.telegram_bot = Bot(token=bot_token)
                print(f"Telegram bot configured successfully")
            except Exception as e:
                print(f"Telegram bot initialization failed: {e}")
                self.telegram_bot = None
    
    async def send_telegram_alert(self, message):
        """Send alert via Telegram"""
        if not self.telegram_bot or not self.chat_id:
            print("Telegram not configured, skipping alert")
            return False
        
        try:
            await self.telegram_bot.send_message(
                chat_id=self.chat_id,
                text=f"🚨 WiFi Security Alert\n\n{message}",
                parse_mode='HTML'
            )
            print(f"Telegram alert sent successfully")
            return True
        except Exception as e:
            print(f"Telegram alert failed: {e}")
            return False
    
    def send_threat_alert(self, alert):
        """Send alert through Telegram only if configured"""
        # Only send if Telegram is properly configured
        if not self.bot_token or not self.chat_id:
            print(f"Telegram not configured - Alert not sent: {alert['type']}")
            return
        
        message = f"<b>{alert['type']}</b>\n\n"
        message += f"Severity: {alert['severity'].upper()}\n"
        message += f"Description: {alert['description']}\n"
        
        if alert.get('details'):
            message += f"\nDetails:\n"
            for key, value in alert['details'].items():
                message += f"• {key}: {value}\n"
        
        # Send Telegram alert
        try:
            asyncio.run(self.send_telegram_alert(message))
            print(f"Telegram alert sent successfully: {alert['type']}")
        except Exception as e:
            print(f"Failed to send Telegram alert: {e}")
