from django.shortcuts import render
from django.http import JsonResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def login_view(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')

        # Selenium logic to verify credentials
        success = authenticate_with_selenium(user_id, password)

        if success:
            return JsonResponse({'status': 'success', 'message': 'Authentication Successful!'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Authentication Failed!'})

    return render(request, 'auth_app/login.html')


def authenticate_with_selenium(user_id, password):
    # Configure Selenium
    options = Options()
    options.add_argument('--headless')  # Run in headless mode for production
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    try:
        # Replace with the target website URL
        target_url = 'https://example.com/login'
        driver.get(target_url)

        # Locate input fields and enter credentials (adjust locators as needed)
        driver.find_element(By.ID, 'username').send_keys(user_id)
        driver.find_element(By.ID, 'password').send_keys(password, Keys.RETURN)

        time.sleep(2)  # Wait for the page to load

        # Check for a successful login (adjust logic based on the site)
        if "Welcome" in driver.page_source:
            return True
        return False
    except Exception as e:
        print(f"Error during Selenium authentication: {e}")
        return False
    finally:
        driver.quit()
