# 📰 DOE-SP Scraper and PDF Generator

This project is a web scraper designed to extract relevant information from the **Diário Oficial do Estado de São Paulo (DOE-SP)** website, generate a PDF report with the extracted content, and send the report via email. The tool automates the process of monitoring and archiving important content from the DOE-SP.

---

## ✨ Features

- 🔍 **Web Scraping**: Automatically navigates the DOE-SP website to extract specific content based on predefined sections and keywords.
- 🖨️ **PDF Generation**: Creates a well-structured PDF report using the extracted data.
- 📧 **Email Integration**: Sends the generated PDF to a specified recipient via email.
- ⚙️ **Error Handling**: Includes robust error handling for scraping, file generation, and email sending.
- 🔒 **Environment Configuration**: Uses environment variables for sensitive data like email credentials and scraping parameters.
- 🐳 **Docker Support**: Run the application in a containerized environment for easy deployment.


---

## 🚀 Technologies Used

- **Python** 🐍: Core programming language.
- **Selenium** 🌐: For web scraping and browser automation.
- **ReportLab** 🖨️: For generating PDF reports.
- **smtplib** ✉️: For sending emails via SMTP.
- **dotenv** 🔒: For managing environment variables.
- **ZoneInfo** 🌍: For timezone management.
- **Docker** 🐳: For containerized deployment.

---

## 🔑 Environment Variables

The following environment variables need to be configured in a `.env` file:

| **Variable**   | **Description**                     | **Example**                |
|----------------|-------------------------------------|----------------------------|
| `EMAIL`        | Sender's email address             | `your-email@gmail.com`     |
| `PASSWORD`     | Sender's email password            | `your-email-password`      |
| `DESTINATARIO` | Recipient's email address          | `recipient-email@gmail.com`|
| `DATA`         | Keywords to filter content         | `keyword1,keyword2,keyword3`|


---

## 📦 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/doe-sp-scraper.git
   cd doe-sp-scraper
2. Build the container:
   ```bash
   docker compose build
3. Run the containr?
    ```bash
   docker compose run
---

## 📜 License
This project is licensed under the MIT License. See the LICENSE file for details.