import os
import glob
from natsort import natsorted
from moviepy.editor import VideoFileClip, concatenate_audioclips

def get_video_files(directory):
    video_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith((".mp4", ".avi", ".mkv")):
                video_files.append(os.path.join(root, file))
    return video_files

def concatenate_video_audio(video_files, output_audio_filename):
    audio_clips = []
    for file in video_files:
        clip = VideoFileClip(file)
        audio_clip = clip.audio
        if audio_clip is not None:
            audio_clips.append(audio_clip)
        clip.reader.close()

    if audio_clips:
        final_audio = concatenate_audioclips(audio_clips)
        final_audio.write_audiofile(output_audio_filename, codec='mp3')
        print("Final audio 'final.mp3' has been created.")
    else:
        print("No audio clips found in the video files.")

if __name__ == "__main__":
    directory = os.path.abspath(os.path.dirname(__file__))  # Replace with your directory path
    output_audio_filename = "final.mp3"

    video_files = get_video_files(directory)
    if not video_files:
        print("No video files found in the specified directory and its subdirectories.")
    else:
        sorted_video_files = natsorted(video_files)
        concatenate_video_audio(sorted_video_files, output_audio_filename)