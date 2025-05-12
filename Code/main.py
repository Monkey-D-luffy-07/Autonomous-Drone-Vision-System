import cv2
import tkinter as tk
from tkinter import filedialog

def main(video_path):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    fast = cv2.FastFeatureDetector_create()
    orb = cv2.ORB_create(nfeatures=500)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    prev_frame = None
    prev_keypoints = None
    prev_descriptors = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        keypoints = fast.detect(gray, None)
        keypoints, descriptors = orb.compute(gray, keypoints)

        if descriptors is None or len(descriptors) == 0:
            prev_frame = frame
            prev_keypoints = keypoints
            prev_descriptors = descriptors
            continue

        if prev_descriptors is not None and len(prev_descriptors) > 0:
            matches = bf.match(prev_descriptors, descriptors)
            matches = sorted(matches, key=lambda x: x.distance)


            # Calculate and print metrics
            num_matches = len(matches)
            avg_distance = sum(m.distance for m in matches) / num_matches if num_matches > 0 else float('inf')

            print(f"Frame Match Count: {num_matches}, Avg Match Distance: {avg_distance:.2f}")


            match_img = cv2.drawMatches(
                prev_frame, prev_keypoints, frame, keypoints,
                matches[:50], None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
            )
            cv2.imshow("Feature Matches", match_img)

        prev_frame = frame
        prev_keypoints = keypoints
        prev_descriptors = descriptors

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Use a file dialog to select the video file
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    video_path = filedialog.askopenfilename(
        title="Select Video File",
        filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv"), ("All files", "*.*")]
    )

    if video_path:
        main(video_path)
    else:
        print("No file selected.")
