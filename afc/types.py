from collections import namedtuple

StatusChange = namedtuple("StatusChange", ['status', 'revision'])
PageInfo = namedtuple("PageInfo", ['id', 'namespace', 'title'])
Revision = namedtuple("Revision", ['id', 'timestamp', 'text'])
