import os
import natsort


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
