import os
import sys
from pathlib import Path
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox

# False for command line use only
interfaceBool = True

src = "//ds1517/Marketing/Brockytony/!_brockytony/Bilder"
dest = "//ds1517/Bildmaterial"

thumbnailsize = 1024, 1024



# user interface config setup

if interfaceBool == True:
	tk.Tk().withdraw()

	messagebox.showinfo("tif2jpg", "1. Declare source folder \n\n2. Declare destination folder \n\n3. Enjoy automatic tif to jpg conversion ")

	src = filedialog.askdirectory(initialdir=src)
	if src == "":
		messagebox.showerror("tif2jpg", "Error: no source directory given")
		quit("The program will end because there was no source directory given.")

	dest = filedialog.askdirectory(initialdir=dest)
	if dest == "":
		messagebox.showerror("tif2jpg", "Error: no destination directory given")
		quit("The program will end because there was no destination directory given.")



# progress bar setup

def progress(count, total, suffix=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '#' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))
    sys.stdout.flush()

def analyse(src, filetype):
	imgSum = 0
	for filepath in Path(src).glob('**/*.' + filetype):
		imgSum += 1
	
	return imgSum

imgSum_i = 0
imgSum = analyse(src, "tif")
imgSum += analyse(src, "tiff")



# main function

def duplicateFiletype(src, filetype):
	global imgSum_i, imgSum
	
	for filepath in Path(src).glob('**/*.' + filetype):
		filepathREL = os.path.relpath(filepath, src)
		dirs = os.path.dirname(filepathREL)
		
		searchFiletype = "tif" if filetype == "tiff" or filetype == "tif" else filetype
		if os.path.basename(dirs).lower().find(searchFiletype) != -1:
			filepathTEMP = os.path.dirname(filepathREL)
			filepathREL = os.path.dirname(filepathTEMP) + "/" + os.path.basename(filepathREL)
			dirs = os.path.dirname(dirs)
		
		if os.path.isdir(dest + "/" + dirs) == False:
			os.makedirs(dest + "/" + dirs)
			print("Dirs created: " + dirs)
		
		
		filepathNEW = dest + "/" + filepathREL.replace("." + filetype, ".jpg")
		
		if os.path.exists(filepathNEW) == False:
			im = Image.open(filepath)
			im.thumbnail(thumbnailsize, Image.ANTIALIAS)
			
			if im.mode in ('RGBA', 'LA'):
				fill_color = (255, 255, 255)
				background = Image.new(im.mode[:-1], im.size, fill_color)
				background.paste(im, im.split()[-1])
				im = background
			im.save(filepathNEW)
			
			print("File created: " + filepathNEW)
		
		progress(imgSum_i, imgSum)
		imgSum_i += 1



# run

duplicateFiletype(src, "tiff")
duplicateFiletype(src, "tif")



# clean end

if interfaceBool == True:
	messagebox.showinfo("tif2jpg", "All tif files were successfully converted.")
	
	tk.Tk().destroy()
