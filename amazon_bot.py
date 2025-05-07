import base64
from selenium import webdriver  
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
import requests
from dotenv import load_dotenv
import os
import ocr 

# Load the .env file
load_dotenv()

# Now you can access the variables
phone = os.getenv("phone")
pass_ = os.getenv("pass")


def init(coupon):
    ######## Add Chrome absolute path here #############
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

# Automatically match ChromeDriver version to your local Chromium version
    for idx,value in enumerate(coupon):
        service = Service(ChromeDriverManager(driver_version="135.0.7049.52").install())
        driver = webdriver.Chrome(service=service, options=options)
        #driver.get("https://www.amazon.in/apay-products/gc/claim")
        driver.get("https://www.amazon.de/gc/redeem/")
    #login phase
    # email or phone number 
        dialog = driver.find_element(By.ID,"ap_email")   
        dialog.send_keys(phone)
        button = driver.find_element(By.ID, "continue")
        button.click()
    ## entering password
        dialog = driver.find_element(By.ID,"ap_password")   
        dialog.send_keys(pass_)
        button = driver.find_element(By.ID, "signInSubmit")
        button.click()
        coupon_code = driver.find_element(By.ID,"gc-redemption-input")
        captcha_box = driver.find_element(By.ID, "gc-captcha-code-input")
        # passing the capcha if present 
        if captcha_box:
            captcha_element = driver.find_element(By.ID, 'gc-captcha-image')
            src_data = captcha_element.get_attribute('src')
            response = requests.get(src_data)
            with open(f"/home/theanonymouse/ksi_tnl/temp_youtube_download/captcha{idx}.jpg","wb") as f:
                f.write(response.content)
            result = ocr.init(fr"/home/theanonymouse/ksi_tnl/temp_youtube_download/captcha{idx}.jpg")
            if result!=[]:
                print(result)
                captcha_box.send_keys(result[0])
                coupon_code.send_keys(value) # real coupon for testing purpose # fyi its know claimed
                button = driver.find_element(By.ID,"gc-redemption-apply-button")
                a = input()
                button.click()                                        
            else:
                 print(f"Captcha text could not be read from temp_youtube_download/captcha{idx}.png")
        else:
            print("Captcha element not found :")
            coupon_code.send_keys(value) 
            button = driver.find_element(By.ID, "gc-redemption-apply-button")
            button.click()
            
            
            
        
        
        
      
        
        
        
        
        
        
        
    
    
    
    
    
    





