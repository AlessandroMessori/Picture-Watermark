from os import listdir,mkdir,environ
from os.path import isfile, join
from PIL import Image
from tkinter import filedialog

def watermark_with_transparency(input_path, output_path, watermark_path):
    base_image = Image.open(input_path).convert("RGBA")
    watermark = Image.open(watermark_path).convert("RGBA")
    width, height = base_image.size
    position = (int(width * 0.8),int(height * 0.9))

    transparent = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    transparent.paste(base_image, (0, 0))
    transparent.paste(watermark, position, mask=watermark)
    transparent.save(output_path)

def getImages(dir_path):
    all_files = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]
    return list(filter(lambda x:x.split(".")[1] in ["png","jpeg"], all_files))

def watermark_dir(dir_path):
    images = getImages(dir_path)

    try:
        mkdir(dir_path + "_firmate/")
    except:
        pass

    for img in images:
        split = img.split(".")
        output_path = dir_path + "_firmate/" + split[0] + "_watermarked." + split[1] 
        watermark_with_transparency(dir_path + "/" + img,output_path, 'firma.png')

def create_window():    
    if environ.get('DISPLAY','') == '':
        print('no display found. Using :0.0')
        environ.__setitem__('DISPLAY', ':0.0')

    folder_selected = filedialog.askdirectory()
    watermark_dir(folder_selected)

if __name__ == '__main__':
    create_window()



