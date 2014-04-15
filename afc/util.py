import logging, sys

def setup_logging(debug=False):
	logging.basicConfig(
		level=logging.DEBUG if debug else logging.INFO,
		stream=sys.stderr,
		format='%(asctime)s %(name)-8s %(message)s',
		datefmt='%b-%d %H:%M:%S'
	)

