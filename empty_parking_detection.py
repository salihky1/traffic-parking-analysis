import cv2
import pickle
import os

class ParkingSlotMarker:
    def __init__(self, image_path="your.jpg", data_file="points.pkl"):
        self.image_path = image_path
        self.data_file = data_file
        self.points = []
        self.rectangle_width = 46
        self.rectangle_height = 20

        self.load_points()

    def load_points(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "rb") as f:
                    self.points = pickle.load(f)
            except:
                self.points = []
        else:
            self.points = []

    def save_points(self):
        with open(self.data_file, "wb") as f:
            pickle.dump(self.points, f)

    def mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.points.append((x, y))
            self.save_points()

        elif event == cv2.EVENT_RBUTTONDOWN:
            for i, (px, py) in enumerate(self.points):
                if px < x < px + self.rectangle_width and py < y < py + self.rectangle_height:
                    self.points.pop(i)
                    self.save_points()
                    break

    def draw_slots(self, image):
        for (x, y) in self.points:
            cv2.rectangle(
                image,
                (x, y),
                (x + self.rectangle_width, y + self.rectangle_height),
                (255, 0, 0),
                2
            )

    def run(self):
        cv2.namedWindow("Parking Slot Editor")
        cv2.setMouseCallback("Parking Slot Editor", self.mouse_callback)

        while True:
            image = cv2.imread(self.image_path)
            if image is None:
                raise FileNotFoundError("Image file could not be loaded.")

            self.draw_slots(image)

            instructions = [
                "Left Click: Add parking slot",
                "Right Click: Remove parking slot",
                "Press Q to exit"
            ]

            y_offset = 30
            for line in instructions:
                cv2.putText(
                    image,
                    line,
                    (10, y_offset),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2
                )
                y_offset += 25

            cv2.imshow("Parking Slot Editor", image)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break

        cv2.destroyAllWindows()


if __name__ == "__main__":
    marker = ParkingSlotMarker("your.jpg")
    marker.run()
