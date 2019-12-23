#################################################
"""            FIXML                """
#################################################
import xml.etree.cElementTree as ET
import xml.dom.minidom
import dicttoxml
from . import order

def getAttributes(tag):
    """Convert non-nested key/vals in dict into dict on their own
    """
    return dict([(k,v) for k,v in tag.items() if
            type(v) == type("")
            and '__' not in k 
    ])




def FIXML(order):
    """Turn order object into http request body in XML
    """
    root = ET.Element(
        'FIXML',
        attrib={'xmlns':"http://www.fixprotocol.org/FIXML-5-0-SP2"}
    )

    print(order)
    
    o_attrib   = getAttributes(order['Order'])
    qty_attrib = getAttributes(order['Order']['OrdQty'])
    inst_attrib   = getAttributes(order['Order']['Instrmt'])

    o        = ET.SubElement(root,'Order', attrib=o_attrib )
    instrmt  = ET.SubElement(o,'Instrmt',attrib=inst_attrib)
    qty      = ET.SubElement(o,'OrdQty', attrib=qty_attrib)


    raw = ET.tostring(root)#.decode('utf-8')

    dom = xml.dom.minidom.parseString(raw)

    return raw
