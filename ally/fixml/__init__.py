#################################################
"""            FIXML                """
#################################################
import xml.etree.cElementTree as ET

from .. import order

all=['FIXML']


############################
def pretty_print_POST(req):
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in 
    this function because it is programmed to be pretty 
    printed and may differ from the actual request.
    """
    print('{}\n{}\n{}\n\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))
############################
def FIXML(order, account, test=False):
    
    if test:
#         return '<?xml version="1.0" encoding="UTF-8"?>' +
        return """
<FIXML xmlns="http://www.fixprotocol.org/FIXML-5-0-SP2">
  <Order TmInForce="0" Typ="1" Side="1" Acct="12345678">
    <Instrmt SecTyp="CS" Sym="F"/>
    <OrdQty Qty="1"/>
  </Order>
</FIXML>
        """
    
    TmInForce = {
        'GTC':'1', # GOOD TILL CANCELLED
        'GFD':'0', # GOOD FOR DAY
        'MOC':'7'  # MARKET ON CLOSE
    }
    side = {
        'buy':'1',
        'sell':'2',
        'short':'5',
    }
    if order.price == None:
        typ = '1'
    else:
        typ = '2'
        
    root = ET.Element('FIXML')
    
    o = ET.SubElement(root,'Order')
    
    instrument = ET.SubElement(o,'Instrmt')
    qty = ET.SubElement(o,'OrdQty')
    
    o.attrib['TmInForce'] = TmInForce[order.timespan]
    o.attrib['Side'] = side[order.side]
    o.attrib['Typ'] =  typ
    o.attrib['Acct'] =  str(account)
    
    instrument.attrib['Sym'] = order.sym
    instrument.attrib['SecTyp'] = order.sectype
    qty.attrib['Qty'] = str(order.qty)
    
    root.attrib['xmlns'] = "http://www.fixprotocol.org/FIXML-5-0-SP2"
    
    return ET.tostring(root).decode('utf-8')