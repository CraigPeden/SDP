import cv2
import tools




class Camera(object):
    """
    Camera access wrapper.
    """

    def __init__(self, port=0, pitch=0):
        self.capture = cv2.VideoCapture(port)
        calibration = tools.get_croppings(pitch=pitch)
        self.crop_values = tools.find_extremes(calibration['outline'])

        # Parameters used to fix radial distortion
        radial_data = tools.get_radial_data()
        self.nc_matrix = radial_data['new_camera_matrix']
        self.c_matrix = radial_data['camera_matrix']
        self.dist = radial_data['dist']

    def get_frame(self):
        """
        Retrieve a frame from the camera.
        Returns the frame if available, otherwise returns None.
        """
        # status, frame = True, cv2.imread('img/i_all/00000003.jpg')
        status, frame = self.capture.read()
        frame = self.fix_radial_distortion(frame)
        if status:
            return frame[
                self.crop_values[2]:self.crop_values[3],
                self.crop_values[0]:self.crop_values[1]
            ]

    def fix_radial_distortion(self, frame):
        return cv2.undistort(
            frame, self.c_matrix, self.dist, None, self.nc_matrix)

    def get_adjusted_center(self, frame):
        return (320-self.crop_values[0], 240-self.crop_values[2])
