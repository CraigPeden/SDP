import cv2
import numpy as np
from vision import tools
import json
import os




class Preprocessing(object):
	def __init__(self, options=None):
		self.path = os.path.dirname(os.path.realpath(__file__))
		self.global_calibration = self.get_json_calibration()
		if self.global_calibration == -1:
			print 'dddd'

		if not options:
			# Which methods to run
			self.options = {
				'normalize': False,
				'background_sub': False,
				'calibrate': False
			}

		# Default setting for background subtractor
		self.background_sub = None

	def get_options(self):
		return self.options

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
			frame = cv2.blur(frame, (2, 2))
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
		y_points = [4.8 * height / 6, 3 * height / 6,  1.2 * height / 6]
		bounds = np.array([[zones[i][0], zones[i][1], 2 * height/3, height] for i in range(0, 4)])
		bounds = np.append(bounds, np.array([[zones[i][0], zones[i][1], height / 3, 2 * height / 3] for i in range(0, 4)]), axis=0)
		bounds = np.append(bounds, np.array([[zones[i][0], zones[i][1], 0, height / 3 ] for i in range(0, 4)]), axis=0)

		if self.options['calibrate']:

			mids = np.array([((zones[i][0] + zones[i][1]) / 2) for i in range(0, 4)])
			sectors = np.array([[x_co, y_co] for y_co in y_points for x_co in mids ])
			sectors_values = np.array([self.get_avg(frame, 5, sec[0], sec[1]) for sec in sectors])

			calibration = {}
			avg_overall = np.mean([[self.get_avg(frame, 8, x_co, y_co)] for x_co in mids for y_co in y_points], axis=0)
			calibration['avg'] = avg_overall[0].tolist()
			calibration['sectors'] = sectors.tolist()
			calibration['sectors_values'] = sectors_values.tolist()
			self.write_json_avg(calibration, pitch)
		else:
			calibration_get = self.get_json_calibration(pitch)
			sectors = np.array(calibration_get['sectors'])
			sectors_values = np.array(calibration_get['sectors_values'])
			avg_overall = np.array(calibration_get['avg'])

		for i in range(0, len(sectors)):
			frame[bounds[i][2]:bounds[i][3], bounds[i][0]:bounds[i][1]] -= (sectors_values[i] - avg_overall)

		return frame

	def get_avg(self, frame, radius, xin, yin):
		rad = np.array( [[yin + i, xin + j] for i in range(-radius, radius) for j in range(-radius,radius)])
		a = np.mean(np.array([frame[rid[0], rid[1]] for rid in rad]), axis=0)
		return a

	def get_json_calibration(self, pitch=0, filename='/avg.json'):
		try:
			calibration = tools.get_json(self.path + filename)
			if pitch == 0:
				return calibration['pitch_0']
			else:
				return calibration['pitch_1']
		except:
			return -1


	def write_json_avg(self, avg, pitch=0, filename='/avg.json',):
		calibration = {}
		if (pitch == 0):
			calibration['pitch_0'] = avg
			if self.get_json_calibration(1) == -1:
				calibration['pitch_1'] = avg
			else:
				calibration['pitch_1'] = self.get_json_calibration(1)
		else:
			calibration['pitch_1'] = avg
			if self.get_json_calibration(0) == -1:
				calibration['pitch_0'] = avg
			else:
				calibration['pitch_0'] = self.get_json_calibration(0)
		tools.write_json(self.path + filename, calibration)
		return 0