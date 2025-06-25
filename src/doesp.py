import time
from datetime import date

from src.browser import Browser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

section = [
    "Atos Normativos",
    "Atos de Pessoal",
    "Atos de Gestão e Despesas"
]

def scraping_doesp():
    browser = Browser()

    date_today = date.today() 
    browser.open(f"https://doe.sp.gov.br/sumario?editionDate={date_today}")

    time.sleep(3)
    WebDriverWait(browser.driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Executivo')]"))
    ).click()
    time.sleep(1)

    var_aux = False
    for i in range(len(section)):
        WebDriverWait(browser.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//button[contains(., '{section[i]}')]"))
        ).click()
        time.sleep(1)

        try:
            WebDriverWait(browser.driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='__next']/div[2]/div/div[4]/div/div[2]/div/div[1]/div/div/div"))
            ).click()
            time.sleep(1)

            WebDriverWait(browser.driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, "//li[contains(., 'Secretaria da Educação')]"))
            ).click()
            time.sleep(1)
        except Exception as e:
            pass
        
        try:
            element_list = WebDriverWait(browser.driver, 2).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//div[contains(@class, "MuiTreeItem-label") and contains(text(), "Diretoria de Ensino - Região de Assis")]/../..')
                )
            )
            if element_list:
                var_aux = True
                break
        except Exception as e:
            var_aux = False
            
    if var_aux == False:
        date_now = str(date_today).split("-")
        day = date_now[-1]
        year = date_now[0]
        month = date_now[1]
        str_date = day+"/"+month+"/"+year
        print(f"Não existem matérias para o dia {str_date}")
   
    if var_aux == True:         
        try:
            links = element_list.find_elements(By.TAG_NAME, "a")
            for link in links:
                link.click()
        except Exception as e:
            print("If element of Diretoria de Ensino de Assis not found, impossible for get links.")
            pass
        
        abas = browser.driver.window_handles
        for handle in abas[1:]:
            browser.driver.switch_to.window(handle)
            time.sleep(2)
            header = WebDriverWait(browser.driver, 2).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, 'css-1n1clc2')
                )
            ).text
            time.sleep(1)
            
            content = WebDriverWait(browser.driver, 2).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, 'css-1e09a5c')
                )
            ).text
            time.sleep(1)

            print(header)
            print(content)
            print("--------------------------------\n")