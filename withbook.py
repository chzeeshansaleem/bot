from playwright.sync_api import sync_playwright
import requests
import base64

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
                # page.goto('https://blsitalypakistan.com/bls_appmnt/bls-italy-appointment')
                # page.goto('https://blsitalypakistan.com/bls_appmnt/bls-italy-appointment/MXlPR0VGNDEwMjEyNjM3NTc')
                # page.goto('https://blsitalypakistan.com/bls_appmnt/bls-italy-appointment/NHFtcG9zMDEwNjU5OTQyMjM/ODRnSndXUzI2MDgxMzkwODM0')  
                page.goto('https://blsitalypakistan.com/bls_appmnt/bls-italy-appointment/NER5VGp1MDYwNDUyOTc1OTI/ODR6REFyUTI4NzQ2NTc1Mjkz/MVZobE9jMzA0MzY5MTg0Nzc')

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
                disabled_dates = page.query_selector_all('.datepicker-days tbody td.label-slotfull')
                for date in disabled_dates:
                    day = date.inner_text()
                    print(f'Disabled date: {day}')
                
                # Find the first available date
                available_date = page.query_selector('.datepicker-days tbody td:not(.label-slotfull):not(.old):not(.new):not(.label-slotfull)')
                if available_date:
                    available_date.click()
                    print('Date selected')

                    # Click on the book button (replace with the actual button selector)
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

if __name__ == "__main__":
    main()


#.label-available  class for green color


