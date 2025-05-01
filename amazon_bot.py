import base64
from selenium import webdriver  
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
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
# optional: options.add_argument("--headless")

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
        claim_code_input_box = WebDriverWait(driver, 10).until(
        #EC.presence_of_element_located((By.ID, "claim-Code-input-box")
        EC.presence_of_element_located((By.ID,"gc-redemption-input")))
        captcha_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "gc-captcha-solution-input")))
        # passing the capcha if present 
        if captcha_box:
            captcha_element = driver.find_element(By.ID, 'gc-captcha-image')
            src_data = captcha_element.get_attribute('src')

            if src_data.startswith('data:image/png;base64,'):
            #     # Extract base64 data
                base64_data = src_data.split(',')[1]
            #     # Decode base64 to image bytes
                image_data = base64.b64decode(base64_data)
            #     # Save image temporarily
                with open(fr"/home/theanonymouse/ksi_tnl/temp_youtube_download/captcha{idx}.png", 'wb') as f:
                    f.write(image_data)
                
                result = ocr.init(fr"/home/theanonymouse/ksi_tnl/temp_youtube_download/captcha{idx}.png")
                if result!=[]:
                    print(result)
                    shadow_root = driver.execute_script('return arguments[0].shadowRoot', captcha_box )
                    captcha_input = shadow_root.find_element(By.CSS_SELECTOR, 'input')
                    captcha_input.send_keys(result[0])
                    # Get the shadow root
                    #shadow_root = driver.execute_script("return arguments[0].shadowRoot",claim_code_input_box)
                    #coupon_code = shadow_root.find_element(By.CSS_SELECTOR, "input")
                    coupon_code.send_keys(value) # real coupon for testing purpose # fyi its know claimed
                    #button = driver.find_element(By.CLASS_NAME, "add-gift-card-button")
                    button = driver.find_element(By.CLASS_NAME,"gc-redemption-apply-button")
                    button.click()                                        
                else:
                    print(f"Captcha text could not be read from temp_youtube_download/captcha{idx}.png")
            else:
                print("Captcha image src is not in expected base64 format.")
        else:
            print("Captcha element not found :")
            # Get the shadow root
            # in europe website its not the input box of coupon is not custom <tux-input> its only <input>
            #shadow_root = driver.execute_script('return arguments[0].shadowRoot', claim_code_input_box)
            #coupon_code = shadow_root.find_element(By.CSS_SELECTOR, 'input')
            coupon_code.send_keys(value) # real coupon for testing purpose # fyi its know claimed
            # for us based use this one
            #button = driver.find_element(By.CLASS_NAME, "add-gift-card-button")
            # for europe use this link 
            button = driver.find_element(By.CLASS_NAME, "gc-redemption-apply-button")
            button.click()
            
            
            
        
        
        
      
        
        
        
        
        
        
        
    
    
    
    
    
    





