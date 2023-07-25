import os
import cv2
from datetime import timedelta
from natsort import natsorted
from tqdm import tqdm
import time

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
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

    total_frames = sum(int(cv2.VideoCapture(file).get(cv2.CAP_PROP_FRAME_COUNT)) for file in video_files)

    progress_bar = tqdm(total=total_frames, unit="frames", desc="Merging videos", dynamic_ncols=True)

    start_time = time.time()

    audio = None
    for file in video_files:
        cap = cv2.VideoCapture(file)
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            out.write(frame)
            progress_bar.update(1)
        cap.release()

        clip = VideoFileClip(file)
        if audio is None:
            audio = clip.audio
        else:
            audio = audio.set_duration(audio.duration + clip.audio.duration)
    
    out.release()
    progress_bar.close()

    final_clip = VideoFileClip(output_file)
    final_clip = final_clip.set_audio(audio)
    final_clip.write_videofile(output_file, codec="libx264", audio_codec="aac")

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"\nVideo merging completed. Time taken: {timedelta(seconds=elapsed_time)}")

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
        # Sort the video files using natsorted
        sorted_video_files = natsorted(video_files)

        durations = get_video_durations(sorted_video_files)

        print("List of video durations:")
        for file, duration in zip(sorted_video_files, durations):
            print(f"{file}: {format_duration(duration)}")

        total_duration = sum(durations)
        print("\nTotal duration of all videos:")
        print(f"{format_duration(total_duration)}")

        output_filename = os.path.join(current_directory, "final.mp4")
        merge_videos(sorted_video_files, output_filename)
        print(f"\nVideos merged and saved as '{output_filename}'.")

if __name__ == "__main__":
    main()