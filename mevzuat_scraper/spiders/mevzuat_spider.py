import scrapy
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

class MevzuatSeleniumSpider(scrapy.Spider):
    name = "MevzuatSeleniumSpider"
    start_urls = ['https://www.mevzuat.gov.tr']
    
    MEVZUAT_SELECTORS = {
        "Kanun": {
            "link_title": "Kanunlar",
            "form_id": "kanunlar_form"
        },
        "Cumhurbaşkanlığı Kararnamesi": {
            "link_title": "Cumhurbaşkanlığı Kararnameleri",
            "form_id": "cumhurbaskanligiKararnameleri_form"
        },
        "Cumhurbaşkanlığı ve Bakanlar Kurulu Yönetmeliği": {
            "link_title": "Cumhurbaşkanlığı ve Bakanlar Kurulu Yönetmelikleri",
            "form_id": "cumhurbaskanligiveBakanlarKuruluYonetmelikleri_form"
        },
        "Kanun Hükmünde Kararname": {
            "link_title": "Kanun Hükmünde Kararnameler",
            "form_id": "kanunHukmundeKararnameler_form"
        },
        "Tüzük": {
            "link_title": "Tüzükler",
            "form_id": "tuzukler_form"
        },
        "Kurum ve Kuruluş Yönetmeliği": {
            "link_title": "Kurum Kuruluş ve Üniversite Yönetmelikleri",
            "form_id": "kurumKurulusVeUniversiteYonetmelikleri_form"
        },
        "Tebliğ": {
            "link_title": "Tebliğler",
            "form_id": "tebligler_form"
        }
    }

    def __init__(self, start_year=None, end_year=None, mevzuat_turu="Kanun", *args, **kwargs):
        super(MevzuatSeleniumSpider, self).__init__(*args, **kwargs)
        options = Options()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)
        
        self.start_year = start_year
        self.end_year = end_year
        self.mevzuat_turu = mevzuat_turu
        
    def parse(self, response):
        self.driver.get(response.url)
        
        # Seçilen mevzuat türüne göre selector'ları al
        selectors = self.MEVZUAT_SELECTORS.get(self.mevzuat_turu)
        if not selectors:
            raise ValueError(f"Desteklenmeyen mevzuat türü: {self.mevzuat_turu}")
            
        # İlgili mevzuat türü linkine tıkla
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f'a[title="{selectors["link_title"]}"]'))
        ).click()

        # Arama formunu bekle
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.ID, selectors["form_id"]))
        )
 
        # Form elementini bul
        form = self.driver.find_element(By.ID, selectors["form_id"])

        # Form içindeki elementleri bul
        form.find_element(By.ID, "BaslangicTarihi").send_keys(str(self.start_year))
        form.find_element(By.ID, "BitisTarihi").send_keys(str(self.end_year))
        form.find_element(By.ID, "btnSearch").click()
        
        # Sayfanın tamamen yüklendiğinden emin ol
        WebDriverWait(self.driver, 20).until(
            lambda driver: self.driver.find_element(By.ID, "loaderContainer").get_attribute("style") == "display: none;"
        )
        time.sleep(10)
        while True:
            try:
                # Get the list of laws
                kanunlar_table = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.ID, "DataTables_Table_0"))
                )
                
                kanunlar_rows = kanunlar_table.find_elements(By.TAG_NAME, "tr")

                for row in kanunlar_rows:
                    try:
                        # Find the link for each law
                        link_element = row.find_element(By.CSS_SELECTOR, "td a")
                        link = link_element.get_attribute("href")

                        # Open the link in a new tab
                        self.driver.execute_script("window.open(arguments[0]);", link)

                        # Switch to the new tab
                        self.driver.switch_to.window(self.driver.window_handles[-1])

                        # Switch to the iframe containing the law details
                        iframe = WebDriverWait(self.driver, 20).until(
                            EC.presence_of_element_located((By.ID, "mevzuatDetayIframe"))
                        )
                        self.driver.switch_to.frame(iframe)

                        # Get the page content
                        html_content = self.driver.page_source
                        soup = BeautifulSoup(html_content, 'html.parser')
                        
                        # Extract text only from the <body> tag
                        body_content = soup.body.get_text(separator=' ', strip=True)

                        # Yield the results
                        yield {
                            'url': link,
                            'full_text': body_content
                        }

                        # Close the current tab and switch back to the main tab
                        self.driver.close()
                        self.driver.switch_to.window(self.driver.window_handles[0])

                    except Exception as e:
                        print(f"Error occurred: {e}")

                # Move to the next page
                try:
                    next_page_button = self.driver.find_element(By.CSS_SELECTOR, 'li.paginate_button.page-item.active + li.paginate_button.page-item')
                    if 'disabled' in next_page_button.get_attribute('class'):
                        # If the next page button is disabled, we are on the last page
                        break
                    next_page_button.click()

                    # Ensure the next page is fully loaded
                    WebDriverWait(self.driver, 20).until(
                        lambda driver: self.driver.find_element(By.ID, "loaderContainer").get_attribute("style") == "display: none;"
                    )
                    time.sleep(3)  # Wait for the page to load

                except Exception as e:
                    print(f"Error occurred: {e}")
                    break

            except Exception as e:
                print(f"Error occurred: {e}")
                break

    def closed(self, reason):
        self.driver.quit()
