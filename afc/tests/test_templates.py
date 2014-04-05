from nose.tools import eq_

from .. import templates

def test_talk_extraction():
	wikitext = """
{{WikiProject Biography|living=yes|class=B|listas=Lidow}}
{{WikiProject Articles for creation|class=B|ts=20140405064935|reviewer=TheIrishWarden}}
{{WikiProject Business|class=B}}
	"""
	
	eq_("accepted", templates.extract_status(wikitext))

def test_main_extraction():
	wikitext = """
{{AFC submission|t||ts=20140405172941|u=Tfccontractetc|ns=5}} <!--- Important, do not remove this line before article has been created. --->
'''Ahmed El Dani''' (أحمد داني) was born on May 25, 1994 (19 years old) at only 13 years of age he managed to make his way into the Toronto FC Academy. Played for one of the best clubs in the Greater Toronto Area; the Mississauga Falcons, he managed to attract the attention of many. One in particular which took him to the highest position of his time (17 years old), and managed to find a spot on Team Ontario's list. After suffering a knee injury and undergoing surgery, no longer met requirements and became a free non- professional agent. Several months later he caught attention of coach D. and found a spot on his level A roster. 

'''Content of Player Profile'''
	"""
	
	eq_("draft", templates.extract_status(wikitext))

def test_extract_draft():
	wikitext = """
 <!--- Important, do not remove this line before article has been created. --->
'''Ahmed El Dani''' (أحمد داني) was born on May 25, 1994 (19 years old) at only 13 years of age he managed to make his way into the Toronto FC Academy. Played for one of the best clubs in the Greater Toronto Area; the Mississauga Falcons, he managed to attract the attention of many. One in particular which took him to the highest position of his time (17 years old), and managed to find a spot on Team Ontario's list. After suffering a knee injury and undergoing surgery, no longer met requirements and became a free non- professional agent. Several months later he caught attention of coach D. and found a spot on his level A roster. 

'''Content of Player Profile'''
	"""
	
	eq_(
		"draft", 
		templates.extract_status("{{AFC submission|t||ts=20140405172941|u=Tfccontractetc|ns=5}}")
	)
	
	eq_(
		"pending", 
		templates.extract_status("{{AFC submission|||ts=20140405172941|u=Tfccontractetc|ns=5}}")
	)
	
	eq_(
		"reviewing", 
		templates.extract_status("{{AFC submission|r||ts=20140405172941|u=Tfccontractetc|ns=5}}")
	)
	
	eq_(
		"accepted", 
		templates.extract_status("{{AFC submission|a||ts=20140405172941|u=Tfccontractetc|ns=5}}")
	)
	
	eq_(
		"declined", 
		templates.extract_status("{{AFC submission|d||ts=20140405172941|u=Tfccontractetc|ns=5}}")
	)
	
	eq_(
		"unknown", 
		templates.extract_status("{{AFC submission|WTF||ts=20140405172941|u=Tfccontractetc|ns=5}}")
	)

def test_precedence():
	
	eq_(
		"declined", 
		templates.extract_status(
			"{{AFC submission|WTF||ts=20140405172941|u=Tfccontractetc|ns=5}}" +
			"{{AFC submission|D||ts=20140405172941|u=Tfccontractetc|ns=5}}" +
			"{{AFC submission|a||ts=20140405172941|u=Tfccontractetc|ns=5}}"
		)
	)

