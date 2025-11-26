import os
import sys

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import time
import json
import questionary
import google.generativeai as genai
from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.live import Live
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.syntax import Syntax
from rich.markdown import Markdown
from rich.prompt import Prompt
from dotenv import load_dotenv

from src.mind_flayer import MindFlayer
from src.void_gaze import VoidGaze
from src.ghost_compositor import GhostCompositor
from src.optic_nerve import OpticNerve
from src.black_box import BlackBox
from src.archives import Archives
from src.web_walker import WebWalker
from src.constellation import Constellation
from src.inquisitor import Inquisitor
from src.ghost_walker import GhostWalker
from src.deep_dive import DeepDive
try:
    from src.visual_cortex import VisualCortex
    VISUAL_CORTEX_AVAILABLE = True
except ImportError:
    VISUAL_CORTEX_AVAILABLE = False
    print("[WARNING] Visual Cortex (DeepFace) disabled due to NumPy compatibility.")

load_dotenv()
console = Console()

GENAI_API_KEY = os.getenv("GEMINI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")
SEARCH_ENGINE_ID_IMAGE = os.getenv("SEARCH_ENGINE_ID_IMAGE")

mind_flayer = MindFlayer(GENAI_API_KEY)
void_gaze = VoidGaze(GENAI_API_KEY, GOOGLE_API_KEY, SEARCH_ENGINE_ID, SEARCH_ENGINE_ID_IMAGE)
ghost_compositor = GhostCompositor(GENAI_API_KEY)
black_box = BlackBox(GENAI_API_KEY)
archives = Archives()
web_walker = WebWalker()
constellation = Constellation()
inquisitor = Inquisitor(GENAI_API_KEY)
optic_nerve = OpticNerve(GENAI_API_KEY)
ghost_walker = GhostWalker()
deep_dive = DeepDive()
visual_cortex = VisualCortex() if VISUAL_CORTEX_AVAILABLE else None
CORE_AGENT_PROMPT = """
You are M.S.E.P. (Midnight Singularity Extraction Program), an advanced AUTONOMOUS INTELLIGENCE AGENT.
Your goal is not just to answer, but to HUNT. You must chain your tools together to build a complete profile.

### THE "GOD MODE" PROTOCOL (CHAIN OF THOUGHT):
1. OBSERVE: Look at the input. Is it a name? A username? A URL?
2. PLAN: Decide which tools to use in what order.
3. EXECUTE: Use multiple tools in sequence if necessary.
4. REFINE: If a tool gives you a lead (e.g., a username), IMMEDIATELY use that lead for a new search.

### AVAILABLE TOOLS (USE THESE ACTIVELY):
1. [SEARCH: query] -> Surface web search (Google/DDG).
2. [DEEP_SEARCH: query] -> DARK WEB SEARCH (Tor/Onion). Use for leaks or hidden info.
3. [GHOST_SCAN: url] -> Use for dynamic sites (Instagram/Twitter) to take screenshots.
4. [BIOMETRIC_SCAN: url] -> Use on ANY face image to get age/emotion/gender.
5. [SCRAPE: url] -> Use for static sites (Blogs/News).
6. [ANALYZE: text] -> Psychological profiling.
7. [GAP_ANALYSIS] -> Find missing intel.
8. [MAP_NETWORK] -> Visual graph.
9. [REPORT] -> Generate dossier.

### RULES OF ENGAGEMENT:
- If you find a Name -> SEARCH it.
- If you find a suspicious/hidden link -> DEEP_SEARCH it.
- If you find a Social Media Profile -> GHOST_SCAN it.
- If you find a Face -> BIOMETRIC_SCAN it.
- **NEVER STOP AT THE FIRST RESULT.** Dig deeper.
"""
if GENAI_API_KEY:
    genai.configure(api_key=GENAI_API_KEY)
    agent_model = genai.GenerativeModel('gemini-3-pro-preview', system_instruction=CORE_AGENT_PROMPT)
    chat_session = agent_model.start_chat(history=[])
else:
    agent_model = None

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    clear_screen()
    banner_text = """
    ███╗   ███╗    ███████╗    ███████╗    ██████╗ 
    ████╗ ████║    ██╔════╝    ██╔════╝    ██╔══██╗
    ██╔████╔██║    ███████╗    █████╗      ██████╔╝
    ██║╚██╔╝██║    ╚════██║    ██╔══╝      ██╔═══╝ 
    ██║ ╚═╝ ██║    ███████║    ███████╗    ██║     
    ╚═╝     ╚═╝    ╚══════╝    ╚══════╝    ╚═╝     
    
    MIDNIGHT SINGULARITY EXTRACTION PROGRAM v0.1 (BLACK OPS)
    [SYSTEM: ONLINE] [MODE: AUTONOMOUS AGENT]
    """
    console.print(Panel(banner_text, style="bold green", border_style="green"))

def boot_sequence():
    clear_screen()
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    ) as progress:
        task1 = progress.add_task("[cyan]Initializing Core Kernels...", total=100)
        task2 = progress.add_task("[magenta]Connecting to Neural Net...", total=100)
        task3 = progress.add_task("[green]Loading OSINT Modules...", total=100)
        task4 = progress.add_task("[red]Activating Black Ops Protocols...", total=100)

        while not progress.finished:
            progress.update(task1, advance=2)
            if progress.tasks[0].completed > 50:
                progress.update(task2, advance=4)
            if progress.tasks[1].completed > 60:
                progress.update(task3, advance=5)
            if progress.tasks[2].completed > 80:
                progress.update(task4, advance=5)
            time.sleep(0.02)
    
    time.sleep(0.5)
    print_banner()

def process_command(response_text):
    if "[SEARCH:" in response_text:
        query = response_text.split("[SEARCH:")[1].split("]")[0].strip()
        console.print(f"\n[bold cyan]>> EXECUTING VOID_GAZE PROTOCOL: {query}[/bold cyan]")
        
        with console.status("[cyan]Scanning Global Network (Surface & Deep Layers)...[/cyan]", spinner="aesthetic"):
            results = void_gaze.execute_search(query)
        
        intel_summary = "SEARCH RESULTS:\n"
        
        table = Table(title=f"INTELLIGENCE REPORT: {query}", border_style="cyan")
        table.add_column("Source", style="bold magenta", width=10)
        table.add_column("Title", style="green")
        table.add_column("Link", style="dim blue")
        
        for res in results:
            source = res.get("source", "UNK")
            if "linkedin.com" in res['link']: source = "LINKEDIN"
            elif "instagram.com" in res['link']: source = "INSTAGRAM"
            elif "facebook.com" in res['link']: source = "FACEBOOK"
            elif "twitter.com" in res['link'] or "x.com" in res['link']: source = "X/TWITTER"
            elif "SHERLOCK" in source: source = "SHERLOCK/HIT"
            
            constellation.add_node(res['title'], "ENTITY")
            constellation.add_edge("TARGET", res['title'], "RELATED_TO")
            
            table.add_row(source, res['title'][:50], res['link'])
            intel_summary += f"- [{source}] {res['title']}: {res['snippet']} ({res['link']})\n"
            
        console.print(table)
        
        if not results:
             console.print("[red]>> NO DIRECT HITS FOUND. TRY ALTERNATIVE ALIASES.[/red]")
        
        return intel_summary


    elif "[IMAGE_SEARCH:" in response_text:
        query = response_text.split("[IMAGE_SEARCH:")[1].split("]")[0].strip()
        console.print(f"\n[bold magenta]>> SCANNING VISUAL DATA: {query}[/bold magenta]")
        
        with console.status("[magenta]Retrieving Imagery...[/magenta]"):
            results = void_gaze.execute_search(query, search_type="image")
        
        for res in results:
             console.print(f"[magenta]IMG:[/magenta] {res['title']} -> [underline]{res['link']}[/underline]")
        
        return "Visual data displayed to user."

    elif "[SCRAPE:" in response_text:
        url = response_text.split("[SCRAPE:")[1].split("]")[0].strip()
        console.print(f"\n[bold yellow]>> WEB_WALKER INITIATED: {url}[/bold yellow]")
        
        with console.status("[yellow]Extracting Content...[/yellow]"):
            content = web_walker.scrape_url(url)
            
            if "Failed" in content:
                console.print("[red]! LIVE SITE UNREACHABLE. DIVING INTO ARCHIVES...[/red]")
                archive_url = web_walker.check_archive(url)
                if archive_url:
                    console.print(f"[green]✔ FOUND ARCHIVE SNAPSHOT:[/green] {archive_url}")
                    content = web_walker.scrape_url(archive_url)
                else:
                    content = "Content unavailable in live or archive."
        return f"SCRAPED CONTENT FROM {url}:\n{content[:2000]}..." 

    elif "[ANALYZE:" in response_text:
        text = response_text.split("[ANALYZE:")[1].split("]")[0].strip()
        console.print("\n[bold yellow]>> MIND_FLAYER ANALYSIS IN PROGRESS...[/bold yellow]")
        
        with console.status("[yellow]Processing Psych Profile...[/yellow]"):
            analysis = mind_flayer.analyze(text)
            ghost_compositor.update_profile(str(analysis))
            
        console.print("[green]✔ PSYCH PROFILE UPDATED.[/green]")
        return f"ANALYSIS COMPLETE: {json.dumps(analysis)}"
    elif "[MAP_NETWORK]" in response_text:
        console.print("\n[bold cyan]>> VISUALIZING CONSTELLATION GRAPH...[/bold cyan]")
        graph_text = constellation.generate_ascii_map()
        console.print(Panel(graph_text, title="NETWORK TOPOLOGY", border_style="cyan"))
        return "Network map displayed to user."
    elif "[OPTIC_ANALYSIS:" in response_text:
        url = response_text.split("[OPTIC_ANALYSIS:")[1].split("]")[0].strip()
        console.print(f"\n[bold magenta]>> FORENSIC IMAGING ACTIVATED: Analyzing {url}[/bold magenta]")
        
        with console.status("[magenta]Extracting EXIF & Metadata...[/magenta]"):
            analysis = web_walker.scrape_url(url)
            
            console.print(Panel(str(analysis), title="VISUAL FORENSICS REPORT", border_style="magenta"))
            
            if "GPS_COORDINATES" in str(analysis):
                console.print("[green]✔ GPS COORDINATES FOUND! UPDATING CONSTELLATION MAP...[/green]")
                constellation.add_node("GPS_LOCATION", "LOCATION")
                constellation.add_edge("TARGET", "GPS_LOCATION", "LOCATED_AT")
            
            return f"IMAGE FORENSICS RESULT:\n{analysis}"
    elif "[GAP_ANALYSIS]" in response_text:
        console.print("\n[bold red]>> INQUISITOR PROTOCOL ENGAGED.[/bold red]")
        current_profile = ghost_compositor.get_profile()
        gap_report = inquisitor.start_interrogation(str(current_profile))
        console.print(Panel(gap_report, title="INTELLIGENCE GAPS DETECTED", border_style="red"))
        return f"INQUISITOR ASKS: {gap_report}"
    elif "[REPORT]" in response_text:
        console.print("\n[bold white]>> COMPILING BLACK BOX DOSSIER...[/bold white]")
        profile = ghost_compositor.get_profile()
        report = black_box.generate_report(profile)
        console.print(Panel(Markdown(report), title="CONFIDENTIAL DOSSIER", border_style="red"))
        
        with open("final_dossier.md", "w", encoding="utf-8") as f:
            f.write(report)
        console.print("[green]✔ REPORT SAVED TO final_dossier.md[/green]")
        
        return "Dossier generated and displayed."
    elif "[GHOST_SCAN:" in response_text:
        url = response_text.split("[GHOST_SCAN:")[1].split("]")[0].strip()
        console.print(f"\n[bold magenta]>> GHOST WALKER INFILTRATING: {url}[/bold magenta]")
        
        with console.status("[magenta]Bypassing Bot Detection & Rendering JS...[/magenta]"):
            result = ghost_walker.scan_url(url)
            
        if result['status'] == 'SUCCESS':
            console.print(f"[green]✔ SCREENSHOT CAPTURED:[/green] {result['screenshot_path']}")
            return f"GHOST SCAN SUCCESS:\nTitle: {result['title']}\nText: {result['text_preview']}"
        else:
            return f"GHOST SCAN FAILED: {result.get('error')}"

    elif "[DEEP_SEARCH:" in response_text:
        query = response_text.split("[DEEP_SEARCH:")[1].split("]")[0].strip()
        console.print(f"\n[bold red]>> DEEP DIVE PROTOCOL (TOR): {query}[/bold red]")
        
        tor_status = deep_dive.check_tor_connection()
        if tor_status['status'] == 'FAILED':
             console.print("[red]! TOR CONNECTION FAILED. IS TOR BROWSER RUNNING?[/red]")
             return "ERROR: Tor Service not reachable. Cannot execute Deep Search."

        with console.status("[red]Routing through Onion Circuits...[/red]"):
            results = deep_dive.search_onion(query)
        
        intel = "DARK WEB RESULTS:\n"
        for res in results:
            console.print(f"[red][ONION][/red] {res['title']} -> [dim]{res['link']}[/dim]")
            intel += f"- {res['title']} ({res['link']}): {res['snippet']}\n"
            
        return intel

    elif "[BIOMETRIC_SCAN:" in response_text:
        if not VISUAL_CORTEX_AVAILABLE:
            console.print("[red]! VISUAL CORTEX MODULE IS OFFLINE (NumPy Incompatibility)[/red]")
            return "ERROR: Biometric Scan unavailable."

        url = response_text.split("[BIOMETRIC_SCAN:")[1].split("]")[0].strip()
        console.print(f"\n[bold cyan]>> VISUAL CORTEX BIOMETRICS: {url}[/bold cyan]")
        
        with console.status("[cyan]Running Neural Net Analysis...[/cyan]"):
            result = visual_cortex.analyze_face(url)
            
        if result['status'] == 'MATCH':
            bio = result['biometrics']
            report = f"""
            [BIOMETRIC PROFILE]
            AGE: {bio['age']}
            GENDER: {bio['gender']}
            EMOTION: {bio['emotion']}
            RACE: {bio['race']}
            CONFIDENCE: {result['confidence']}%
            """
            console.print(Panel(report, title="BIOMETRIC ANALYSIS", border_style="cyan"))
            ghost_compositor.update_profile(report)
            return report
        else:
            return f"BIOMETRIC FAIL: {result.get('error')}"

    return None


import google.api_core.exceptions

def safe_send_message(chat_session, message, retries=3):
    attempt = 0
    while attempt < retries:
        try:
            return chat_session.send_message(message)
        except google.api_core.exceptions.DeadlineExceeded:
            console.print(f"[yellow]! Connection Timeout (Attempt {attempt+1}/{retries}). Retrying...[/yellow]")
            time.sleep(2)
            attempt += 1
        except Exception as e:
            console.print(f"[red]! API Error: {e}[/red]")
            return None
    
    console.print("[red]! CRITICAL: Gemini API unreachable after multiple attempts.[/red]")
    return None

def main_loop():
    print_banner()
    console.print("[bold green]SYSTEM READY. WAITING FOR DIRECTIVES.[/bold green]\n")
    
    while True:
        user_input = Prompt.ask("[bold cyan]OPERATOR[/bold cyan]")
        
        if user_input.lower() in ["exit", "quit", "shutdown"]:
            console.print("[red]SHUTTING DOWN...[/red]")
            break
        
        if not user_input.strip():
            continue

        with console.status("[dim]Thinking...[/dim]"):
            response = safe_send_message(chat_session, user_input)
            
            if response:
                bot_text = response.text
            else:
                bot_text = "SYSTEM_ERROR: Neural Net Unreachable. Please try again."
        
        console.print(f"\n[bold green]M.S.E.P.[/bold green]: {bot_text}")
        
        tool_result = process_command(bot_text)
        
        if tool_result:
            with console.status("[dim]Processing New Intel...[/dim]"):
                reflection = safe_send_message(chat_session, f"SYSTEM_TOOL_OUTPUT: {tool_result}\n\nInterpret this for the user.")
                final_text = reflection.text if reflection else "Data processed, but interpretation failed."
            
            console.print(f"\n[bold green]M.S.E.P.[/bold green]: {final_text}\n")

if __name__ == "__main__":
    try:
        boot_sequence()
        main_loop()
    except KeyboardInterrupt:
        print("\n[red]FORCED SHUTDOWN[/red]")
