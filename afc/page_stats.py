import getpass, docopt, logging, sys, time
help_and_opts = """
Gathers statistics about pages soon after their creation. 

Usage:
  productive_new_editors <start_date> <end_date> [-n=<edits>] [-t=<days>] 
      [--defaults-file=<path>] [-h=<host>] [-u=<name>] [-d=<name>]
      [--debug] 
  productive_new_editors --version
  productive_new_editors (-h | --help)

Options:
  --version               Show version
  (-h | --help)           Show help
  <start_date>            The minimum user_registration to include
  <end_date>              The maximum user_registration to include
  -n=<edits>              The number of productive edits required to be considered productive [default: 1]
  -t=<days>               The number of days since registration to look for productive edits [default: 1]
  --defaults-file=<path>  The default config file for connecting to mysql.
  -h | --host=<host>      The mysql host to connect to [default: s1-analytics-slave.eqiad.wmnet]
  -u | --user=<name>      The mysql username to connect with [default: {user}]
  -d | --db=<name>        The mysql database to connect to [default: enwiki]
  --debug                 Show debugging info?

""".format(user=getpass.getuser())
__doc__ = help_and_opts

from mw import database, Timestamp

from menagerie.formatting import tsv

DAY_SECONDS = 60*60*24 # Number of seconds in a day.  Used a few time to convert
                       # days to seconds. 

logger = logging.getLogger("page_stats")

def main():
	args = docopt.docopt(__doc__, version="0.0.1")

	logging.basicConfig(
		level=logging.DEBUG if args["--debug"] else logging.INFO,
		stream=sys.stderr,
		format='%(asctime)s %(name)-8s %(message)s',
		datefmt='%b-%d %H:%M:%S'
	)

	# Constructing a DB this way is lame, but it's necessary for proper handling
	# of the defaults-file argument. 
	db_kwargs = {
		'user': args['--user'],
		'host': args['--host'],
		'db': args['--db']
	}
	if args['--defaults-file'] != None:
		db_kwargs['read_default_file'] = args['--defaults-file']
	db = database.DB.from_params(**db_kwargs)

	run(
		db, 
		Timestamp(args['<start_date>']), 
		Timestamp(args['<end_date>']),
		int(args['-n']),
		int(args['-t']),
		args["--debug"]
	)
