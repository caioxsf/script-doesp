import time
from datetime import date

from src.browser import Browser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scraping_doesp():
    browser = Browser()

    date_today = date.today() 
    browser.open(f"https://doe.sp.gov.br/sumario?editionDate=2025-6-18")

    WebDriverWait(browser.driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Executivo')]"))
    ).click()
    time.sleep(1)

    WebDriverWait(browser.driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Atos Normativos')]"))
    ).click()
    time.sleep(1)

    WebDriverWait(browser.driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='__next']/div[2]/div/div[4]/div/div[2]/div/div[1]/div/div/div"))
    ).click()
    time.sleep(1)

    WebDriverWait(browser.driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//li[contains(., 'Secretaria da Educação')]"))
    ).click()
    time.sleep(1)

    aux = False
    i = 0
    while True:
        try:
            if aux == False:
                try:
                    element_list = WebDriverWait(browser.driver, 2).until(
                        EC.presence_of_element_located(
                            (By.ID, f"mui-tree-view-{i}-777a380f-509a-48b6-4ebd-08db6b9689d9")
                        )
                    )
                except:
                    pass
            if element_list:
                aux = True
                break
            i += 1
        except Exception as e:
            print("Error for get element of Diretoria de Ensino de Assis: ", e)
        
    time.sleep(1)
    links = element_list.find_elements(By.XPATH, ".//a")
    for link in links:
        link.click()
