from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def test_driver():
    print("started")
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    driver = webdriver.Remote(
        command_executor="http://selenium:4444",
        options=chrome_options
    )
    driver.get("https://n.rivals.com/content/prospects/2016/chance-lytle-2486")
    div = driver.find_element(By.CSS_SELECTOR, "[data-philter='prospect-profile-info'] div")
    print(div.get_attribute("innerText"))
