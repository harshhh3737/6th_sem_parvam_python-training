from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 15)

try:
    driver.get("https://scholar.parvam.in/student/login")

    # ✅ Auto fill email
    email = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='email' or @name='email' or @name='username']"))
    )
    email.clear()
    email.send_keys("harshalaharshala7@gmail.com")

    # ✅ Auto fill password
    password = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='password']"))
    )
    password.clear()
    password.send_keys("harshalamahesh@2707005")

    # ✅ Auto click login button
    login_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
    )
    login_btn.click()

    print("✅ Auto login completed")

except Exception as e:
    print("❌ Error:", e)