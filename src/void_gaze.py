import json
from googleapiclient.discovery import build
from .prompts import VOID_GAZE_SYSTEM_PROMPT
from .config import MODEL_NAME
import google.generativeai as genai
from duckduckgo_search import DDGS

class VoidGaze:
    def __init__(self, gemini_api_key, google_api_key, search_engine_id, search_engine_id_image=None):
        self.google_api_key = google_api_key
        self.search_engine_id = search_engine_id
        self.search_engine_id_image = search_engine_id_image
        
        if gemini_api_key:
            genai.configure(api_key=gemini_api_key)
            self.model = genai.GenerativeModel(MODEL_NAME, system_instruction=VOID_GAZE_SYSTEM_PROMPT)
        else:
            self.model = None

    def generate_queries(self, profile):
        if not self.model:
            return ["Error: Gemini API Key missing."]
        
        try:
            response = self.model.generate_content(
                f"TARGET PROFILE:\n{json.dumps(profile)}",
                generation_config={"response_mime_type": "application/json"}
            )
            return json.loads(response.text)
        except Exception as e:
            return [f"Error generating queries: {str(e)}"]

    def execute_search(self, query, search_type="web", smart_expand=True):
        results = []
        search_queries = []
        if " " not in query and len(query) > 3:
            print(f"[!] POTENTIAL USERNAME DETECTED: {query}")
            print(f"[>] INITIATING SHERLOCK PROTOCOL for '{query}'...")
            sherlock_hits = self._run_sherlock_scan(query)
            results.extend(sherlock_hits)
        exact_query = f'"{query}"'
        search_queries.append(exact_query)
        if smart_expand and self.model and search_type == "web":
            print(f"[+] Engaging AI Target Analysis for: {query}...")
            try:
                ai_dorks = self.generate_queries({"target_identifier": query})
                if isinstance(ai_dorks, list):
                    print(f"[+] AI Generated Attack Vectors: {len(ai_dorks)} vectors found.")
                    search_queries.extend(ai_dorks[:3])
            except Exception as e:
                print(f"[!] AI Query Generation Failed: {e}")
        if search_type == "web":
            social_queries = [
                f'site:linkedin.com {exact_query}',
                f'site:instagram.com {exact_query}',
                f'site:facebook.com {exact_query}',
                f'site:twitter.com {exact_query}'
            ]
            search_queries.extend(social_queries)
        unique_queries = list(dict.fromkeys(search_queries))
        print(f"[>] Executing Deep Scan with {len(unique_queries)} vectors...")
        
        for q in unique_queries:
            google_results = self._search_google(q, search_type, num_results=2)
            if isinstance(google_results, list):
                results.extend(google_results)
            if search_type == "web":
                ddg_results = self._search_ddg(q, max_results=5) # 5 per query is enough
                if isinstance(ddg_results, list):
                    results.extend(ddg_results)
        if len(results) < 3:
            print(f"[!] Low signal. Engaging loose search protocol for: {query}")
            google_loose = self._search_google(query, search_type, num_results=3)
            if isinstance(google_loose, list):
                results.extend(google_loose)
            if search_type == "web":
                ddg_loose = self._search_ddg(query, max_results=10)
                if isinstance(ddg_loose, list):
                    results.extend(ddg_loose)
        unique_results = []
        seen_links = set()
        
        for res in results:
            if res['link'] not in seen_links:
                unique_results.append(res)
                seen_links.add(res['link'])
                
        return unique_results[:40]

    def _search_google(self, query, search_type, num_results=3):
        if not self.google_api_key:
             return []
        
        target_cx = self.search_engine_id
        search_params = {"q": query, "num": num_results}
        
        if search_type == "image":
            if not self.search_engine_id_image:
                return []
            target_cx = self.search_engine_id_image
            search_params["searchType"] = "image"
            search_params["num"] = 10
        elif not self.search_engine_id:
             return []

        try:
            service = build("customsearch", "v1", developerKey=self.google_api_key)
            search_params["cx"] = target_cx
            res = service.cse().list(**search_params).execute()
            
            items = res.get("items", [])
            parsed_results = []
            
            for item in items:
                result_data = {
                    "source": "GOOGLE",
                    "title": item.get("title"),
                    "link": item.get("link"),
                    "snippet": item.get("snippet")
                }
                if "image" in item:
                    result_data["image_context"] = item.get("image")
                parsed_results.append(result_data)
            
            return parsed_results
        except Exception:
            return []

    def _run_sherlock_scan(self, username):
        import requests
        
        targets = [
            {"name": "GitHub", "url": f"https://github.com/{username}"},
            {"name": "Instagram", "url": f"https://instagram.com/{username}"},
            {"name": "Twitter/X", "url": f"https://twitter.com/{username}"},
            {"name": "Spotify", "url": f"https://open.spotify.com/user/{username}"},
            {"name": "Pinterest", "url": f"https://pinterest.com/{username}"},
            {"name": "Steam", "url": f"https://steamcommunity.com/id/{username}"},
            {"name": "Reddit", "url": f"https://www.reddit.com/user/{username}"},
            {"name": "Medium", "url": f"https://medium.com/@{username}"},
            {"name": "Vimeo", "url": f"https://vimeo.com/{username}"},
            {"name": "SoundCloud", "url": f"https://soundcloud.com/{username}"},
            {"name": "About.me", "url": f"https://about.me/{username}"},
            {"name": "Wattpad", "url": f"https://www.wattpad.com/user/{username}"},
            {"name": "Flickr", "url": f"https://www.flickr.com/people/{username}"},
            {"name": "Etsy", "url": f"https://www.etsy.com/shop/{username}"},
            {"name": "Patreon", "url": f"https://www.patreon.com/{username}"}
        ]
        
        hits = []
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        for target in targets:
            try:
                r = requests.get(target['url'], headers=headers, timeout=5)
                if r.status_code == 200:
                    print(f"    [+] CONFIRMED HIT: {target['name']}")
                    hits.append({
                        "source": f"SHERLOCK: {target['name']}",
                        "title": f"{username} on {target['name']}",
                        "link": target['url'],
                        "snippet": f"Active profile found on {target['name']} matching username '{username}'."
                    })
            except:
                pass
                
        return hits

    def _search_ddg(self, query, max_results=20):
        try:
            with DDGS() as ddgs:
                ddg_results = list(ddgs.text(query, region="tr-tr", safesearch="off", max_results=max_results))
            
            parsed_results = []
            if ddg_results:
                for res in ddg_results:
                    parsed_results.append({
                        "source": "DDG",
                        "title": res.get("title"),
                        "link": res.get("href"),
                        "snippet": res.get("body")
                    })
            return parsed_results
        except Exception as e:
            return []
