# Name:             Multi-object and multi-class bounding box labeling tool
# Purpose:          Label object bounding boxes and class for Detection data
# Original Author:  Qiushi
#                   https://github.com/puzzledqs/BBox-Label-Tool/tree/multi-class
#                   06/06/2014
# Modified by:      Mikaël Swawola, 12/07/2018
#
# License:          MIT License
#
# ==============================================================================


from __future__ import division
from tkinter import *
from tkinter import Tk, messagebox, filedialog
from PIL import Image, ImageTk
import os, sys
from tkinter import ttk
import glob
import random

from pathlib import Path

# Colors for the bounding boxes
COLORS = ['red', 'blue', 'yellow', 'pink', 'cyan', 'green', 'black']

# Supported image formats
IMAGE_FORMATS = ['.jpeg', '.jpg', '.png', '.JPEG', '.PNG', '.JPG']

# Maximum size for width or height, because scrolling and zooming the image is not supported yet
MAX_SIZE = 512

# Name of the text file containing the labels
LABEL_FILE = 'class.txt'

class BboxTool():
    """
    Bounding Box Labeling Class
    """

    def setup_main_frame(self, master):
        """
        Setup the main frame
        """

        self.parent = master
        self.parent.title("Multi-object bounding box labeling tool")
        self.frame = Frame(self.parent)
        self.frame.pack(fill=BOTH, expand=1) # Make the frame fill the entire parent
        root.resizable(width=True, height=True)


    def setup_widgets(self):
        """
        Setup the widgets
        """

        # Title label for directory
        title_label = Label(self.frame, text="Images Directory:")
        title_label.grid(row=0, column=0, sticky=W)
        
        # Label for directory
        self.dir = StringVar()
        directory = Label(self.frame, textvariable=self.dir)
        directory.grid(row=0, column=1, sticky=W)
        
        # Label for current image
        self.curimg = StringVar()
        curim = Label(self.frame, textvariable=self.curimg)
        curim.grid(row=1, column=0, columnspan=2, sticky=W)
        
        # Load Button
        self.ldBtn = Button(self.frame, text="Load", command=self.load_directory)
        self.ldBtn.grid(row=0, column=2, sticky=W+E)


    def initialize_class_members(self):
        """
        Initialize global state
        """

        self.image_list = []
        self.outDir = ''
        self.current_img = 1 # Default to the 1st image in the collection
        self.directory = 0
        self.imagename = ''
        self.labelfilename = ''
        self.tkimg = None
        self.ratio = None
        self.selected_label = ''
        self.multi_label = True

    def set_label(self, eventObject):
        """
        """
        self.selected_label = self.cbox_label.get()


    def setup_combobox_widget(self):
        """
        Setup the combobox for label selection.

        The combobox is shown only if the 'class.txt' file exist

        """
        temp = []
        try:
            with Path(LABEL_FILE).open() as f:
                for line in f.readlines():
                    temp.append(line.strip('\n'))
        except:
            self.multi_label = False
            return

        lb = Label(self.frame, text = 'Labels:')
        lb.grid(row=1, column=2, sticky=W)
        self.cbox_label = ttk.Combobox(self.frame, state='readonly')
        self.cbox_label.bind("<<ComboboxSelected>>", self.set_label)
        self.cbox_label.grid(row=2, column=2)
        
        self.cbox_label['values'] = temp
        self.cbox_label.current(0)
        self.selected_label = self.cbox_label.get()

    def __init__(self, master):
        
        self.initialize_class_members()
        self.setup_main_frame(master)
        self.setup_widgets()

        # initialize mouse state
        self.STATE = {}
        self.STATE['click'] = 0
        self.STATE['x'], self.STATE['y'] = 0, 0

        # reference to bbox
        self.bboxIdList = []
        self.bboxId = None
        self.bboxList = []
        self.hl = None
        self.vl = None

        # main panel for labeling
        self.mainPanel = Canvas(self.frame, cursor='tcross')
        self.mainPanel.bind("<Button-1>", self.mouseClick)
        self.mainPanel.bind("<Motion>", self.mouseMove)
        self.parent.bind("<Escape>", self.cancelBBox)  # press <Espace> to cancel current bbox
        #self.parent.bind("s", self.cancelBBox)
        self.parent.bind("<Left>", self.prevImage)
        self.parent.bind("<Right>", self.nextImage)
        self.mainPanel.grid(row = 3, column = 0, rowspan = 4, columnspan=2, sticky = W+N)

        self.setup_combobox_widget()

        # showing bbox info & delete bbox
        self.lb1 = Label(self.frame, text = 'Bounding boxes:')
        self.lb1.grid(row = 3, column = 2,  sticky = W+N)
        self.listbox = Listbox(self.frame, width = 22, height = 12)
        self.listbox.grid(row = 4, column = 2, sticky = N)
        self.btnDel = Button(self.frame, text = 'Delete', command = self.delBBox)
        self.btnDel.grid(row = 5, column = 2, sticky = W+E+N)
        self.btnClear = Button(self.frame, text = 'ClearAll', command = self.clearBBox)
        self.btnClear.grid(row = 6, column = 2, sticky = W+E+N)

        # control panel for image navigation
        self.ctrPanel = Frame(self.frame)
        self.ctrPanel.grid(row = 7, column = 1, columnspan = 2, sticky = W+E)
        self.prevBtn = Button(self.ctrPanel, text='<< Prev', width = 10, command = self.prevImage)
        self.prevBtn.pack(side = LEFT, padx = 5, pady = 3)
        self.nextBtn = Button(self.ctrPanel, text='Next >>', width = 10, command = self.nextImage)
        self.nextBtn.pack(side = LEFT, padx = 5, pady = 3)
        self.progLabel = Label(self.ctrPanel, text = "Progress:     /    ")
        self.progLabel.pack(side = LEFT, padx = 5)
        self.tmpLabel = Label(self.ctrPanel, text = "Go to Image No.")
        self.tmpLabel.pack(side = LEFT, padx = 5)
        self.idxEntry = Entry(self.ctrPanel, width = 5)
        self.idxEntry.pack(side = LEFT)
        self.goBtn = Button(self.ctrPanel, text = 'Go', command = self.gotoImage)
        self.goBtn.pack(side = LEFT)

        # display mouse position
        self.disp = Label(self.ctrPanel, text='')
        self.disp.pack(side = RIGHT)

        self.frame.columnconfigure(1, weight = 1)
        self.frame.rowconfigure(4, weight = 1)

    def set_directory(self, path):
        """
        """

        self.directory = Path(path)
        if not self.directory.is_dir() or not self.directory.exists():
            showerror("Error!", message = f"{self.directory} doesn't exist!")
            self.dir.set("")
            return

        self.dir.set(self.directory) # Update directory label


    def load_directory(self):
        """
        """

        # Select directory to process
        path = filedialog.askdirectory()
        
        # Give focus to the parent
        self.parent.focus()
        
        # Set directory
        self.set_directory(path)

        # Get image list
        imageList = list(self.directory.iterdir())
        self.image_list = [x for x in imageList if x.suffix in IMAGE_FORMATS]
        if len(self.image_list) == 0:
            print(f'No images found in {path}')
            return

        # Setup output dir
        self.outDir = Path('Labels')/self.directory.name
        if not Path('Labels').exists():
            Path('Labels').mkdir()
        if not self.outDir.exists():
            self.outDir.mkdir()
        
        self.loadImage()
        print(f'{len(self.image_list)} images loaded from {self.directory}')


    def loadImage(self):
        """
        Load image
        """

        imagepath = self.image_list[self.current_img - 1]
        img = Image.open(imagepath)
        self.curimg.set(imagepath.name)

        width, height = img.size

        # Resize image to fit on screen (zooming and scrolling are not supported yet)
        if width > height:
            if width > MAX_SIZE:
                self.ratio = width / MAX_SIZE
                img.thumbnail((MAX_SIZE,int(height/self.ratio)))
        else:
            if height > MAX_SIZE:
                self.ratio = height / MAX_SIZE
                img.thumbnail((int(width/self.ratio), MAX_SIZE))

        self.tkimg = ImageTk.PhotoImage(img)
        self.mainPanel.config(width=max(self.tkimg.width(), MAX_SIZE), height=max(self.tkimg.height(), MAX_SIZE))
        self.mainPanel.create_image(0, 0, image = self.tkimg, anchor=NW)
        
        # Update Progress indicator
        self.progLabel.config(text = f"{self.current_img}/{len(self.image_list)}")

        # load labels
        self.clearBBox()
        self.imagename = imagepath.stem
        labelname = self.imagename + '.txt'
        self.labelfilename = os.path.join(self.outDir, labelname)
        bbox_cnt = 0
        if os.path.exists(self.labelfilename):
            with open(self.labelfilename) as f:
                for (i, line) in enumerate(f):
                    if i == 0:
                        bbox_cnt = int(line.strip())
                        continue
                    tmp = line.split()
                    self.bboxList.append(tuple(tmp))
                    tmpId = self.mainPanel.create_rectangle(int(tmp[0]), int(tmp[1]), \
                                                            int(tmp[2]), int(tmp[3]), \
                                                            width = 2, \
                                                            outline = COLORS[(len(self.bboxList)-1) % len(COLORS)])
                    self.bboxIdList.append(tmpId)
                    self.listbox.insert(END, '%s : (%d, %d) -> (%d, %d)' %(tmp[4],int(tmp[0]), int(tmp[1]), \
                    												  int(tmp[2]), int(tmp[3])))
                    self.listbox.itemconfig(len(self.bboxIdList) - 1, fg = COLORS[(len(self.bboxIdList) - 1) % len(COLORS)])


    def save_bounding_box(self):
        """
        Save Bounding box
        """

        with open(self.labelfilename, 'w') as f:
            f.write('%d\n' %len(self.bboxList))
            for bbox in self.bboxList:
                if self.ratio != None:
                    bbox = (int(bbox[0]*self.ratio),
                     int(bbox[1]*self.ratio),
                     int(bbox[2]*self.ratio),
                     int(bbox[3]*self.ratio))
                f.write(' '.join(map(str, bbox)) + '\n')
        print(f'Image {self.labelfilename} saved')


    def mouseClick(self, event):
        if self.STATE['click'] == 0:
            self.STATE['x'], self.STATE['y'] = event.x, event.y
        else:
            x1, x2 = min(self.STATE['x'], event.x), max(self.STATE['x'], event.x)
            y1, y2 = min(self.STATE['y'], event.y), max(self.STATE['y'], event.y)
            if self.multi_label:
                self.bboxList.append((x1, y1, x2, y2, self.selected_label))
            else:
                self.bboxList.append((x1, y1, x2, y2))
            self.bboxIdList.append(self.bboxId)
            self.bboxId = None
            self.listbox.insert(END, '(%d, %d) -> (%d, %d)' %(x1, y1, x2, y2))
            self.listbox.itemconfig(len(self.bboxIdList) - 1, fg = COLORS[(len(self.bboxIdList) - 1) % len(COLORS)])
        self.STATE['click'] = 1 - self.STATE['click']

    def mouseMove(self, event):
        self.disp.config(text = 'x: %d, y: %d' %(event.x, event.y))
        if self.tkimg:
            if self.hl:
                self.mainPanel.delete(self.hl)
            self.hl = self.mainPanel.create_line(0, event.y, self.tkimg.width(), event.y, width = 2)
            if self.vl:
                self.mainPanel.delete(self.vl)
            self.vl = self.mainPanel.create_line(event.x, 0, event.x, self.tkimg.height(), width = 2)
        if 1 == self.STATE['click']:
            if self.bboxId:
                self.mainPanel.delete(self.bboxId)
            self.bboxId = self.mainPanel.create_rectangle(self.STATE['x'], self.STATE['y'], \
                                                            event.x, event.y, \
                                                            width = 2, \
                                                            outline = COLORS[len(self.bboxList) % len(COLORS)])

    def cancelBBox(self, event):
        if 1 == self.STATE['click']:
            if self.bboxId:
                self.mainPanel.delete(self.bboxId)
                self.bboxId = None
                self.STATE['click'] = 0

    def delBBox(self):
        sel = self.listbox.curselection()
        if len(sel) != 1 :
            return
        idx = int(sel[0])
        self.mainPanel.delete(self.bboxIdList[idx])
        self.bboxIdList.pop(idx)
        self.bboxList.pop(idx)
        self.listbox.delete(idx)

    def clearBBox(self):
        for idx in range(len(self.bboxIdList)):
            self.mainPanel.delete(self.bboxIdList[idx])
        self.listbox.delete(0, len(self.bboxList))
        self.bboxIdList = []
        self.bboxList = []

    def prevImage(self, event = None):
        self.save_bounding_box()
        if self.current_img > 1:
            self.current_img -= 1
            self.loadImage()

    def nextImage(self, event = None):
        self.save_bounding_box()
        if self.current_img < len(self.image_list):
            self.current_img += 1
            self.loadImage()

    def gotoImage(self):
        idx = int(self.idxEntry.get())
        if 1 <= idx and idx <= len(self.image_list):
            self.save_bounding_box()
            self.current_img = idx
            self.loadImage()


if __name__ == '__main__':
    root = Tk()
    _ = BboxTool(root)
    root.mainloop()
