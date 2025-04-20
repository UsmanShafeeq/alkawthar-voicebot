import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin
import json

class AlKawtharScraper:
    def __init__(self):
        self.base_url = "https://alkawthar.edu.pk/"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AlKawtharVoiceBot/1.0'
        })
        self.timeout = 10

    def get_university_info(self):
        """Get comprehensive university information"""
        return {
            'news': self.get_news(),
            'admissions': self.get_admissions(),
            'contact': self.get_contact_info(),
            'last_updated': datetime.now().isoformat()
        }

    def get_news(self, limit=5):
        """Get latest university news"""
        try:
            response = self.session.get(self.base_url, timeout=self.timeout)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            news_items = []
            news_container = soup.find('div', class_='news-section') or soup.find('section', class_='latest-news')
            
            if news_container:
                for item in news_container.find_all('div', class_='news-item')[:limit]:
                    title = item.find('h3').get_text(strip=True) if item.find('h3') else "No title"
                    date = item.find('span', class_='date').get_text(strip=True) if item.find('span', class_='date') else ""
                    content = item.find('p').get_text(strip=True) if item.find('p') else ""
                    
                    news_items.append({
                        'title': title,
                        'date': date,
                        'content': content
                    })
            
            return news_items
        except Exception as e:
            print(f"Error scraping news: {e}")
            return []

    def get_admissions(self):
        """Get admission information"""
        try:
            response = self.session.get(urljoin(self.base_url, 'admissions'), timeout=self.timeout)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            admissions = []
            admission_section = soup.find('div', class_='admission-info') or soup.find('section', id='admissions')
            
            if admission_section:
                for item in admission_section.find_all('div', class_='admission-item'):
                    title = item.find('h3').get_text(strip=True) if item.find('h3') else "Admission"
                    content = item.find('p').get_text(strip=True) if item.find('p') else ""
                    
                    admissions.append({
                        'title': title,
                        'content': content
                    })
            
            return admissions
        except Exception as e:
            print(f"Error scraping admissions: {e}")
            return []

    def get_contact_info(self):
        """Get contact information"""
        try:
            response = self.session.get(urljoin(self.base_url, 'contact-us'), timeout=self.timeout)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            contact = {}
            contact_section = soup.find('div', class_='contact-info') or soup.find('address')
            
            if contact_section:
                phones = [li.get_text(strip=True) for li in contact_section.find_all('li', class_='phone')]
                emails = [li.get_text(strip=True) for li in contact_section.find_all('li', class_='email')]
                address = contact_section.get_text('\n', strip=True)
                
                contact = {
                    'phones': phones,
                    'emails': emails,
                    'address': address
                }
            
            return contact
        except Exception as e:
            print(f"Error scraping contact info: {e}")
            return {}