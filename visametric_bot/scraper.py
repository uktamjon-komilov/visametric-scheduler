import os
import re
import time
import random
import urllib
from datetime import datetime, timedelta
import gc

import pydub
import speech_recognition as sr

from celery.utils.log import get_task_logger

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from django.conf import settings

from .helpers import is_valid_url
from .models import Customer

USER_AGENT_LIST = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
)

logger = get_task_logger(__name__)

class WebScraper:
    def __init__(self, customer: Customer) -> None:
        self.url = "https://uz-appointment.visametric.com/uz/appointment-form"
        self._launch_browser()
        self.customer = customer

    def _launch_browser(self):
        """
            A method that configures the selenium web driver and opens up a browser instance
            If the '--headless' argument was added, the web driver runs in the background without a GUI
        """
        
        chrome_options = webdriver.ChromeOptions()

        # uncomment below line if you want to run it without a GUI (mainly on VPS)

        chrome_options.add_argument("--headless")

        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-setuid-sandbox")
        chrome_options.add_argument("--disable-dev-shm-using")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("start-maximized")
        chrome_options.add_argument("disable-infobars")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        
        # Randomize and choose one of the user agents to make the website not detect our bot
        user_agent = random.choice(USER_AGENT_LIST)
        chrome_options.add_argument(f"user-agent={user_agent}")

        logger.debug("scraper 70")

        if settings.USE_REMOTE_DRIVER:
            self.driver = webdriver.Remote(
                command_executor="http://selenium:4444",
                options=chrome_options,
                desired_capabilities=DesiredCapabilities.CHROME
            )
        else:
            self.driver = webdriver.Firefox(options=chrome_options)
        
        logger.debug("scraper 81")

        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self._delay()
        self.driver.get(self.url)
        logger.debug("scraper 86")
    
    def __del__(self):
        self.driver.quit()
        del self.driver
        gc.collect()

        
    def _delay(self, waiting_time: int=5):
        """
            Implicitly waiting method that helps us to be undetectable, the browser wait 'waiting_time' seconds
        """
        self.driver.implicitly_wait(waiting_time)

    def check_availability(self) -> bool:
        """
            This function checks is there are any available application places
        """
        user_living_place = self.customer.address
        self.driver.find_element(By.ID, "country").find_elements(By.TAG_NAME, "option")[2].click()
        self.driver.find_element(By.ID, "visitingcountry").find_elements(By.TAG_NAME, "option")[1].click()
        cities = Select(self.driver.find_element(By.ID, "city"))
        values = [option.text for option in cities.options]

        if user_living_place in values:
            cities.select_by_visible_text(user_living_place)

        self.driver.find_element(By.ID, "office").find_elements(By.TAG_NAME, "option")[1].click()
        self.driver.find_element(By.ID, "officetype").find_elements(By.TAG_NAME, "option")[1].click()
        self.driver.find_element(By.ID, "totalPerson").find_elements(By.TAG_NAME, "option")[1].click()

        available_day_info = self.driver.find_element(By.ID, "availableDayInfo").find_element(By.TAG_NAME, "div").text

        if available_day_info != "Sana mavjud emas":
            return True
        
        return False
    
    def select_option_by_text(self, select_elem, text: str) -> None:
        """Select an option from a dropdown by text."""
        options = Select(select_elem).options
        for option in options:
            if option.text == text:
                option.click()
                break

    def select_birthday(self, date: str) -> None:
        """Select the birth date of the customer."""
        year, month, day = date.split('-')
        self.select_option_by_text(self.driver.find_element(By.ID, 'birthday1'), day)
        self.select_option_by_text(self.driver.find_element(By.ID, 'birthmonth1'), month)
        self.select_option_by_text(self.driver.find_element(By.ID, 'birthyear1'), year)

    def fill_personal_info(self) -> None:
        """Fill the personal information section of the form."""
        self.driver.find_element(By.ID, 'name1').send_keys(self.customer.first_name)
        self.driver.find_element(By.ID, 'surname1').send_keys(self.customer.last_name)
        self.driver.find_element(By.ID, 'localname1').send_keys(self.customer.first_name + ' ' + self.customer.last_name)
        options = self.driver.find_element(By.ID, 'nationality1')
        self.select_option_by_text(options, text='Uzbekistan')
        self.select_birthday(self.customer.birth_date.strftime('%Y-%m-%d'))
        self.driver.find_element(By.ID, 'passport1').send_keys(self.customer.passport_number)
        self.driver.execute_script(
            f"arguments[0].value = '{self.customer.passport_valid_date.strftime('%d-%m-%Y')}';",
            self.driver.find_element(By.ID, 'passportExpirationDate1')
        )
        self.driver.find_element(By.ID, 'email1').send_keys(self.customer.email)
        self.driver.find_element(By.ID, 'phone1').send_keys(self.customer.phone_number)

    
    def select_day(self, days, order_by: str) -> None:
        """Select a day from the calendar based on the specified order."""
        if order_by == 'increase':
            day_to_click = days[0]
        else:
            day_to_click = days[-1]
        day_to_click.click()

    def fill_form(self) -> None:
        """Fill the entire form."""

        order_by = "increase"
        if self.check_availability():
            
            self.driver.find_element(By.ID, 'btnAppCountNext').click()
            wait = WebDriverWait(self.driver, 10)

            self.fill_personal_info()

            btn = self.driver.find_element(By.ID, 'btnAppPersonalNext')
            self.driver.execute_script("arguments[0].scrollIntoView();", btn)
            btn.click()
            btn = self.driver.find_element(By.ID, 'btnAppPreviewNext')
            self.driver.execute_script("arguments[0].scrollIntoView();", btn)
            btn.click()
            btn = self.driver.find_element(By.ID, 'personalapproveTerms')
            self.driver.execute_script("arguments[0].scrollIntoView();", btn)
            btn.click()
            btn = self.driver.find_element(By.ID, 'btnCreditCard')
            self.driver.execute_script("arguments[0].scrollIntoView();", btn)
            btn.click()

            starting_journey = datetime.today().date() + timedelta(days=10)
            ending_journey = starting_journey + timedelta(days=10)
            self.driver.execute_script(
                f"arguments[0].value = '{starting_journey.strftime('%d-%m-%Y')}';",
                self.driver.find_element(By.NAME, 'travelStartDate')
            )
            self.driver.execute_script(
                f"arguments[0].value = '{ending_journey.strftime('%d-%m-%Y')}';",
                self.driver.find_element(By.NAME, 'travelEndDate')
            )

            datepicker = self.driver.find_element(By.ID, 'tarihGoster')
            self.driver.execute_script("arguments[0].style.display = 'block';", datepicker)
            self.driver.find_element(By.XPATH, "//input[@class='form-control calendarinput']").click()
            days = self.driver.find_elements(By.XPATH, "//td[@class='day']")

            self.select_day(days, order_by)

            wait.until(EC.visibility_of_element_located((By.XPATH, "//button[contains(@class, 'noPrime')]"))).click()
            self.driver.find_element(By.ID, 'btnAppCalendarNext').click()
            self.solve_recaptcha()


            self._delay(5)
            self.driver.switch_to.default_content()
            time.sleep(2)
            try:
                self.driver.find_element(By.ID, "btnAppServicesNext").click()
            except:
                pass

            time.sleep(3)
            
            self.driver.find_elements(By.TAG_NAME, "a")[-1].get_attribute("href")
                
            self.customer.is_active = False
            self.customer.url_for_document = self.driver.find_elements(By.TAG_NAME, "a")[-1].get_attribute("href")
            self.customer.save()
            # driver.quit()

    def solve_recaptcha(self):
        """Solve reCAPTCHA using audio challenge."""

        frames = self.driver.find_elements(By.TAG_NAME, "iframe")
        recaptcha_control_frame = None
        recaptcha_challenge_frame = None

        for frame in frames:
            if re.search('reCAPTCHA', frame.get_attribute("title")):
                recaptcha_control_frame = frame
                
            if re.search('recaptcha challenge', frame.get_attribute("title")):
                recaptcha_challenge_frame = frame

        self.driver.switch_to.frame(recaptcha_control_frame)
        self.driver.find_element(By.CLASS_NAME, "recaptcha-checkbox-border").click()

        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(recaptcha_challenge_frame)
        
        try:
            time.sleep(3)
            try:
                self.driver.find_element(By.ID, "recaptcha-audio-button").click()
                src = self.driver.find_element(By.ID, "audio-source").get_attribute("src")
                path_to_mp3 = os.path.normpath(os.path.join(os.getcwd(), "sample.mp3"))
                path_to_wav = os.path.normpath(os.path.join(os.getcwd(), "sample.wav"))
                urllib.request.urlretrieve(src, path_to_mp3)

                try:
                    sound = pydub.AudioSegment.from_mp3(path_to_mp3)
                    sound.export(path_to_wav, format="wav")
                    sample_audio = sr.AudioFile(path_to_wav)
                except Exception as e:
                    print("[ERR] Unable to convert audio file: ", e)
                    return None

                r = sr.Recognizer()
                with sample_audio as source:
                    audio = r.record(source)
                key = r.recognize_google(audio)

                # Submit the reCAPTCHA response
                self.driver.switch_to.default_content()
                self.driver.switch_to.frame(recaptcha_challenge_frame)
                audio_response = self.driver.find_element(By.ID, "audio-response")
                audio_response.send_keys(key.lower())
                audio_response.send_keys(Keys.ENTER)
                return key.lower()
            except:
                pass
            # Download and convert the audio file
            
        except NoSuchElementException:
            pass
