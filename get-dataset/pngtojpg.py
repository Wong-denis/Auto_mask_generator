from PIL import Image
import os

# get list of all filename in folder
path = "rgb_dataset"
dir_list = os.listdir(path)

print("All filenames in dataset:")
print(dir_list)

for filename in dir_list:
    # open  image 
    img_png = Image.open(path+'/'+filename)


    # print(filename[:-3])
    img_png.save(filename[:-3]+'jpg')
