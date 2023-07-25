import os
import cv2
from datetime import timedelta
from natsort import natsorted
from moviepy.editor import VideoFileClip, concatenate_videoclips

def get_video_durations(video_files):
    durations = []
    for file in video_files:
        clip = VideoFileClip(file)
        duration = clip.duration
        durations.append(duration)
        clip.close()
    return durations

def format_duration(seconds):
    return str(timedelta(seconds=seconds))
    


def merge_videos(video_files, output_file):
    video_clips = [VideoFileClip(file) for file in video_files]

    final_clip = concatenate_videoclips(video_clips, method="compose")

    final_clip.write_videofile(output_file, codec="libx264", audio_codec="aac")

    progress_bar.close()

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
