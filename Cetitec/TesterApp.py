import sys
import re
import os

class TestError(Exception):
	def __init__(self, message, code, exit = False):    #class for extended exceptions. Added code for writing in the output file and terminating the program        
		super().__init__(message)
		self.code = code
		self.exit = exit

#function for getting the file number and checking file name format

def get_file_num(name):
	match = re.match(r"TestInput(\d{2})\.txt", name)
	if match == None: 
		raise Exception("Invalid file name format!")
	return match[1]

#return a list of input, factor and offset
def read_input(file):
	hex = file.read(8)
	if len(hex) != 8: raise TestError("Value truncated", 0xffffeeee, True)

	try:
		vals = (int(hex[0:4], base=16), int(hex[4:6], base=16), int(hex[6:8], base=16))
		if vals[0] > 0x100: raise TestError("Invalid input value", 0xffff0100)
		if vals[1] <= 0 or vals[1] >= 0xff: raise TestError("Invalid factor value", 0xffffff00)
		return vals
	except ValueError:
		raise TestError("Invalid characters for hex conversion", 0xffffffff, True)
	
#main code written in try block
try:
	#argument from command line
	file_num = get_file_num(sys.argv[1])
	#with block for safety
	with open(sys.argv[1], "r") as tst_input:
		with open("TestOutput"+file_num+".txt", "w") as tst_output:			
			file_size = os.stat(sys.argv[1]).st_size
			while tst_input.tell() < file_size:
				try:
					(inValue, factor, offset) = read_input(tst_input)
					#writing value in output file and padding with 0
					tst_output.write("{:0>4x}".format(inValue * factor + offset))

				except TestError as te:
					#error codes for output file
					tst_output.write("{:0>8x}".format(te.code))
					if te.exit: raise te
			tst_output.write("{:0>8x}".format(0xffff0000))
except Exception as e: 
	print(e)

