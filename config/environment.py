# config/environment.py
import json
import os
from selenium.webdriver.chrome.options import Options

class Environment:
    def __init__(self):
        self.config_file = os.path.join(os.path.dirname(__file__), 'config.json')
        self.env = os.getenv('TEST_ENV', 'dev')  # Default to 'dev' if not specified
        self.config = self._load_config()

    def _load_config(self):
        with open(self.config_file, 'r') as f:
            configs = json.load(f)
            return configs[self.env]

    @property
    def base_url(self):
        return self.config['base_url']

    @property
    def timeout(self):
        return self.config['timeout']

    def get_browser_options(self):
        options = Options()
        if self.config['headless']:
            options.add_argument('--headless')
        return options

    def get_credentials(self, user_type):
        return self.config['credentials'].get(user_type, {})

    def get_screenshot_dir(self):
        screenshot_dir = self.config['screenshot_dir']
        os.makedirs(screenshot_dir, exist_ok=True)
        return screenshot_dir