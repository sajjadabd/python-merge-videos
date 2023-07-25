import os
import cv2
from datetime import timedelta
from natsort import natsorted
from tqdm import tqdm
import time
from moviepy.editor import VideoFileClip, AudioFileClip , concatenate_audioclips



def concatenate_video_audio(video_files, output_audio_filename):
    audio_clips = []
    for file in video_files:
        clip = VideoFileClip(file)
        audio_clip = clip.audio
        if audio_clip is not None:
            audio_clips.append(audio_clip)
        #clip.reader.close()

    if audio_clips:
        final_audio = concatenate_audioclips(audio_clips)
        final_audio.write_audiofile(output_audio_filename, codec='mp3')
        print("Final audio 'final.mp3' has been created.")
    else:
        print("No audio clips found in the video files.")
        
        
def set_audio_to_video(video_file, audio_file, output_file):
    video_clip = VideoFileClip(video_file)
    audio_clip = AudioFileClip(audio_file)

    # Set audio of the video clip to the audio clip
    video_clip = video_clip.set_audio(audio_clip)

    # Save the output video with the combined audio
    video_clip.write_videofile(output_file, codec="libx264", audio_codec="aac")

    video_clip.reader.close()
    audio_clip.reader.close()
    
    


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

    for file in video_files:
        cap = cv2.VideoCapture(file)
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            out.write(frame)
            progress_bar.update(1)
        cap.release()

    out.release()
    progress_bar.close()

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"\nVideo merging completed. Time taken: {timedelta(seconds=elapsed_time)}")

def main():
    # Get the absolute path of the current directory (where the script is located)
    current_directory = os.path.abspath(os.path.dirname(__file__))
    output_audio_filename = "final.mp3"

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
        
        
        concatenate_video_audio(sorted_video_files, output_audio_filename)
        

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
        
    video_file = "final.mp4"
    audio_file = "final.mp3"
    output_file = "final_video.mp4"    
    set_audio_to_video(video_file, audio_file, output_file)

if __name__ == "__main__":
    main()