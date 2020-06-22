import ally
import json
import time
import concurrent.futures

a = ally.Ally()

# print(h)
def job ():
	print("Submitting job")
	return a.timesales('spy', startdate='2020-06-19', enddate='2020-06-19', block=False)

with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:

	print("Submitting requests")
	# Submit all our orders
	futures = {
		executor.submit(job): i
		for i in range(200)
	}
	print("Submitted!")
	
	print("Getting results...")
	for future in concurrent.futures.as_completed(futures):
		try:
			print(future.result(), "#{}".format(futures[future]))
		except:
			raise
