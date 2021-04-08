from selenium import webdriver
from selenium.webdriver.firefox.options import Options
def configuration():
    opt = Options()
    opt.add_argument("--headless")
    driver = webdriver.Firefox(executable_path=".\geckodriver\geckodriver.exe",options=opt)
    return driver
