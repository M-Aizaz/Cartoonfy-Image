# -*- coding: utf-8 -*-
"""
Created on Wed Oct 20 21:48:09 2021

@author: Aizaz
"""

import cv2 #for image processing
import easygui #to open the filebox
import numpy as np #to store image
import imageio #to read image stored at particular path
import sys
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image


def upload():
    ImagePath=easygui.fileopenbox()
    cartoonify(ImagePath)
    
def cartoonify(ImagePath):
     org_img=cv2.imread(ImagePath)
     org_img=cv2.cvtColor(org_img,cv2.COLOR_BGR2RGB)

     if org_img is None:
            print("Can not find any image. Choose appropriate file")
            sys.exit()
        
     r1=cv2.resize(org_img,(240,360))
     plt.imshow(r1, cmap='gray')
     
     gray=cv2.cvtColor(org_img,cv2.COLOR_RGB2GRAY)
     r2=cv2.resize(gray,(240,360))
     
     sooth=cv2.medianBlur(gray,5)
     r3=cv2.resize(sooth,(240,360))
     
     edges = cv2.adaptiveThreshold(sooth, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
     r4 = cv2.resize(edges, (240,360))
     #cv2.imshow('Canny Edge Detection', r4)
     
     colorImage = cv2.bilateralFilter(org_img, 9, 300, 300)
     r5 = cv2.resize(colorImage, (240, 360))
     cartoonImage = cv2.bitwise_and(colorImage, colorImage, mask=edges)
     r6 = cv2.resize(cartoonImage, (240, 360))
     #cv2.imshow("ss",r6)
     #cv2.waitKey(0)
     #cv2.destroyAllWindows()
     
     images=[r1,r2, r3, r4, r5, r6]
     fig, axes = plt.subplots(3,2, figsize=(8,8), subplot_kw={'xticks':[], 'yticks':[]}, gridspec_kw=dict(hspace=0.1, wspace=0.1))
     for i, ax in enumerate(axes.flat):
        ax.imshow(images[i], cmap='gray')
     plt.show()
     
#upload()
#cartoonify()
def save(ReSized6, ImagePath):
    #saving an image using imwrite()
    newName="cartoonified_Image"
    path1 = os.path.dirname(ImagePath)
    extension=os.path.splitext(ImagePath)[1]
    path = os.path.join(path1, newName+extension)
    cv2.imwrite(path, cv2.cvtColor(r6, cv2.COLOR_RGB2BGR))
    I = "Image saved by name " + newName +" at "+ path
    tk.messagebox.showinfo(title=None, message=I)
    
    top=tk.Tk()
    top.geometry('400x400')
    top.title('Cartoonify Your Image !')
    top.configure(background='white')
    label=Label(top,background='#CDCDCD', font=('calibri',20,'bold'))
                
    upload=Button(top,text="Cartoonify an Image",command=upload,padx=10,pady=5)
    upload.configure(background='#364156', foreground='white',font=('calibri',10,'bold'))           
    upload.pack(side=TOP,pady=50)
    
    save1=Button(top,text="Save cartoon image",command=lambda: save(ImagePath, ReSized6),padx=30,pady=5)
    save1.configure(background='#364156', foreground='white',font=('calibri',10,'bold'))
    save1.pack(side=TOP,pady=50)
    top.mainloop()