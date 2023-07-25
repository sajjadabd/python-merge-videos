import os
import glob

def get_all_mp4_videos(directory):
    return os.path.join(directory, '**/*.mp4') 
    mp4_files = glob.glob(os.path.join(directory, '**/*.mp4') , recursive=True)
    
    
    """
    for file in :
        if os.path.isfile(file):
            mp4_files.append(file)
    """
    return mp4_files

def main():
    root_directory = os.path.abspath(os.path.dirname(__file__))
    #root_directory = "."  # Set the root directory here (you can replace "." with your desired path)
    mp4_files = get_all_mp4_videos(root_directory)
    print( mp4_files )
    return
    if not mp4_files:
        print("No MP4 video files found.")
    else:
        print("List of MP4 videos:")
        for file in mp4_files:
            print(file)

if __name__ == "__main__":
    main()
