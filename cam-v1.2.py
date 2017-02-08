import os
import time
import datetime
import random
import commands

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

# CONSTANTS
ROUTER_IP = '192.168.2.1'
#camboy_MAC = '0c:8b:fd:3b:eb:42' #KYLE
camboy_MAC = '24:77:03:e3:78:94' #PAT
camgirl_MAC = '84:4b:f5:2e:e7:45' #B10C laptop
#phone_MAC = '14:5a:05:b8:8e:89' #KYLE 
phone_MAC = '94:94:26:19:86:f3' #PAT

# NEW CONSTANTS
driver = webdriver.Firefox()

# Testing Mac Address
B10CLaptopMacAddressXpath = "//td[preceding-sibling::td='84:4b:f5:2e:e7:45']//a[@title='Click to remove this entry']"	
KylePCMacAddressXpath = "//td[preceding-sibling::td='0c:8b:fd:3b:eb:42']//a[@title='Click to remove this entry']"
KenziesIpadMacAddressXpath = "//td[preceding-sibling::td='34:e2:fd:b1:6f:c0']//a[@title='Click to remove this entry']"
KylesiPhoneMacAddressXpath = "//td[preceding-sibling::td='14:5a:05:b8:8e:89']//a[@title='Click to remove this entry']"

enableButtonXpath = "//*[@id='contener']/div[3]/table[2]/tbody/tr/td[3]/ul/li[1]/input"	
disableButtonXpath = "//*[@id='contener']/div[3]/table[2]/tbody/tr/td[3]/ul/li[2]/input"
saveButtonXpath = "//*[@id='Confirm']"

enableButtonElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(enableButtonXpath))
disableButtonElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(disableButtonXpath))
saveButtonElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(saveButtonXpath))



INTERVAL = 120	
JITTER = 0
SATURDAY = 5
SUNDAY = 6

HOLIDAYS = [{"month":1,  "day":01},
	    {"month":2,  "day":16},
	    {"month":4,  "day":03},
	    {"month":4,  "day":06},
	    {"month":5,  "day":18},
	    {"month":7,  "day":01},
	    {"month":8,  "day":03},
	    {"month":9,  "day":07},
	    {"month":10, "day":12},
	    {"month":12, "day":25},
	    {"month":12, "day":26}]


def is_kyle_at_work(hnow):
	if hnow.tm_hour >= 17:
		return False
	elif hnow.tm_hour >= 14:
		return True
	elif hnow.tm_hour >= 13:
		return False
	elif hnow.tm_hour >= 9:
		return True
	else:
		return False


def is_today_a_day_off(hnow):
	if hnow.tm_wday == SATURDAY or \
	   hnow.tm_wday == SUNDAY:
		return True

	for day in HOLIDAYS:
		if day["month"] == hnow.tm_mon and \
	           day["day"]   == hnow.tm_mday:
			return True

	return False


def get_html_file_name(html_output):
	for item in html_output[1].split("\n"):
		if "Saving to:" in item:
			file_line = item.split()

	file_name = file_line[2].replace("\xe2\x80\x98","")
	file_name = file_name.replace("\xe2\x80\x99","")
	return file_name
	


def get_mac_filtering_html(router_ip):
	linux_html_get_cmd = """wget {0}/index.cgi?page=MACFilter --user=admin --password=admin""".format(router_ip)

	html_output = commands.getstatusoutput(linux_html_get_cmd) 

	if not "200 OK" in html_output[1]:
		print "MAC Filtering HTTP GET did not return OK"
		print html_output
		return False

	html_file_name = get_html_file_name(html_output)
	html_file = open(html_file_name, "r")
	html_file = html_file.read()
	return html_file


def is_mac_filter_enabled(html):
    start = "MAC Filtering Status:"
    end = "Check to enable MAC Filtering"
    parse = ((html.split(start))[1].split(end)[0])

    if "Enabled" in parse:
	return True

    return False

	
def is_mac_online(html, mac):
    count = 0
    for line in html.split("\n"):
	if count == 2:
	    if "wifi_enable" in line:
		return True
	    break
	if count != 0:
	    count += 1
	if mac in line:
	    count += 1

    return False

# Control APIs
# DEPRECIATED
# def get_mac_addr_position(html, mac):
#    for line in html.split("\n"):
#	if mac in line:
#	    string = line
#	    for item in string.split(" "):
#		if "mac" in item:
#		    string = item
#		    return int(''.join(ele for ele in string if ele.isdigit()))
#
#   return -1


#def open_mac_filter_page():
#
#    chromedriver = "/home/pkhordoc/Downloads/chromedriver"
#    os.environ["webdriver.chrome.driver"] = chromedriver
#    driver = webdriver.Chrome(chromedriver)
#    URL = "http://admin:admin@192.168.2.1/index.cgi?page=MACFilter&"
#    driver.get(URL)
#    return driver


#def find_mac_filter_settings(driver):
#    for i in range(21):
#        ActionChains(driver).send_keys(Keys.TAB).perform()


#def disable_mac_filtering():
#    driver = open_mac_filter_page()
#    find_mac_filter_settings(driver)
#    ActionChains(driver).send_keys(Keys.ARROW_RIGHT).perform()
#    ActionChains(driver).send_keys(Keys.ENTER).perform()
#    driver.close()

#def enable_mac_filtering(html, mac_array):
#    driver = open_mac_filter_page()
#    find_mac_filter_settings(driver)
#    ActionChains(driver).send_keys(Keys.ARROW_LEFT).perform()
#    
#    first = True
#    for mac in mac_array:
#	if first == False:
#	    find_mac_filter_settings(driver)
#	else:
#	    first = False
#	mac_position = get_mac_addr_position(html, mac)
#	if mac_position == -1:
#	    continue
#	for i in range(mac_position + 1):
#	    ActionChains(driver).send_keys(Keys.TAB).perform()
#	    
#	ActionChains(driver).send_keys(Keys.ENTER).perform()
#
#    ActionChains(driver).send_keys(Keys.ENTER).perform() 
#    driver.close()
	
def enable_mac_filtering(enableButton, saveButton):
	driver.get("http://admin:admin@192.168.2.1/index.cgi?page=MACFilter")
	enableButton.click()
	saveButton.click()


def disable_mac_filtering(disableButton, saveButton):
	driver.get("http://admin:admin@192.168.2.1/index.cgi?page=MACFilter")
	disableButton.click()
	saveButton.click()
	
def remove_mac_address(macAddressXpath):
	removeMacAddressElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(macAddressXpath))
	removeMacAddressElement.click()
	
def refresh_network_devices():
	driver.get("http://192.168.2.1/index.cgi?page=table_device&sessionid=RspO9pZHzB865AP1zCS844AL3BC6Dtm")
	refreshButtonXpath = "//*[@id='Refresh_button']/a"
	refreshButtonElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(refreshButtonXpath))
	refreshButtonElement.click()	
 

### Main() ###
sleep_time = 0
old_filter_settings = False
while (1):
	# Iteration State
	at_work = False
	mac_filter_enabled = False
	camboy_enabled = False
	camgirl_enabled = False
	phone_online = False

	# Iteration Actions
	enable_filter = False
	disable_filter = False
	block_camboy = False
	block_camgirl = False

	current_time = time.time()
	current_timeh = time.localtime(current_time)

	sleep_time = random.randint((INTERVAL-JITTER), \
			            (INTERVAL+JITTER))

	if is_kyle_at_work(current_timeh):
		at_work = True	

	if is_today_a_day_off(current_timeh):
		at_work = False
		sleep_time = 24*60*60


	# get MAC Filtering configuration from router
	# refresh mac table
	html = get_mac_filtering_html(ROUTER_IP)
	if not html:
		print "Sleeping for %d seconds" \
		       % (sleep_time) 
		time.sleep(sleep_time)
		continue	

	#Parse html to get Router state
	mac_filter_enabled = is_mac_filter_enabled(html)
	phone_online = is_mac_online(html, phone_MAC)
	if mac_filter_enabled:
		camboy_enabled = camboy_MAC in html
		camgirl_enabled = camgirl_MAC in html

	# Figure out if router has been reset since last sleep
	if mac_filter_enabled not old_filter_settings:
	    print "Router has been reset, OLD=%d, NEW=%d" \
	          % (old_filter_settings, mac_filter_enabled)

 	# Figure out what actions need to be taken	
	if at_work and not phone_online:
	    old_filter_settings = True
	    if not mac_filter_enabled:
	        enable_filter = True
	    if camboy_enabled:
		block_camboy = True
	    if camgirl_enabled:
		block_camgirl = True
	else:
	    old_filter_settings = False
	    if mac_filter_enabled:
		disable_filter = True

	# Perform the actions
	if block_camboy or block_camgirl or  enable_filter:
		remove_mac_address(B10CLaptopMacAddressXpath)
	   	enable_mac_filtering(enableButtonElement, saveButtonElement)
	elif disable_filter:
	    disable_mac_filtering(disableButtonElement, saveButtonElement)

	driver.quit()
	# Print iteration state and control information
	print "\n"
	print datetime.datetime.now()
        print "At Work: {0}, Filter: {1}, Boy Access: {2},"\
              " Girl Access: {3}, Phone Online: {4}"\
              .format(at_work, mac_filter_enabled, \
                     camboy_enabled, camgirl_enabled,\
                     phone_online)
	print "Enable Filter: {0}, Disable Filter: {1}, " \
	       "Block CamBoy: {2}, Block CamGirl: {3}"\
	       .format(enable_filter, disable_filter, \
		       block_camboy, block_camgirl)
	print "Sleeping for %d seconds" \
	      % (sleep_time)
	os.system("rm *index*")

	# Sleep for some time
	time.sleep(5)
