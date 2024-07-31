# import requests
# import base64

# def solve_captcha(image_path):
#     # Open and encode the image
#     with open(image_path, "rb") as image_file:
#         encoded_string = base64.b64encode(image_file.read()).decode('ascii')
    
#     # API endpoint and credentials
#     url = 'https://api.apitruecaptcha.org/one/gettext'
#     data = { 
#         'userid': 'chzeeshan1322@gmail.com', 
#         'apikey': 'TSHAnblkz2ZfilBybGKA',  
#         'data': encoded_string
#     }
    
#     # Make the request to the API
#     try:
#         response = requests.post(url=url, json=data)
#         response.raise_for_status()  # Raise an error for HTTP issues
#         result = response.json()
        
#         # Check if the response contains the captcha solution
#         if 'result' in result:
#             return result['result']
#         else:
#             print("Error: Captcha result not found in response.")
#             return None
#     except requests.RequestException as e:
#         print(f"HTTP error occurred: {e}")
#         return None
#     except ValueError as e:
#         print(f"Error parsing response JSON: {e}")
#         return None

# # Example usage
# captcha_solution = solve_captcha('cap3.jpg')
# print(f"Captcha solution: {captcha_solution}")
