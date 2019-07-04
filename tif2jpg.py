import os
from pathlib import Path
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox

createThumbnail = messagebox.askyesno("Question","Sollen Thumbnails erstellt werden?")
if createThumbnail == False:
	quit()
thumbnailsize = 768, 768

src = "M:/Brockytony/!_brockytony/Bilder"
dest = "C:/Users/felix.baumgaertner/Desktop/test"

root = tk.Tk()
root.withdraw()
src = filedialog.askdirectory(initialdir=src)
if src == "":
	print("The program will end because there is no source directory given.")
	quit()
dest = filedialog.askdirectory(initialdir=dest)
if dest == "":
	print("The program will end because there is no destination directory given.")
	quit()
root.destroy()



def duplicateFiletype(src, filetype):
	for filepath in Path(src).glob('**/*.' + filetype):
		filepathREL = os.path.relpath(filepath, src)
		dirs = os.path.dirname(filepathREL)
		
		if os.path.isdir(dest + "/" + dirs) == False:
			os.makedirs(dest + "/" + dirs)
			print("Dirs created: " + dirs)
		
		
		filepathNEW = dest + "/" + filepathREL.replace("." + filetype, ".jpg")
		
		if createThumbnail == True and os.path.exists(filepathNEW) == False:
			im = Image.open(filepath)
			im.thumbnail(thumbnailsize, Image.ANTIALIAS)
			
			if im.mode in ('RGBA', 'LA'):
				fill_color = (255, 255, 255)
				background = Image.new(im.mode[:-1], im.size, fill_color)
				background.paste(im, im.split()[-1])
				im = background
			im.save(filepathNEW)
			
			print("File created: " + filepathNEW)


duplicateFiletype(src, "tiff")
duplicateFiletype(src, "tif")


print("Done!")
