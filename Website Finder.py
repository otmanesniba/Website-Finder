import time
import os
import random
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent
import pyfiglet
from colorama import Fore, Style, init
from datetime import datetime

# Initialize colorama
init()

# ================== DRIVER SETUP ==================
def setup_edge_driver():
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    
    # Realistic browser configuration
    ua = UserAgent(browsers=['edge'])
    user_agent = ua.random
    options.add_argument(f"user-agent={user_agent}")
    options.add_argument("--window-size=1280,720")

    # Configure driver path (update this to your actual path)
    edge_path = r'C:\Users\otmane sniba\Desktop\out of topic\msedgedriver.exe'
    service = Service(executable_path=edge_path)
    
    driver = webdriver.Edge(service=service, options=options)
    
    # Remove automation flags
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"}
    )
    
    return driver

# ================== WEBSITE FINDER LOGIC ==================
def find_official_website(driver, company_name):
    try:
        driver.get("https://www.google.com")
        time.sleep(random.uniform(1, 3))
        
        # Accept cookies if needed
        try:
            driver.find_element(By.XPATH, "//div[text()='Accept all']").click()
            time.sleep(1)
        except:
            pass

        # Perform human-like search
        search_box = driver.find_element(By.NAME, "q")
        for char in f"{company_name} official website":
            search_box.send_keys(char)
            time.sleep(random.uniform(0.1, 0.3))
        search_box.send_keys(Keys.RETURN)
        time.sleep(random.uniform(2, 4))

        # Process results
        results = driver.find_elements(By.CSS_SELECTOR, "div.g")[:3]
        blacklist = ['wikipedia', 'linkedin', 'crunchbase']
        
        for result in results:
            try:
                link = result.find_element(By.TAG_NAME, "a")
                url = link.get_attribute("href").lower()
                if any(b in url for b in blacklist):
                    continue
                if company_name.split()[0].lower() in url:
                    return url
            except:
                continue
                
        return "No official website found"
    
    except Exception as e:
        return f"Error: {str(e)}"

# ================== USER INTERFACE ==================
def show_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    ascii_banner = pyfiglet.figlet_format("WebSite Finder", font="slant")
    print(Fore.CYAN + Style.BRIGHT + ascii_banner)
    credit_text = pyfiglet.figlet_format("by OTMANE SNIBA", font="digital")
    print(Fore.MAGENTA + credit_text + Style.RESET_ALL)

def get_companies():
    show_banner()
    print(Fore.YELLOW + "╔" + "═"*58 + "╗")
    print(Fore.YELLOW + "║" + Fore.CYAN + "        ENTER COMPANY NAMES OR FILE PATH".ljust(58) + Fore.YELLOW + "║")
    print(Fore.YELLOW + "╚" + "═"*58 + "╝" + Style.RESET_ALL)
    
    while True:
        source = input(f"\n{Fore.GREEN}•{Style.RESET_ALL} Enter companies (comma-separated) or .txt file path: ").strip()
        
        if source.endswith('.txt'):
            try:
                with open(source, 'r') as f:
                    companies = [line.strip() for line in f.readlines() if line.strip()]
                if companies:
                    return companies
                print(Fore.RED + "File is empty! Try again." + Style.RESET_ALL)
            except Exception as e:
                print(Fore.RED + f"File error: {str(e)}" + Style.RESET_ALL)
        else:
            companies = [c.strip() for c in source.split(',') if c.strip()]
            if companies:
                return companies
            print(Fore.RED + "Invalid input! Try again." + Style.RESET_ALL)

def animated_processing(message):
    symbols = ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷']
    for _ in range(10):
        for symbol in symbols:
            print(Fore.YELLOW + f"\r{symbol} {message}..." + Style.RESET_ALL, end="")
            time.sleep(0.1)

def save_results(results):
    desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop')
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f"Website_Results_{timestamp}.txt"
    filepath = os.path.join(desktop, filename)
    
    header = f"""╔{'═'*70}╗
║{'WEBSITE FINDER RESULTS'.center(70)}║
╠{'═'*70}╣
║ Date: {timestamp.ljust(62)}║
║ Companies Processed: {str(len(results)).ljust(49)}║
╠{'═'*70}╣\n"""
    
    body = ""
    for idx, result in enumerate(results, 1):
        company, website = result.split(':', 1)
        body += f"║ {idx:03d}. {company.strip().ljust(40)} ➔ {website.strip().ljust(20)} ║\n"
    
    footer = f"╚{'═'*70}╝\n"
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(header + body + footer)
    
    print(Fore.GREEN + f"\nResults saved to: {filepath}" + Style.RESET_ALL)
    return filepath

# ================== MAIN PROGRAM ==================
def main():
    companies = get_companies()
    
    print(Fore.MAGENTA + "\n" + "═"*60)
    print(f" Starting search for {Fore.CYAN}{len(companies)}{Fore.MAGENTA} companies ".center(60, '⚡'))
    print("═"*60 + Style.RESET_ALL)
    
    driver = setup_edge_driver()
    results = []
    
    try:
        for idx, company in enumerate(companies, 1):
            animated_processing(f"Processing {company}")
            website = find_official_website(driver, company)
            
            result_line = f"{company}: {website}"
            results.append(result_line)
            
            status_icon = Fore.GREEN + "✓" if "http" in website else Fore.RED + "✗"
            print(f"\r{status_icon}{Style.RESET_ALL} {Fore.CYAN}{idx:03d}/{len(companies)}{Style.RESET_ALL} {company.ljust(30)} ➔ {website}")
            
            time.sleep(random.uniform(3, 7))  # Human-like delay
        
        saved_file = save_results(results)
        
        print(Fore.MAGENTA + "\n" + "═"*60)
        print(f" {Fore.GREEN}PROCESS COMPLETE!{Fore.MAGENTA} ".center(60, '■'))
        print("═"*60 + Style.RESET_ALL)
        
        input(Fore.YELLOW + "\nPress ENTER to open results file..." + Style.RESET_ALL)
        os.startfile(saved_file)

    finally:
        driver.quit()

if __name__ == "__main__":
    main()