#################################################
"""			FIXML				"""
#################################################
import pyximport; pyximport.install()
import xml.etree.cElementTree as ET
import xml.dom.minidom
# This prevents collisions
from . import order as order_utils

def getAttributes(tag):
	"""Convert non-nested key/vals in dict into dict on their own
	"""
	return dict([(k,v) for k,v in tag.items() if
			type(v) == type("")
			and '__' not in k 
	])




def FIXML(orderd,verbose=False):
	"""Turn order object into http request body in XML
	"""
	root = ET.Element(
		'FIXML',
		attrib={'xmlns':"http://www.fixprotocol.org/FIXML-5-0-SP2"}
	)

	if verbose:
		print(orderd)

	ordReqT	 = order_utils.orderReqType(orderd)
	
	o_attrib	= getAttributes( orderd[ordReqT] )
	qty_attrib  = getAttributes( orderd[ordReqT]['OrdQty'] )
	inst_attrib = getAttributes( orderd[ordReqT]['Instrmt'] )

	o		= ET.SubElement( root, ordReqT, attrib=o_attrib )
	instrmt  = ET.SubElement( o,  'Instrmt', attrib=inst_attrib )
	qty	  = ET.SubElement( o,  'OrdQty', attrib=qty_attrib )


	raw = ET.tostring( root )

	# dom = xml.dom.minidom.parseString(raw)

	return raw
