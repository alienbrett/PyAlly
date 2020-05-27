from ..Api import Endpoint, RequestType



class Clock ( Endpoint ):
	_type		= RequestType.Info
	_resource	= 'market/clock.json'



class Status ( Endpoint ):
	_type		= RequestType.Info
	_resource	= 'utility/status.json'






	
def clock ():
	return Clock.request()

def status ():
	return Status.request()
