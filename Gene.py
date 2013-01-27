from Oligo import Oligo
from ProgressBar import ProgressBar
from BadOligo import BadOligo

class Gene:
  validNucs	= {'A', 'C', 'T', 'G'}
	"""Class Gene
	Used to process dictionary items as genes and saves its external identifier in the database.
	"""
	def __init__(self, header, sequence, chromosomeNumber, DB, logger, fastaFile):
		"""function __init__
		
		sequence: str
		extID: str
		
		returns 
		"""
		global _DB
		global _logger
		_logger				= logger
		_DB					= DB

		_logger.debug("Currently in class {}.".format(__class__.__name__))

		self.extID			= self.getExtID(header)
		_logger.debug("Currently processing: {} {}.'{}'".format(chromosomeNumber, __class__.__name__, self.extID))

		try:
			self.validateSequence(sequence)
		except ValueError as e:
			_logger.error(e)
			exit(2)
		
		self.dbID			= DB.insertDatabase("th6_genes", extID=self.extID, sequence=sequence)
		_logger.debug("Protein ID = {}".format(self.dbID))

		# Schrijven gen in fastaformaat naar multifastafile.
		# fastaFile.write( self.toFasta( sequence, 150 ) )

		# Slaat alleen sequentie op, geen oligo's.
		# return None

		# if _logger.getEffectiveLevel() == 20:
		# 	bar				= ProgressBar(len(sequence)-25)
		# else:
		# 	bar				= False
		bar				= False

		self.oligosNumber	= 0
		for k, v in self.createOligos(self.sequence).items():
			try:
				Oligo(k, v, self.dbID, _DB, _logger)
			except BadOligo as e:
				_logger.debug(e)
			else:
				self.oligosNumber += 1
			finally:
				if bar: bar.update()

		if bar: del(bar)

		_logger.debug("Processed {} oligos of {}.'{}'".format(self.oligosNumber, __class__.__name__, self.extID))

	
	def getExtID(self, header):
		"""function getExtID:
		Splitting the header for the external ID (Genebank identifier).
		
		returns extID
		"""
		splitHeader	= header.split('[protein_id=')
		splitGene	= splitHeader[1].split(']')[0]
		
		return splitGene

	def createOligos(self, dnaSequence):
		"""function:
		Makes oligos from the DNA sequence
		
		returns oligos
		"""
		oligoDict = {}
		for i in range(0,len(dnaSequence)-25):
			oligoDict[i] = dnaSequence[i:25+i]

		return oligoDict

	def validateSequence(self, sequence):
		for nt in set(sequence):
			if not nt in Gene.validNucs:
				raise ValueError("'{}' is not a valid nucleotide.".format(nt))
		else:
			self.sequence	= sequence

	def toFasta(self, sequence, width):
		aaFasta = list(sequence)
		for i in range(0, len(sequence), width+1):
			aaFasta.insert(i, "\n")
		return ">th6_MaartenJoost|{}{}\n\n".format(self.extID, "".join(aaFasta))


def main():
	print("This is a subclass. Please open CliParser.py instead.")
	# from DatabaseProcessor import DatabaseProcessor
	# from logging_ import logger, logging
	# logger.setLevel(logging.INFO)

	# header	= '>lcl|NC_004329.2_cdsid_XP_001349514.1 [gene=VAR] [protein=CDS] [protein_id=XP_001349514.1] [location=join(22369..27372,28303..29661)]'
	# sequence= 'GTTGAATACTGATGTTTCTATTCAAATACATATGGATAATCCTAAACCTATAAATCAATTTAATAATATG'

	# DB		= DatabaseProcessor('', '', logger)
	# gene	= Gene(header, sequence, DB, logger)


if __name__ == '__main__':
	main()
