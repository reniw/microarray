"""Gebruikersklaar script om een eenvoudige ProgressBar te maken en te onderhouden.
Gebruik:  
	bar = ProgressBar(<totaal aantal stappen>)
	bar.update()
OF	bar.update(<aantal stappen>)
"""

import sys

class ProgressBar:
	def __init__(self, steps):
		width		= self.getTerminalSize() - 10
		self.width	= width
		self.aStep	= width / steps
		self.steps	= steps
		self.step	= 0
		self.x		= 0
		sys.stdout.write("[{}]".format(" " * width))
		sys.stdout.flush()
		sys.stdout.write("\b" * (width+1))

	def getTerminalSize(self):
		"""This function tries to get the console length"""
		def ioctl_GWINSZ(fd):
			try:
				import fcntl, termios, struct, os
				cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,'1234'))
			except:
				return
			return cr

		cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
		return int(cr[1])

	def update(self, steps=1):
		self.step  += steps
		length		= round(self.step / self.steps * self.width)
		do			= length - self.x
		self.x		= length

		sys.stdout.write("-" * do)
		sys.stdout.flush()

	def __del__(self):
		sys.stdout.write("\n")

def main():
	import time
	bar = ProgressBar(33)
	for x in range(30):
		time.sleep(0.05)
		bar.update()

if __name__ == '__main__':
	main()
