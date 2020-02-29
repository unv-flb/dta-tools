#version:1.0
#author:unvirtual
import sys
import os
import time
from requests.exceptions import ConnectionError
import requests
from torrequest import TorRequest
from pyfiglet import Figlet

#TEXT COLOR

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

 #FUNCTIONS   

def _error():
	print(bcolors.FAIL+"Only numbers"+bcolors.ENDC)


def quit():
	sys.exit(0)


def get_URL():
	global url
	url = str(input("\nEnter URL(e.g.:http://example.com): "))


def Y_tor(): 
	local_time = time.localtime()
	time_string = time.strftime("%m/%d/%Y, %H:%M:%S ", local_time)
	get_URL()

	with TorRequest(proxy_port=9050, ctrl_port=9051, password=None) as tr:
		try:
			print(bcolors.BOLD+"\n[+] Searching for files...\n"+bcolors.ENDC)

			for line in file:	
				lfi = (str(tr.get(url+line))+" -> "+url+line)
				if lfi.find('200') != -1:
					print(lfi)
				all_test = open("tr_requests.txt","a")
				all_test.write(str("\n"+time_string+lfi))

		except ConnectionError:
			print(bcolors.FAIL+"Connection Error, retry"+bcolors.ENDC)
			Y_tor()	
			
		print(bcolors.WARNING+"FINISHED - see more in tr_requests.txt"+bcolors.ENDC)
		file.close()
		quit()

	
def N_tor():
	local_time = time.localtime()
	time_string = time.strftime("%m/%d/%Y, %H:%M:%S ", local_time)
	get_URL()	
	try: 
		print(bcolors.BOLD+"\n[+] Searching for files...\n"+bcolors.ENDC)
		for line in file:
			lfi = (str(requests.get(url+line))+" -> "+url+line)
			if lfi.find('200') != -1:
				print(lfi)
			all_test = open("requests.txt","a")
			all_test.write(str("\n"+time_string+lfi))
			
	except ConnectionError:
		print(bcolors.FAIL+"Connection Error, retry"+bcolors.ENDC)
		N_tor()
	print(bcolors.WARNING+"FINISHED - see more in requests.txt"+bcolors.ENDC)
	file.close()
	quit()


def ip():
	response = requests.get('http://ipecho.net/plain')
	print(bcolors.FAIL+"\nOriginal IP Address: ", response.text+bcolors.ENDC)
	with TorRequest() as tr:
		tr.reset_identity()
		response = tr.get('http://ipecho.net/plain')
		print(bcolors.OKGREEN+"New Ip Address: ", response.text+bcolors.ENDC)


def tor_requests():
	global user_requests
	x=' '
	print(bcolors.HEADER+x*5+"[-Requests over Tor-]"+x*5+bcolors.ENDC+'\n'+bcolors.BOLD+"-you need to have tor installed-\n"+bcolors.ENDC)
	while True:
		user_requests = str(input("Y/N? : "))
		if (user_requests =="Y") or (user_requests=="y") and len(user_requests)==1:
			os.system('service tor stop')
			ip()
			Y_tor()

		elif (user_requests=="N") or(user_requests=="n") and len(user_requests)==1:
			break
			
		print(bcolors.FAIL+"Please retry"+bcolors.ENDC)
		guessInLower = user_requests.lower()


def get_URL_linuxserv():
	global file
	file = open('./lists/linux_serv.txt','r')
	tor_requests()
	N_tor()

def get_URL_IIS():
	global file
	file = open('./lists/wind_serv.txt','r')
	tor_requests()
	N_tor()

def basic_lfi():
	global file
	file = open('./lists/lists_lfi.txt','r')
	tor_requests()
	N_tor()

def wordpress():
	global file
	file = open('./lists/wordpress.txt','r')
	tor_requests()
	N_tor()

def simplecms():
	global file
	file = open('./lists/simplecms.txt','r')
	tor_requests()
	N_tor()


def serv_vuln():

	servs_lists =["[..]","[1] Linux Serv.","[2] Windows Server","[3] <- Back to menu","[4] Quit\n"];
	print(*servs_lists, sep='\n')
	try:
		serv_choice = int(input('Enter your choice: '))
		while (serv_choice <=0) or (serv_choice >4):
			serv_choice = int(input(bcolors.FAIL+'Your choice must be[1..4]: '+bcolors.ENDC))
		print("")
		serv_ = serv_get.get(serv_choice, "Invalid options")
		print(serv_())

	except ValueError:
		_error()


def cms_menu():
	cms_lists = ["[..]","[1] Wordpress","[2] CMS Simple","[3] <- Back to menu","[4] Quit\n"];
	print(*cms_lists, sep='\n')
	try:
		cms_choice = int(input('Enter your choice: '))
		while (cms_choice <=0) or (cms_choice >4):
			cms_choice = int(input(bcolors.FAIL+'Your choice must be[1..4]: '+bcolors.ENDC))
		print("")
		cms_ = cms_menu.get(cms_choice, "Invalid options")
		print(cms_())

	except ValueError:
		_error()


# MAIN

def main():

	f = Figlet(font='standard')
	print(f.renderText('DTA TOOLS'))

	print(bcolors.WARNING + "Version:1.0"+ bcolors.ENDC)
	print("")

	menus_lists =['[1] Server(Linux & Windows)','[2] CMS','[3] Basic LFI','[4] Quit\n'];
	print(*menus_lists, sep='\n')
	try:
		choices_menu = int(input('Enter your choice: '))
		while (choices_menu <=0) or (choices_menu >4):
			choices_menu = int(input(bcolors.FAIL+'Your choice must be[1..4]: '+bcolors.ENDC))
		print("")
		func = select_menu.get(choices_menu, "Invalid Options")
		print(func())
		
	except ValueError:
		_error()

# MENU_LIST 

serv_get = {
	1:get_URL_linuxserv,
	2:get_URL_IIS,
	3:main,
	4:quit
}

select_menu = {
		1:serv_vuln,
		2:cms_menu,
		3:basic_lfi,
		4:quit
}

cms_menu = {
	
	1:wordpress,
	2:simplecms,
	3:main,
	4:quit
}

if __name__ == "__main__":
	main()
