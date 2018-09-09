from collections import namedtuple


__all__=['ResourceMap']

ResourceMap = namedtuple('ResourceMap', 'resource, model, root_search, search_mapping, url_prefixes, chain_map')
