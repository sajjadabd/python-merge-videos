import os
from moviepy.editor import VideoFileClip, concatenate_videoclips

def get_video_files(directory):
    video_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(".mp4"):
                video_files.append(os.path.join(root, file))
    return video_files

def merge_videos(video_files, output_file):
    clips = [VideoFileClip(file) for file in video_files]
    final_clip = concatenate_videoclips(clips, method="compose")
    final_clip = final_clip.resize(height=720)  # Set the resolution to 720p (HD)
    final_clip.write_videofile(output_file, codec="libx264")
    for clip in clips:
        clip.close()
    final_clip.close()

def main():
    root_directory = "."  # Set the root directory here (you can replace "." with your desired path)
    output_filename = "final.mp4"
    video_files = get_video_files(root_directory)
    
    reverseVideoFiles = video_files
    
    
    video_files.sort()

    
    print()
    print("--------------sort-------------------")
    print(video_files)
    
    
    reverseVideoFiles.reverse()
    
    print()
    print("--------------reverse-------------------")
    print(reverseVideoFiles)
    
    
    
    if not video_files:
        print("No video files found.")
        return
    
    #merge_videos(video_files, os.path.join(root_directory, output_filename))
    print("Video merge completed. Output saved as 'final.mp4' in the root directory.")

if __name__ == "__main__":
    main()
