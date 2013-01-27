import sys
import getopt
import os
from logging_ import logger, logging
from ProbeGenerator_Multi import ProbeGenerator

class CliParser():
  """Class CliParser
	"""
	def __init__(self):
		pass

	def parseArgs(self):
		"""input: parses command line arguments
		possible arguments:
		-f	or	--folder	folderlocation containing the FASTA-files to be processed
		-u	or	--user		needs the username for the database
		-p	or	--password	needs the password for the database
		"""
		try:
			opts, args		= getopt.getopt(sys.argv[1:], 'f:u:p:?v:', ['folder=','user=','password=','help','verbose='])
		except getopt.GetoptError as err:
			print(err)
			sys.exit(2)

		options				= {}

		options['folder']	= None
		options['user']		= None
		options['password']	= None
		options['verbose']	= False

		for o, a in opts:
			if o in ('-?','--help'):
				self.usage()
				sys.exit(0)
			elif o in ('-f', '--folder'):
				options['folder']	= a
			elif o in ('-u','--user'):
				options['user']		= a
			elif o in ('-p','--password'):
				options['password']	= a
			elif o in ('-v','--verbose'):
				options['verbose']	= a

		if not options['user'] or not options['password']:
			print('No or insufficient arguments given.')
			self.usage()
			sys.exit(0)

		return options  

	def usage(self):
		'''OPTIONS
		-f --folder		folderlocation containing the FASTA-files to be processed
		-u --user		username to connect with MySQL
		-p --password	password to connect with MySQL
		-? --help		shows program and usage information
		-v --verbose	to show verbosity information in the terminal (optional)
						MIN;	only info messages
						ALL;	extended verbosity (debug)
		'''
		print(ProbeGenerator.__str__(self))
		print(self.usage.__doc__)

def main():
	cli		= CliParser()
	options = cli.parseArgs()
	_logger = logger
	if options['verbose']:
		if options['verbose'] == "ALL":
			_logger.setLevel(logging.DEBUG)		# level: 10
		elif options['verbose'] == "MIN":
			_logger.setLevel(logging.INFO)		# level: 20
	else:
		_logger.setLevel(logging.WARNING)		# level: 30

	if options['folder'] and os.path.exists(options['folder']):
		fileList= os.listdir(options['folder'])
		probe	= ProbeGenerator(fileList, options['folder'], options['user'], options['password'], _logger)
	elif not options['folder']:
		_logger.error("No folder given.")
		print(cli.usage.__doc__)
	else:
		_logger.error("Folder doesn't exists.")

if __name__ == '__main__':
	main()
