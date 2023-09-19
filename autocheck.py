from flask import Flask
from flask_script import Manager, Server
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
#cron schedule 0 5/2 * * 1-6

def download_selenium():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-smh-usage")
    chrome_options.add_argument("./chromedriver/chromedriver.exe")
    driver = webdriver.Chrome(options=chrome_options)

    if (not driver):
        return "Failed to load Chrome Driver"
    
    driver.get("https://digital.etu.ru/attendance/student")
    result = clicking_button(driver)
    driver.close()
    return result

def clicking_button(driver):
    element = None

    if (not driver):
        return "Failed to load Chrome Driver"

    driver.implicitly_wait(5)
    element = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div[2]/p/div/button') # Войти через ETU ID
    if (element):
        element.click()

        driver.implicitly_wait(2)
        element = driver.find_element(By.XPATH, "/html/body/div/div[1]/div/div[2]/div/form/div[1]/div/div/input")
        element.send_keys("mrsinty@gmail.com")
        element = driver.find_element(By.XPATH, "/html/body/div/div[1]/div/div[2]/div/form/div[2]/div/div/input")
        element.send_keys("Irjkf2345")
        element.send_keys(Keys.RETURN)

        if (element):
            
            driver.implicitly_wait(5)
            element = driver.find_element(By.XPATH, "/html/body/div/div[1]/div/div[2]/div/div[4]/div/div[2]/form/button")
            #авторизоваться
            element.click()

            driver.implicitly_wait(5)

            element = driver.find_element(By.XPATH, '//*[@id="__BVID__47"]/div/div/div[1]/div/div/button')

            print('!!!')

            try:
                element.click()
            except WebDriverException:
                return "Failed to press 'Посетил' button after authorization"
            
        else:
            return "Failed to enter email or password (maybe there's no such element)"
        
    else:
        driver.implicitly_wait(5)
        element = driver.find_element(By.XPATH, '//*[@id="__BVID__47"]/div/div/div[1]/div/div/button')

        print('@@@')

        try:
            element.click()
        except WebDriverException:
            return "Failed to press 'Посетил' button without authorization"

    return "Success!"

class CustomServer(Server):
    def __call__(self, app, *args, **kwargs):
        download_selenium()
        return Server.__call__(self, app, *args, **kwargs)

app = Flask(__name__)
manager = Manager(app)
manager.add_command('runserver', CustomServer(port=3000))

if __name__ == "__main__":
    manager.run()
