from os import listdir,mkdir,environ
from os.path import isfile, join
from PIL import Image
from tkinter import filedialog

#pastes watermark to a picture
def watermark_with_transparency(input_path, output_path, watermark_path):
    #loads images
    base_image = Image.open(input_path).convert("RGBA")
    watermark = Image.open(watermark_path).convert("RGBA")
    width, height = base_image.size

    #scale and position watermark
    size = width if (width > height) else height
    watermark_ratio = 6.5
    resized_watermark = ( int(size / 5) ,int(size / 5 / watermark_ratio))
    position = (int(width * 0.98 - resized_watermark[0] ),int(height * 0.95))
    watermark = watermark.resize(resized_watermark)

    #paste watermark on image and save 
    transparent = Image.new('RGBA', (width,height), (0, 0, 0, 0))
    transparent.paste(base_image, (0, 0))
    transparent.paste(watermark, position, mask=watermark)
    transparent = transparent.convert('RGB')
    transparent.save(output_path)

#returns a list of all images in a folder
def getImages(dir_path):
    all_files = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]
    return list(filter(lambda x:x.split(".")[1] in ["png","jpeg","jpg"], all_files))

#applies watermark to all images in input folder and saves results
def watermark_dir(dir_path):
    images = getImages(dir_path)

    try:
        mkdir(dir_path + "_firmate/")
    except:
        pass

    for img in images:
        split = img.split(".")
        output_path = dir_path + "_firmate/" + split[0] + "_watermarked." + split[1] 
        watermark_with_transparency(dir_path + "/" + img,output_path, 'watermark.png')

#starts window for folder selection
def create_window():    
    if environ.get('DISPLAY','') == '':
        print('no display found. Using :0.0')
        environ.__setitem__('DISPLAY', ':0.0')

    folder_selected = filedialog.askdirectory()
    watermark_dir(folder_selected)

#runs the program
if __name__ == '__main__':
    create_window()



