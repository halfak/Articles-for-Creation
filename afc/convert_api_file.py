import sys

from menagerie.formatting import tsv
from mw import Timestamp

reader = tsv.Reader(sys.stdin)
writer = tsv.Writer(sys.stdout, headers=reader.headers)

for row in reader:
	timestamp = Timestamp(row.timestamp)
	writer.write([
		row.page_id,
		row.page_namespace,
		row.page_title,
		row.rev_id,
		timestamp,
		row.status,
		row.source
	])
