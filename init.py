from playwright.sync_api import sync_playwright
import requests
import base64
import time

# Function to solve ReCAPTCHA using 2Captcha
def solve_recaptcha(api_key, site_key, page_url):
    # Send a request to 2Captcha to solve the ReCAPTCHA
    response = requests.post(
        "http://2captcha.com/in.php",
        data={
            "key": api_key,
            "method": "userrecaptcha",
            "googlekey": site_key,
            "pageurl": page_url
        }
    )

    if response.status_code != 200 or response.text[0:2] != "OK":
        print("Failed to send CAPTCHA request to 2Captcha")
        return None

    captcha_id = response.text.split('|')[1]

    # Check the result of the CAPTCHA solving
    recaptcha_response = None
    while recaptcha_response is None:
        response = requests.get(
            f"http://2captcha.com/res.php?key={api_key}&action=get&id={captcha_id}"
        )
        if response.text[0:2] == "OK":
            recaptcha_response = response.text.split('|')[1]
        elif response.text != "CAPCHA_NOT_READY":
            print("Failed to solve CAPTCHA")
            return None
        time.sleep(3)  # Wait a few seconds before checking again

    return recaptcha_response

# Function to solve CAPTCHA using TrueCaptcha
def solve_captcha(image_path):
    # Read and encode the image
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('ascii')
    
    # TrueCaptcha API endpoint and credentials
    url = 'https://api.apitruecaptcha.org/one/gettext'
    data = { 
        'userid': 'chzeeshan1322@gmail.com', 
        'apikey': 'TSHAnblkz2ZfilBybGKA',  
        'data': encoded_string
    }
    
    # Make the request to the API
    try:
        response = requests.post(url=url, json=data)
        response.raise_for_status()  # Raise an error for HTTP issues
        result = response.json()
        return result['result']
    except requests.RequestException as e:
        print(f"HTTP error occurred: {e}")
        return None

# Main function
def main():
    start_time = time.time()
    api_key = "b1a721cd802ed5ae1e855cfb37907c52"  # 2Captcha API key
    site_key = "6LcQb8klAAAAAHDDKtB3PaB6gvbh-ej4qa8BRKV9"  # Site key for the ReCAPTCHA
    page_url = "https://blsitalypakistan.com/bls_appmnt/bls-italy-appointment/Nk9NeWlxMjA5NjczODY0MjA/ODhtYU5pazgwMzM2NDk4MjUx/MWVNdXJTOTg0MDUyMDY1MTg"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Navigate to the login page
        page.goto('https://blsitalypakistan.com/account/login')

        # Get the CAPTCHA image URL
        captcha_image_element = page.query_selector('#Imageid')
        captcha_image_url = captcha_image_element.get_attribute('src')

        # Download the CAPTCHA image
        captcha_image_response = requests.get(captcha_image_url)
        captcha_image_path = 'captcha.jpg'
        with open(captcha_image_path, 'wb') as f:
            f.write(captcha_image_response.content)

        try:
            captcha_solution = solve_captcha(captcha_image_path)
            print(captcha_solution)
            # Check if captcha_solution is not None
            if captcha_solution is not None:
                # Ensure the input fields are visible before interacting
                page.wait_for_selector('input[placeholder="Enter Email"]', timeout=60000)
                page.wait_for_selector('input[placeholder="Enter Password"]', timeout=60000)
                page.wait_for_selector('input[placeholder="Enter Captcha"]', timeout=60000)

                # Fill in the form
                page.fill('input[placeholder="Enter Email"]', 'chzeeshan1322@gmail.com')
                page.evaluate('''() => {
                    document.querySelector('input[placeholder="Enter Email"]').value = "chzeeshan1322@gmail.com";
                }''')

                page.fill('input[placeholder="Enter Password"]', 'gjgne2$s@!3$b2R')
                page.evaluate('''() => {
                    document.querySelector('input[placeholder="Enter Password"]').value = "gjgne2$s@!3$b2R";
                }''')

                page.fill('input[placeholder="Enter Captcha"]', captcha_solution)
                page.evaluate(f'''() => {{
                    document.querySelector('input[placeholder="Enter Captcha"]').value = "{captcha_solution}";
                }}''')

                # Submit the form
                page.click('button[name="submitLogin"]')

                print('Login successful')

                # Move to the next URL
                page.goto('https://blsitalypakistan.com/bls_appmnt/bls-italy-appointment/NmFqbklsMzM4Nzc1OTYwMjQ')
                page.goto('https://blsitalypakistan.com/bls_appmnt/bls-italy-appointment/Nmxwa1pzNTc4MDIxNjYwNTg/ODhqcXlodzY2MzQ3OTM4MjIx')  
                page.goto('https://blsitalypakistan.com/bls_appmnt/bls-italy-appointment/Nk9NeWlxMjA5NjczODY0MjA/ODhtYU5pazgwMzM2NDk4MjUx/MWVNdXJTOTg0MDUyMDY1MTg')

                # Get the CAPTCHA image URL
                captcha_image_element = page.query_selector('#Imageid')
                captcha_image_url = captcha_image_element.get_attribute('src')

                # Download the CAPTCHA image
                captcha_image_response = requests.get(captcha_image_url)
                captcha_image_path = 'captcha.jpg'
                with open(captcha_image_path, 'wb') as f:
                    f.write(captcha_image_response.content)
                captcha_solution = solve_captcha(captcha_image_path)
                print(captcha_solution)
                page.fill('input[placeholder="Captcha"]', captcha_solution)
                page.evaluate(f'''
                        document.querySelector('input[name="captcha_code"]').value = "{captcha_solution}";
                    ''')

                # Click on the date picker
                page.click('#valAppointmentDate')
                
                # Wait for the date picker to open and be visible
                page.wait_for_selector('.datepicker-days', timeout=60000)
                
                # Find the first available date with the .label-available class
                available_date = page.query_selector('.datepicker-days tbody td.label-available')
                if available_date:
                    available_date.click()
                    print('Date selected')

                    # Select 'Normal' from the appointment type dropdown
                    page.select_option('select#valAppointmentType', 'normal')

                    # Fill in first name and last name
                    page.fill('input[name="valApplicant[1][first_name]"]', 'zeeshan')
                    page.fill('input[name="valApplicant[1][last_name]"]', 'saleem')

                    recaptcha_response = solve_recaptcha(api_key, site_key, page_url)
                    print(recaptcha_response)

                    # Fill in the ReCAPTCHA response
                    page.evaluate(f'''
                        document.getElementById('g-recaptcha-response').value = "{recaptcha_response}";
                    ''')
                        # document.getElementById('g-recaptcha-response').dispatchEvent(new Event('input', {{ bubbles: true }}));
                        # document.getElementById('g-recaptcha-response').dispatchEvent(new Event('change', {{ bubbles: true }}));

                    # # Wait until the reCAPTCHA response is correctly filled
                    # page.wait_for_function('document.getElementById("g-recaptcha-response").value.length > 0')

                    # Ensure that the checkbox is ticked before clicking the Book Now button
                    page.check('input[name="agree"]')

                    # Click on the book button
                    page.click('button#valBookNow')

                    # Wait for the booking confirmation
                        
                    print('Booking successful')
                    # Click on the book button
                    page.click('button[name="book"]')

                    # Wait for the booking confirmation
                    page.wait_for_selector('.booking-confirmation', timeout=60000)
                    print('Booking successful')
                else:
                    print('No available dates found')

            else:
                print('Failed to solve CAPTCHA')

        except Exception as e:
            print('Error solving CAPTCHA:', e)

        browser.close()
        end_time = time.time()  # End timing the entire script
        total_duration = end_time - start_time
        print(f"Total script execution time: {total_duration:.2f} seconds")

if __name__ == "__main__":
    main()
