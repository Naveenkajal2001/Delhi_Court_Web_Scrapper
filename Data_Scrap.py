
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import os
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

class scr:
    def __init__(self):
        self.l = []
        options = Options()
        options.add_argument("--headless")  # Run without opening browser window
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--log-level=3")
        # options.add_argument("--headless")
        s = Service(r"ChromeDriver.exe")
        self.driver = webdriver.Chrome(service=s, options=options)
        self.driver.get("https://delhihighcourt.nic.in/app/get-case-type-status")

    def options(self):
        self.Case_type = self.driver.find_element(by=By.XPATH, value='//*[@id="case_type"]')
        #Wait Until the Options are loaded
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="case_type"]'))
        )
        # List of dropdown Elements
        Dropdown_list=self.Case_type.find_elements(By.TAG_NAME,'option')
        l=[o.text for o in Dropdown_list]
        self.l=l
        return l



    def CaseYear(self):
        self.Case_year = self.driver.find_element(By.XPATH, '//*[@id="case_year"]')
        # Wait Until the Options are loaded
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="case_year"]'))
        )
        # List of dropdown Elements
        Dropdown_list = self.Case_year.find_elements(By.TAG_NAME, 'option')
        Case_year_List = [o.text for o in Dropdown_list]


        return Case_year_List

    def caseInput(self,CaseType,CaseNo,CaseYear):
        value=self.driver.find_element(By.XPATH,'//*[@id="case_number"]')

        Select(self.Case_type).select_by_visible_text(CaseType)
        value.send_keys(CaseNo)
        Select(self.Case_year).select_by_visible_text(CaseYear)

        # Captcha
        text=self.driver.find_element(By.XPATH,'//*[@id="captcha-code"]').text
        # print(text)
        self.driver.find_element(By.XPATH, '//*[@id="captchaInput"]').send_keys(text)

        # Clicking Event Submit the form
        self.driver.execute_script("document.getElementById('search').click();")
        print("Search button clicked")


        # # Wait for the loader to appear first (optional safety check)
        # WebDriverWait(self.driver, 10).until(
        #     EC.presence_of_element_located((By.ID, "caseTable_processing"))
        # )

        # # Wait until the loader is hidden (style: display:none)
        # WebDriverWait(self.driver, 20).until(
        #     lambda d: d.find_element(By.ID, "caseTable_processing").value_of_css_property("display") == "none"
        # )
        #
        # # Now the table should be fully loaded, wait for at least one row (excluding header)
        # WebDriverWait(self.driver, 10).until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, "#caseTable tbody tr"))
        # )
        try:
            alert_title = self.driver.find_element(By.ID, "swal2-title").text
            if alert_title.strip().lower() == "alert":
                print("Invalid CAPTCHA or input. Reloading...")
                self.driver.refresh()
                return None  # Optional: signal retry
        except:
            pass


        # Get and return result HTML
        time.sleep(2)
        self.result_html = self.driver.find_element(By.XPATH,'//*[@id="caseTable"]').get_attribute("outerHTML")
        # print(result_html)
        try:
            empty_cell = self.driver.find_element(By.ID, "dt-empty")
            if "no data available in table " in empty_cell.text.lower():
                # print("No result found — wrong input.")
                self.driver.find_element(By.XPATH, '//*[@id="case_number"]').clear()
                self.driver.find_element(By.XPATH, '//*[@id="captchaInput"]').clear()
                return "<p style='color:red;'>No result found. Please check your input.</p>"
        except:
            pass  # No empty-cell found, data likely exists

        # Clear Contents from the input
        self.driver.find_element(By.XPATH, '//*[@id="case_number"]').clear()
        self.driver.find_element(By.XPATH, '//*[@id="captchaInput"]').clear()

        # print(result_html)
        # soup = BeautifulSoup(result_html, 'html.parser')
        #
        # # for tag in soup.find_all("a", href=True):
        # #     print(tag)  # Should look normal
        # #     print(tag['href'])
        # result = []
        # rows = soup.find_all("tr")
        # # print(rows)
        #
        # for i, row in enumerate(rows):
        #     row_data = []
        #     order_details = []  # For storing date+PDF from second page
        #
        #     for cell in row.find_all(["th","td"]):
        #         # time.sleep(2)
        #         # print(row)
        #         # print(cell)
        #         link = cell.find_all("a", href=True)
        #         # print(link)
        #         for li in link:
        #             if i!=0:  # Only for data rows
        #                 link_href = li.get("href")
        #                 if link_href:
        #                     self.driver.get(link_href)
        #                     # link_text = li.get_text(strip=True)
        #                 # link_href = li.get("href")
        #                 # print(link_href)
        #                 # for tag in soup.find_all("a", href=True):
        #                 #     print(tag)  # Should look normal
        #                 #     print(tag['href'])
        #
        #                 # Go to linked page
        #                 time.sleep(3)
        #                 WebDriverWait(self.driver, 10).until(
        #                     EC.presence_of_element_located((By.ID, "caseTable")))
        #                 second_html = self.driver.find_element(By.ID, "caseTable").get_attribute(
        #                     "outerHTML")
        #                 soup2 = BeautifulSoup(second_html, "html.parser")
        #
        #                 second_rows = soup2.find_all("tr")
        #                 # print(second_rows)
        #                 # for sec_row in second_rows:
        #                 #     cols2 = sec_row.find_all("td")
        #                 #     if cols2:
        #                 #         order_details.append(cols2[0].get_text(strip=True))
        #                     # if isinstance(link_href, str):
        #                     #     self.driver.get(link_href)
        #                     #     time.sleep(2)
        #                     #     print("Yes")
        #                     # else:
        #                     #     print("Invalid link, skipping:", link_href)
        #                     #     continue
        #
        #                 try:
        #                     # table = self.driver.find_element(By.ID, "caseTable")
        #                     # order_html = table.get_attribute("outerHTML")
        #                     # order_soup = BeautifulSoup(order_html, "html.parser")
        #
        #                     # Extract Rows
        #
        #                     for sec_row in second_rows[1:]:  # Skip header row
        #                         cols2 = sec_row.find_all("td")
        #                         if cols2:
        #                             date_text = cols2[2].text.strip()
        #                             pdf_link = cols2[1].find("a")
        #                             # print(pdf_link)
        #                             if pdf_link and pdf_link.has_attr("href"):
        #                                 href = pdf_link.get('href')
        #                                 order_details.append({'date': date_text, 'href': href})
        #
        #                         row_data.append({'text': li.get_text(strip=True), 'href': link_href})  # Case title
        #                     row_data.append(order_details)
        #                 except Exception as e:
        #                     print("Error extracting order details:", e)
        #
        #                 # row_data.append({'text': link_text, 'href': link_href})
        #             else:
        #                 row_data.append(cell.get_text(strip=True))
        #
        #         if i != 0:
        #             row_data.append(order_details)  # Append orders column only to data rows
        #
        #         result.append(row_data)
        # print(self.result_html)
        return self.result_html




    def casestatus(self):
        soup = BeautifulSoup(self.result_html, 'html.parser')
        # print(soup)
        result = []
        base_url = "https://delhihighcourt.nic.in"  # Replace if different

        rows = soup.find_all("tr")

        for i, row in enumerate(rows):
            row_data = []
            order_details = []

            cells = row.find_all(["th", "td"])
            # print(cells)
            next_page_url = None  # To store the actual link

            for cell in cells:
                link_tag = cell.find("a", href=True)
                # print(link_tag)
                if link_tag:
                    href = link_tag.get('href')
                    # Fix relative URLs if needed
                    if href.startswith("/"):
                        href = base_url + href
                    next_page_url = href  # Store it for visiting

                    # Also store the visible text
                    row_data.append({'text': link_tag.get_text(strip=True), 'href': href})
                else:
                    # Just store plain cell text
                    row_data.append(cell.get_text(strip=True))

            # Now go to the second page if link was found
            if next_page_url and i != 0:
                try:
                    self.driver.get(next_page_url)
                    time.sleep(2)
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.ID, "caseTable"))
                    )

                    second_html = self.driver.find_element(By.ID, "caseTable").get_attribute("outerHTML")
                    soup2 = BeautifulSoup(second_html, 'html.parser')
                    second_rows = soup2.find_all("tr")[1:]  # skip header row

                    for sec_row in second_rows:
                        cols2 = sec_row.find_all("td")
                        if len(cols2) >= 3:
                            date = cols2[2].get_text(strip=True)
                            pdf_tag = cols2[1].find("a", href=True)
                            if pdf_tag:
                                pdf_link = pdf_tag['href']
                                # print(pdf_link)
                                order_details.append({'date': date, 'pdf': pdf_link})

                except Exception as e:
                    print("Error fetching second page:", e)

            if i != 0:
                row_data.append(order_details)
                result.append(row_data)
        # print(result)

        return result

    def back(self):
        self.driver.back()

    # print(result)



# a=scr()
# a.options()
# a.CaseYear()
# a.caseInput('ARB.A.','12','2016')
# a.casestatus()
