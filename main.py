import os

import sys
import json
from dotdict import dotdict
from threading import Thread
from time import sleep,time
from datetime import datetime,timedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException,NoSuchElementException,ElementNotInteractableException,StaleElementReferenceException,InvalidSessionIdException,NoSuchWindowException

from dotenv import load_dotenv
import google.generativeai as genai

import random, string
import pyfiglet
import colorama
from colorama import Fore, Style
import contextlib
from requests import get
import ctypes

# Initialize colorama
colorama.init()

# Create large text

genai.configure(api_key="AIzaSyB9UsvHeP31-s2KGe_l3nFACVDz7DDoYVE")

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
)

chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        "Can you please make a search (in string without quotes) answering this prompt: Search on Bing for the meaning of a word you do not fully understand.​",
      ],
    },
    {
      "role": "model",
      "parts": [
        "meaning of  ubiquitous",
      ],
    },
  ]
)
WORD_LIST = get('https://www.mit.edu/~ecprice/wordlist.10000').text.split('\n')
HUGE = sys.float_info.max
a = {}
class Main:
    def __init__(self,mode=None,args:dict={}):
        if mode is None: return
        self.before(mode,args)
    
    def before(self,mode=None,args:dict={}):
        print('started',mode)
        if mode is None: return
        try:
            self.run = True
            Thread(target=self.start,args=(mode,args)).start()
            self.original_stderr = sys.stderr
            def listen():
                while self.run:
                    sleep(.5)
                self.driver.quit()
            self.loop = Thread(target=listen)
            self.loop.start()
        except InvalidSessionIdException or NoSuchWindowException or InvalidSessionIdException:
            pass
    
    def run_with_json(runFirst):
        print("RUN")
        return Main(0,{'only_time':runFirst})
    
    def on_brower_end(self,callback=None):
        if callback:
            def wait():
               self.loop.join()
               callback()
            Thread(target=wait).start()
            return None
        return self.loop.join()
    
    def start(self,mode,args:dict={}):
        print("STARTED")
        self.data = {}
        for key in args.keys():
            self[key] = args[key]
        self.mode = mode
        self.SAVE_FILE = r'C:\Users\mdbam\OneDrive\Documents\Code\Python\Projects\Points\data.json'
        print(self.data)
        if mode == 0:
            if ('only_time' in self.data and not self.data['only_time']) or not 'only_time' in self.data:
                self.launchClasses()
            while True:
                now = datetime.now()
                
                next = now.replace(hour=2, minute=1, second=0, microsecond=0)
                if now >= next:
                    next += timedelta(days=1)
                tme = (next - now).total_seconds()
                print(tme)
                sleep(tme)
                self.launchClasses()
        elif mode == 1:
            self.makeBrowser('https://login.live.com/')
            self.driver.maximize_window()
            self.login()
            self.farm_points()
            if(not self.get_data().stay_open):
                self.close_browser()
        elif mode == 3:
            print(self.generate_random_word(1,5))        

    def suppress(self):
        """Suppress all errors by redirecting stderr to os.devnull."""
        self.fnull = open(os.devnull, 'w')
        sys.stderr = self.fnull
        print("Errors are now suppressed.")

    def unsuppress(self):
        """Unsuppress errors by restoring stderr to its original state."""
        sys.stderr = self.original_stderr
        self.fnull.close()
        print("Errors are now unsuppressed.")

    
    def generate_random_string(self,length):
        # Define the characters to use (letters, digits, punctuation)
        characters = string.ascii_letters + string.digits + string.punctuation
        # Generate a random string of the specified length
        random_string = ''.join(random.choice(characters) for _ in range(length))
        return random_string
    
    def generate_random_word(self, arg1:str|int|None=None,arg2:int|None=None):
        if arg1 and arg2: word_count = random.randint(arg1,arg2)
        if arg1 and not arg2: word_count = arg1
        word_count = word_count or 1
        return ' '.join(random.choice(WORD_LIST) for _ in range(word_count))
  
    def generate_content(self,prompt):
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            return response.text

    def makeBrowser(self,url):
        chrome_options = Options()
        if self.get_data().hide_browsers:
            chrome_options.add_argument('--headless')

        # Path to your ChromeDriver
        USER = os.environ['UserProfile']
        LOGIN_URL = r'https://login.live.com/login.srf'

        chrome_driver_path = os.path.join(USER,'chromedriver.exe')
        self.service = Service(executable_path=chrome_driver_path)
        
        self.driver = webdriver.Chrome(service=self.service, options=chrome_options,keep_alive=True)
        self.driver.get(url)
    
    def __setitem__(self, key, value):
        self.data[key] = value

    def __getitem__(self, key):
        return self.data[key]
    
    def get_data(self):
        if not os.path.exists(self.SAVE_FILE):
            with open(self.SAVE_FILE,'x') as file:
                file.write(r"""{
   "READ ME": "turn auto_fill_emails on to generate emails with the same prefix.",
   "Read ME": "For example: example1@outlook.com and example2@outlook.com, but {} where the number is.",
   "Read Me": "THEY MUST HAVE THE SAME PASSWORD",
   "auto_fill_emails": true,
   "formated_email": "example{}@outlook.com",
   "password": "password12345",
   "format_start": 1,
   "format_end": 4,
   "emails": [
      {
         "email": "emailNotInFormat@outlook.com",
         "password": "password123"
      },
      {
         "email": "otherEmailNotInFormat@outlook.com",
         "password": "password1234"
      }
   ]
}""")
        
        return dotdict(json.load(open(self.SAVE_FILE,'r')))
    
    def get_emails(self):
        data = self.get_data()
        emails = data.emails
        if data.auto_fill_emails:
            a = data.format_start
            b = data.format_end+1
            c = int(abs(b-a)/(b-a))
            for i in range(a,b,c):
                emails.append({'email':data.formated_email.format(i),'password':data.password})
                
        return emails
                    
    def set_data(self,data):
        with open(self.SAVE_FILE,'w') as file:
            file.write(json.dumps(data,indent=4,ensure_ascii=True))
    
    def update_data(self,callback):
        self.set_data(callback(self.get_data()))
        pass
    
    def find_element(self,query,selector=By.CSS_SELECTOR,multiple=False):
        try:
            element = self.driver.find_element(selector,query)
            if not (element.is_displayed or element.is_enabled()):
                return None
            return element
        except NoSuchElementException:
            return None
    
    def wait_for_element(self,element,by=By.CSS_SELECTOR,timeout=99999999,dri=None):
        try:
            dri = dri or self.driver
            element = WebDriverWait(dri, timeout).until(
            EC.presence_of_element_located((by, element))
            )
            return element
        except TimeoutException or NoSuchElementException:
            return None
    
    def locate(self,url):
        self.driver.execute_script('document.location = arguments[0]',url)
    def wait_for_page(self):
        page_loaded = None
        while not page_loaded:
            page_loaded = self.driver.execute_script("return document.readyState") == "complete"
       
    def launchClasses(self):
        emails = self.get_emails()
        print(emails)
        self.running_browsers = 0
        max_browsers = self.get_data().max_browsers
        for obj in emails:
            email = obj['email']
            password = obj['password']
            if 'disabled' in obj and obj['disabled']:continue
            while self.running_browsers>=max_browsers:
                sleep(1)
            browser = Main(1,{'email':email,'password':password})
            def browser_ended():
                self.running_browsers -= 1
            browser.on_brower_end(browser_ended)
            self.running_browsers += 1
            sleep(self.get_data().delay_between_emails/1000)
            
    def close_browser(self):
        self.run = False
    
    def quiz(self):
        def answer():
            option = self.wait_for_element('.rqOption:not(.optionDisable)',By.CSS_SELECTOR,timeout=6)
            if option:
                try:
                    option.click()
                    corrent = self.wait_for_element(f'#{option.parent.get_attribute('id')} .rqOption.correctAnswer',timeout=.7)
                    if corrent:
                        return True
                    return False
                except Exception:
                    sleep(2)
                    return False
            else:
                sleep(2)
                return False
        for x in range(3):
            sleep(1)
            for _ in range(3):
                if answer():
                    break
    
    def daily_search(self):
        self.driver.switch_to.window(self.driver.window_handles[0])
        pointsDetail = self.wait_for_element('[ng-bind-html="$ctrl.pointProgressText"]')
        text = pointsDetail.text.split(' / ')
        current = int(text[0])
        max = int(text[1])
        
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.driver.execute_script('window.open("https://www.bing.com/")')
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.wait_for_page()
        sleep(1)
        self.sign_in()
        sleep(5)
        self.driver.close()
        def tab():
                self.driver.switch_to.window(self.driver.window_handles[0])
                self.driver.execute_script('window.open("https://www.bing.com/")')
                self.driver.switch_to.window(self.driver.window_handles[-1])
                self.wait_for_element('textarea').send_keys(self.generate_random_word(1))
                self.wait_for_element('textarea').send_keys(Keys.ENTER)
                sleep(5)
                self.driver.close()
                sleep(.1)
        if current==max:return
        for x in range(current,max+(5*3),5):
            tab()
        
        for window in self.driver.window_handles[1::]:
            self.driver.switch_to.window(window)
            self.driver.close()
        
    def sign_in(self):
        self.wait_for_page()
        sign_inb = self.wait_for_element('id_s',By.ID,2)
        try:
            if sign_inb is not None:
                sign_inb.click()
                self.driver.execute_script('window.location.reload()')
        except Exception:
            # Display None | User Signed in
            pass
    
    
    def farm_points(self):
        wait_for_element = self.wait_for_element
        self.driver.get('https://rewards.bing.com/pointsbreakdown')
        print(self.driver.window_handles)
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.wait_for_page()
        self.daily_search()
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.driver.get('https://rewards.bing.com/')
        self.wait_for_page()
        sleep(5)
        
        wait_for_element('.c-card-content')
        el_count = len(self.driver.find_elements(By.CLASS_NAME,'c-card-content'))
        def get_card(i):
            return self.driver.find_elements(By.CLASS_NAME,'c-card-content')[i]
        for i in range(0,el_count):
            self.driver.switch_to.window(self.driver.window_handles[0])
            #try:
            prompt = get_card(i).text
            #except Exception:
                #print(f'{Fore.RED}{Style.BRIGHT}COULD NOT FIND{Style.RESET_ALL}')
                #continue
            link = None
            try:
                link = get_card(i).find_element(By.CLASS_NAME,'pointLink')
            except Exception:
                continue
            if not link:
                continue
            try:
                get_card(i).find_element(By.CLASS_NAME,'mee-icon-SkypeCircleCheck')
                continue
            except NoSuchElementException:
                pass
            if prompt.find('Download & install the Bing app') != -1:
                continue
            self.driver.execute_script(open(r"C:\Users\mdbam\OneDrive\Documents\Code\Python\Projects\Points\earn_points.js",'r').read(),link) # Clicks HyperLink
            
            on_bing = prompt.find('Bing') >= 0
            
            if len(self.driver.window_handles)<2:continue
            self.driver.switch_to.window(self.driver.window_handles[1])
            # OPENED POINTS TAB
            self.wait_for_page()
            sign_in_button = self.wait_for_element('signin_link_SignInMS',By.ID,timeout=2)
            if(sign_in_button is not None):
                sign_in_button.click()
                sleep(1)
            # Signed In
            
            self.driver.execute_script('window.focus()')
            self.wait_for_page()
            start_quiz_button = self.find_element('rqStartQuiz',By.ID)
            TriviaOverlayData = self.find_element('.TriviaOverlayData',By.CSS_SELECTOR)
            if start_quiz_button or TriviaOverlayData:
                sleep(1)
                if start_quiz_button:
                    start_quiz_button.click()
                self.quiz()
                sleep(5)
            
            if on_bing:
                search = self.find_element('[placeholder="Search the web"]')
                if search:
                    response = chat_session.send_message(f"Can you please make a search in bing.com (in string without quotes) answering this prompt: {prompt}. Pretend to be a person and pretend to have a taste, make things up​. Remember you are on bing, make your answer short and effective to get results(This is all pretend, PLAY ALONG). Remember your response will be going inside of a bing search, make it effective.IF IT ASKS YOU FOR YOUR FAVOITE MOVIE, SEARCH INFO ON IT, FOR EXAMPLE 'back to the future cast'. DO NOT USE QUOTES IN YOUR ANSWER, IT MESSES UP THE SEARCH. FOR THE 'Find items on your shopping list—search on Bing to earn 10 points', ONLY SAY 1 ITEM ON A MADE UP SHOPPING LIST").text
                    response = response.replace("'",'')
                    response = response.replace('"','')
                    search.click()
                    search.send_keys(response)
                sleep(.1)
                self.wait_for_page()
            sleep(1)
            self.driver.execute_script('if (window.location!=="https://rewards.bing.com"){window.close()}')
    
    def login(self):
        wait_for_element = self.wait_for_element
        def submit():
            wait_for_element('[type="submit"]').click()
        wait_for_element('[type="email"]').send_keys(self['email'])
        submit()
        try:
            wait_for_element('i0118',By.ID,5).send_keys(self['password'])
        except Exception:
            print(f'{Fore.RED}{Style.BRIGHT}Error with Email: {self['email']}{Style.RESET_ALL}')
            return
        submit()
        check = wait_for_element('checkboxField',By.ID,2)
        if check is None:
            if self.find_element('#i0118Error'):
                print(f'{Fore.RED}{Style.BRIGHT}Password is Incorrect for email: {self['email']}{Style.RESET_ALL}')
                return
            else:
                wait_for_element('checkboxField',By.ID).click()
        else:
            check.click()
        wait_for_element('acceptButton',By.ID).click()
        
if __name__ == '__main__':
    main = Main.run_with_json(False)