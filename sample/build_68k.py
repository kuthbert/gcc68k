#=================================
# 68k Build
#=================================

import sys, os
import re
from format_68k import *

__title__ = "68k Build"
__author = "Hekar Khani"
__version__ = "1.0"
__doc__ = "Simple build system for the 68k"

source_regex = "^.*\.c$"
header_regex = "^.*\.h$"
link_regex = "^.*\.(s)$"

# Directories to add to $PATH
paths = ["E:\\cygwin\\bin", "E:\\cygwin\\usr\\local\\m68k\\bin"]

cc = "m68k-coff-gcc"
inc = "-I."
ccflags = inc + "-mc68000 -ffreestanding -O0 -mshort -S"
objcopy = "m68k-coff-objcopy -O binary"
ld = "locator"
ldflags = ""

s = ' '
srcext = '.c'
asmext = '.s'

asmfinal = "proj.asm"
binfinal = "final_binary"

start_file = "startup.s"
# Code files are any files that aren't in the 
bss_filename = "globals.s"

#=========================================
#=========================================

loc_base = { 'code':0, 'bss':9000 }

def all():
	build()
	link()

def build():
	global paths
	for path in paths:
		os.environ['PATH'] += ";" + path

	files = os.listdir(os.curdir)
	# translates all the files into assembly
	for file in files:
		match = re.match(source_regex, file)
		if match:
			# translate the file into assembly
			command = cc + s + ccflags + s
			command += file
			run(command)
			
			# format the file into "Visual 68k's" assembly
			v68kformat(file.replace(srcext, asmext))

def link():
	global bss_filename
	
	code_contents = "; Created by 68k Build\n"
	code_contents += "\tORG $" + str(loc_base['code']) + "\n"
	
	code_contents += readfile(start_file)
	
	files = os.listdir(os.curdir)
	for file in files:
		match = re.match(link_regex, file)
		if match and file != start_file and file != bss_filename:
			code_contents += readfile(file) + '\n'
	
	bss_contents = "; BSS contents below"
	bss_contents += readfile(bss_filename)
	
	contents = code_contents + bss_contents + '\n\tEND start\n'
	
	f = open(asmfinal, 'w')
	f.write(contents)
	f.close()

def clean():
	files = os.listdir(os.curdir)
	for file in files:
		srcmatch = re.match(source_regex, file)
		if srcmatch:
			os.remove(file.replace(srcext, asmext))
	
def run(comm):
	print(comm)
	os.system(comm)
	
def readfile(filename):
	f = open(filename, 'r')
	
	contents = ""
	for line in f.readlines():
		contents += line
	
	f.close()
	
	return contents
	
def main():
	argv = sys.argv
	argc = len(argv)
	if argc > 1:
		for i in range(1, argc):
			eval(argv[i] + "()")
	else:
		all()
		
main()