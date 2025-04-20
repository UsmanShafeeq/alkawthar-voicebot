from scraper.alkawthar_scraper import AlKawtharScraper
from voice.voice_interface import VoiceInterface
from config.settings import CONFIG
import time

class AlKawtharVoiceBot:
    def __init__(self):
        self.scraper = AlKawtharScraper()
        self.voice = VoiceInterface()
        self.university_name = CONFIG['university_name']
        self.commands = {
            'news': {
                'handler': self.handle_news,
                'description': 'Get the latest university news'
            },
            'admission': {
                'handler': self.handle_admissions,
                'description': 'Get admission information'
            },
            'contact': {
                'handler': self.handle_contact,
                'description': 'Get contact details'
            },
            'help': {
                'handler': self.handle_help,
                'description': 'List available commands'
            }
        }

    def handle_news(self):
        news = self.scraper.get_news()
        if news:
            response = f"Here are the latest {self.university_name} updates: "
            for item in news[:3]:  # Limit to 3 news items
                response += f"{item['title']}. {item['content'][:100]}... "
            self.voice.speak(response)
        else:
            self.voice.speak("Sorry, I couldn't retrieve the latest news at this time.")

    def handle_admissions(self):
        admissions = self.scraper.get_admissions()
        if admissions:
            response = f"Here's {self.university_name} admission information: "
            for item in admissions[:3]:  # Limit to 3 items
                response += f"{item['title']}. {item['content'][:100]}... "
            self.voice.speak(response)
        else:
            self.voice.speak("Sorry, admission information is currently unavailable.")

    def handle_contact(self):
        contact = self.scraper.get_contact_info() or CONFIG['fallback_data']['contact']
        response = (f"{self.university_name} contact information: "
                   f"Phone: {contact.get('phones', [CONFIG['fallback_data']['contact']['phone']])[0]}. "
                   f"Email: {contact.get('emails', [CONFIG['fallback_data']['contact']['email']])[0]}. "
                   f"Address: {contact.get('address', CONFIG['fallback_data']['contact']['address'])}")
        self.voice.speak(response)

    def handle_help(self):
        help_text = "I can help with: "
        for cmd, details in self.commands.items():
            help_text += f"Say '{cmd}' to {details['description']}. "
        self.voice.speak(help_text)

    def process_command(self, command):
        if not command:
            return
            
        for cmd, details in self.commands.items():
            if cmd in command:
                details['handler']()
                return
                
        self.voice.speak("I didn't understand that. Say 'help' for available commands.")

    def run(self):
        self.voice.speak(f"Welcome to {self.university_name} voice assistant. How can I help you?")
        self.voice.start_continuous_listen(self.process_command)
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.voice.speak("Goodbye!")
            self.voice.stop_listening()

if __name__ == "__main__":
    bot = AlKawtharVoiceBot()
    bot.run()