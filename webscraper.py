from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import io
from PIL import Image

querys = ['one real  full banana']

def download_image(download_path, url, file_name):
	try:
		image_content = requests.get(url).content
		image_file = io.BytesIO(image_content)
		image = Image.open(image_file)
		file_path = download_path + file_name

		with open(file_path, "wb") as f:
			image.save(f, "JPEG")

		print("Success")
	except Exception as e:
		print('FAILED -', e) 

def scroll_to_bottom():
        '''Scroll to the bottom of the page
        '''
        last_height = driver.execute_script('return document.body.scrollHeight')
        while True:
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            time.sleep(2)

            new_height = driver.execute_script('return document.body.scrollHeight')
            try:
                element = driver.find_element(
                    by=By.CSS_SELECTOR,
                    value='.YstHxe input'
                )
                element.click()
                time.sleep(2)
            except:
                pass

            if new_height == last_height:
                break

            last_height = new_height

for query in querys:
      #options = webdriver.ChromeOptions()
      #service = Service(executable_path='/Users/sandeepanghosh/Downloads/chromedriver_mac_arm64/chromedriver')
      driver =webdriver.Safari() #webdriver.Chrome(service=service, options=options)
      driver.maximize_window()
      url = 'https://images.google.com/'
      driver.get(
              url=url
        )
      box = driver.find_element(
              by=By.XPATH,
              value='//div[@jscontroller="vZr2rb"]//textarea'
        )
      box.send_keys(query)
      box.send_keys(Keys.ENTER)
      time.sleep(2)
      scroll_to_bottom()
      time.sleep(2)
      img_results = driver.find_elements(
              by=By.XPATH,
              value="//img[contains(@class,'rg_i Q4LuWd')]"
        )
      print(f'Total images -> {len(img_results)}')
       
      c=314
      image_url=[]
      for img_result in img_results[314::]:
            WebDriverWait(
                driver,
                15
            ).until(
                EC.element_to_be_clickable(
                    img_result
                )
            )
            img_result.click()
            time.sleep(2)
            print("image clicked")
            try:
                  actual_img = driver.find_element(by=By.XPATH,
        value="//img[contains(@class,'r48jcc pT0Scc iPVvYb')]")
                  print("success")
                  src = actual_img.get_attribute("src")
                  print(src)
                  image_url.append(src)
                  download_image("/Users/sandeepanghosh/Downloads/Dataset/bread/", src,'breadbread'+str(c) + ".jpg")
                  c=c+1
            except:
                  continue
    #   for i, url in enumerate(image_url):
    #         download_image("E:/dataset/", url, query+str(i) + ".jpg")
    #   image_url=[]
    
            


      
      