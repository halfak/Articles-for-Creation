"""
API extractor -- gathers AfC status changes by querying the API.  

Usage:
  api_extractor <pages> [<completed>] [--api=<uri>] [--config=<path>] [--debug]
  api_extractor --version
  api_extractor (-h | --help)

Options:
  --version           Show version
  (-h | --help)       Show help
  <pages>             Path to a tsv file containing information about pages to process
  <completed>         Path to a file containing pre-processed page changes.
  --api=<uri>         The uri for some mediawiki api [default: https://en.wikipedia.org/w/api.php].
  --config=<path>     Path to a configuration file [default: config/main.yaml].
  --debug             Show debugging information
"""
import sys, docopt, logging, getpass

from menagerie.formatting import tsv
from mw import api, Timestamp
from mw.lib import title

from . import templates
from .types import PageInfo, Revision, StatusChange
from .util import setup_logging

logging.getLogger("requests").setLevel(logging.WARNING)

HEADERS = [
	"page_id",
	"page_namespace",
	"page_title",
	"rev_id",
	"timestamp",
	"status",
	"source"
]

logger = logging.getLogger("api_extractor")

def read_completed(path):
	logger.debug("Reading completed page status changes...")
	reader = tsv.Reader(
		open(path),
		types = [
			int, # page_id
			int, # page_namespace
			str, # page_title
			int, # rev_id
			str, # timestamp
			str, # status
			str  # source
		]
	)
	completed_ids = set()
	for row in reader:
		completed_ids.add(row.page_id)
	
	logger.debug("Built an index over {0} completed pages.".format(len(completed_ids)))
	return completed_ids

def read_pages(path):
	logger.debug("Reading in pages to process...")
	reader = tsv.Reader(
		open(path),
		types = [
			int, # page_id
			int, # page_namespace
			str, # page_title
			int, # archived
			str  # identified_by
		]
	)
	pages = set()
	for row in reader:
		page_info = PageInfo(row.page_id, row.page_namespace, row.page_title)
		pages.add(page_info)
	
	logger.debug("Built indexes for {0} pages.".format(len(pages)))
	return pages

def main():
	
	args = docopt.docopt(__doc__, version="0.0.1")
	setup_logging(args['--debug'])
	
	pages = read_pages(args['<pages>'])
	completed_ids = read_completed(args['<completed>'])
	
	remaining_pages = [page for page in pages if page.id not in completed_ids]
	logger.debug("Processing {0} remaining pages.".format(len(remaining_pages)))
	
	run(remaining_pages, args['--api'], args['--debug'])


def run(pages, api_uri, debug):
	session = api.Session(api_uri)
	
	sys.stderr.write("Log into the API at [{0}]:\n".format(api_uri))
	sys.stderr.write("Username: ")
	username = input("")
	password = getpass.getpass("Password: ", stream=sys.stderr)
	
	session.login(
		username=username,
		password=password
	)
	logger.info("Successfully logged in.")
	
	title_parser = title.Parser.from_api(session)
	
	writer = tsv.Writer(sys.stdout, headers=HEADERS)
	
	logger.debug("Processing pages.")
	for page in pages:
		
		try:
			ns = title_parser.get_namespace(page.namespace)
		except KeyError:
			logger.error("Could not locate namespace {0}.  Skipping {1}.".format(page.namespace, page.title))
			continue
		
		page_name = ns.name + ":" + page.title
		logger.debug("Processing {0}:".format(page_name))
		
		revs = session.deleted_revs.query(
			titles={page_name}, 
			direction="newer",
			properties=['revid', 'content']
		)
		revisions = (Revision(r['revid'], Timestamp(r['timestamp']), r.get('*', '')) for r in revs)
		
		changes = templates.detect_changes(revisions)
		
		for old, new in changes:
			if debug: sys.stderr.write(".")
			if new != None:
				writer.write([
					page.id,
					page.namespace,
					page.title,
					new.revision.id,
					new.revision.timestamp,
					new.status,
					"api (archived)"
				])
		
		if debug: sys.stderr.write("\n")
		
