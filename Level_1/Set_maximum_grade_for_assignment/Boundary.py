from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import time

# tài khoản mật khẩu cho giảng viên
USERNAME = 'teacher'
PASSWORD = 'moodle'

class MoodleTest():
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome()
        
    def log_in(self): #hàm login với username và password
        self.driver.get('https://qa.moodledemo.net/')
        self.driver.maximize_window()
        self.driver.find_element(By.LINK_TEXT, 'Log in').click()
        self.driver.find_element(By.NAME, 'username').send_keys(self.username)
        self.driver.find_element(By.NAME, 'password').send_keys(self.password + Keys.ENTER)
        time.sleep(5)
    
    def log_out(self): #hàm logout
        self.driver.find_element(By.ID, 'user-menu-toggle').click()
        self.driver.find_element(By.LINK_TEXT, 'Log out').click()

    def set_max_grade(self, max_grade): #hàm các bước để vào cài đặt điểm tối đa
        self.driver.find_element(By.LINK_TEXT, "My courses").click() #vào mục "My courses"
        time.sleep(3)
        self.driver.find_element(By.LINK_TEXT, "Activity examples").click() #vào khóa học có tên "Activity examples"
        self.driver.find_element(By.LINK_TEXT, "Assignment with marking guide").click() #vào bài tập có tên "Assignment with marking guide"
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, "Settings").click() #ấn nút Settings
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, "Grade").click() #vào cài đặt mục điểm
        time.sleep(1)
        maxgrade_element = self.driver.find_element(By.ID, "id_grade_modgrade_point")  
        actions = ActionChains(self.driver)
        actions.double_click(maxgrade_element).perform() #doubleclick để ghi đề giá trị cũ
        maxgrade_element.send_keys(max_grade) #điền giá trị max_grade mới
        self.driver.find_element(By.ID, "id_submitbutton").click() #ấn submit
        time.sleep(5)
    
    def verify_error(self, file, testid): #hàm kiểm tra xuất lỗi đúng không
        self.driver.find_element(By.ID, "fgroup_id_error_grade").click()
        if self.driver.find_element(By.ID, "fgroup_id_error_grade").text == "Invalid grade value. This must be an integer between 1 and 101":
            print(f"Textcase {testid} passed")
            file.write(f"Textcase {testid} passed\n")
        else:
            print(f"Textcase {testid} failed")
            file.write(f"Textcase {testid} failed\n")
    
    def verify_success(self, file, testid): #hàm kiểm tra xem cài đặt thành công không
        self.driver.find_element(By.CSS_SELECTOR, "div:nth-child(4) > h2").click()
        if self.driver.find_element(By.XPATH, "//h2[contains(.,\'Recalculating grades\')]").text == "Recalculating grades":
            print(f"Textcase {testid} passed")
            file.write(f"Textcase {testid} passed\n")
        else:
            print(f"Textcase {testid} failed")
            file.write(f"Textcase {testid} failed\n")
    
    def testcase(self, file, testid, max_grade): #hàm testcase, nhận file result, testid và input max_grade
        self.set_max_grade(max_grade)
        if max_grade < 1 or max_grade > 100: #lỗi
            self.verify_error(file, testid)
        else:
            self.verify_success(file, testid) #thành công
        time.sleep(3)
   
    def run_test(self):
        self.log_in()
        with open("Boundary_result", 'w') as file: #mở file result để ghi kết quả
            self.testcase(file, 'TC-111-001', 0)
            self.testcase(file, 'TC-111-002', 1)
            self.testcase(file, 'TC-111-003', 2)
            self.testcase(file, 'TC-111-004', 50)
            self.testcase(file, 'TC-111-005', 99)
            self.testcase(file, 'TC-111-006', 100)
            self.testcase(file, 'TC-111-007', 101)
        self.log_out()
        
# Main
test = MoodleTest(USERNAME, PASSWORD)
test.run_test()
test.driver.quit()