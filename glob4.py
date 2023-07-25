import os
import natsort

from moviepy.editor import VideoFileClip, concatenate_videoclips

from datetime import timedelta



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





def get_video_files(directory):
    video_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(".mp4"):
                video_files.append(os.path.join(root, file))
                
    video_files = natsort.natsorted(video_files)
    return video_files

def merge_videos(video_files, output_file):
    clips = [VideoFileClip(file) for file in video_files]
    final_clip = concatenate_videoclips(clips, method="compose")
    final_clip = final_clip.resize(height=1080)  # Set the resolution to 720p (HD)
    final_clip.write_videofile(output_file, codec="libx264")
    for clip in clips:
        clip.close()
    final_clip.close()

def main():
    root_directory = "."  # Set the root directory here (you can replace "." with your desired path)
    output_filename = "final.mp4"
    video_files = get_video_files(root_directory)
    
    
    #for file in video_files:
    #    print(file)
    
    
    
    if not video_files:
        print("No video files found.")
        return
    else:
        durations = get_video_durations(video_files)

        #print("List of video durations:")
        #for file, duration in zip(video_files, durations):
        #    print(f"{file}: {format_duration(duration)}")

        total_duration = sum(durations)
        
        print("\nTotal duration of all videos:")
        print(f"{format_duration(total_duration)}")
        
        print()
        
    return
    
    merge_videos(video_files, os.path.join(root_directory, output_filename))
    print("Video merge completed. Output saved as 'final.mp4' in the root directory.")

if __name__ == "__main__":
    main()








"""
def get_all_mp4_videos(directory):
    mp4_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(".mp4"):
                mp4_files.append(os.path.join(root, file))
    
    return mp4_files
    
    
def sort_directories(directories):
    # Use natsort to sort the directory names in a human-friendly way
    return natsort.natsorted(directories)

def main():
    # Get the absolute path of the current directory (where the script is located)
    current_directory = os.path.abspath(os.path.dirname(__file__))

    mp4_files = get_all_mp4_videos(current_directory)
    
    mp4_files = sort_directories(mp4_files)

    if not mp4_files:
        print("No MP4 video files found in the current directory and its subdirectories.")
    else:
        print("List of MP4 videos:")
        for file in mp4_files:
            print(file)

if __name__ == "__main__":
    main()
    
"""
