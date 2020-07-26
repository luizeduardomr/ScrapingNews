from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from traceback import print_exc
from selenium import webdriver

import time
import os


options = Options()
options.headless = True

GET   = lambda x : GLOBAL_BR.find_element_by_xpath(x)
ID	  = lambda x : GLOBAL_BR.find_element_by_id(x)
CLASS = lambda x : GLOBAL_BR.find_element_by_class_name(x)
FIND  = lambda x : GET(x) if x.startswith('/') else ID(x)
TXT   = lambda x : FIND(x).text.strip()
CLICK = lambda x : FIND(x).click()
LINK  = lambda x : FIND(x).get_attribute('href')

def init():
	try:
		END()
	except:
		pass

	global GLOBAL_BR
	GLOBAL_BR = webdriver.Chrome(executable_path=os.path.join('src','chromedriver'+ext), options=options)

init()

END = lambda : (GLOBAL_BR.quit(), os.system('killall chromedriver'))

class cod_found:
	def set(self, val):
		self.cod = val
	def get(self):
		return self.cod
wait_code = cod_found()

class element_has_info:
	def __init__(self, getters):
		self.getters = getters

	def __call__(self, driver):
		wait_code.set(-1)

		for i,getter in enumerate(self.getters):
			try:
				var = getter()
				wait_code.set(i)
				break
			except Exception as e:
				var = False

		if not var and wait_code.get() != -1:
			return True

		return var

waiter = WebDriverWait(GLOBAL_BR, 5)
_wait  = lambda *getters : waiter.until(element_has_info(getters))

WAIT_CLICK = lambda x : _wait(lambda : CLICK(x))
WAIT_TXT   = lambda x : _wait(lambda : TXT(x))
WAIT_GET   = lambda x : _wait(lambda : GET(x))
WAIT_ID	   = lambda x : _wait(lambda : ID(x))
WAIT_FIND  = lambda x : _wait(lambda : FIND(x))
WAIT_LINK  = lambda x : _wait(lambda : LINK(x))
WAIT_CLASS = lambda x : _wait(lambda : CLASS(x))