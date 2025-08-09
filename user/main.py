# import tkinter
import customtkinter as tk
import tkinter.messagebox
import os
from pathlib import Path
from PIL import Image
import client






# Theme
tk.set_appearance_mode('dark')
font = lambda size: ('Ariel', size, 'bold')

# App frame
root = tk.CTk()
root.geometry('480x720')
root.title('Save Files')
root.iconbitmap('images/icon.ico')
root.resizable(False, False)

#================================ Download ================================

def list_storage(names = [], selected=-1):
    # Clear the list frame
    for widget in files_scroll.winfo_children():
        widget.destroy()
    selected_var.set('')

    if not names:
        names = client.list_storage()
    
    for i in range(len(names)):
        file_type = names[i].split('.')[-1]
        icon_path = 'images/file-types' 
        
        #  Choose an icon based on file type
        if file_type in ['png', 'jpg', 'jpeg', 'ico']: # File is image
            icon_path = os.path.join(icon_path, 'img.png')
        elif file_type in ['txt', 'rtf', 'log', 'eml', 'docx']: # File is text
            icon_path = os.path.join(icon_path, 'text.png')
        else:
            icon_path = os.path.join(icon_path, 'default.png')
        
        button = tk.CTkButton(files_scroll, command=lambda index=i: select_file(names, index), image=tk.CTkImage(Image.open(icon_path), size=(15, 15)), width=360, text=names[i], anchor='w', fg_color=('blue' if selected == i else 'gray'), font=font(15))
        button.pack(pady=2)


def select_file(names, index):
    list_storage(names, index)
    selected_var.set(names[index])
    print(names[index])

def download_file():
    filename = selected_var.get()

    if not filename:
        tkinter.messagebox.showwarning(title='input error', message=f'no file was selected!\nplease select a file from the list by clicking on it')
        list_storage()
        return
    
    chunks = client.get_file(filename)
    if not chunks:
        tkinter.messagebox.showerror(title='error', message=f'file not found!')
        return

    dir_path = tk.filedialog.askdirectory(
        title='Select a dir',
        initialdir=os.path.join(Path.home(), 'Downloads')
    )
    if dir_path == '':
        dir_path = os.path.join(Path.home(), 'Downloads')

    path = os.path.join(dir_path, filename)
    print(path)

    try:
        with open(path, 'wb') as file:
            for chunk in chunks:
                file.write(chunk)
        tkinter.messagebox.showinfo(title='success', message=f'file written successfuly!\nfile path: {path}')

    except:
        tkinter.messagebox.showerror(title='error', message=f"couldn't write file!")




# Title
title1 = tk.CTkLabel(root, text='Download File', font=font(25))
title1.pack(pady=20)

# Refresh server files
refresh_frame = tk.CTkFrame(root, fg_color='#242424')
refresh_btn = tk.CTkButton(refresh_frame, command=list_storage, width=15, image=tk.CTkImage(Image.open('images/refresh.png'), size=(15, 15)), text='')
refresh_label = tk.CTkLabel(refresh_frame, text='refresh list', text_color='gray', font=font(15))

refresh_frame.pack(padx=(0, 250))
refresh_btn.pack(padx=(10, 5), pady=10, side=tk.LEFT)
refresh_label.pack(padx=(0, 10), pady=10)

# List storage
files_scroll = tk.CTkScrollableFrame(root, width=360)
files_scroll.pack(pady=(0, 10))

# Download file
download_btn = tk.CTkButton(root, command=download_file, text='download', font=font(25))
download_btn.pack(pady=(5, 0))

# Selected file
selected_var = tk.StringVar()
selected_label = tk.CTkLabel(root, textvariable=selected_var, text_color='gray')
selected_label.pack()







# Seperator
sep = tk.CTkFrame(root, height=2, fg_color='gray')
sep.pack(padx=10, pady=10, fill='x')




#================================ Upload ================================

def browse_files():
    path = tk.filedialog.askopenfilename(
        title='Select a file',
        initialdir=os.path.join(Path.home(), 'Downloads'),
        filetypes=(('All files','*.*'), ('tiff files','*.tiff'))
    )
    path_input_btn.delete(0, tk.END)
    path_input_btn.insert(tk.END, path)

def upload_file():
    path = path_input_btn.get()

    if not path:
        tkinter.messagebox.showwarning(title='input error', message='enter a file path')
        return
    
    if not client.upload_file(path):
        tkinter.messagebox.showwarning(title='input error', message='file not found')
        return

    list_storage()




# Title
title1 = tk.CTkLabel(root, text='Upload File', font=font(25))
title1.pack(pady=20)
    
# Upload input
upload_frame = tk.CTkFrame(root)
path_input_btn = tk.CTkEntry(upload_frame, width=290, height=40, placeholder_text='Enter a file path', font=font(15))
browse_files = tk.CTkButton(upload_frame, command=browse_files, text='files', width=60, height=40, fg_color='gray', hover_color='darkgray', font=font(15))

upload_frame.pack()
path_input_btn.pack(padx=(10, 0), pady=10, side=tk.LEFT)
browse_files.pack(padx=10, side=tk.RIGHT)

# Upload button
upload_btn = tk.CTkButton(root, command=upload_file, text='UPLOAD FILE', font=font(35), width=380, height=60)
upload_btn.pack()





# Run app if client connects
if client.start():
    list_storage()
    root.mainloop()
    client.close_app()
else:
    tkinter.messagebox.showerror(title='connection failed', message=f"wasn't able to connect to the server\nthe server might be inactive")