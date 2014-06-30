# -*- coding: utf-8 -*-

import os
import os.path
import datetime
import shutil
import pwd
import re
import sys
from optparse import OptionParser
from config import CONFIG

hosts = CONFIG['hosts']
vhost = CONFIG['vhost']
projectPath = CONFIG['projectPath']
documentRoot = CONFIG['documentRoot']
browser = CONFIG['browser']
os.chdir(os.path.dirname(__file__))

class Project():
	def __init__(self):
		self.domain = ''
		self.path = ''
		self.documentRoot = ''
		self.template = ''

		self.checkConfig()

	def checkConfig(self):
		if not os.path.isdir(projectPath):
			print 'cannot find base project path.'
			exit()
		if not os.path.isdir('/Applications/' + browser):
			print 'cannot find browser path.'
			exit()

	def run(self):
		parser = OptionParser()
		parser.add_option('--mode', dest='mode')

		options, args = parser.parse_args()
		if options.mode == "auto":
			self.generateSubdomain()
		else:
			self.waitInputDomain()
			self.waitInputPath()
			self.waitInputDocumentRoot()
			self.waitInputTemplate()

		self.execute()

	def generateSubdomain(self):
		d = datetime.datetime.today()
		self.domain = d.strftime("%Y%m%d%H%M%S") + ".localhost"
		self.path = self.domain
		self.documentRoot = "public"
		self.template = "plain"

	def waitInputDomain(self):
		input = raw_input("Enter your domain name. (e.g. dev.test.com) [] ")
		errorMsg = self.__checkInputDomain(input)
		if errorMsg:
			print errorMsg
			self.waitInputDomain()
		else:
			self.domain = input

	def __checkInputDomain(self, input):
		errorMsg = ''

		if input == '':
			errorMsg = 'This is required.'

		result = re.search("^[0-9A-Za-z\.\-_]+$", input)
		if errorMsg == '' and result == None:
			errorMsg = 'Illigal formart'

		if errorMsg == '' and os.path.isfile(hosts):
			for line in open(hosts):
				pos = line.find("#")
				if pos >= 0:
					continue

				if line.find(input) >= 0:
					errorMsg = input + ' already exists.'
					break

		if errorMsg:
			return 'error:' + errorMsg
		else:
			return ''

	def waitInputPath(self):
		input = raw_input("Enter the project path following '" + projectPath + "'. (e.g. test) [] ")
		errorMsg = self.__checkInputPath(input)
		if errorMsg:
			print errorMsg
			self.waitInputPath()
		else:
			self.path = input

	def __checkInputPath(self, input):
		errorMsg = ''
		if input == '':
			errorMsg = 'This is required.'
		if os.path.isdir(projectPath + input):
			errorMsg = projectPath + input + ' already exists.'

		if errorMsg:
			return 'error:' + errorMsg
		else:
			return ''

	def waitInputDocumentRoot(self):
		input = raw_input("Enter document root directory following '" + projectPath + self.path + "/'. [public] ")
		input = re.sub(r'/$', "", input)
		if input == '':
			input = documentRoot

		self.documentRoot = input

	def waitInputTemplate(self):
		dirs = []
		path = './default'
		for item in os.listdir(path):
			if os.path.isdir(os.path.join(path,item)):
				dirs.append(item)

		template = "/".join(dirs)
		input = raw_input("Choose a template from '" +  template + "'. [] ")
		self.template = input

	def execute(self):
		confirm = "\n---------------------------\n"
		confirm += 'Domain: ' + self.domain + "\n"
		confirm += 'Project Path: ' + projectPath + self.path + "\n"
		confirm += 'Document Root: ' + projectPath + self.path + '/' + self.documentRoot + "\n"
		confirm += 'htaccess: ' + vhost + "\n"
		confirm += 'Template: ' + self.template + "\n"
		confirm += "---------------------------\n"

		input = raw_input(confirm + "\nAre you sure these configurations are all correct?(Y/n) [n] ")
		if input == 'Y':
			self.d = datetime.datetime.today()
			self.writeHosts()
			self.writeHtaccess()
			self.reloadApache()
			self.makeDirectory()
			self.done()
		else:
			self.waitInputDomain()

	def writeHosts(self):
		str = '# created at ' + self.d.strftime('%Y-%m-%d %H:%M:%S') + "\n"
		str += '127.0.0.1    ' + self.domain + "\n"
		os.system('sudo sh -c \'echo "' + str + '" >> ' + hosts + '\'')

	def writeHtaccess(self):
		str = '# created at ' + self.d.strftime('%Y-%m-%d %H:%M:%S') + "\n"
		str += '<VirtualHost *:80>' + "\n"
		str += 'DocumentRoot "' + projectPath + self.path + '/' + self.documentRoot + '"' + "\n"
		str += 'ServerName ' + self.domain + "\n"
		str += '</VirtualHost>' + "\n"

		os.system('sudo sh -c \'echo "' + str + '" >> ' + vhost + '\'')

	def makeDirectory(self):
		documentroot = projectPath + self.path + '/' + self.documentRoot
		template = './default/' + self.template

		if self.template:
			shutil.copytree(template, documentroot)
		else:
			os.makedirs(projectPath + self.path + '/' + self.documentRoot)


	def reloadApache(self):
		os.system('sudo apachectl restart')

	def done(self):
		print "your project successfully generated.\n"
		os.system('/usr/bin/open -a "/Applications/' + browser + '" \'http://' + self.domain + '\'')
		os.system('/usr/bin/open ' + projectPath + self.path)

try:
	if __name__ == '__main__' :
		p = Project()
		p.run()
except KeyboardInterrupt:
	pass


