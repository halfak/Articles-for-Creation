import re

from .types import StatusChange

AfC_submission = re.compile(r'\{\{AfC( |_)submission\|([^\|]*)\|', re.I)
AfC_page = re.compile(r'\{\{WikiProject( |_)Articles( |_)for( |_)creation\|', re.I)


STATUS_MAP = {
	"t": (0, "draft"),
	"": (1, "pending"),
	"r": (2, "reviewing"),
	"a": (3, "accepted"),
	"d": (4, "declined")
}

def extract_status(text):
	
	max_status = (-2, None)
	for match in AfC_submission.finditer(text):
		_, symbol = match.groups()
		
		status = STATUS_MAP.get(symbol.lower(), (-1, "unknown"))
		max_status = max(max_status, status)
	
	if AfC_page.search(text):
		max_status = max(max_status, (3, "accepted"))
	
	return max_status[1]

def detect_changes(revisions):
	current = None
	for revision in revisions:
		status = extract_status(revision.text)
		
		if current == None or status != current.status:
			new = StatusChange(status, revision)
			yield current, new
			
			current = new
		
	
	if current != None:
		yield current, None