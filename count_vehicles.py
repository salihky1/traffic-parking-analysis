import cv2
import numpy as np

class TrafficVehicleCounter:
    def __init__(self, video_path="traffic.mp4"):
        self.video_path = video_path
        self.capture = cv2.VideoCapture(self.video_path)

        if not self.capture.isOpened():
            raise IOError("Video file could not be opened.")

        self.background_subtractor = cv2.createBackgroundSubtractorMOG2(
            history=500,
            varThreshold=25,
            detectShadows=True
        )

        self.vehicle_count = 0
        self.line_start = (0, 150)
        self.line_end = (400, 50)
        self.min_width = 40
        self.min_height = 40

        self.font = cv2.FONT_HERSHEY_DUPLEX

    def draw_counting_line(self, frame):
        cv2.line(frame, self.line_start, self.line_end, (0, 255, 255), 3)

    def process_frame(self, frame):
        fg_mask = self.background_subtractor.apply(frame)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_DILATE, kernel)

        contours, hierarchy = cv2.findContours(
            fg_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
        )

        if hierarchy is None:
            hierarchy = []

        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)

            if w > self.min_width and h > self.min_height:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)

                center_x = x + w // 2
                center_y = y + h // 2
                cv2.circle(frame, (center_x, center_y), 3, (0, 255, 0), -1)

                if 50 < center_x < 70:
                    self.vehicle_count += 1

        return frame, fg_mask

    def draw_vehicle_count(self, frame):
        text = f"Car Count: {self.vehicle_count}"
        cv2.putText(frame, text, (90, 100), self.font, 1.5, (0, 0, 255), 2, cv2.LINE_AA)

    def run(self):
        while True:
            ret, frame = self.capture.read()

            if not ret:
                break

            processed_frame, mask = self.process_frame(frame)

            self.draw_counting_line(processed_frame)
            self.draw_vehicle_count(processed_frame)

            cv2.imshow("Traffic Video", processed_frame)
            cv2.imshow("Foreground Mask", mask)

            key = cv2.waitKey(100) & 0xFF
            if key == ord("q"):
                break

        self.release()

    def release(self):
        self.capture.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    counter = TrafficVehicleCounter("traffic.mp4")
    counter.run()
