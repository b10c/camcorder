from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import time

driver = webdriver.Firefox()

def main():
	
	driver.get("http://admin:admin@192.168.2.1/index.cgi?page=MACFilter")
	
	
	enableButtonXpath = "//*[@id='contener']/div[3]/table[2]/tbody/tr/td[3]/ul/li[1]/input"	
	disableButtonXpath = "//*[@id='contener']/div[3]/table[2]/tbody/tr/td[3]/ul/li[2]/input"
	saveButtonXpath = "//*[@id='Confirm']"

	enableButtonElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(enableButtonXpath))
	disableButtonElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(disableButtonXpath))
	saveButtonElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(saveButtonXpath))

	#Testing Mac Adress
	B10CLaptopMacAddressXpath = "//td[preceding-sibling::td='84:4b:f5:2e:e7:45']//a[@title='Click to remove this entry']"
	
	KylePCMacAddressXpath = "//td[preceding-sibling::td='0c:8b:fd:3b:eb:42']//a[@title='Click to remove this entry']"
	KenziesIpadMacAddressXpath = "//td[preceding-sibling::td='34:e2:fd:b1:6f:c0']//a[@title='Click to remove this entry']"
	KylesiPhoneMacAddressXpath = "//td[preceding-sibling::td='14:5a:05:b8:8e:89']//a[@title='Click to remove this entry']"
	
	#removeMacAddressElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(removeMacAddressXpath))	
	#removeMacAddressElement.click()
	
	#remove_mac_address(B10CLaptopMacAddressXpath)
	
	#enable_mac_filtering(enableButtonElement, saveButtonElement)
	#disable_mac_filtering(disableButtonElement, saveButtonElement)
	
	refresh_network_devices()
	
	#driver.quit()

def enable_mac_filtering(enableButton, saveButton):
	enableButton.click()
	saveButton.click()

def disable_mac_filtering(disableButton, saveButton):
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

### MAIN ###
main()

