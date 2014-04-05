"""
Dump extractor -- gathers AfC status changes by processing dump.

Usage:
	dump_extractor <pages> <dump>... [--config=config/main.yaml]
	dump_extractor --version
	dump_extractor (-h | --help)

Options:
	--version      Show version
	(-h | --help)  Show help
	<pages>        Path to a tsv file containing information about pages to process (all other pages will be ignored)
	<dump>         Path to an xml_dump file to process
	--config=PATH  Path to a configuration file
"""
import sys, docopt
from collections import namedtuple

from menagerie.formatting import tsv
from mw import api, xml_dump

from . import templates

HEADERS = [
	"page_id",
	"page_namespace",
	"page_title",
	"rev_id",
	"timestamp",
	"status",
	"source"
]


def main():
	args = docopt.docopt(__doc__, version="0.0.1 test")
	
	reader = tsv.Reader(
		open(args['<pages>']),
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
	
	dump_paths = [xml_dump.file(path) for path in args['<dump>']]
	
	run(page_ids, namespace_titles, dump_paths)


StatusChange = namedtuple("Status", ['status', 'revision', 'source'])
PageInfo = namedtuple("Page", ['id', 'namespace', 'title'])
Revision = namedtuple("Revision", ['id', 'timestamp'])

def run(page_ids, namespace_titles, dump_paths):
	
	def process_dump(dump, path):
		
		for page in dump:
			
			# Try to match the current page to our mappings
			page_info = None
			source = None
			if page.id in page_ids:
				page_info = page_ids[page.id]
				source = "id match"
			elif page.namespace == 1 and (0, page.title) in namespace_titles:
				page_info = namespace_titles[(0, page.title)]
				source = "talk page"
			
			
			if page_info != None:
				current = None
				for revision in page:
					status = templates.extract_status(revision.text)
					
					if current == None or status != current.status:
						new = StatusChange(status, revision, source)
						yield page_info, current, new
						
						current = new
					
				
				if current != None:
					yield current, None
				
		
	
	writer = tsv.Writer(sys.stdout, headers=HEADERS)
	
	for page_info, old, new in xml_dump.map(dump_paths, process_dump):
		
		if new != None:
			writer.write([
				page_info.id,
				page_info.namespace,
				page_info.title,
				new.revision.id,
				new.revision.timestamp,
				new.status,
				new.source
			])


