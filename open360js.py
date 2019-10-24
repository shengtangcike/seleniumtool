import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# __browser_url = r'D:\Program Files\360Chrome\Chrome\Application\360chrome.exe'
__browser_url = r'D:\Program Files (x86)\360\360se6\Application\360se.exe'
chrome_options = Options()
chrome_options.binary_location = __browser_url
# chrome_options.add_argument(r"user-data-dir=C:\Users\WIN10\AppData\Local\Temp\scoped_dir13744_21778\Default")
chrome_options.add_argument(r"C:\Users\WIN10\AppData\Local\Temp\scoped_dir12768_11190\Default")
browser = webdriver.Chrome(chrome_options=chrome_options)
browser.get("https://passport.csdn.net/login")
time.sleep(2)
browser.quit()