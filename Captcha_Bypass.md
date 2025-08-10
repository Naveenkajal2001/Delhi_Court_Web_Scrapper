==========================================Captcha Bypass Strategy=================================================

1. Understanding the Challenge
  - The Delhi Court case status website implements a basic text-based captcha to prevent automated scraping. Normally, this would require OCR or manual input to solve.

2. Observation
  - On inspecting the page’s HTML structure, it was discovered that the captcha text is not embedded in an image but is actually rendered as plain text inside a DOM element.
    This means the captcha is accessible directly via Selenium by targeting the element containing it.

3. Solution Approach
  - Instead of attempting OCR, the captcha text is extracted from the HTML element and directly used in the form submission.

Steps:

1. Locate the captcha DOM element by its unique XPath or CSS selector.

2. Extract the text content using Selenium’s .text property.

3. Automatically insert the extracted captcha text into the captcha input field.

4. Submit the form as usual.

Example Code :- 

	# Locate captcha element and extract text
          captcha_element = driver.find_element(By.ID, "captcha_text")
          captcha_value = captcha_element.text.strip()

	# Fill in captcha field
	  captcha_input = driver.find_element(By.ID, "captcha_input")
	  captcha_input.send_keys(captcha_value)

	# Submit form
	  submit_button = driver.find_element(By.ID, "submit_button")
	  submit_button.click()

4. Security Implications
  - This works only because the captcha is displayed as plain text in the DOM.
  - If the site later changes to an image-based captcha, this method will no longer work, and OCR or third-party captcha-solving services may be required.

5. Advantages
 - No need for image processing or AI.

 - Fast and reliable while the current site design is used.

 - Eliminates human intervention for captcha entry.