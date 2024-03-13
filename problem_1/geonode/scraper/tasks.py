from celery import shared_task 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .models import Proxy

@shared_task
def scrape_task():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')

    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=options
    )

    driver.get("https://geonode.com/free-proxy-list")

    target_locator = (By.CSS_SELECTOR,"td.capitalize")

    wait = WebDriverWait(driver, 60)
    wait.until(EC.presence_of_element_located(target_locator))

    proxie_body = driver.find_element(By.TAG_NAME, "tbody")
    proxie_rows = proxie_body.find_elements(By.TAG_NAME, "tr")

    proxies = []

    for row in proxie_rows:
        proxie_data = row.find_elements(By.TAG_NAME, 'td')
        proxy = {
            "IP ADDRESS": proxie_data[0].text,
            "PORT": proxie_data[1].text,
            "PROTOCOL": proxie_data[3].text,
            "COUNTRY": proxie_data[2].text,
            "UPTIME": proxie_data[7].text
        }
        proxies.append(proxy)
        # save to db
        p = Proxy.objects.create(
            ip=proxie_data[0].text,
            port=proxie_data[1].text,
            protocol=proxie_data[3].text,
            country=proxie_data[2].text,
            uptime=proxie_data[7].text
        )
        p.save()
        print("Proxy saved to db")

    driver.quit()
    return f"Task Complete! count of data {len(proxies)}"