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

    def enter_form(self): #hàm vào form tạo sự kiện
        self.driver.find_element(By.LINK_TEXT, "Dashboard").click() #vào mục "Dashboard"
        time.sleep(5)
        self.driver.find_element(By.XPATH, "//button[contains(.,\'New event\')]").click() #ấn nút "New event"
        time.sleep(3)
    
    def select_timestart(self, day, month, year, hour, minute): #hàm chọn timestart
        self.driver.find_element(By.XPATH, f"//select[@id='id_timestart_day']/option[. = '{day}']").click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, f"//select[@id='id_timestart_month']/option[. = '{month}']").click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, f"//select[@id='id_timestart_year']/option[. = '{year}']").click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, f"//select[@id='id_timestart_hour']/option[. = '{hour}']").click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, f"//select[@id='id_timestart_minute']/option[. = '{minute}']").click()
        time.sleep(1)
        
    def select_timeuntil(self, day, month, year, hour, minute): #hàm chọn timeuntil
        self.driver.find_element(By.ID, "id_duration_1").click()
        self.driver.find_element(By.XPATH, f"//select[@id='id_timedurationuntil_day']/option[. = '{day}']").click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, f"//select[@id='id_timedurationuntil_month']/option[. = '{month}']").click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, f"//select[@id='id_timedurationuntil_year']/option[. = '{year}']").click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, f"//select[@id='id_timedurationuntil_hour']/option[. = '{hour}']").click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, f"//select[@id='id_timedurationuntil_minute']/option[. = '{minute}']").click()
        time.sleep(1)
    
    def type_desc_and_loc(self, desc, loc): #hàm điền vào trường mô tả và vị trí
        self.driver.switch_to.frame(0)
        self.driver.find_element(By.CSS_SELECTOR, "p").click()
        tinymce = self.driver.find_element(By.ID, "tinymce")
        self.driver.execute_script("if(arguments[0].contentEditable === 'true') {arguments[0].innerHTML = '<p>"+desc+"</p>'}", tinymce)
        self.driver.switch_to.default_content()
        self.driver.find_element(By.ID, "id_location").click()
        self.driver.find_element(By.ID, "id_location").send_keys(loc)
    
    def type_num_loop(self, num_loop): #hàm điền số lần lặp lại
        self.driver.find_element(By.ID, "id_repeat").click()
        repeats = self.driver.find_element(By.ID, "id_repeats")
        actions = ActionChains(self.driver)
        actions.double_click(repeats).perform()
        repeats.send_keys(num_loop) 
    
    def delete_event(self): #hàm xóa sự kiện vừa thêm
        self.driver.find_element(By.CSS_SELECTOR, "a > .fa-trash").click()
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, ".modal-footer > .btn-primary").click()
        time.sleep(5)
    
    def change_time(self, time): #hàm chỉnh thời gian từ kiểu 24h sang 12h
        time_change = int(time)
        time_notation = 'AM'
        if time_change >= 12:
            time_notation = 'PM'
        if time_change > 12:
            time_change -= 12
        return time_change, time_notation
        
    def verify_time_notuntil(self, time_start): #hàm kiểm tra xem thời gian sự kiện được thêm đúng không khi không có timeuntil
        time_change, time_notation = self.change_time(time_start[3])
        if not self.driver.find_element(By.CSS_SELECTOR, ".row:nth-child(1) > .col-11").text == f"{time_start[5]}, {time_start[0]} {time_start[1]}, {time_change}:{time_start[4]} {time_notation}":
            return False
        return True
    
    def verify_time_until(self, time_start, time_until): #hàm kiểm tra xem thời gian sự kiện được thêm đúng không khi không có timeuntil
        #chi xet truong hop test_until chi test doi gio, phut    
        time_start_change, time_start_notation = self.change_time(time_start[3])
        time_until_change, time_until_notation = self.change_time(time_until[3])
        if not self.driver.find_element(By.CSS_SELECTOR, ".row:nth-child(1) > .col-11").text == f"{time_start[5]}, {time_start[0]} {time_start[1]}, {time_start_change}:{time_start[4]} {time_start_notation} » {time_until_change}:00 {time_until_notation}":
            return False
        return True
    
    def verify_success(self, title, time_start, description = None, location = None, time_until = None): #hàm kiểm tra việc tạo sự kiện thành công
        self.driver.find_element(By.LINK_TEXT, title).click()
        time.sleep(5)
        if not self.driver.find_element(By.XPATH, f"//h5[contains(.,'{title}')]").text == title: #kiểm tra tiêu đề sự kiện
            return False 
        if description:
            if not self.driver.find_element(By.CSS_SELECTOR, ".description-content > p").text == description: #kiểm tra mô tả sự kiện
                return False
        if location:
            if not self.driver.find_element(By.CSS_SELECTOR, ".location-content").text == location: #kiểm tra vị trí sự kiện
                return False
        self.driver.find_element(By.LINK_TEXT, f"{time_start[5]}, {time_start[0]} {time_start[1]}").click() #vào xem các sự kiện của ngày đó
        if time_until: 
            return self.verify_time_until(time_start, time_until) #kiểm tra thời gian khi có timeuntil
        return self.verify_time_notuntil(time_start)  #kiểm tra thời gian khi không có timeuntil

    def verify_required_title(self, testid, file): #hàm kiểm tra lỗi không nhập trường tiêu đề
        self.driver.find_element(By.ID, "id_error_name").click()
        if self.driver.find_element(By.ID, "id_error_name").text == "- Required":
            print(f"Textcase {testid} passed")
            file.write(f"Textcase {testid} passed\n")
        else:
            print(f"Textcase {testid} failed")
            file.write(f"Textcase {testid} failed\n")
        self.driver.find_element(By.XPATH, "//div[5]/div[2]/div/div/div/button/span").click() #đóng form
        time.sleep(3)
   
    def testcase1(self, file, testid, title, time_start): #testcase1 normal flow
        #Student creates an event with two basic fields
        result = True
        self.enter_form()
        self.driver.find_element(By.ID, "id_name").click()
        self.driver.find_element(By.ID, "id_name").send_keys(title)
        time.sleep(3)
        self.select_timestart(time_start[0], time_start[1], time_start[2], time_start[3], time_start[4])
        self.driver.find_element(By.XPATH, "//button[contains(.,\'Save\')]").click()
        time.sleep(5)
        result = self.verify_success(title, time_start)
        if result == True:
            print(f"Textcase {testid} passed")
            file.write(f"Textcase {testid} passed\n")
        else:
            print(f"Textcase {testid} failed")
            file.write(f"Textcase {testid} failed\n")
        self.delete_event()
    
    def testcase2(self, file, testid, title, time_start, description, location): #testcase2 alternative flow 1
        #Student creates an event with more fields, chooses "Không xác định thời lượng" and chooses "Lặp lại sự kiện này"
        result = True
        self.enter_form()
        self.driver.find_element(By.ID, "id_name").click()
        self.driver.find_element(By.ID, "id_name").send_keys(title)
        time.sleep(3)
        self.select_timestart(time_start[0], time_start[1], time_start[2], time_start[3], time_start[4])
        self.driver.find_element(By.XPATH, "//a[contains(.,\'Show more...\')]").click()
        time.sleep(3)
        self.type_desc_and_loc(description, location)
        self.type_num_loop("1") #chi test lap 1 lan
        self.driver.find_element(By.XPATH, "//button[contains(.,\'Save\')]").click()
        time.sleep(5)
        result = self.verify_success(title, time_start, description, location)
        if result == True:
            print(f"Textcase {testid} passed")
            file.write(f"Textcase {testid} passed\n")
        else:
            print(f"Textcase {testid} failed")
            file.write(f"Textcase {testid} failed\n")
        self.delete_event()
        
    def testcase3(self, file, testid, time_start): #testcase3 alternative flow 2
        #Important fields are not filled
        self.enter_form()
        self.driver.find_element(By.ID, "id_name").click()
        self.driver.find_element(By.ID, "id_name").send_keys("")
        time.sleep(3)
        self.select_timestart(time_start[0], time_start[1], time_start[2], time_start[3], time_start[4])
        self.driver.find_element(By.XPATH, "//button[contains(.,\'Save\')]").click()
        time.sleep(5)
        self.verify_required_title(testid, file)
        
    def testcase4(self, file, testid, title, time_start, description, location, time_until): #testcase4 alternative flow 3
        #Student creates an event with more fields, chooses "Tới" and chooses "Lặp lại sự kiện này"
        #lưu ý: test_until chi test doi gio, phut
        result = True
        self.enter_form()
        self.driver.find_element(By.ID, "id_name").click()
        self.driver.find_element(By.ID, "id_name").send_keys(title)
        time.sleep(3)
        self.select_timestart(time_start[0], time_start[1], time_start[2], time_start[3], time_start[4])
        self.driver.find_element(By.XPATH, "//a[contains(.,\'Show more...\')]").click()
        time.sleep(3)
        self.type_desc_and_loc(description, location)
        self.select_timeuntil(time_until[0], time_until[1], time_until[2], time_until[3], time_until[4])
        self.type_num_loop("1") #chi test lap 1 lan
        self.driver.find_element(By.XPATH, "//button[contains(.,\'Save\')]").click()
        time.sleep(5)
        result = self.verify_success(title, time_start, description, location, time_until)
        if result == True:
            print(f"Textcase {testid} passed")
            file.write(f"Textcase {testid} passed\n")
        else:
            print(f"Textcase {testid} failed")
            file.write(f"Textcase {testid} failed\n")
        self.delete_event()
    
    def testcase5(self, file, testid, title, time_start, description, location, duration_minutes): #testcase5 alternative flow 4
        #Student creates an event with more fields, chooses "Thời lượng tính bằng phút" and chooses "Lặp lại sự kiện này"
        #duration chi test doi gio, phut
        result = True
        self.enter_form()
        self.driver.find_element(By.ID, "id_name").click()
        self.driver.find_element(By.ID, "id_name").send_keys(title)
        time.sleep(3)
        self.select_timestart(time_start[0], time_start[1], time_start[2], time_start[3], time_start[4])
        self.driver.find_element(By.XPATH, "//a[contains(.,\'Show more...\')]").click()
        time.sleep(3)
        self.type_desc_and_loc(description, location)
        self.driver.find_element(By.ID, "id_duration_2").click()
        self.driver.find_element(By.ID, "id_timedurationminutes").click()
        self.driver.find_element(By.ID, "id_timedurationminutes").send_keys(duration_minutes)
        self.type_num_loop("1") #chi test lap 1 lan
        self.driver.find_element(By.XPATH, "//button[contains(.,\'Save\')]").click()
        time.sleep(5)
        time_until = [time_start[0], time_start[1], time_start[2], str(int(time_start[3])+duration_minutes//60), str(int(time_start[4])+duration_minutes%60), time_start[5]]
        result = self.verify_success(title, time_start, description, location, time_until)
        if result == True:
            print(f"Textcase {testid} passed")
            file.write(f"Textcase {testid} passed\n")
        else:
            print(f"Textcase {testid} failed")
            file.write(f"Textcase {testid} failed\n")
        self.delete_event()
        
    def testcase6(self, file, testid, title, time_start, description, location): #testcase6 alternative flow 5
        #Student creates an event with more fields, choose "Không xác định thời lượng" and doesn't choose "Lặp lại sự kiện này"
        result = True
        self.enter_form()
        self.driver.find_element(By.ID, "id_name").click()
        self.driver.find_element(By.ID, "id_name").send_keys(title)
        time.sleep(3)
        self.select_timestart(time_start[0], time_start[1], time_start[2], time_start[3], time_start[4])
        self.driver.find_element(By.XPATH, "//a[contains(.,\'Show more...\')]").click()
        time.sleep(3)
        self.type_desc_and_loc(description, location)
        self.driver.find_element(By.XPATH, "//button[contains(.,\'Save\')]").click()
        time.sleep(5)
        result = self.verify_success(title, time_start, description, location)
        if result == True:
            print(f"Textcase {testid} passed")
            file.write(f"Textcase {testid} passed\n")
        else:
            print(f"Textcase {testid} failed")
            file.write(f"Textcase {testid} failed\n")
        self.delete_event()
        
    def testcase7(self, file, testid, title): #testcase7 exception flow 1
        #Student want to exit
        self.enter_form()
        self.driver.find_element(By.ID, "id_name").click()
        self.driver.find_element(By.ID, "id_name").send_keys(title)
        self.driver.find_element(By.XPATH, "//div[5]/div[2]/div/div/div/button/span").click()
        time.sleep(3)
        if self.driver.find_element(By.XPATH, "//h1[contains(.,\'Dashboard\')]").text == "Dashboard":
            print(f"Textcase {testid} passed")
            file.write(f"Textcase {testid} passed\n")
        else:
            print(f"Textcase {testid} failed")
            file.write(f"Textcase {testid} failed\n")
   
    def run_test(self):
        self.log_in()
        with open("UseCase_result", 'w') as file: #mở file result để ghi kết quả
            self.testcase1(file, 'TC-051-001', "Học từ vựng", ['31', 'May', '2024', '07', '00', 'Friday'])
            self.testcase2(file, 'TC-051-002', "Học từ vựng", ['31', 'May', '2024', '07', '00', 'Friday'], "Học 100 từ", "Nhà")
            self.testcase3(file, 'TC-051-003', ['31', 'May', '2024', '07', '00', 'Friday'])
            self.testcase4(file, 'TC-051-004', "Học từ vựng", ['31', 'May', '2024', '07', '00', 'Friday'], "Học 100 từ", "Nhà", ['31', 'May', '2024', '09', '00', 'Friday'])
            self.testcase5(file, 'TC-051-005', "Học từ vựng", ['31', 'May', '2024', '07', '00', 'Friday'], "Học 100 từ", "Nhà", 120)
            self.testcase6(file, 'TC-051-006', "Học từ vựng", ['31', 'May', '2024', '07', '00', 'Friday'], "Học 100 từ", "Nhà")
            self.testcase7(file, 'TC-051-007', "Học từ vựng")
        self.log_out()
        
# Main
test = MoodleTest(USERNAME, PASSWORD)
test.run_test()
test.driver.quit()