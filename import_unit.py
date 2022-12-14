from PIL import Image
from config import *
import os
from sys import argv, exit
from threading import Thread
from stable_diffusion.dream import regenerate_unit, clear_dream_dirs, ensure_api_key

def get_dynamic_units(type='air'):
    dir = f'graphics/units_dynamic/{type}/'
    return sorted(list(map(lambda p: dir + p, os.listdir(dir))))

def get_static_units(type='air'):
    dir = f'graphics/units_static/{type}/'
    return sorted(list(map(lambda p: dir + p, os.listdir(dir))))

def clear_folder(dir):
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

def extract_frame(img, frame):
    w, h = img.size
    half_w = int(w/2)
    half_h = int(h/2)
    frame_boxes = [
        (0, 0, half_w, half_h),
        (half_w, 0, w, half_h),
        (0, half_h, half_w, h),
        (half_w, half_h, w, h)]
    
    tile_size = (half_w, half_h)
    img_frame = img.crop(frame_boxes[frame-1])
    frame_box = img_frame.getbbox()
    img_frame = img_frame.crop(frame_box)
    img_out = Image.new(mode="RGBA", size=tile_size)
    img_out.paste(img_frame, (
        int((tile_size[0]-img_frame.size[0])/2), 
        int((tile_size[1]-img_frame.size[1])/2)))
    img_out.thumbnail((96, 96), Image.ANTIALIAS)
    return img_out

def regenerate_all_units():
    ensure_api_key()

    # clear_folder('graphics/units_dynamic/air')
    # clear_folder('graphics/units_dynamic/ground')
    clear_dream_dirs()
    tasks = []
    for i in range(1, 4):

        thread1 = Thread(target=regenerate_unit, name=f'aworker{i}', args=('air', i))
        thread1.start()
        tasks.append(thread1)

        thread2 = Thread(target=regenerate_unit, name=f'gworker{i}', args=('ground', i))
        thread2.start()
        tasks.append(thread2)

    for t in tasks:
        t.join()

def import_unit(type='air', unit_no = None):
    # build a list of images to process
    queue = []
    if unit_no:
        queue = [f'stable_diffusion/{type}/{unit_no}.png']
    else:
        dir = f'stable_diffusion/{type}/'
        queue = list(map(lambda p: dir + p, os.listdir(dir)))

    # process each image in the list...
    paths = []
    for image_file in queue:
        img = Image.open(image_file)
        img = img.convert("RGBA")
        
        # convert the background to alpha 
        datas = img.getdata()
        newData = []
        for item in datas:
            if (item[0] >= 240 and item[1] >= 240 and item[2] >= 240):
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)
        img.putdata(newData)
        
        # extract and normalize each of the 4 frames from the source image
        frame1 = extract_frame(img, 1)
        frame2 = extract_frame(img, 2)
        frame3 = extract_frame(img, 3)
        frame4 = extract_frame(img, 4)

        # combine the 4 frames back into a single image in a format suitable for the game to use
        image_out = Image.new(mode="RGBA", size=(192, 192))
        image_out.paste(frame1, (0,0))
        image_out.paste(frame2, (96,0))
        image_out.paste(frame3, (0,96))
        image_out.paste(frame4, (96,96))

        path = f'graphics/units_dynamic/{type}/{os.path.basename(image_file)}'
        image_out.save(path, "PNG")
        paths.append(path) 
    return paths

def import_all_units():
    print('Importing A.I. generated units...')
    air_paths = import_unit('air')
    ground_paths = import_unit('ground')
    print('done.')
    return air_paths + ground_paths
    

if __name__ == '__main__':
    if len(argv) == 3:
        type = argv[1]
        file_path = argv[2]
        import_unit(type, file_path)
    elif len(argv) == 2:
        type = argv[1]
        import_unit(type)
    else:
        exit('Incorrect number of arguments specified.')
