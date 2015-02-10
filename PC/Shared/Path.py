import sys
from os.path import join
sdp_directory = '/group/teaching/sdp/sdp6/'
pygame_directory = join(sdp_directory, 'libraries/lib64/python2.6/site-packages')
pyinotify_directory = join(sdp_directory, 'libraries/lib/python2.6/site-packages')
sys.path.extend([pygame_directory, pyinotify_directory])
