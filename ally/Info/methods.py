from ..Api import Endpoint, RequestType



class Clock ( Endpoint ):
	_type		= RequestType.Info
	_resource	= 'market/clock.json'



class Status ( Endpoint ):
	_type		= RequestType.Info
	_resource	= 'utility/status.json'






	
def clock ( *args, **kwargs ):
	return Clock().request()

def status ( *args, **kwargs ):
	return Status().request()
