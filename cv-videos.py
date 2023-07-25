import os
import cv2
import natsort

from datetime import timedelta

def get_video_durations(video_files):
    durations = []
    for file in video_files:
        cap = cv2.VideoCapture(file)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frame_count / fps
        durations.append(duration)
        cap.release()
    return durations

def format_duration(seconds):
    return str(timedelta(seconds=seconds))

def merge_videos(video_files, output_file):
    cap = cv2.VideoCapture(video_files[0])
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_file, fourcc, 30.0, (width, height))

    for file in video_files:
        cap = cv2.VideoCapture(file)
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            out.write(frame)
        cap.release()
    out.release()

def main():
    # Get the absolute path of the current directory (where the script is located)
    current_directory = os.path.abspath(os.path.dirname(__file__))

    video_files = []
    for root, _, files in os.walk(current_directory):
        for file in files:
            if file.lower().endswith(".mp4"):
                video_files.append(os.path.join(root, file))

    if not video_files:
        print("No MP4 video files found in the current directory and its subdirectories.")
    else:
        #video_files = natsort.natsorted(video_files)
        durations = get_video_durations(video_files)

        print("List of video durations:")
        for file, duration in zip(video_files, durations):
            print(f"{file}: {format_duration(duration)}")

        total_duration = sum(durations)
        print("\nTotal duration of all videos:")
        print(f"{format_duration(total_duration)}")

        output_filename = os.path.join(current_directory, "final.mp4")
        merge_videos(video_files, output_filename)
        print(f"\nVideos merged and saved as '{output_filename}'.")

if __name__ == "__main__":
    main()
