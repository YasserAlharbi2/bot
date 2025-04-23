import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def run_bot(filepath):
    # 1. open webdriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    chrome_options.binary_location = "/usr/bin/chromium-browser"  # جرب هذا المسار
    # أو "/usr/bin/google-chrome" أو "/usr/bin/chromium" حسب اللي متوفر

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

    # 2. Open Login Page
    driver.get("https://sysdawa.moia.gov.sa/login")
    time.sleep(2)  # Wait for the page to load

    # 2. Enter login details (by html name attributes)
    username = driver.find_element(By.NAME, "username")
    password = driver.find_element(By.NAME, "password")

    username.send_keys("1016411728")  # Replace with your username
    password.send_keys("2313")  # Replace with your password
    password.send_keys(Keys.RETURN)  # Press Enter to submit login
    time.sleep(3)  # Wait for login to complete

    # 3. Reading Data From Excel Sheet Using pandas
    # df= pd.read_excel("برنامج الاحياء النائية.xlsx")
    df = pd.read_excel(filepath)

    # save all column in lists
    name = df["name"]
    timee = df["time"]
    date = df["date"]
    street = df["street"]
    address = df["address"]
    number = df["number"]
    # Loop For All Rows that not blank in Excel
    for i in range(len(name.values)):

        # 4. Go to Add page after sign in
        driver.get("https://sysdawa.moia.gov.sa/Activities_C/add")
        time.sleep(2)

        # 5. Now finding form fields and pass data on it
        
        # First Field : daiaa select
        # finding daiaa html element with id open_lookup_Preacher_ID_1
        anchor = driver.find_element(By.XPATH, "//a[@id='open_lookup_Preacher_ID_1']")
        anchor.click() # click select to show all daiaa list
        wait = WebDriverWait(driver, 10) # waiting until pop-up showing
        # wait until search field appear in DOM 
        Daiia_name = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='search']")))
        time.sleep(3)
        # clear previous search value
        Daiia_name.clear()
        time.sleep(3)
        # fill search field with itretor daiaa name then press enter
        Daiia_name.send_keys(name.values[i])
        Daiia_name.send_keys(Keys.ENTER)
        Daiia_name.clear()
        time.sleep(2)
        # Now Find First result and select it by data-ind='0' attribute
        result_anchor = driver.find_element(By.XPATH, "//a[@data-ind='0']")
        # if result available then select it
        if result_anchor.is_displayed() and result_anchor.is_enabled():  # Ensure it's visible and clickable
            result_anchor.click()
            print("Element clicked!")


        # Second Field : subject select
        # finding subject html element with id open_lookup_Subject_ID_1
        # same daiaa 
        anchor = driver.find_element(By.XPATH, "//a[@id='open_lookup_Subject_ID_1']")
        anchor.click()
        wait = WebDriverWait(driver, 10)
        subject_name = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='search']")))
        time.sleep(3)
        subject_name.clear()
        time.sleep(3)
        subject_name.send_keys(address.values[i])
        subject_name.send_keys(Keys.ENTER)
        subject_name.clear()
        time.sleep(2)
        result_subject = driver.find_element(By.XPATH, "//a[@data-ind='0']")
        if result_subject.is_displayed() and result_subject.is_enabled():  # Ensure it's visible and clickable
            result_subject.click()
            print("Element clicked!")

        # Third Field : Date select
        # seprate date in two variable [ in excel for example 23/10]
        datesplit = date.values[i]
        day, month = datesplit.split('/')
        # finding date html elements with ids
        YearDate = driver.find_element(By.ID, "value_Umulqura_Year_1")  # Adjust selector
        MonthDate = driver.find_element(By.ID, "value_Umulqura_Month_1")  # Adjust selector
        DayDate = driver.find_element(By.ID, "value_Umulqura_Day_1")  # Adjust selector
        # select date values
        selectYear= Select(YearDate)
        selectYear.select_by_value("1446")
        time.sleep(2)
        selectMonth= Select(MonthDate)
        selectMonth.select_by_value(month)
        time.sleep(2)
        selectDay= Select(DayDate)
        selectDay.select_by_value(day)

            
        # Forth Field : subjectTime
        # finding subjectTime html element with id value_Activities_Time_1
        subjectTime = driver.find_element(By.ID, "value_Activities_Time_1")  # Adjust selector
        # Fill field with time
        subjectTime.send_keys(timee.values[i])
        # time.sleep(2)


        # Fifth Field : subjectType
        # finding subjectType html element with id value_ActivityType_ID_1
        # same as date except value selected by index not text
        subjectType = driver.find_element(By.ID, "value_ActivityType_ID_1")  # Adjust selector
        selectsubjectType= Select(subjectType)
        # time.sleep(2)
        selectsubjectType.select_by_index(7)

        # Sixth Field : language
        # finding language html element with id value_Language_ID_1
        # same as subjectType
        language = driver.find_element(By.ID, "value_Language_ID_1")  # Adjust selector
        # time.sleep(2)
        selectlanguage= Select(language)
        selectlanguage.select_by_index(1)

        # Seventh Field : PlaceType 
        # finding PlaceType html element with id value_PlacesType_ID_1
        # same as subjectType
        PlaceType = driver.find_element(By.ID, "value_PlacesType_ID_1")  # Adjust selector
        # time.sleep(2)
        selectPlaceType= Select(PlaceType)
        selectPlaceType.select_by_index(1)

        # Eighth Field : Place
        # finding Place html element with id value_Activities_Place_1
        # split data same as date but by –
        # same as subjectTime
        streetssplit = street.values[i]
        streett, cityy = streetssplit.split('–')
        Place = driver.find_element(By.ID, "value_Activities_Place_1")  # Adjust selector
        Place.send_keys(streett)

        # Nineth Field : City
        # finding City html element with id value_Governorate_ID_1
        # same as subjectType
        City = driver.find_element(By.ID, "value_Governorate_ID_1")  # Adjust selector
        # time.sleep(2)
        selectCity= Select(City)
        selectCity.select_by_index(1)


        # Tenth Field : Center
        # finding Center html element with id value_Address1_1
        # same as subjectTime
        center = driver.find_element(By.ID, "value_Address1_1")  # Adjust selector
        center.send_keys("مركز الدعوة والإرشاد بالعاصمة المقدسة")

        # Eleventh Field : Street
        # finding Street html element with id value_Address2_1
        # same as subjectTime
        streets = driver.find_element(By.ID, "value_Address2_1")  # Adjust selector
        streets.send_keys(cityy)


        # Twelve Field : lat
        # finding lat html element with id value_Latitude_1
        # same as subjectTime
        lat = driver.find_element(By.ID, "value_latitude_1")  # Adjust selector
        lat.clear()
        lat.send_keys("24.774265")

        # Thirteen Field : long
        # finding long html element with id value_Longitude_1
        # same as subjectTime
        long = driver.find_element(By.ID, "value_longitude_1")  # Adjust selector
        long.clear()
        long.send_keys("46.738586")


        # 6. Click submit button
        submit_button = driver.find_element(By.ID, "saveButton1")  # Adjust selector
        submit_button.click()

        time.sleep(6)  # Wait for form submission

    # 7. Close webPage after all data added
    driver.close()
    return "تم تشغيل البوت بنجاح (تجريبي)"
