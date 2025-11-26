import requests
from stem import Signal
from stem.control import Controller
import socket
import socks # pysocks needed for patching socket
import time

class DeepDive:
    def __init__(self):
        self.proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }
        self.session = requests.Session()
        self.session.proxies.update(self.proxies)

    def check_tor_connection(self):
        try:
            ip_check = self.session.get("http://httpbin.org/ip", timeout=10).json()
            return {
                "status": "CONNECTED",
                "tor_ip": ip_check.get("origin"),
                "message": "Tor Circuit Established"
            }
        except Exception as e:
            return {
                "status": "FAILED",
                "message": "Is Tor Browser/Service running? Connection refused.",
                "error": str(e)
            }

    def renew_tor_identity(self):
        try:
            with Controller.from_port(port=9051) as controller:
                controller.authenticate()
                controller.signal(Signal.NEWNYM)
                return "Tor Identity Rotated (New IP)"
        except Exception as e:
            return f"Failed to rotate IP: {e}"

    def search_onion(self, query):
        print(f"[DeepDive] Querying Dark Web for: {query}")
        
        search_url = f"https://ahmia.fi/search/?q={query}"
        
        try:
            resp = self.session.get(search_url, timeout=30)
            
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(resp.text, 'html.parser')
            results = []
            
            for item in soup.select('li.result'):
                title = item.select_one('h4').get_text(strip=True) if item.select_one('h4') else "Unknown"
                link = item.select_one('a')['href']
                snippet = item.select_one('p').get_text(strip=True) if item.select_one('p') else ""
                
                results.append({
                    "source": "TOR/AHMIA",
                    "title": title,
                    "link": link,
                    "snippet": snippet
                })
                
            return results[:10]
            
        except Exception as e:
            return [{"source": "ERROR", "title": "Deep Search Failed", "snippet": str(e), "link": "N/A"}]


