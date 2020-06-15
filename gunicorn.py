import os

self_path = os.path.dirname(os.path.realpath(__file__))

bind       = '127.0.0.1:60000'
# Usually 2-4 x $(NUM_CORES)
workers    = 4
user       = 'videostore'
proc_name  = 'videostore'
pythonpath = self_path
