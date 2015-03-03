import cv2
import numpy
from vision import tools

class Preprocessing(object):

	def __init__(self, options=None):
		if not options:
			# Which methods to run
			self.options = {
				'normalize': False,
				'background_sub': False
			}

		# Default setting for background subtractor
		self.background_sub = None

	def get_options(self):
		return self.options;

	def run(self, frame, pitch, options):

		self.options = options

		results = {
			'frame': frame
		}

		# Apply normalization
		if self.options['normalize']:
			# Normalize only the saturation channel
			results['frame'] = self.normalize(frame, pitch)
			# print 'Normalizing frame'

		# Apply background subtraction
		if self.options['background_sub']:
			frame = cv2.blur(frame, (2,2))
			# print 'running sub'
			if self.background_sub is not None:
				bg_mask = self.background_sub.apply(frame)
			else:
				self.background_sub = cv2.BackgroundSubtractorMOG2(0, 30, False)
				bg_mask = self.background_sub.apply(frame)
			results['background_sub'] = bg_mask

		return results

	def normalize(self, frame, pitch=0):
		width = frame.shape[1]
		height = frame.shape[0]
		zones = tools.get_zones(width, height, pitch=pitch)
		mids = [((zones[i][0] + zones[i][1]) / 2) for i in range(0, 4)]
		s_low = [frame[3*height/4, x_co] for x_co in mids]
		s_high = [frame[height/4, x_co] for x_co in mids]
		avg = [sum(i) / (len(i)) for i in zip(*(s_low + s_high))]

		for i in range(0, len(zones)):
			for j in range(0,3):
				frame[0:height/2, zones[i][0]:zones[i][1] ] += (s_high[i] - avg)
				frame[height/2:height, zones[i][0]:zones[i][1] ] += (s_low[i] - avg)

		return frame