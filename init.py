from playwright.sync_api import sync_playwright
import requests
import base64
import time

# Function to solve ReCAPTCHA using 2Captcha
def solve_recaptcha(api_key, site_key, page_url):
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
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('ascii')
    
    url = 'https://api.apitruecaptcha.org/one/gettext'
    data = { 
        'userid': 'chzeeshan1322@gmail.com', 
        'apikey': 'TSHAnblkz2ZfilBybGKA',  
        'data': encoded_string
    }
    
    try:
        response = requests.post(url=url, json=data)
        response.raise_for_status()
        result = response.json()
        return result['result']
    except requests.RequestException as e:
        print(f"HTTP error occurred: {e}")
        return None

# Main function
def main():
    start_time = time.time()
    api_key = "5914a93f7203b094b671e13d20c4f1c0"
    site_key = "6LcQb8klAAAAAHDDKtB3PaB6gvbh-ej4qa8BRKV9"
    page_url = "https://blsitalypakistan.com/bls_appmnt/bls-italy-appointment/NmJPQ1JUODIyNTA2NTA0MTY/ODh6WWRjUzQ2MzEzOTU4MjYw/MU9NbXRuNTEzNzQ5OTgzMjA"

    user_and_payment_details = {
        'email': 'example@gmail.com',
        'password': 'enterpassword',
        'first_name': 'First Name',
        'last_name': 'Last Name',
        'card_number': '4111111111111111',
        'expiry_month': 'January',
        'expiry_year': '2024',
        'cvv': '123',
        "service_type":'family_reunion',

    }
    appointments = ['Islamabad','Lahore','Multan','fasialabad']
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

                page.fill('input[placeholder="Enter Email"]', user_and_payment_details['email'])
                page.evaluate(f'''() => {{
                                document.querySelector('input[placeholder="Enter Email"]').value = "{user_and_payment_details['email']}";
                            }}''')
                page.fill('input[placeholder="Enter Password"]', user_and_payment_details['password'])
                page.evaluate(f'''() => {{
                                document.querySelector('input[placeholder="Enter Password"]').value = "{user_and_payment_details['password']}";
                            }}''')
                page.fill('input[placeholder="Enter Captcha"]', captcha_solution)
                page.evaluate(f'''() => {{
                                document.querySelector('input[placeholder="Enter Captcha"]').value = "{captcha_solution}";
                            }}''')
                page.click('button[name="submitLogin"]')
                print('Login successful')
                available_date = None

                for appointment in appointments:
                    if available_date is not None:
                        break
                # Move to the next URL
                    if(appointment == "quetta"):
                        
                        page.goto('https://blsitalypakistan.com/bls_appmnt/bls-italy-appointment/NmFqbklsMzM4Nzc1OTYwMjQ')
                        if(user_and_payment_details['service_type']=="family_reunion"):
                            page.goto('https://blsitalypakistan.com/bls_appmnt/bls-italy-appointment/NU1FeWVmNzM2MjQ4MDU0OTM/ODVxRXluazY0Njk1ODczODkw')
                            current_url = page.url
                            print("Current URL:", current_url)
                            page.goto('https://blsitalypakistan.com/bls_appmnt/bls-italy-appointment/NmJPQ1JUODIyNTA2NTA0MTY/ODh6WWRjUzQ2MzEzOTU4MjYw/MU9NbXRuNTEzNzQ5OTgzMjA')
                        elif (user_and_payment_details['service_type']=="national_work"):
                            page.goto('https://blsitalypakistan.com/bls_appmnt/bls-italy-appointment/NVlsUEpnNzY0OTMwMTIxOTY/ODZxdERJTDQzOTg4NjkwNTQ3')   
                            page.goto('https://blsitalypakistan.com/bls_appmnt/bls-italy-appointment/NkdkVEVKNTE5MjQ4NjcwNjE/OTBuSG9MSjYzNTI3MDExODU0/MWJ5QmFsMTE4NzI2Njk0NDA')
                    elif(appointment == "Islamabad"):
                        
                        page.goto('https://blsitalypakistan.com/bls_appmnt/bls-italy-appointment/MWVrYWREMjQ1OTkwMzI3NDg')
                        if(user_and_payment_details['service_type']=="family_reunion"):
                            page.goto('https://blsitalypakistan.com/bls_appmnt/bls-italy-appointment/MUdpSXNmNTgwNjI2MDc0ODk/NjdVYVhZZDYyNzI1NjkxODUx')
                            page.goto('https://blsitalypakistan.com/bls_appmnt/bls-italy-appointment/MUdaZVVjMjM3NDA4NjcxMDk/NjdMRldldzg3MjE5NjIzMTU3/MVRIeGhRMjcyNzg5MTM4NTE')
                        elif (user_and_payment_details['service_type']=="national_work"):
                            page.goto('https://blsitalypakistan.com/bls_appmnt/bls-italy-appointment/MWdMWG1NMTUwNzYyOTQ4ODc/NjhtZ1l3Wjk4MTQ0MTUzNzY3')   
                            page.goto('https://blsitalypakistan.com/bls_appmnt/bls-italy-appointment/MUdoZnBhMTgzMDA5MjYyNzM/NjhZT1ZrWDYyNDMxMTk5MjU4/MWVZVWpJNjg3MjQwMTYxNTU') 
                    elif(appointment=="Lahore"):
                        
                        page.goto('https://blsitalypakistan.com/bls_appmnt/bls-italy-appointment/Mmpjd3FyMzg2MTA0OTU0MDg')
                        if(user_and_payment_details['service_type']=="family_reunion"):
                            page.goto('https://blsitalypakistan.com/bls_appmnt/bls-italy-appointment/MlRpdWR6NDU1ODcyMDExOTM/ODJuT2dVejEzMDg4MDI3OTY0')
                            #for type of applicants indviuals
                            page.goto('https://blsitalypakistan.com/bls_appmnt/bls-italy-appointment/MnplR2NOMzEwOTE3OTM3MjU/ODJmbWdVTzIxMjAwMzgxNDY5/MURjaFdPMzE0OTYwNTM3NDA') 
                        elif (user_and_payment_details['service_type']=="national_work"):
                            page.goto('https://blsitalypakistan.com/bls_appmnt/bls-italy-appointment/MnhvYlVlMzc3NTU4NjQwMzI/NzhLSXpOcTM0ODU5Mjk0NzA2')  
                            #for type of applicants indviuals
                            page.goto('https://blsitalypakistan.com/bls_appmnt/bls-italy-appointment/Mkh5VFFJMDg0MjM3OTU2MjY/NzhMUGZZdTE0ODU5MzI2ODUx/MXVlcHpPNzA0MjU2MzYwNzM')  
                    elif(appointment=="Multan"):
                        #for appointment center
                        page.goto('https://blsitalypakistan.com/bls_appmnt/bls-italy-appointment/NUxyYlRjODk1NDEyNzYwNDE') 
                        if(user_and_payment_details['service_type']=="family_reunion"):
                            #for service type
                            page.goto('https://blsitalypakistan.com/bls_appmnt/bls-italy-appointment/NU1FeWVmNzM2MjQ4MDU0OTM/ODVxRXluazY0Njk1ODczODkw')
                            #for type of applicants
                            page.goto('https://blsitalypakistan.com/bls_appmnt/bls-italy-appointment/NXVpdHllNzE4NjU1OTI2NDI/ODVQSGRqYTQwOTc1NDI2MjE4/MVBBUUlGMDM2MzU4OTc4NDE')
                        elif (user_and_payment_details['service_type']=="national_work"):
                            page.goto('https://blsitalypakistan.com/bls_appmnt/bls-italy-appointment/NVlsUEpnNzY0OTMwMTIxOTY/ODZxdERJTDQzOTg4NjkwNTQ3')   
                            page.goto('https://blsitalypakistan.com/bls_appmnt/bls-italy-appointment/NVpIU3Z3ODkxNjgwNzk1NTI/ODZpVlFFQjA0MDQyMTMyOTc4/MVZabXVUMzUwODMwMjY4NzE')
                    elif(appointment=="fasialabad"):
                        
                        page.goto('https://blsitalypakistan.com/bls_appmnt/bls-italy-appointment/NG9LT3FpNjIzNjgwNTE5NDc')
                        if(user_and_payment_details['service_type']=="family_reunion"):
                            #for service type family_reunion
                            page.goto('https://blsitalypakistan.com/bls_appmnt/bls-italy-appointment/NFBSSlFJOTYwMzU2MzQyNDE/ODNBdGlNVTU0MDk3Mzg5NTcw')
                            #for type of applicants indviuals
                            page.goto('https://blsitalypakistan.com/bls_appmnt/bls-italy-appointment/NEViakZvMTAyNDc2OTM1NDg/ODNqcWVCZjcxNTU4MzcwODEz/MVdqd3psMzYxMjA3NzUyOTg')
                        elif (user_and_payment_details['service_type']=="national_work"):
                            #for service type national work
                            page.goto('https://blsitalypakistan.com/bls_appmnt/bls-italy-appointment/NERmT2R6MTM1NDk3MTY4MDk/ODRCRVRocTIwNTE2NzQ5MTI5')   
                            #for type of applicants indviuals
                            page.goto('https://blsitalypakistan.com/bls_appmnt/bls-italy-appointment/NFVmcFhlNTc5NDE4NjczOTM/ODRlbXFIdzgyMDE0ODc3NTI5/MWRUZkhXMDE5NTM5NDE0Mzc')   

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
                    print("available_date",available_date)
                if available_date:
                    available_date.click()
                    print('Date selected')

                    page.select_option('select#valAppointmentType', 'normal')
                    page.fill('input[name="valApplicant[1][first_name]"]', user_and_payment_details['first_name'])
                    page.fill('input[name="valApplicant[1][last_name]"]', user_and_payment_details['last_name'])

                    recaptcha_response = solve_recaptcha(api_key, site_key, page_url)
                    print(recaptcha_response)

                    # Fill in the ReCAPTCHA response
                    page.evaluate(f'''
                        document.getElementById('g-recaptcha-response').value = "{recaptcha_response}";
                    ''')

                    page.check('input[name="agree"]')
                    page.click('button#valBookNow')

                    print('Booking successful')
                    current_url = page.url
                    print("after booking URL:", current_url)
                    # Fill in the card number
                    # Ensure the fields are available and interactable before filling them
                    page.wait_for_selector('input[id="cardNumber"]', state='visible')
                    page.wait_for_selector('select[ng-model="month"]', state='visible')
                    page.wait_for_selector('select[ng-model="selectedYear"]', state='visible')
                    page.wait_for_selector('input[id="ValidationCode"]', state='visible')
                    current_url = page.url
                    print("after slector:", current_url)
                    # Debugging: Check if the fields are correctly identified
                    print(page.evaluate('document.querySelector("input[id=\'cardNumber\']") !== null'))
                    print(page.evaluate('document.querySelector("select[ng-model=\'month\']") !== null'))
                    print(page.evaluate('document.querySelector("select[ng-model=\'selectedYear\']") !== null'))
                    print(page.evaluate('document.querySelector("input[id=\'ValidationCode\']") !== null'))

                    # Fill in the card number
                    page.fill('input[id="cardNumber"]', user_and_payment_details['card_number'])
                    page.evaluate(f'''() => {{
                        document.querySelector('input[id="cardNumber"]').value = "{user_and_payment_details['card_number']}";
                    }}''')

                    # Debugging: Check if the card number is filled
                    print(page.evaluate('document.querySelector("input[id=\'cardNumber\']").value'))

                    # Select the expiry month
                    page.select_option('select[ng-model="month"]', str(user_and_payment_details['expiry_month']))

                    # Debugging: Check if the expiry month is selected
                    print(page.evaluate('document.querySelector("select[ng-model=\'month\']").value'))

                    # Select the expiry year
                    page.select_option('select[ng-model="selectedYear"]', str(user_and_payment_details['expiry_year']))

                    # Debugging: Check if the expiry year is selected
                    print(page.evaluate('document.querySelector("select[ng-model=\'selectedYear\']").value'))

                    # Fill in the CVV
                    page.fill('input[id="ValidationCode"]', user_and_payment_details['cvv'])
                    page.evaluate(f'''() => {{
                        document.querySelector('input[id="ValidationCode"]').value = "{user_and_payment_details['cvv']}";
                    }}''')

                    # Debugging: Check if the CVV is filled
                    print(page.evaluate('document.querySelector("input[id=\'ValidationCode\']").value'))

                    # Click on the pay button
                    page.click('input#btnPay')

                    print('Booking successful')


                    # Click on the pay button
                    page.click('input#btnPay')

                    print('Booking successful')

                    print('Payment successful')
                    time.sleep(3)
                    page.goto('https://blsitalypakistan.com/account/logout')
                else:
                    print('No available dates found')

            else:
                print('Failed to solve CAPTCHA')

        except Exception as e:
            print('Error solving CAPTCHA:', e)

        browser.close()
        end_time = time.time()
        total_duration = end_time - start_time
        print(f"Total script execution time: {total_duration:.2f} seconds")
 
if __name__ == "__main__":
    while True:
     main()
