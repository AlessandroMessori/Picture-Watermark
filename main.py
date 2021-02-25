from os import listdir, mkdir, environ
from os.path import isfile, join
from PIL import Image
from tkinter import filedialog

# pastes watermark to a picture
def watermark_with_transparency(input_path, output_path, watermark_path, transformer):
    # loads images
    base_image = Image.open(input_path).convert("RGBA")
    watermark = Image.open(watermark_path).convert("RGBA")
    #watermark = Image.new("RGB", watermark.size, "RED")
    width, height = base_image.size

    # applies transformation to watermark
    watermark,position = transformer(watermark,width,height) 

    # paste watermark on image and saves
    transparent = paste_watermark(base_image,watermark,position)
    transparent.save(output_path)

# pastes watermark over a base image at a certain position
def paste_watermark(base,watermark,position):
    width, height = base.size
    transparent = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    transparent.paste(base, (0, 0))
    transparent.paste(watermark, position, mask=watermark)
    transparent = transparent.convert('RGB')
    return transparent

# scale and position watermark on the corner
def transform_corner(watermark, width, height):
    size = width if (width > height) else height
    watermark_ratio = 6.5
    resized_watermark = (int(size / 5), int(size / 5 / watermark_ratio))
    position = (int(width * 0.98 - resized_watermark[0]), int(height * 0.95))
    return (watermark.resize(resized_watermark),position)

# scale and position watermark diagonally
def transform_center(watermark,width,height):
    watermark = watermark.resize((width,int(height/3)))
    watermark2 = watermark.copy()
    watermark2.putalpha(128)
    watermark.paste(watermark2, watermark)
    return (watermark,(0,int(height/2-height/6)))

# returns a list of all images in a folder
def getImages(dir_path):
    all_files = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]
    return list(filter(lambda x: x.split(".")[1] in ["png", "jpeg", "jpg"], all_files))

# applies watermark to all images in input folder and saves results
def watermark_dir(dir_path):
    images = getImages(dir_path)

    create_dir(dir_path + "_firmate/")
    create_dir(dir_path + "_trasparente/")

    for img in images:
        split = img.split(".")
        output_path = dir_path + "_firmate/" + split[0] + "_watermarked." + split[1]
        output_path2 = dir_path + "_trasparente/" + split[0] + "_watermarked." + split[1]

        watermark_with_transparency(dir_path + "/" + img, output_path, 'watermark.png',transform_corner)
        watermark_with_transparency(dir_path + "/" + img, output_path2, 'watermark.png',transform_center)

#creates a directory
def create_dir(path):
    try:
        mkdir(path)
    except:
        pass

# starts window for folder selection
def create_window():
    if environ.get('DISPLAY', '') == '':
        print('no display found. Using :0.0')
        environ.__setitem__('DISPLAY', ':0.0')

    folder_selected = filedialog.askdirectory()
    watermark_dir(folder_selected)


# runs the program
if __name__ == '__main__':
    create_window()
