import os
from celery import shared_task 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .models import Proxy

@shared_task
def scrape_task():
    chrome_driver_path = os.getenv("CHROMEDRIVER_PATH", "/usr/bin/chromedriver")

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--remote-debugging-port=9222")

    try:
        driver = webdriver.Chrome(
            service=ChromeService(chrome_driver_path),
            options=options
        )

        driver.get("https://geonode.com/free-proxy-list")

        target_locator = (By.TAG_NAME, "table")

        wait = WebDriverWait(driver, 60)
        wait.until(EC.presence_of_element_located(target_locator))

        proxie_body = driver.find_element(By.TAG_NAME, "tbody")
        proxie_rows = proxie_body.find_elements(By.TAG_NAME, "tr")

        proxies = []

        for row in proxie_rows:
            proxie_data = row.find_elements(By.TAG_NAME, "td")
            proxy = {
                "ip": proxie_data[0].text,
                "port": proxie_data[1].text,
                "protocol": proxie_data[3].text,
                "country": proxie_data[2].text,
                "uptime": proxie_data[7].text
            }
            proxies.append(proxy)

        # bulk insert for efficiency
        Proxy.objects.bulk_create([
            Proxy(**proxy) for proxy in proxies
        ])

        return f"Task Complete! {len(proxies)} proxies saved."

    except Exception as e:
        return f"Scraping failed: {str(e)}"

    finally:
        try:
            driver.quit()
        except:
            pass
