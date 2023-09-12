from flask import Flask, request
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
# py -3 -m pip install webdriver_manager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
#cron schedule 0 5/2 * * 1-6

app = Flask(__name__)
#driver = None

def download_selenium():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-smh-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
    if (not driver):
        return "Failed to load Chrome Driver"
    
    driver.get("https://digital.etu.ru/attendance/student")
    result = clicking_button(driver)
    driver.close()
    return result

def clicking_button(driver):
    element = None
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div[2]/p/div/button'))
        )
    finally:
        element.click()


    driver.implicitly_wait(1)
    element = driver.find_element(By.XPATH, "/html/body/div/div[1]/div/div[2]/div/form/div[1]/div/div/input")
    element.send_keys("mrsinty@gmail.com")
    element = driver.find_element(By.XPATH, "/html/body/div/div[1]/div/div[2]/div/form/div[2]/div/div/input")
    element.send_keys("Irjkf2345")
    element.send_keys(Keys.RETURN)
    if (not element):
        return "Failed to enter email or password (maybe there's no such element)"

    driver.implicitly_wait(5)

    element = driver.find_element(By.XPATH, "/html/body/div/div[1]/div/div[2]/div/div[4]/div/div[2]/form/button")
    if (element):
        element.click()
    else:
        return "Failed to press 'Авторизоваться' button"

    element = driver.find_element(By.XPATH, 'XPATH //*[@id="__BVID__47"]/div/div/div[1]/div/div/button')
    if (element):
        element.click()
    else:
        return "Failed to press 'Посетил' button"

    return "Success!"

@app.route('/', methods=['GET','POST'])
def home():
    if(request.method == 'GET'):
        return download_selenium()
    #elif(request.method == 'POST'):

if (__name__ == "__main__"):
    app.run(debug=True, port=3000)


#driver = webdriver.Chrome()
#driver.get("https://digital.etu.ru/attendance/student")

#CSS_SELECTOR "#__BVID__46 > div > div > div:nth-child(1) > div > div > button"
#XPATH //*[@id="__BVID__47"]/div/div/div[1]/div/div/button
#сам элемент <button data-v-2a931ce0="" type="button" class="btn custom-button small mt-3 btn-primary"> Отметиться </button>
#elements = driver.find_element(By.CLASS_NAME, "card class-card mt-2 current")
#elem2 = elements.find_element(By.CLASS_NAME, "card-body").find_element(By.CLASS_NAME, "btn custom-button small mt-3 btn-primary")

#element = driver.find_element(By.CLASS_NAME, 'tab-content')
#element = driver.find_element(By.XPATH, '//*[@id="__BVID__47"]/div/div/div[1]/div/div/button')
#element.click()
#action = webdriver.common.action_chains.ActionChains(driver)
#action.move_to_element_with_offset(el, 5, 5)
#action.click()
#action.perform()
#print(element)
#time.sleep(30)
#driver.implicitly_wait(10)
