import sys, trace

def init():
	global theTracer
	theTracer = \
	     trace.Trace( ignoredirs=sys.path[1:], trace=True, count=False )
