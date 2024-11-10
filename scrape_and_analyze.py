from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Укажите полный путь к chromedriver
chrome_driver_path = "C:\\Users\\ionel\\Desktop\\senti.ai\\chromedriver.exe"
service = Service(chrome_driver_path)

# Укажите путь к Chrome
chrome_options = Options()
chrome_options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
chrome_options.add_argument("--start-maximized")

# Настройка и запуск браузера
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get("https://app.getquin.com/en")

print("Контент найден. Начинается сбор данных...")

# Ждём, пока элементы с сообщениями загрузятся
try:
    # Устанавливаем ожидание для загрузки основного контента
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='infinite_list']"))
    )
    
    # Прокрутка страницы для загрузки дополнительного контента
    last_height = driver.execute_script("return document.body.scrollHeight")
    messages = []

    while True:
        # Сбор данных на текущей высоте
        elements = driver.find_elements(By.CSS_SELECTOR, "[data-testid='infinite_list'] .Activities_activity__phjsY")
        for element in elements:
            try:
                message = element.text
                if message not in messages:  # Чтобы избежать дублирования
                    messages.append(message)
            except Exception as e:
                print(f"Ошибка при сборе сообщения: {e}")

        # Прокручиваем страницу вниз
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        # Проверяем, достигли ли конца страницы
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    print(f"Собрано {len(messages)} сообщений.")
    for msg in messages:
        print(msg)

except Exception as e:
    print(f"Произошла ошибка: {e}")

finally:
    # Завершаем работу браузера
    driver.quit()
