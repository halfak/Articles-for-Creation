"""
Dump extractor -- gathers AfC status changes by processing XML dump files.

Usage:
  dump_extractor <pages> <dump>... [--config=<path>] [--debug]
  dump_extractor --version
  dump_extractor (-h | --help)

Options:
  --version      Show version
  (-h | --help)  Show help
  <pages>        Path to a tsv file containing information about pages to process (all other pages will be ignored)
  <dump>...      Paths to an xml_dump files to process
  --config=PATH  Path to a configuration file
  --debug        Show debugging info?
"""
import sys, docopt, logging

from menagerie.formatting import tsv
from mw import xml_dump
from mw.lib import title

from . import templates
from .types import PageInfo, Revision, StatusChange
from .util import setup_logging

HEADERS = [
	"page_id",
	"page_namespace",
	"page_title",
	"rev_id",
	"timestamp",
	"status",
	"source"
]

logger = logging.getLogger("dump_extractor")

def read_pages(path):
	logger.info("Reading in pages to process...")
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
	namespace_titles = {}
	page_ids = {}
	for row in reader:
		page_info = PageInfo(row.page_id, row.page_namespace, row.page_title)
		namespace_titles[(row.page_namespace, row.page_title)] = page_info
		if row.page_id != None:
			page_ids[row.page_id] = page_info
	
	
	logger.info("Built indexes for {0} pages.".format(len(page_ids)))
	return page_ids, namespace_titles

def main():
	args = docopt.docopt(__doc__, version="0.1.0")
	
	setup_logging(args['--debug'])
	
	dump_paths = [xml_dump.file(path) for path in args['<dump>']]
	
	page_ids, namespace_titles = read_pages(args['<pages>'])
	
	run(page_ids, namespace_titles, dump_paths)

def run(page_ids, namespace_titles, dump_paths):
	
	def process_dump(dump, path):
		
		for page in dump:
			page_title = title.normalize(page.title) # Converts " " to "_"
			
			# Try to match the current page to our mappings
			page_info = None
			source = None
			if page.id in page_ids:
				page_info = page_ids[page.id]
				source = "id match"
			elif (page.namespace, page_title) in namespace_titles:
				page_info = namespace_titles[(page.namespace, page_title)]
				source = "namespace/title match"
			elif page.namespace == 1 and (0, page_title) in namespace_titles:
				page_info = namespace_titles[(0, page_title)]
				source = "talk page"
			
			
			if page_info != None:
				changes = templates.detect_changes(
					Revision(r.id, r.timestamp, r.text or "") for r in page
				)
				
				for current, new in changes:
					yield page_info, current, new, source
				
		
	
	writer = tsv.Writer(sys.stdout, headers=HEADERS)
	
	for page_info, old, new, source in xml_dump.map(dump_paths, process_dump):
		
		if new != None:
			writer.write([
				page_info.id,
				page_info.namespace,
				page_info.title,
				new.revision.id,
				new.revision.timestamp,
				new.status,
				source
			])


