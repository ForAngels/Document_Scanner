from PIL import ImageTk
import PIL
from PIL import ImageDraw,ImageFont
import numpy as np
from PIL import Image
from tkinter import *
import tkinter as tk
import cv2
import glob,os
import time,datetime
from urllib.request import urlopen
from pathlib import Path
from skimage.filters import threshold_local
from pdf2docx import Converter

window = Tk()
window.configure(background='white')
window.title("Document Scanner App")
width = window.winfo_screenwidth()
height = window.winfo_screenheight()
window.geometry(f'{width}x{height}')
window.iconbitmap('./main/cs.ico')
window.resizable(0, 0)
launch = False


w = 385;h = 535
size = (w, h)

def launch_mobile_cam():
    global capture2, crop_count, cropped_images, pdf_count, pdf_b, scanned_images, button4
    url = text.get()
    crop_count = 0
    pdf_count = 0
    scanned_images = []

    capture2 = tk.Button(window, text='Capture Image', bg="black", fg="white", width=22,
                   height=1, font=('times', 22, 'bold '),command = cropped_image, activebackground='yellow')
    capture2.place(x=27, y=620)

    

    pdf_img = PIL.Image.open('./main/pdf.png')
    pdf_img = pdf_img.resize((200, 70), PIL.Image.ANTIALIAS)
    sp_img1 = ImageTk.PhotoImage(pdf_img)

    pdf_b = Button(window, borderwidth=0, command=pdf_generate, image=sp_img1, bg='white')
    pdf_b.pack()
    pdf_b.image = sp_img1
    pdf_b.place(x=430, y=80)

    

    try:
        if url == '':
            notification = tk.Label(window, text='Check the URL !', width=20, height=1, fg="white", bg="firebrick1",
                            font=('times', 13, ' bold '))
            notification.place(x=24, y=68)
            window.after(2000, destroy_widget, notification)
        else:
            global display, imageFrame, capture1, img
            imageFrame = tk.Frame(window)
            imageFrame.place(x=24, y=80)

            display = tk.Label(imageFrame)
            display.grid()

            capture1 = tk.Button(window, text='Turn off', bg="green", fg="black", width=12,
                           height=1, font=('times', 14, 'bold '), command=destroy_cam,
                           activebackground='yellow')
            capture1.place(x=430, y=33)

            def show_frame():
                global img
                img_resp = urlopen(url)
                img_arr = np.array(bytearray(img_resp.read()), dtype=np.uint8)
                frame = cv2.imdecode(img_arr, -1)
                frame = cv2.rotate(frame, cv2.cv2.ROTATE_90_CLOCKWISE)


                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
                rgb = cv2.cvtColor(cv2image, cv2.COLOR_RGBA2RGB)
                img = PIL.Image.fromarray(rgb)
                img1 = img.resize(size, PIL.Image.ANTIALIAS)
                imgtk = ImageTk.PhotoImage(image=img1)
                display.imgtk = imgtk
                display.configure(image=imgtk)
                display.after(10, show_frame)
            show_frame()
    except Exception as e:
        print(e)
        notification1 = tk.Label(window, text='Connection Closed !', width=20, height=1, fg="white", bg="firebrick1",
                        font=('times', 13, ' bold '))
        notification1.place(x=24, y=68)
        window.after(2000, destroy_widget, notification1)
        imageFrame.destroy()
        display.destroy()
        capture1.destroy()
        capture2.destroy()

def destroy_widget(widget):
    widget.destroy()

def destroy_cam():
    imageFrame.destroy()
    display.destroy()
    capture1.destroy()
    capture2.destroy()


def cropped_image():
    global cropping, crop_count, launch, scanned_images
    launch = True
    repn = Path('Original_image')
    if repn.is_dir():
        pass
    else:
        os.mkdir('Original_image')
    crop_count += 1

    img1 = img.copy()
    img1 = cv2.cvtColor(np.asarray(img1), cv2.COLOR_RGB2BGR)
    cn = './Original_image/img_' + str(crop_count) + '.jpg'
    cv2.imwrite(cn, img1)

    imlab2 = tk.Label(window, text="Original Image : "+ cn[16:], width=22, height=1, fg="black", bg="yellow",
                     font=('times', 15, ' bold '))
    imlab2.place(x=430, y=140)

    imageFrame2 = tk.Frame(window)
    imageFrame2.place(x=430, y=170)

    display2 = tk.Label(imageFrame2)
    display2.grid()

    cv2image = cv2.cvtColor(img1, cv2.COLOR_BGR2RGBA)
    rgb = cv2.cvtColor(cv2image, cv2.COLOR_RGBA2RGB)
    img2 = PIL.Image.fromarray(rgb)
    img2 = img2.resize((270, 480), PIL.Image.ANTIALIAS)
    imgtk = ImageTk.PhotoImage(image=img2)
    display2.imgtk = imgtk
    display2.configure(image=imgtk)
    window.after(10000, destroy_widget, display2)
    window.after(10000, destroy_widget, imageFrame2)
    window.after(10000, destroy_widget, imlab2)

    imgr = cv2.imread(cn)
    imgr = cv2.cvtColor(imgr, cv2.COLOR_BGR2GRAY)
    t = threshold_local(imgr, 17, offset=15, method='gaussian')
    imgr = (imgr > t).astype('uint8') * 255
    repn = Path('Converted_image')
    if repn.is_dir():
        pass
    else:
        os.mkdir('Converted_image')
    cn1 = './Converted_image/img_' + str(crop_count) + '.jpg'
    cv2.imwrite(cn1,imgr)
    scanned_images.append(cn1)
    print(scanned_images)
    imlab4 = tk.Label(window, text="Scanned: "+ cn[16:], width=22, height=1, fg="white", bg="black",
                     font=('times', 15, ' bold '))
    imlab4.place(x=730, y=140)

    imageFrame4 = tk.Frame(window)
    imageFrame4.place(x=730, y=170)

    display4 = tk.Label(imageFrame4)
    display4.grid()

    cv2image4 = cv2.cvtColor(imgr, cv2.COLOR_GRAY2RGBA)
    rgb4 = cv2.cvtColor(cv2image4, cv2.COLOR_RGBA2RGB)
    img4 = PIL.Image.fromarray(rgb4)
    img4 = img4.resize((270, 480), PIL.Image.ANTIALIAS)
    imgtk4 = ImageTk.PhotoImage(image=img4)
    display4.imgtk = imgtk4
    display4.configure(image=imgtk4)
    window.after(10000, destroy_widget, display4)
    window.after(10000, destroy_widget, imageFrame4)
    window.after(10000, destroy_widget, imlab4)

def pdf_generate():
    global pdf_count, pdf_b, launch, scanned_images
    print(launch)
    if launch == False:
        notification = tk.Label(window, text='Capture the Images first !', width=20, height=1, fg="white", bg="firebrick1",
                        font=('times', 13, ' bold '))
        notification.place(x=24, y=68)
        window.after(2000, destroy_widget, notification)
        destroy_cam()
        pdf_b.destroy()
    else:
        pdf_b.destroy()
        pdf_count+=1


        repn = Path('Scanned_PDF')
        if repn.is_dir():
            pass
        else:
            os.mkdir('Scanned_PDF')


        img = PIL.Image.new('RGB', (100, 30), color=(255, 255, 255))
        fnt = ImageFont.truetype('./main/arial.ttf', 13)
        d = ImageDraw.Draw(img)
        d.text((5, 10), "Scanned PDF ", font=fnt,fill=(0, 0, 0))
        img.save('./Converted_image/z.jpg')
        scanned_images.append('./Converted_image/z.jpg')


        image_list = []
        for image in scanned_images:
            img = PIL.Image.open(image)
            img = img.convert('RGB')
            image_list.append(img)
        image_list.pop(-1)
        ts = time.time()
        timeStam = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        Hour, Minute, Second = timeStam.split(":")
        img.save('./Scanned_PDF/Scanned_'+str(pdf_count)+'_'+str(Hour)+'_'+str(Minute)+'_'+str(Second)+'.pdf',save_all=True, append_images=image_list)

        notification = tk.Label(window, text='PDF Downloaded Successfully !', width=30, height=1, fg="black", bg="green",
                        font=('times', 13, ' bold '))
        notification.place(x=850, y=450)
        window.after(2000, destroy_widget, notification)
        destroy_cam()




lab = tk.Label(window, text="Enter your URL", width=18, height=1, fg="black", bg="blue",
               font=('times', 16, ' bold '))
lab.place(x=24, y=5)

text = tk.Entry(window, borderwidth=4, width=34, bg="white", fg="black", font=('times', 16, ' bold '))
text.place(x=24, y=35)
text.insert(0,'http://192.168.0.13:8080/shot.jpg')

capture = tk.Button(window, text='Turn on', bg="blue", fg="black", width=12,
               height=1, font=('times', 14, 'bold '), command=launch_mobile_cam, activebackground='yellow')
capture.place(x=430, y=33)

window.mainloop()