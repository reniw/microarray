import pymysql
import sys

class DatabaseProcessor:
  """Class DatabaseProcessor
	Connects to MySQL when an object is created, creates the tables needed for this project and provides a function to insert data to the database.
	"""
	tables		 = ["th6_oligos", "th6_genes"]
	createTables = ["CREATE TABLE IF NOT EXISTS th6_oligos(\
						gene			int			NOT NULL,\
						nt_index		int,\
						melting_t		float,\
						gcperc			float,\
						oligo			char(25)	NOT NULL,\
						FOREIGN KEY(gene) REFERENCES th6_genes,\
						PRIMARY KEY(gene, nt_index));",
					"CREATE TABLE IF NOT EXISTS th6_genes(\
						id				int			auto_increment NOT NULL UNIQUE,\
						sequence		text,\
						extID			text		NOT NULL,\
						PRIMARY KEY(id));" ]
	
	def __init__(self, user, passw, logger, db=None, drop=False):
		"""initialize function
		Connects to MySQL given a username, password and optionaly the database. If the database was not given 
		the capitalized username is used as database. It also creats the needed tables in case they were not present.
		The __DBconn is a private object and holds the MySQL connection.
		user:  (str)
		db:    (str)
		passw: (str)
		"""
		global _DB
		self._logger					= logger

		self._logger.debug("Currently in class {}. Object created by: {}".format(__class__.__name__, sys._getframe(1).f_code.co_name))
		if db == None:
			self.__databaseDB	= user.capitalize()
		else:
			self.__databaseDB	= db
		
		try:
			self.__DBconn = pymysql.connect(host='mysql.bin', port=3306, user=user, passwd=passw, db=self.__databaseDB)
		except pymysql.err.OperationalError as e:
			self._logger.error("Connecting to MySQL has failed. Wrong username ('{}') or password ('{}' ({}))?".format(user, len(passw) * "*", len(passw)))
			self.__DBconn = None
			sys.exit(1)
		else:
			self._logger.info("Successfully connected to MySQL: '{}'".format(self.__databaseDB))


		cursor	= self.__DBconn.cursor()
		if drop:
			self._logger.info("Dropping tables: {}".format(', '.join(DatabaseProcessor.tables)))
			for table in DatabaseProcessor.tables:
				cursor.execute("DROP TABLE IF EXISTS {};".format(table))
		for query in DatabaseProcessor.createTables:
			cursor.execute(query)
		cursor.close()

	def __del__(self):
		"""destroy function
		Closes the connection to MySQL and prints 'MySQL connection closed.'
		"""
		if self.__DBconn:
			self.__DBconn.close()
			self._logger.info('MySQL connection closed.')
		else:
			pass
			self._logger.error('No MySQL connection object found.')

	def insertDatabase(self, table, **kwargs):
		"""function insertDatabase
		Inserts the given data into the given table of the earlier connected database.
		
		table:  Tablename in the used database (str)
		kwargs: columnA='', columnB='', ...
		
		returns the tuple id of the last inserted data.
		"""
		if not table in DatabaseProcessor.tables: 
			try:
				raise LookupError("Tablename not valid: '{}.{}'".format(self.__databaseDB, table))
			except LookupError as e:
				self._logger.error("{}. Use one of the following tables: {}".format(e, ', '.join(DatabaseProcessor.tables)))
				sys.exit(1)

		for key in kwargs:
			kwargs[key] = str(kwargs[key])

		columns	= "`,`".join(kwargs.keys())
		data	= "','".join(kwargs.values())

		self._logger.debug("Writing data to MySQL: '{}.{}.(`{}`)'. Caller: {}.{}".format(self.__databaseDB, table, columns, sys._getframe(1).f_locals['self'].__class__.__name__, sys._getframe(1).f_code.co_name))

		cursor	= self.__DBconn.cursor()
		cursor.execute("INSERT INTO " + table + "(`" + columns + "`) VALUES('" + data + "');")
		cursor.execute("SELECT last_insert_id();")
		dataId	= str(cursor.fetchone()[0])
		cursor.close()
		
		return dataId

def main():
	print("This is a subclass. Please open CliParser.py instead.")
	from logging_ import logger, logging
	logger.setLevel(logging.INFO)

	# _DB	= DatabaseProcessor('', '', logger)
	# print(_DB.insertDatabase('', columnA='', columnB=''))

if __name__ == '__main__':
	main()
