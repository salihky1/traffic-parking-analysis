import cv2
import pickle
import numpy as np
import os


class ParkingSpaceChecker:
    def __init__(self, image_path="your.jpg", points_file="points.pkl"):
        self.image_path = image_path
        self.points_file = points_file
        self.space_width = 40
        self.space_height = 20
        self.threshold = 150
        self.positions = []

        self.load_positions()
        self.image = cv2.imread(self.image_path)

        if self.image is None:
            raise FileNotFoundError("Image file could not be loaded.")

    def load_positions(self):
        if os.path.exists(self.points_file):
            with open(self.points_file, "rb") as f:
                self.positions = pickle.load(f)
        else:
            self.positions = []

    def preprocess(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3, 3), 1)
        thresh = cv2.adaptiveThreshold(
            blur,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV,
            25,
            16
        )
        median = cv2.medianBlur(thresh, 5)
        dilated = cv2.dilate(median, np.ones((3, 3)), iterations=1)
        return dilated

    def check_spaces(self, processed_frame, display_frame):
        free_count = 0

        for pos in self.positions:
            x, y = pos
            crop = processed_frame[y:y + self.space_height, x:x + self.space_width]
            non_zero_count = cv2.countNonZero(crop)

            if non_zero_count < self.threshold:
                color = (0, 255, 0)  # Free (green)
                free_count += 1
            else:
                color = (0, 0, 255)  # Occupied (red)

            cv2.rectangle(
                display_frame,
                (x, y),
                (x + self.space_width, y + self.space_height),
                color,
                2
            )

        cv2.putText(
            display_frame,
            f"Free Spaces: {free_count}/{len(self.positions)}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 0),
            2
        )

    def run(self):
        while True:
            display = self.image.copy()
            processed = self.preprocess(self.image)

            self.check_spaces(processed, display)

            cv2.imshow("Parking Space Detection", display)

            key = cv2.waitKey(0) & 0xFF
            if key == ord("q"):
                break

        cv2.destroyAllWindows()


if __name__ == "__main__":
    checker = ParkingSpaceChecker("your.jpg", "points.pkl")
    checker.run()
