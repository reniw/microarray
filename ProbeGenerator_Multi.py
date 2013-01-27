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
import os

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
		del(_DB)

		self.chromosomeNumber	= 0
		self.oligosNumber		= 0
		self.genesNumber		= 0

		self.processFiles(files, self.folderPath, user, password)


	def processFiles(self, files, folderPath, user, password):
		"""function processFiles
		
		returns []
		"""
		if _logger.getEffectiveLevel() == 30:
			
			sumSize			= 0
			for file in files:
				sumSize		+= os.path.getsize(folderPath+file)
			bar				= ProgressBar(sumSize)
		else:
			bar				= False

		#Creating MULTI FASTA file, with all genens
		# fastaFile = open(os.path.expanduser("~/Documents/th6_MaartenJoost_multi.fasta"), 'w')
		fastaFile = None

		# http://docs.python.org/2/library/multiprocessing.html
		from multiprocessing import Process, Queue, Pipe
		def doChromosome(q, folderPath, _logger, bar, fastaFile, user, password, pipeB):
			"""Thread function. Is executed per Thread.
			"""
			_DB							 = DatabaseProcessor(user, password, _logger)

			while not q.empty():
				file					 = q.get()
				chromosome				 = Chromosome(file, folderPath, _DB, _logger, fastaFile)
				pipeB.send({'chromosomeNumber': 1, 
								'oligosNumber': chromosome.oligosNumber, 
								 'genesNumber': chromosome.genesNum})

				del(chromosome)
				if bar: bar.update(os.path.getsize(folderPath+file))

			pipeB.send({'quit': 1})
			del(_DB)

		q = Queue()

		pipeA, pipeB = Pipe()

		for file in sorted(files):
			q.put(file)

		processNumber = 8
		processList = []

		for i in range(processNumber):
			processList.append(Process(target=doChromosome, args=(q, folderPath, _logger, bar, fastaFile, user, password, pipeB)))
		
		for p in processList:
			p.start()


		for p in processList:
			p.join()
		else:
			if bar: del(bar)

		while (True):
			for k, v in pipeA.recv().items():
				if k == "quit":
					processNumber -= v
				elif k == "chromosomeNumber":
					self.chromosomeNumber	+= v
				elif k == "oligosNumber":
					self.oligosNumber		+= v
				elif k == "genesNumber":
					self.genesNumber		+= v
				if processNumber == 0:
					break

	def __str__(self):
		return __doc__

	def __del__(self):
		_logger.info("Processed {} oligos in {} genes in {} chromosomes.".format(self.oligosNumber, self.genesNumber, self.chromosomeNumber))

def main():
	print("This is a subclass. Please open CliParser.py instead.")

if __name__ == '__main__':
	main()
