from logging_ import logger
from BadOligo import BadOligo
import sys

class Oligo:
  """Class Oligo
	Used to process sequences as oligonucleotides and saves validated sequences in the database.
	"""
	def __init__(self, index, sequence, geneID, DB, logger):
		"""function __init__
		
		gene:		Gene() object to retreve its ID for referential integrity between the Gene and its oligonucleotides.
		oligoIndex:	The start nucleotide of the gene sequence.
		"""
		global _DB
		global _logger
		_logger			= logger
		_DB				= DB

		_logger.debug("Currently in class {}.".format(__class__.__name__))
		_logger.debug("Currently processing: {}.'{}'.'{}'".format(__class__.__name__, geneID, index))

		self.sequence					= self.getComplement(sequence)
		self.geneID						= geneID
		self.index						= index

		self.getHairpins()		
		self.getNucleotideRepeats()

		self.cgCount, self.cgPercentage	= self.getCGContent()
		self.meltingTemp				= self.calcMeltingTemperature()

		_logger.debug("{}.'{}'.'{}' passed.".format(__class__.__name__, geneID, index))
		_DB.insertDatabase("th6_oligos", gene=self.geneID, nt_index=index, melting_t=self.meltingTemp, gcperc=self.cgPercentage, oligo=self.sequence)
	
	def getComplement(self, sequence):
		"""function createComplDNA
		Creates a reversed complementairy sequence of a given sequence.
		returns a string.
		"""
		return sequence.translate(str.maketrans('TAGCtagc', 'ATCGATCG'))[::-1]
	
	def getCGContent(self):
		"""function calcCGCount
		Calculates the absolute and relative C and G content of the complementairy oligo sequence.
		returns list containing an integer (absolute) and a rounded float (percentage) of this C/G content.
		"""
		cgCount	= self.sequence.count('C') + self.sequence.count('G')
		cgPerc	= round(cgCount / len(self.sequence), 2)
		return [cgCount, cgPerc]
	
	def calcMeltingTemperature(self):
		# http://www.basic.northwestern.edu/biotools/oligocalc.html
		"""function calcMeltingTemperature
		Calculates the melting point (Tm) of the complementairy oligo sequence.
		returns a float (temperature) of melting point.
		"""	
		return round(64.9 + 41 * (self.cgCount - 16.4) / len(self.sequence), 2)
	
	def getHairpins(self):
		"""function calcHairpins
		Calculates the change that a the oligo will form a hairpin.
		returns a float
		"""
		import re
		for i in range(len(self.sequence) - 4):
			pattern = '[ACGT]*?' + self.sequence[i:i+5] + '[ACGT]{3,8}' + self.getComplement(self.sequence[i:i+5]) + '[ACGT]*?'
			
			if re.search(pattern, self.sequence):
				raise BadOligo("{}.'{}'.'{}' constructs a hairpin and will be discarded.".format(__class__.__name__, self.geneID, self.index))
		else:
			return False
	
	def getNucleotideRepeats(self):
		"""function getNucleotideRepeats
		Calculates the presents of nucleotide repeats (AAAA, CCCC, TTTT or GGGG) and Simple Sequence Repeats.
		returns a boolean
		"""
		nucs	= ['A', 'C', 'T', 'G']
		for nt1 in nucs:
			if (nt1 * 4) in self.sequence:
				raise BadOligo("{}.'{}'.'{}' contains mononucleotide repeats and will be discarded.".format(__class__.__name__, self.geneID, self.index))
			for nt2 in nucs:
				if (3 * (nt1+nt2)) in self.sequence:
					raise BadOligo("{}.'{}'.'{}' contains dinucleotide repeats and will be discarded.".format(__class__.__name__, self.geneID, self.index))
		else:
			return False

def main():
	print("This is a subclass. Please open CliParser.py instead.")
	# from DatabaseProcessor import DatabaseProcessor
	# from logging_ import logger, logging
	# logger.setLevel(logging.INFO)

	# DB		= DatabaseProcessor('', '', logger, drop=False)
	# oligo	= Oligo(88, 'GTGGTGGCCCAATAGGTGGCCCAAA', '8', DB, logger)
		
if __name__ == '__main__':
	main()
