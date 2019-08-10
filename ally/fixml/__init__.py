#################################################
"""            FIXML                """
#################################################
import xml.etree.cElementTree as ET
from .. import order

all=['FIXML']

############################
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

############################
# Format an order according to the FIXML specifications
# https://www.ally.com/api/invest/documentation/fixml/ for more info
def FIXML(order, account):
    
    # Safety first!
    if not order.valid:
        return ""
    
    if order.price == None:
        # Market
        typ = '1'
    else:
        # limit
        typ = '2'
        
    # Create root
    root = ET.Element('FIXML')
    
    o = ET.SubElement(root,'Order')
    
    instrument = ET.SubElement(o,'Instrmt')
    qty = ET.SubElement(o,'OrdQty')
    
    # Add order attributes
    o.attrib['TmInForce'] = TmInForce[order.timespan]
    o.attrib['Side']      = side[order.side]
    o.attrib['Acct']      = str(account)
    o.attrib['Typ']       = typ
    
    # Add instrument attributes
    instrument.attrib['SecTyp'] = order.sectype
    instrument.attrib['Sym']    = order.sym
    
    # Add quantity attributes
    qty.attrib['Qty'] = str(order.qty)
    
    root.attrib['xmlns'] = "http://www.fixprotocol.org/FIXML-5-0-SP2"
    
    # Return string
    return ET.tostring(root).decode('utf-8')