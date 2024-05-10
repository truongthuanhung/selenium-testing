from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import time

#tài khoản mật khẩu cho sinh viên
USERNAME = 'student'
PASSWORD = 'moodle'

class MoodleTest():
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome()
        
    def log_in(self):#hàm login với username và password
        self.driver.get('https://qa.moodledemo.net/')
        self.driver.maximize_window()
        self.driver.find_element(By.LINK_TEXT, 'Log in').click()
        self.driver.find_element(By.NAME, 'username').send_keys(self.username)
        self.driver.find_element(By.NAME, 'password').send_keys(self.password + Keys.ENTER)
        time.sleep(5)
    
    def log_out(self):#hàm logout
        self.driver.find_element(By.ID, 'user-menu-toggle').click()
        self.driver.find_element(By.LINK_TEXT, 'Log out').click()

    def enter_export_calendar(self): #hàm các bước để vào lấy địa chỉ mạng của lịch
        self.driver.find_element(By.LINK_TEXT, "Dashboard").click() #vào mục "Dashboard"
        time.sleep(5)
        self.driver.find_element(By.XPATH, "//a[contains(.,\'Import or export calendars\')]").click() #ấn nút Import or export calendars
        time.sleep(3)
        self.driver.find_element(By.XPATH, "//button[contains(.,\'Export calendar\')]").click() #ấn nút Export calendar
        time.sleep(3)
    
    def verify_success(self): #hàm kiểm tra lấy địa chỉ thành công
        value = self.driver.find_element(By.ID, "calendarexporturl").get_attribute("value")
        if not value == "https://qa.moodledemo.net/calendar/export_execute.php?userid=4&authtoken=3a825938ad829a496e27567fc51ef1b6839f4c6c&preset_what=all&preset_time=weeknow":
            return False #nếu địa chỉ mạng không đú return false
        self.driver.find_element(By.XPATH, "//button[contains(.,\'Copy URL\')]").click() #ấn Copy URL
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, ".toast-message").click()
        if not self.driver.find_element(By.CSS_SELECTOR, ".toast-message").text == "Calendar URL copied to clipboard": 
            return False #Nếu không hiện "Calendar URL copied to clipboard" return False
        return True

    def verify_required(self, option): #hàm kiểm tra lỗi khi nhập thiếu các trường required
        if option == "noevents" or option == "noboth": #thiếu trường events hoặc cả 2
            self.driver.find_element(By.ID, "fgroup_id_error_events").click()
            if not self.driver.find_element(By.ID, "fgroup_id_error_events").text == "Required":
                return False
        if option == "noperiod" or option == "noboth": #thiếu trường period hoặc cả 2
            self.driver.find_element(By.ID, "fgroup_id_error_period").click()
            if not self.driver.find_element(By.ID, "fgroup_id_error_period").text == "Required":
                return False
        return True #không thiếu trường nào
    
    def verify_switchtohome(self): #hàm kiểm tra việc chuyển site thành công - chuyển đến "Home"
        self.driver.find_element(By.LINK_TEXT, "Home").click()
        time.sleep(3)
        alert = self.driver.switch_to.alert 
        alert.accept() #Nhấn Rời khỏi trên alert
        if not self.driver.find_element(By.XPATH, "//h1[contains(.,'Moodle QA Testing Site')]").text == "Moodle QA Testing Site":
            return False #nếu không chuyển đến được trang Home return False
        return True #chuyển thành công
            
    def print_result(self, file, testid, result): #hàm in kết quả
        if result:
            print(f"Textcase {testid} passed")
            file.write(f"Textcase {testid} passed\n")
        else:
            print(f"Textcase {testid} failed")
            file.write(f"Textcase {testid} failed\n")
   
    def testcase1(self, file, testid): #testcase1 lấy địa chỉ thành công
        self.enter_export_calendar()
        self.driver.find_element(By.ID, "id_events_exportevents_all").click()
        self.driver.find_element(By.ID, "id_period_timeperiod_weeknow").click()
        self.driver.find_element(By.ID, "id_generateurl").click()
        time.sleep(3)
        self.print_result(file, testid, self.verify_success())
    
    def testcase2(self, file, testid): #testcase2 quên nhập trường period
        self.enter_export_calendar()
        self.driver.find_element(By.ID, "id_events_exportevents_all").click()
        self.driver.find_element(By.ID, "id_generateurl").click()
        result = self.verify_required("noperiod")
        self.driver.find_element(By.ID, "id_period_timeperiod_weeknow").click()
        self.driver.find_element(By.ID, "id_generateurl").click()
        time.sleep(3)
        self.print_result(file, testid, result and self.verify_success())

    def testcase3(self, file, testid): #testcase3 chuyển đến Home khi đang nhập
        self.enter_export_calendar()
        self.driver.find_element(By.ID, "id_events_exportevents_all").click()
        self.print_result(file, testid, self.verify_switchtohome())
   
    def run_test(self):
        self.log_in()
        with open("UseCase_result", 'w') as file: #mở file result để ghi kết quả
            self.testcase1(file, 'TC-061-001')
            self.testcase2(file, 'TC-061-002')
            self.testcase3(file, 'TC-061-003')
        self.log_out()
        
# Main
test = MoodleTest(USERNAME, PASSWORD)
test.run_test()
test.driver.quit()