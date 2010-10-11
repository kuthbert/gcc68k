#=================================
# 68k Format
#=================================

import re
import copy

__title__ = "68k Format"
__author = "Hekar Khani"
__version__ = "0.9"
__doc__ = "Formats GCC 3.4.2 68k output for Easy68k usage"

author = "student"
remove = ["#NO_APP", 
	"^.*\.(data|even|file|glob|globl|text|section|skip).*$"]

# Reformat an assembly file from GCC's Motorola Syntax 
# into something acceptable by Visual 68K 
def v68kformat(filename):
	i = 0
	
	f = open(filename, 'r')
	filelines = f.readlines()
	f.close()
	
	lines = []
	# Comb through each line
	for line in filelines:
		newline = line
		# check if line that should be deleted completely
		exclude = False
		for remre in remove:
			match = re.match(remre, line)
			if match:
				exclude = True

		if not exclude:
			# Remove optimized jumps
			newline	= newline.replace("__main", "main")
			newline	= newline.replace("muls.l", "muls.w")
			newline	= newline.replace("extb", "ext")
			newline	= newline.replace("link.w", "link")
			newline	= newline.replace("jbra", "bra.l")
			newline	= newline.replace("jbeq", "beq.l")
			newline	= newline.replace("jbge", "bge.l")
			newline	= newline.replace("jbgt", "bgt.l")			
			newline	= newline.replace("jble", "ble.l")
			newline	= newline.replace("jbhi", "bhi.l")
			newline	= newline.replace("jbls", "bls.l")
			newline	= newline.replace("jblt", "blt.l")
			newline	= newline.replace("jbne", "bne.l")
			newline	= newline.replace("jbvs", "bvs.l")
			newline	= newline.replace("jbvc", "bvc.l")
			newline	= newline.replace("jbsr", "bsr.l")
			
			newline	= newline.replace(".byte", "dc.b")
			newline = newline.replace("%", "")
			lines.append(newline)

	
	lines.insert(0, asm68k_fileheader(filename))
	
	f = open(filename, 'w')
	# Write the new file
	for line in lines:
		if line != "":
			f.write(line)
	
	f.close()
	
def asm68k_fileheader(filename):
	global author
	
	header = """\n\n
;=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
; Filename: """ + filename + """
; Author: """ + author + """
;=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
\n\n"""
	
	return header