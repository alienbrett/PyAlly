
def _dot_flatten ( d ):
	"""Flatten a dict into a.b.c. ... for
	{
		a: {
			b: {
				c: {
					...
				}
			}
		}
	}

	This method preserves the data grouping in a way,
		and is usually reversible
	"""
	result = {}
	
	for k,v in d.items():
		
		# append k.z for z in valttened
		if type(v) == type({}):
			v = _dot_flatten ( v )
			for vk,vv in v.items():
				result['.'.join([k,vk])] = vv
		
		else:
			result[k] = v

	return result
