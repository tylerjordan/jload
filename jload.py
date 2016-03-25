# File: jload.py
# Author: Tyler Jordan
# Modified: 4/15/2015
# Purpose: Assist CBP engineers with Juniper configuration tasks

import sys,fileinput,code,re,csv
import utility

from utility import *

from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from lxml import etree
from getpass import getpass

def importCsv(csvfile):
	try:
		my_file = open(csvfile)
		csv_data = csv.reader(my_file)
		my_list = [row for row in csv_data]
		my_list.pop(0)
		my_file.close()
		return my_list
	except Exception,err:
		print("ERROR: Encountered exception while iporting csv file :%s. Exception is : %s . \n Exiting the program.")%(csvfile,str(err))
		sys.exit(1)

def isSet(templatefile):
	isitSet = False
	try:
		my_file = open(templatefile, 'r')
		first_line = my_file.readline()
		if (re.match( r'^set\s.+', first_line)):
			isitSet = True
		return isitSet
	except Exception,err:
		print("ERROR: Encountered exception while checking template file format :%s. Exception is : %s . \n Exiting the program.")%(templatefile,str(err))
		sys.exit(1)

def getCSVHeaders(csvfile):
	try:
		my_file = open(csvfile)
		csv_data = csv.reader(my_file)
		header_list = next(csv_data)
		my_file.close()
		return header_list
	except Exception,err:
		print("ERROR: Encountered exception while retrieving csv headers : %s . Exception is : %s . \n Exiting the program.")%(csvfile,str(err))
		sys.exit(1)

def printProgress(logtype,hostname,message):
	print("%s:%s:%s")%(logtype,hostname,message)

def deployConfig(my_device_list_dict, my_username, my_password, my_config_template_file):
	my_hostname=""
	try:
		my_hostname=my_device_list_dict["mgmt_ip"]
		printProgress("INFO",my_hostname,"Connecting to device through netconf.")
		dev=Device(my_hostname,user=my_username,password=my_password)
		dev.open()
		dev.timeout=3*60
		cu = Config(dev)
		printProgress("INFO",my_hostname,"Going to load template the config now.")
		
		# Determine if template file is in "set" or "bracketed" format
		if isSet(my_config_template_file):
			rsp=cu.load(template_path=my_config_template_file,format='set',template_vars=my_device_list_dict)
		else:
			rsp=cu.load(template_path=my_config_template_file,template_vars=my_device_list_dict)
		
		printProgress("INFO",my_hostname,"Performing diff between active and candidate config.")
		cu.pdiff()
		printProgress("INFO",my_hostname,"Performing commit check")
		if cu.commit_check():
			printProgress("INFO",my_hostname,"commit check was successfull.")
			printProgress("INFO",my_hostname,"performing commit now.")
			commit_status=cu.commit()
			printProgress("INFO",my_hostname,"disconnecting from device.")
			dev.close()
			return commit_status
		else:
			return False
	except Exception,err:
		printProgress("ERROR",my_hostname,"Encountered exception while deploying config")
		printProgress("ERROR",my_hostname,str(err))
		return False

def main():
	print("\nWelcome to Junos Configuration Deployment Tool \n")
	# Try to get correct path format, checks for Windows or Linux
	try:
		path_list = getSystemPaths()
		csv_path = path_list['csv_path']
		template_path = path_list['template_path']		
	except Exception, e:
		print "Unable to determine platform. Exiting..."
		exit()
	# Get CSV File Name
	fileList = getFileList(csv_path)
	csv_file = getOptionAnswer("Choose a csv file", fileList)
	# Get Config Template
	fileList = getFileList(template_path)
	template_file = getOptionAnswer("Choose a template file", fileList)
	template_file = template_path + template_file
	# Get username and password parameters
	username = getInputAnswer("\nEnter your device username")
	password = getpass(prompt="\nEnter your device password: ")
	# Import CSV into array
	row_csv_list = importCsv(csv_path + csv_file)
	header_csv_list = getCSVHeaders(csv_path + csv_file)
	device_list_dict = {}
	# Loop through each record
	for i in row_csv_list:
		rownum = 0;
		for h in header_csv_list:
			device_list_dict[h]=i[rownum]
			rownum += 1
		if deployConfig(device_list_dict,username,password,template_file):
			printProgress("INFO",device_list_dict["hostname"],"Successfully deployed config on device.")
		else:
			printProgress("ERROR",device_list_dict["hostname"],"Config deployment failed!")
		print("")

if __name__ == '__main__':
	main()