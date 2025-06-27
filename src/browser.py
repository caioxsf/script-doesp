from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class Browser:
    """
    Class for the browser.\n
    """
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-software-rasterizer')
        chrome_options.add_argument('--window-size=1920,1080')
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    def open(self, url):
        self.driver.get(url)

