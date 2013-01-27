from Gene import Gene

class Chromosome():
  """Class Chromosome
	"""
	# Attributes:
	fileContent = None  # (str) 
	geneDict = None  # ({}) 
	id = None  # (int) 
			
	# Operations
	def __init__(self, filePath, folderPath, DB, logger, fastaFile):
		"""function __init__
		
		filePath: 

		
		returns 
		"""
		global _DB
		global _logger
		_logger				= logger
		_DB					= DB

		_logger.debug("Currently in class {}.".format(__class__.__name__))
		self.folderPath		= folderPath
		self.filePath		= filePath
		self.chromosoom		= self.filePath.split("|")[0]
		_logger.info("Currently processing: {}.'{}'".format(__class__.__name__, self.chromosoom))

		genes				= self.getGenes(self.filePath, self.folderPath)

		self.genesNum		= 0
		self.oligosNumber	= 0
		for k,v in sorted(genes.items()):
			gene			= Gene(k, v, self.chromosoom, _DB, _logger, fastaFile)
			self.oligosNumber += gene.oligosNumber
			self.genesNum	+= 1
			del(gene)

		_logger.info("Processed {} oligos in {} genes of {}.'{}'.".format(self.oligosNumber, self.genesNum, __class__.__name__, self.chromosoom))
			
	def getGenes(self,filePath,folderPath):
		"""function getGenes
		
		returns a dictionary with the header as key and as value the sequence
		"""
		sequenceFile	= open(folderPath+'/'+filePath, 'r')
		sequenceDict	= {}
		for line in sequenceFile:
			if '>' in line:
				sequenceKey = line.rstrip()
				
				sequenceValue = ''
			elif line == '\n':
				sequenceDict[sequenceKey] = sequenceValue
			else:
				sequenceValue += line.rstrip()
				sequenceDict[sequenceKey] = sequenceValue

		return sequenceDict

def main():
    print("This is a subclass. Please open CliParser.py instead.")

if __name__ == '__main__':
	main()
