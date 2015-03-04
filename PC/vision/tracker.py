import cv2
import numpy as np
from collections import namedtuple
import warnings

# Turning on KMEANS fitting:
KMEANS = False

# Turn off warnings for PolynomialFit
warnings.simplefilter('ignore', np.RankWarning)
warnings.simplefilter('ignore', RuntimeWarning)

BoundingBox = namedtuple('BoundingBox', 'x y width height')
Center = namedtuple('Center', 'x y')


class Tracker(object):
    def get_contours(self, frame, adjustments):
        """
        Adjust the given frame based on 'min', 'max', 'contrast' and 'blur'
        keys in adjustments dictionary.
        """
        try:
            if frame is None:
                return None
            if adjustments['blur'] > 1:
                frame = cv2.blur(frame, (adjustments['blur'], adjustments['blur']))

            if adjustments['contrast'] > 1.0:
                frame = cv2.add(frame, np.array([float(adjustments['contrast'])]))

            # Convert frame to HSV
            frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # Create a mask
            frame_mask = cv2.inRange(frame_hsv, adjustments['min'], adjustments['max'])

            # Apply threshold to the masked image, no idea what the values mean
            return_val, threshold = cv2.threshold(frame_mask, 127, 255, 0)

            # Find contours
            contours, hierarchy = cv2.findContours(
                threshold,
                cv2.RETR_TREE,
                cv2.CHAIN_APPROX_SIMPLE
            )
            # print contours
            return contours
        except:
            return None

    # TODO: Used by Ball tracker - REFACTOR
    def preprocess(self, frame, crop, min_color, max_color, contrast, blur):
        # Crop frame
        frame = frame[crop[2]:crop[3], crop[0]:crop[1]]

        # Apply simple kernel blur
        # Take a matrix given by second argument and calculate average of those pixels
        if blur > 1:
            frame = cv2.blur(frame, (blur, blur))

        # Set Contrast
        if contrast > 1.0:
            frame = cv2.add(frame, np.array([float(contrast)]))

        # Convert frame to HSV
        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Create a mask
        frame_mask = cv2.inRange(frame_hsv, min_color, max_color)

        kernel = np.ones((5, 5), np.uint8)
        erosion = cv2.erode(frame_mask, kernel, iterations=1)

        # Apply threshold to the masked image, no idea what the values mean
        return_val, threshold = cv2.threshold(frame_mask, 127, 255, 0)

        # Find contours, they describe the masked image - our T
        contours, hierarchy = cv2.findContours(
            threshold,
            cv2.RETR_TREE,
            cv2.CHAIN_APPROX_SIMPLE
        )
        return (contours, hierarchy, frame_mask)

    def get_contour_extremes(self, cnt):
        """
        Get extremes of a countour.
        """
        leftmost = tuple(cnt[cnt[:, :, 0].argmin()][0])
        rightmost = tuple(cnt[cnt[:, :, 0].argmax()][0])
        topmost = tuple(cnt[cnt[:, :, 1].argmin()][0])
        bottommost = tuple(cnt[cnt[:, :, 1].argmax()][0])
        return (leftmost, topmost, rightmost, bottommost)

    def get_bounding_box(self, points):
        """
        Find the bounding box given points by looking at the extremes of each coordinate.
        """
        leftmost = min(points, key=lambda x: x[0])[0]
        rightmost = max(points, key=lambda x: x[0])[0]
        topmost = min(points, key=lambda x: x[1])[1]
        bottommost = max(points, key=lambda x: x[1])[1]
        return BoundingBox(leftmost, topmost, rightmost - leftmost, bottommost - topmost)

    def get_contour_corners(self, contour):
        """
        Get exact corner points for the plate given one contour.
        """
        if contour is not None:
            rectangle = cv2.minAreaRect(contour)
            box = cv2.cv.BoxPoints(rectangle)
            return np.int0(box)

    def join_contours(self, contours):
        """
        Joins multiple contours together.
        """
        cnts = []
        for i, cnt in enumerate(contours):
            area = cv2.contourArea(cnt)

            if len(cnt) >= 4 and area > 100:
                cnts.append(cnt)
        cnt = reduce(lambda x, y: np.concatenate((x, y)), cnts) if len(cnts) else None

        return cnt

    def get_largest_contour(self, contours):
        """
        Find the largest of all contours.
        """
        areas = [cv2.contourArea(c) for c in contours]
        return contours[np.argmax(areas)]

    def get_contour_centre(self, contour):
        """
        Find the center of a contour by minimum enclousing circle approximation.

        Returns: ((x, y), radius)
        """
        return cv2.minEnclosingCircle(contour)

    def get_angle(self, line, dot):
        """
        From dot to line
        """
        diff_x = dot[0] - line[0]
        diff_y = line[1] - dot[1]
        angle = np.arctan2(diff_y, diff_x) % (2 * np.pi)
        return angle


class RobotTracker(Tracker):
    def __init__(self, color, crop, offset, pitch, name, calibration):
        """
        Initialize tracker.

        Params:
            [string] color      the name of the color to pass in
            [(left-min, right-max, top-min, bot-max)]
                                crop  crop coordinates
            [int]       offset          how much to offset the coordinates
            [int]       pitch           the pitch we're tracking - used to find the right colors
            [string]    name            name for debug purposes
            [dict]      calibration     dictionary of calibration values
        """
        self.name = name
        self.crop = crop

        self.data = {
            'x': None, 'y': None,
            'name': self.name,
            'angle': None,
            'dot': None,
            'dot_diff': 10000.0,
            'box': None,
            'direction': None,
            'front': None
        }

        self.color = [calibration[color]]

        self.color_name = color
        self.offset = offset
        self.pitch = pitch
        self.calibration = calibration

    def get_plate(self, frame):
        """
        Given the frame to search, find a bounding rectangle for the green plate

        Returns:
            list of corner points
        """

        height, width, channel = frame.shape

        if height > 0 and width > 0:
            cv2.cv.SaveImage("test_blob.jpg", cv2.cv.fromarray(frame.copy()))
        # Adjustments are colors and contrast/blur
            adjustments = self.calibration['plate']
            contours = self.get_contours(frame.copy(), adjustments)
            return self.get_contour_corners(self.join_contours(contours))

        return None

    def get_blob(self, frame):
        height, width, channel = frame.shape

        if height > 0 and width > 0:
            #frame = cv2.GaussianBlur(frame.copy(), (5, 5), 0)
            temp = self.kmeans(frame)

            cv2.cv.SaveImage("test_blob.jpg", cv2.cv.fromarray(temp.copy()))
            gray = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)

            thresh1 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

            cv2.cv.SaveImage("test_blob_cnt_thresh.jpg", cv2.cv.fromarray(thresh1.copy()))
            #thresh1 = cv2.GaussianBlur(thresh1.copy(), (5, 5), 0)
            contours, hi = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            #cnt = self.get_largest_contour(contours)

            contours = [c for c in contours if 150 < cv2.contourArea(c) < 250]

            #cnt = self.join_contours(contours)

            cnt = reduce(lambda x, y: np.concatenate((x, y)), contours) if len(contours) else None

            if cnt is not None:
                rect = cv2.minAreaRect(cnt)
                #cnt = self.get_contour_corners(cnt)

                box = cv2.cv.BoxPoints(rect)

                box = np.int0(box)

                cv2.drawContours(frame, [box], -1, (0, 255, 0), 1)
                cv2.cv.SaveImage("test_blob_cnt.jpg", cv2.cv.fromarray(frame.copy()))
                return box

        return None


    def get_dot(self, frame, x_offset, y_offset):
        """
        Find center point of the black dot on the plate.

        Method:
            1. Assume that the dot is within some proximity of the center of the plate.
            2. Fill a dummy frame with black and draw white cirlce around to create a mask.
            3. Mask against the frame to eliminate any robot parts looking like dark dots.
            4. Use contours to detect the dot and return it's center.

        Params:
            frame       The frame to search
            x_offset    The offset from the uncropped image - to be added to the final values
            y_offset    The offset from the uncropped image - to be added to the final values
        """


        # Create dummy mask
        height, width, channel = frame.shape
        if height > 0 and width > 0:
            temp = cv2.GaussianBlur(frame.copy(), (5, 5), 0)
            cv2.cv.SaveImage("test_col.jpg", cv2.cv.fromarray(temp))

            gray = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)
            cv2.cv.SaveImage("test_gray.jpg", cv2.cv.fromarray(gray))

            thresh1 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
                                            cv2.THRESH_BINARY_INV, 11, 2)

            cv2.cv.SaveImage("test.jpg", cv2.cv.fromarray(thresh1))

            contours, hi = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            contours_temp = [(c, cv2.contourArea(c)) for c in contours if 20 < cv2.contourArea(c) < 60]

            contours = []

            for cnt in contours_temp:
                (x, y), radius = cv2.minEnclosingCircle(cnt[0])
                diffs = 0
                for c in cnt[0]:
                    diffs += (radius - self.distance(c[0], (x, y))) ** 2

                contours.append((cnt[0], diffs))

            contours.sort(key=lambda tup: tup[1])

            if contours and len(contours) > 0:
                cv2.drawContours(frame, [contours[0][0]], -1, (0, 255, 0), 1)

                cv2.cv.SaveImage("test_col_cnt.jpg", cv2.cv.fromarray(frame))
                (x, y), radius = self.get_contour_centre(contours[0][0])
                return (Center(x + x_offset, y + y_offset), contours[0][1], radius)

        return (None, None, None)

    def find(self, frame, queue):
        """
        Retrieve coordinates for the robot, it's orientation and speed - if
        available.

        Process:
            1. Find green plate
            2. Create a smaller frame with just the plate
            3. Find dot inside the green plate (the smaller window)
            4. Use plate corner points from (1) to determine angle

        Params:
            [np.array] frame                - the frame to scan
            [multiprocessing.Queue] queue   - shared resource for process

        Returns:
            None. Result is put into the queue.
        """
        # Set up variables
        x = y = angle = None
        sides = direction = None
        plate_corners = None
        dot = front = None
        front = rear = None

        # Trim the image to only consist of one zone
        frame = frame[self.crop[2]:self.crop[3], self.crop[0]:self.crop[1]]
        cv2.cv.SaveImage("pitch.jpg", cv2.cv.fromarray(frame.copy()))
        (dot, diff, radius) = self.get_dot(frame.copy(), self.offset, 0)



        # (1) Find the plates


        if dot is not None:

            size = 24
            plate_frame = frame.copy()[
                          int(dot.y) - size:int(dot.y) + size,
                          int(dot.x) - size:int(dot.x) + size
            ]
            plate_corners = self.get_blob(plate_frame)
            print 'Calc', plate_corners

            est = [(int(dot.x) - size / 2, int(dot.y) + size / 2), (int(dot.x) - size / 2, int(dot.y) - size),
                   (int(dot.x) + size / 2, int(dot.y) - size), (int(dot.x) + size / 2, int(dot.y) + size / 2)]

            print 'Est:', est


            #if plate_corners is None:
            plate_corners = est

            # print marker_corners
            if plate_corners is not None:
                # print 'Bounding', self.get_bounding_box(plate_corners)
                # Since get_dot adds offset, we need to remove it
                dot_temp = Center(dot[0] - self.offset, dot[1])

                # plate_corners = [(x + self.offset, y) for (x, y) in plate_corners]

                #plate_corners = [(int(dot.x)-size/2, int(dot.y)+size/2), (int(dot.x)-size/2, int(dot.y)-size), (int(dot.x)+size/2, int(dot.y)-size), (int(dot.x)+size/2, int(dot.y)+size/2)]

                # Find two points from plate_corners that are the furthest from the dot

                distances = [
                    (
                        (dot_temp.x - p[0]) ** 2 + (dot_temp.y - p[1]) ** 2,  # distance
                        p[0],  # x coord
                        p[1]  # y coord
                    ) for p in plate_corners]

                distances.sort(key=lambda x: x[0], reverse=True)

                # Front of the kicker should be the first two points in distances
                front = distances[:2]
                rear = distances[2:]

                # Calculate which of the rear points belongs to the first of the front
                first = front[0]
                front_rear_distances = [
                    (
                        (first[1] - p[0]) ** 2 + (first[2] - p[1]) ** 2,
                        p[1],
                        p[2]
                    ) for p in rear]
                front_rear_distances.sort(key=lambda x: x[0])


                # Direction is a line between the front points and rear points
                direction = (
                    Center(
                        (first[1] + front[1][1]) / 2 + self.offset,
                        (front[1][2] + first[2]) / 2),
                    Center(
                        (front_rear_distances[1][1] + front_rear_distances[0][1]) / 2 + self.offset,
                        (front_rear_distances[1][2] + front_rear_distances[0][2]) / 2)
                )

                angle = self.get_angle(direction[1], direction[0])

                # Offset the x coordinates




                if front is not None:
                    front = [(p[1] + self.offset, p[2]) for p in front]

                if rear is not None and dot is not None:
                    rear = [(p[1] + self.offset, p[2]) for p in rear]

                    width = self.distance(rear[0], rear[1])

                    d1 = self.dist_point_line(front[0], rear[0], dot)
                    d2 = self.dist_point_line(front[1], rear[1], dot)

                    if d1 < d2:
                        d = d1
                        i = 1
                    else:
                        d = d2
                        i = -1

                    delta = width / 2.0 - d
                    print 'Delta', delta
                    print 'Width', width
                    unit_vector = [(rear[0][0] - rear[1][0]) / width, (rear[0][1] - rear[1][1]) / width]

                    offset_1 = int(np.ceil(i * unit_vector[0] * delta))
                    offset_2 = int(np.ceil(i * unit_vector[1] * delta))

                    print 'Offset', offset_1

                    # Offset the x coordinates
                    #plate_corners = [(p[0] + offset_1, p[1] + offset_2) for p in plate_corners]

                    # Since get_dot adds offset, we need to remove it
                    dot_temp = Center(dot[0] - self.offset, dot[1])

                    # Find two points from plate_corners that are the furthest from the dot

                    distances = [
                        (
                            (dot_temp.x - p[0]) ** 2 + (dot_temp.y - p[1]) ** 2,  # distance
                            p[0],  # x coord
                            p[1]  # y coord
                        ) for p in plate_corners]

                    distances.sort(key=lambda x: x[0], reverse=True)

                    # Front of the kicker should be the first two points in distances
                    front = distances[:2]
                    if front is not None:
                        front = [(p[1] + self.offset, p[2]) for p in front]


                elif self.data['box'] is None:
                    pass
                    #plate_corners = [(p[0] + self.offset, p[1]) for p in plate_corners]

                if dot is None:
                    dot = self.data['dot']

                if direction is None:
                    direction = self.data['direction']

                if front is None:
                    front = self.data['front']

                if angle is None:
                    angle = self.data['angle']

                if x is None:
                    x = self.data['x']

                if y is None:
                    y = self.data['y']

                if plate_corners is None:
                    plate_corners = self.data['box']

                self.data = {
                    'x': None,
                    'y': None,
                    'name': self.name,
                    'angle': angle,
                    'dot': dot,
                    'box': plate_corners,
                    'direction': None,
                    'front': None,
                    'dot_diff': diff
                }

                queue.put(self.data)
                return

        queue.put(self.data)

        return

    def distance(self, P1, P2):
        return np.sqrt((P1[0] - P2[0]) ** 2 + (P1[1] - P2[1]) ** 2)

    def dist_point_line(self, P1, P2, P):
        top = np.abs((P2[1] - P1[1]) * P[0] - (P2[0] - P1[0]) * P[1] + P2[0] * P1[1] - P2[1] * P1[0])
        bottom = self.distance(P1, P2)
        return top / bottom

    def kmeans(self, plate):

        prep = plate.reshape((-1, 3))
        prep = np.float32(prep)

        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        k = 4
        ret, label, colour_centers = cv2.kmeans(prep, k, criteria, 20, cv2.KMEANS_RANDOM_CENTERS)
        colour_centers = np.uint8(colour_centers)

        # Get the new image based on the clusters found
        res = colour_centers[label.flatten()]
        res2 = res.reshape((plate.shape))

        # if self.name == 'Their Defender':
        # colour_centers = np.array([colour_centers])
        # print "********************", self.name
        # print colour_centers
        #     print 'HSV######'
        #     print cv2.cvtColor(colour_centers, cv2.COLOR_BGR2HSV)
        cv2.cv.SaveImage("kmeans.jpg", cv2.cv.fromarray(res2))
        return res2


class BallTracker(Tracker):
    """
    Track red ball on the pitch.
    """

    def __init__(self, crop, offset, pitch, calibration, name='ball'):
        """
        Initialize tracker.

        Params:
            [string] color      the name of the color to pass in
            [(left-min, right-max, top-min, bot-max)]
                                crop  crop coordinates
            [int] offset        how much to offset the coordinates
        """
        self.crop = crop
        # if pitch == 0:
        # self.color = PITCH0['red']
        # else:
        # self.color = PITCH1['red']
        self.color = [calibration['red']]
        self.offset = offset
        self.name = name
        self.calibration = calibration

    def find(self, frame, queue):
        for color in self.color:
            contours, hierarchy, mask = self.preprocess(
                frame,
                self.crop,
                color['min'],
                color['max'],
                color['contrast'],
                color['blur']
            )

            if len(contours) <= 0:
                # print 'No ball found.'
                pass
                # queue.put(None)
            else:
                # Trim contours matrix
                cnt = self.get_largest_contour(contours)

                # Get center
                (x, y), radius = cv2.minEnclosingCircle(cnt)

                queue.put({
                    'name': self.name,
                    'x': x,
                    'y': y,
                    'angle': None,
                    'velocity': None
                })
                return

        queue.put(None)
        return
