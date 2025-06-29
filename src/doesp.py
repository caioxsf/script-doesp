"""
Scraping in website doe-sp and save file to pdf and to send file to e-mail
"""

import time
import os
from zoneinfo import ZoneInfo
from datetime import datetime
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

from src.browser import Browser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

section = {
    "Atos Normativos": ["Secretaria da Educação"],
    "Atos de Pessoal": ["Secretaria da Educação", "Educação I"],
    "Atos de Gestão e Despesas": ["Secretaria da Educação"]
}

def remove_files(dir_folder):
    """
    **Remove files in folder**

    - dir_folder: example: /app/output
    """
    for nome_arquivo in os.listdir(dir_folder):
        full_dir = os.path.join(dir_folder, nome_arquivo)
        if os.path.isfile(full_dir):
            os.remove(full_dir)

def generate_pdf_reportlab(list_content, name_file):
    """
    **list_content:** list of tuplas (header, content)\n
    **name_file:** name of the file to save
    """
    doc = SimpleDocTemplate(name_file, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    for header, content in list_content:
        story.append(Paragraph(f"<b>{header}</b>", styles['Heading2']))
        story.append(Spacer(1, 12))
        story.append(Paragraph(content, styles['Normal']))
        story.append(Spacer(1, 24))

    doc.build(story)

load_dotenv()
def send_email(recipient, subject, body, dir_pdf):
    """
    **Send PDF to e-mail of recipient**
    
    - recipient: e-mail of recipient
    - subject: subject of message
    - body: body of message
    - dir_pdf: dir of pdf
    """
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = os.getenv("EMAIL")
    msg["To"] = recipient
    msg.set_content(body)

    if dir_pdf != "":
        with open(dir_pdf, "rb") as f:
            pdf_data = f.read()
            msg.add_attachment(pdf_data, maintype="application", subtype="pdf", filename=os.path.basename(dir_pdf))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(os.getenv("EMAIL"), os.getenv("PASSWORD"))
        smtp.send_message(msg)

    print("E-mail enviado com sucesso.")
    
    
def scraping_doesp():
    """
    **Scraping of website doe.sp for save important contents diary**
    """
    browser = Browser()

    data = os.getenv("DATA").split(",")
    print(data)
    list_content = []
    date_today = datetime.now(ZoneInfo("America/Sao_Paulo")).date()
    browser.open(f"https://doe.sp.gov.br/sumario?editionDate=2025-06-10")

    time.sleep(3)
    WebDriverWait(browser.driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Executivo')]"))
    ).click()
    time.sleep(1)

    for sec in section:
        try:
            WebDriverWait(browser.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"//button[contains(., '{sec}')]"))
            ).click()
            time.sleep(1)

            for secretaria in section.get(sec, []):
                try:
                    WebDriverWait(browser.driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, "//*[@id='__next']/div[2]/div/div[4]/div/div[2]/div/div[1]/div/div/div"))
                    ).click()
                    time.sleep(1)
                except:
                    continue

                try:
                    WebDriverWait(browser.driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, f"//li[contains(., '{secretaria}')]"))
                    ).click()
                    print(f"Tentando clicar em: {secretaria}")
                    time.sleep(1)
                except:
                    print(f"Não foi possível clicar em: {secretaria}")
                    continue

                try:
                    element_list = WebDriverWait(browser.driver, 2).until(
                        EC.presence_of_element_located(
                            (By.XPATH, '//div[contains(@class, "MuiTreeItem-label") and contains(text(), "Diretoria de Ensino - Região de Assis")]/../..')
                        )
                    )

                    links = element_list.find_elements(By.TAG_NAME, "a")
                    for link in links:
                        link.click()
                    time.sleep(1)

                    abas = browser.driver.window_handles
                    for handle in abas[1:]:
                        browser.driver.switch_to.window(handle)
                        time.sleep(2)

                        header = WebDriverWait(browser.driver, 2).until(
                            EC.presence_of_element_located(
                                (By.CLASS_NAME, 'css-1n1clc2')
                            )
                        ).text

                        content = WebDriverWait(browser.driver, 2).until(
                            EC.presence_of_element_located(
                                (By.CLASS_NAME, 'css-1e09a5c')
                            )
                        ).text

                        if any(dado in content for dado in data):
                            list_content.append((f"{sec} - {secretaria} - {header}", content))

                    for handle in abas[1:]:
                        browser.driver.switch_to.window(handle)
                        browser.driver.close()
                    browser.driver.switch_to.window(abas[0])
                except:
                    continue
        except:
            continue
            
    if list_content:
        output_dir = "/app/output/"
        name_file = os.path.join(output_dir, f"leitura-diario-{date_today}.pdf")
        remove_files(output_dir)
        generate_pdf_reportlab(list_content, name_file)
        pdf_path = f"/app/output/leitura-diario-{date_today}.pdf"
        send_email(
            os.getenv("DESTINATARIO"), 
            "PDF Leitura do Diário Oficial", 
            body="Segue em anexo o PDF gerado.", 
            dir_pdf=pdf_path)
    else:
        send_email(
            os.getenv("DESTINATARIO"), 
            "PDF Leitura do Diário Oficial", 
            body=f"Não existem matérias da Diretoria de Ensino da Região de Assis para a EE ANTÔNIO DE ALMEIDA PRADO no dia {date_today.strftime('%d/%m/%Y')}",
            dir_pdf=""
        )
        print(f"Não existem matérias da Diretoria de Ensino da Região de Assis para a EE ANTÔNIO DE ALMEIDA PRADO no dia {date_today.strftime('%d/%m/%Y')}")
