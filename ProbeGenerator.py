#! usr/bin/python3
# -*- coding: utf-8 -*-

'''
Name:  		ProbeGenerator.py
Purpose:		This class module can be used to create probes using gene sequences provides by multi-FASTA files.
				This is the main class and depends on the following files for further process:
				CliParser.py
				logging_.py
				DatabaseProcessor.py
				Chromosome.py
				Gene.py
				Oligo.py
Author:			Maarten Versluis en Joost Kranendonk
Created:		05/11/2012
Copyright:		(c) Derp
Version:		1.0b
'''

from DatabaseProcessor import DatabaseProcessor
from Chromosome import Chromosome
from ProgressBar import ProgressBar

class ProbeGenerator():
	"""Class ProbeGenerator
	"""
	def __init__(self, files, folderPath, user, password, logger):
		global _DB
		global _logger
		_logger					= logger

		_logger.info("Currently in class {}.".format(__class__.__name__))
		self.folderPath			= folderPath
		_DB						= DatabaseProcessor(user, password, _logger, drop=True)

		self.chromosomeNumber	= 0
		self.oligosNumber		= 0
		self.genesNumber		= 0

		self.processFiles(files, self.folderPath)

		
	def processFiles(self, files, folderPath):
		"""function processFiles
		
		returns []
		"""
		if _logger.getEffectiveLevel() == 30:
			import os
			sumSize			= 0
			for file in files:
				sumSize		+= os.path.getsize(folderPath+file)
			bar				= ProgressBar(sumSize)
		else:
			bar				= False

		#Creating MULTI FASTA file, with all genens
		import os
		fastaFile = open(os.path.expanduser("~/Documents/th6_MaartenJoost_multi.fasta"), 'w')

		# evt [http://docs.python.org/2/library/multiprocessing.html]
		for file in sorted(files):
			self.chromosomeNumber	+= 1
			chromosome				 = Chromosome(file, folderPath, _DB, _logger, fastaFile)
			self.oligosNumber		+= chromosome.oligosNumber
			self.genesNumber		+= chromosome.genesNum
			del(chromosome)
			if bar: bar.update(os.path.getsize(folderPath+file))

		if bar: del(bar)

	def __str__(self):
		return __doc__

	def __del__(self):
		_logger.info("Processed {} oligos in {} genes in {} chromosomes.".format(self.oligosNumber, self.genesNumber, self.chromosomeNumber))

def main():
	print("This is a subclass. Please open CliParser.py instead.")

if __name__ == '__main__':
	main()
