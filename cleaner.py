import os

def removeAll():
    folder = "./temp_youtube_download"
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

    folder = "./videoChunks"
    for filename in os.listdir(folder):
        file_path = os.path.join(folder,filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
