from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd
import sys

USERNAME = 'student'
PASSWORD = 'moodle'
 
class PostToForumTest():
     def __init__(self, username, password, df):
          # Lưu thông tin của account và set up Driver
          self.username = username
          self.password = password
          self.driver = webdriver.Chrome()
          # df là thuộc tính lưu trữ data đọc từ bảng excel
          self.df = df
          # Method là phương pháp test hiện tại
          self.method = None
        
     def log_in(self):
          # Thưc hiện click nut login trên thành header
          time.sleep(2)
          log_in_button = self.driver.find_element(By.LINK_TEXT, 'Log in')
          log_in_button.click()
          # Tìm đến field username, nhập dữ liệu vào cụ thể ở đây là "student"
          username_input = self.driver.find_element(By.NAME, 'username')
          username_input.clear()
          username_input.send_keys(self.username)
          # Tìm đến field password, nhập dữ liệu vào cụ thể ở đây là "moodle"
          password_input = self.driver.find_element(By.NAME, 'password')
          password_input.clear()
          password_input.send_keys(self.password + Keys.ENTER)
          time.sleep(3)
    
     def log_out(self):
          # Click vào icon account của User để xuất cữa sổ dropdown
          time.sleep(2)
          menu_toggle_element = self.driver.find_element(By.ID, 'user-menu-toggle')
          menu_toggle_element.click()
          # Click chọn tuy chọn log out
          log_out_button = self.driver.find_element(By.LINK_TEXT, 'Log out')
          log_out_button.click()
          time.sleep(3)
            
     def postToForum(self):
          with open("PostToForumTestLogs", 'w') as file:
               # Phương thức thực hiện quá trình test chức năng search courses
               # Loop qua các testcase có trong file excel được lưu trong thuộc tính self.df
               for i in range(len(self.df)):
                    # tìm và click vào "My courses" trên thành điều hướng của website
                    self.driver.find_element(By.LINK_TEXT , "My courses").click()
                    time.sleep(3)
                    
                    # tìm và click chọn vào khóa học Activity examples 
                    self.driver.find_element(By.XPATH, "//div/div/div/div/div/a/div").click()
                    time.sleep(1)
                    
                    # tìm và click chọn vào forum "A standard forum for general use"
                    self.driver.find_element(By.LINK_TEXT, f'{self.df.iloc[i]["FORUM"]}').click()
                    time.sleep(1)
                    
                    # tìm và click chọn button vào forum "Add discussion topic" để tiến hành thêm mới discussion
                    self.driver.find_element(By.LINK_TEXT, "Add discussion topic").click()
                    time.sleep(1)
                    
                    # check nếu trong testcase có Advandce Mode 
                    if not pd.isna(self.df.iloc[i]["ADVANDED_MODE"]):
                         # tìm và click chọn vào forum "advandce" để thêm các trường thông tin (attachment và tag)
                         self.driver.find_element(By.NAME, "advancedadddiscussion").click()
                         time.sleep(2)
                    
                         
                    # check nếu trong testcase có nôi dung cho field Subject 
                    if not pd.isna(self.df.iloc[i]["SUBJECT"]):
                         # tim và nhập nôi dung và field Subject
                         subject_element = self.driver.find_element(By.NAME, "subject")
                         subject_element.send_keys(self.df.iloc[i]["SUBJECT"])
                         time.sleep(2)
                    
                         
                    # check nếu trong testcase có nôi dung cho field Message    
                    if not pd.isna(self.df.iloc[i]["MESSAGE"]):
                         # thực hiên các bược switch frame và chọn đên phần chen nói dung cho field Message
                         self.driver.switch_to.frame(0)
                         self.driver.find_element(By.CSS_SELECTOR, "html").click()
                         element = self.driver.find_element(By.XPATH, "//body[@id=\'tinymce\']")
                         self.driver.execute_script(f"if(arguments[0].contentEditable === 'true') {{arguments[0].innerText = '{self.df.iloc[i]['MESSAGE']}'}}", element)
                         self.driver.switch_to.default_content()
                         time.sleep(2)
                    
                         
                    # check nếu trong testcase có nôi dung cho field Attachment   
                    if not pd.isna(self.df.iloc[i]["ATTACHMENT"]):    
                         # tìm và click chọn vòa biểu tường file để chèn file
                         self.driver.find_element(By.XPATH , "//div/div[2]/div/div/div/a/i").click()
                         time.sleep(3)
                         # chọn sang tìm kiếm các file đã upload gần đây
                         self.driver.find_element(By.LINK_TEXT , "Recent files").click()
                         time.sleep(3)
                         # chọn file cần upload 
                         self.driver.find_element(By.XPATH , "//a/div/div[3]").click()
                         time.sleep(3)
                         # tìm và ấn vào button "Select this file"
                         self.driver.find_element(By.XPATH , "//form/div[4]/div/button").click()
                         time.sleep(3)

                    
                    # Print ra method test hiện tại
                    prevMethod = self.method
                    self.method = self.df.iloc[i]["METHOD_TEST"]
                    if self.method != prevMethod:
                         print(self.method)
                         file.write(f"{self.method}\n")
                         
                     
                   # có 2 loại action chình ["Post" , "Cancel"]
                    if self.df.iloc[i]["ACTION"] == "submit":
                         # tìm và click vào button xác nhận post to forum
                         self.driver.find_element(By.NAME, "submitbutton").click()
                         time.sleep(5)
                    elif self.df.iloc[i]["ACTION"] == "cancel":
                         # tìm và click vào button cancel
                         if not pd.isna(self.df.iloc[i]["ADVANDED_MODE"]):
                              self.driver.find_element(By.NAME, "cancel").click()
                         else:
                              self.driver.find_element(By.NAME, "cancelbtn").click()
                         time.sleep(3)
                         print(f"PASS - {self.df.iloc[i]['TC_ID']} - Action Cancel and No Verify Text\n")
                         file.write(f"PASS - {self.df.iloc[i]['TC_ID']} - Action Cancel and No Verify Text\n")
                         # self.log_out()
                         continue
                         
                    # Handle verify the result
                    if self.df.iloc[i]["EXPECT"] == "Your post was successfully added.":
                         # tim phân từ chưa string  "Your post was successfully added." và lấy text để so sánh với string Verify
                         verify_element = self.driver.find_element(By.XPATH, "//p")
                         verify_element_text = verify_element.text
                         if verify_element_text == self.df.iloc[i]["EXPECT"]:
                              # Nếu có thì -> Pass testcase
                              print(f"PASS - {self.df.iloc[i]['TC_ID']} - VERIFY_TEXT: {self.df.iloc[i]['EXPECT']} - RESULT_TEXT: {verify_element.text}\n")
                              file.write(f"PASS - {self.df.iloc[i]['TC_ID']} - VERIFY_TEXT: {self.df.iloc[i]['EXPECT']} - RESULT_TEXT: {verify_element.text}\n")
                         else:
                              # Nếu ko thì -> Failed testcase
                              print("FAIL -" , self.df.iloc[i]["TC_ID"] , "- EXPECT:" , self.df.iloc[i]["EXPECT"], "- RESULT",self.df.iloc[i]["NOTE"])
                              file.write(f"FAIL - {self.df.iloc[i]['TC_ID']} - VERIFY_TEXT: {self.df.iloc[i]['EXPECT']} - RESULT_TEXT: {verify_element_text} - NOTE: {self.df.iloc[i]['NOTE']}\n")
                              time.sleep(3)
                              
                    elif self.df.iloc[i]["EXPECT"] == "Required":
                         # tìm dòng "- Required" đươc cảnh báo dười Subject hoặc Message trong thường hợp missing data
                         if pd.isna(self.df.iloc[i]["SUBJECT"]):
                              verify_element = self.driver.find_element(By.XPATH, "//div[@id='id_error_subject']")
                         else:
                              verify_element = self.driver.find_element(By.XPATH, "//div[@id='id_error_message']")
                              
                         verify_element_text = verify_element.text
                         if verify_element_text == "- " + self.df.iloc[i]["EXPECT"]:
                              # Nếu có thì -> Pass testcase
                              print(f"PASS - {self.df.iloc[i]['TC_ID']} - VERIFY_TEXT: - {self.df.iloc[i]['EXPECT']} - RESULT_TEXT: {verify_element.text}\n")
                              file.write(f"PASS - {self.df.iloc[i]['TC_ID']} - VERIFY_TEXT: {self.df.iloc[i]['EXPECT']} - RESULT_TEXT: {verify_element.text}\n")
                         else:
                              # Nếu ko thì -> Failed testcase
                              print("FAIL -" , self.df.iloc[i]["TC_ID"] , "- EXPECT:" , self.df.iloc[i]["EXPECT"], "- RESULT",self.df.iloc[i]["NOTE"])
                              file.write(f"FAIL - {self.df.iloc[i]['TC_ID']} - VERIFY_TEXT: {self.df.iloc[i]['EXPECT']} - RESULT_TEXT: {verify_element_text} - NOTE: {self.df.iloc[i]['NOTE']}\n")
                              time.sleep(3)
                              
                    elif self.df.iloc[i]["EXPECT"] == "Maximum of 255 characters":
                         # tim phân từ chưa string  "Maximum of 255 characters" và lấy text để so sánh với string Verify
                         verify_element = self.driver.find_element(By.ID, "id_error_subject")
                         verify_element_text = verify_element.text
                         if verify_element_text == "- " + self.df.iloc[i]["EXPECT"]:
                              # Nếu có thì -> Pass testcase
                              print(f"PASS - {self.df.iloc[i]['TC_ID']} - VERIFY_TEXT: - {self.df.iloc[i]['EXPECT']} - RESULT_TEXT: {verify_element.text}\n")
                              file.write(f"PASS - {self.df.iloc[i]['TC_ID']} - VERIFY_TEXT: {self.df.iloc[i]['EXPECT']} - RESULT_TEXT: {verify_element.text}\n")
                         else:
                              # Nếu ko thì -> Failed testcase
                              print("FAIL -" , self.df.iloc[i]["TC_ID"] , "- EXPECT:" , self.df.iloc[i]["EXPECT"], "- RESULT",self.df.iloc[i]["NOTE"])
                              file.write(f"FAIL - {self.df.iloc[i]['TC_ID']} - VERIFY_TEXT: {self.df.iloc[i]['EXPECT']} - RESULT_TEXT: {verify_element_text} - NOTE: {self.df.iloc[i]['NOTE']}\n")
                         
                         # tìm button cancel để có thể xóa và logout mà không hiện một arlert của browser yêu cầu xác nhận xóa dữ liệu
                         if not pd.isna(self.df.iloc[i]["ADVANDED_MODE"]):
                              self.driver.find_element(By.NAME, "cancel").click()
                         else:
                              self.driver.find_element(By.NAME, "cancelbtn").click()
                         time.sleep(3)
               
               
     def run_test(self):
         
          self.driver.get('https://qa.moodledemo.net/')
          
          self.driver.maximize_window()
          
          self.log_in()
          
          self.postToForum()
           
          self.log_out()
          
        
# RUN TEST
 
test = PostToForumTest(USERNAME, PASSWORD, pd.read_excel(sys.argv[1]))

test.run_test()

test.driver.quit()


#  "cli run test" : "python PostToForumTest.py PostToForum.xlsx" 
