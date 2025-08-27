import random
import time
import sys
import os
import subprocess
import pyautogui
import shutil   
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Ρυθμίσεις Edge
options = webdriver.EdgeOptions()
options.add_argument("--start-maximized")

prefs = {
    "download.default_directory": r"C:\\Users\\gchatzakis\\Downloads",
    "download.prompt_for_download": False
}
options.add_experimental_option("prefs", prefs)

# URLs
urls = {
    1: "https://www.cnn.com",
    2: "https://mail.google.com",
    3: "https://www.youtube.com",
    4: "https://github.com",
    5: "https://www.w3schools.com/images/myw3schoolsimage.jpg"
}

driver = None

def accept_cookies(driver):
    try:
        buttons = driver.find_elements(By.TAG_NAME, "button")
        for btn in buttons:
            text = btn.text.lower()
            if "accept" in text or "agree" in text:
                btn.click()
                print("Accepted cookies")
                time.sleep(1)
                break
    except:
        pass

def scroll_page(driver, times):
    for _ in range(times):
        driver.execute_script("window.scrollBy(0, window.innerHeight/2);")
        time.sleep(random.uniform(1, 2))

def open_downloaded_file(file_path):
    if os.path.exists(file_path):
        print(f"Opening file: {file_path}")
        proc = subprocess.Popen(['start', '', file_path], shell=True)
        time.sleep(5)
        proc.terminate()
    else:
        print("File not found to open.")

def notepad_simulation():
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    file_path = os.path.join(base_path, "demo.txt")
    copy_path = os.path.join(base_path, "demo_copy.txt")

    # Άνοιγμα Notepad
    subprocess.Popen(["notepad.exe"])
    time.sleep(2)

    # Γράψιμο κειμένου
    pyautogui.typewrite("Hello, this is the first sentence.\n", interval=0.05)
    pyautogui.typewrite("Hello, this is the second sentence.", interval=0.05)
    time.sleep(1)

    # Save με Ctrl+S
    pyautogui.hotkey("ctrl", "s")
    time.sleep(1)
    pyautogui.typewrite(file_path, interval=0.05)
    pyautogui.press("enter")
    time.sleep(2)

    # Κλείσιμο Notepad
    subprocess.call(["taskkill", "/IM", "notepad.exe", "/F"])
    time.sleep(1)

    # Εκτέλεση με Notepad
    subprocess.Popen(["notepad.exe", file_path])
    time.sleep(5)

    # Κλείσιμο Notepad
    subprocess.call(["taskkill", "/IM", "notepad.exe", "/F"])
    time.sleep(1)

    shutil.copy(file_path, copy_path)

    # Open copy
    subprocess.Popen(["notepad.exe", copy_path])
    time.sleep(5)
    subprocess.call(["taskkill", "/IM", "notepad.exe", "/F"])
    time.sleep(1)

    for f in [file_path, copy_path]:
        if os.path.exists(f):
            os.remove(f)
            print(f"{f} Deleted.")


while True:
    action = random.randint(1, 8)

    if action in range(1, 6):  # Sites + download
        if driver is None:
            driver = webdriver.Edge(options=options)

        url = urls[action]
        driver.get(url)
        time.sleep(3)
        accept_cookies(driver)

        if action == 1:  # CNN scroll
            scroll_times = random.randint(3, 7)
            scroll_page(driver, scroll_times)

        elif action == 2:  # Gmail login simulation
            try:
                email = driver.find_element(By.ID, "identifierId")
                email.send_keys("testuser@example.com")
                driver.find_element(By.ID, "identifierNext").click()
                time.sleep(3)
            except:
                print("Gmail login elements not found.")

        elif action == 3:  # YouTube search
            search_box = driver.find_element(By.NAME, "search_query")
            search_box.send_keys("TedX")
            search_box.send_keys(Keys.ENTER)
            time.sleep(3)
            videos = driver.find_elements(By.ID, "video-title")
            if videos:
                videos[0].click()
                time.sleep(random.randint(5, 10))

        elif action == 5:  # Download file
            time.sleep(5)
            file_path = r"C:\Users\\gchatzakis\\Downloads\\dummy.pdf"
            open_downloaded_file(file_path)

    elif action == 6:  # Close browser
        if driver is not None:
            print("Closing browser")
            driver.quit()
            driver = None
        else:
            print("No browser to close, skipping close.")

    elif action == 7:  # Open browser
        if driver is None:
            print("Opening new browser")
            driver = webdriver.Edge(options=options)
        else:
            print("Browser already open, skipping open.")

    elif action == 8:  # Notepad simulation
        notepad_simulation()

    time.sleep(random.randint(3, 6))
