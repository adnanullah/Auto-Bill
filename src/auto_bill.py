import os
import atexit
import requests
from ConfigParser import SafeConfigParser
from datetime import datetime
from selenium import webdriver


class AutoBill(object):

    def __init__(self, config, script_path='.'):
        self.__config = config
        self.__script_path = script_path
        self.__username = self.__config.get('credentials', 'username')
        self.__password = self.__config.get('credentials', 'password')
        self.__sign_in_url = self.__config.get('uris', 'sign-in')
        self.__download_url = self.__config.get('uris', 'download')

        self.__driver = webdriver.PhantomJS()
        self.__driver.implicitly_wait(5)
        atexit.register(self.close)

    def close(self):
        self.__driver.quit()

    def login(self):
        self.__driver.get(self.__sign_in_url)
        
        txt_username = self.__driver.find_element_by_css_selector('#username')
        txt_password = self.__driver.find_element_by_css_selector('#password')
        submit = self.__driver.find_element_by_css_selector('.btn-primary')
        
        txt_username.send_keys(self.__username)
        txt_password.send_keys(self.__password)
        submit.click()

    def view_bill(self):
        view_current_bill = self.__driver.find_element_by_css_selector('#myBills div.fl a.newCta')
        view_current_bill.click()

    def download(self):
        self.login()
        self.view_bill()
        cookies = {}
        for cookie in self.__driver.get_cookies():
            cookies[cookie['name']] = cookie['value']
        r = requests.get(self.__download_url, cookies=cookies)
        now = datetime.now()
        path = self.__config.get('options', 'file-path')
        postfix = self.__config.get('options', 'file-postfix')
        ext = self.__config.get('options', 'file-extension')
        date = now.strftime('%Y-%m')
        output_filename = os.path.abspath(os.path.join(self.__script_path, path, '%s%s%s' % (date, postfix, ext)))
        with open(output_filename, 'wb') as pdf:
            pdf.write(r.content)


if __name__ == '__main__':
    config = SafeConfigParser({'file-path': '.'})
    script_path = os.path.dirname(__file__)
    config.read(os.path.abspath(os.path.join(script_path, 'auto_bill.cfg')))
    AutoBill(config, script_path).download()
