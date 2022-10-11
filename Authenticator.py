import os
import re
import cv2
import time
import pyotp
import base64
import pickle
import qrcode
import hashlib
import platform
import threading
import pyautogui
import pyperclip

import numpy as np

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename

from PIL import Image, ImageTk
from pyzbar import pyzbar
from urllib.parse import unquote
from cryptography.fernet import Fernet


class StoreData():
    def __init__(self):
        info = platform.machine() +'|'+ platform.system() +'|'+ platform.processor() +'|XOyxcU6QZHKexzpi4orOlxRua8rytbSy'
        hashed = hashlib.sha512(info.encode()).hexdigest()
        hashed = ' '.join([hashed[i:i+32] for i in range(0, len(hashed), 32)])
        hashed = hashed[::-1]
        hashed = ''.join(hashed)

        key = hashlib.md5(hashed.encode()).hexdigest()[:32]
        key = base64.urlsafe_b64encode(key.encode())
        self.fernet = Fernet(key)

    def save(self, arr, filename):
        try:
            obj = pickle.dumps(arr, pickle.HIGHEST_PROTOCOL)
            encrypted = self.fernet.encrypt(obj)
            with open(filename, 'wb+') as f:
                f.write('DO NOT DELETE OR MODIFY THIS FILE!\n'.encode())
                f.write(encrypted)
            return True
        except:
            return False
            

    def load(self, filename):
        if not os.path.exists(filename):
            return []
        try:
            with open(filename, 'rb') as f:
                encrypted_reload = f.readlines()[1]
                decrypted = self.fernet.decrypt(encrypted_reload)
            arr = pickle.loads(decrypted)
            return arr
        except:
            return False
        
class ScanQR():    
    def scan(self, mode=0, img_path=None):
        '''
        mode:
            0 - screenshot
            1 - import image
        img_path: if 'mode' is import image: require path to the image
        '''
        codes = []
        if mode == 0:
            img = pyautogui.screenshot()
            img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        elif mode == 1:
            if img_path:
                img = cv2.imread(os.path.normpath(img_path))
            else:
                return False
        
        img = cv2.cvtColor(img,0)
        barcode = pyzbar.decode(img)
        for obj in barcode:
            barcodeData = obj.data.decode("utf-8")
            codes.append(str(barcodeData))
        return codes

    
class Auth():
    def __init__(self):
        self.totp = ''

    def set_code(self, secret_key):
        self.totp = pyotp.TOTP(secret_key)

    def get_code(self):
        print(self.totp.now())


class GUI():
    def __init__(self):
        self.store_data = StoreData()
        self.file_store = 'secret_key.dat'
        self.url_list_filename = 'url_list.dat'
        self.working_dir = os.getcwd()
        self.terminated = False
        self.update_interval = 1
        self.tmp_account_name = []
        self.is_show_code = False
        self.account_show_code = ''
        self.auto_enter_code = False
        
        self.root = Tk()
        self.root.title("Authenticator")
        self.root.geometry('1200x800+100+100')
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        s = ttk.Style(self.root)
        s.theme_use('clam')
        s.configure('Horizontal.TProgressbar', background='#4CAF50')
        s.configure('green.TButton', background = '#4CAF50')
        s.configure('red.TButton', background = '#ff2020')
        '''
        self.root.tk.call('source', os.path.join(self.working_dir, 'themes', 'breeze-dark', 'breeze-dark.tcl'))
        s.theme_use('breeze-dark')
        '''
        
        Grid.rowconfigure(self.root, 6, weight=1)
        Grid.columnconfigure(self.root, 0, weight=1)
        Grid.columnconfigure(self.root, 1, weight=0)
        
        self.init_app_pwd()
        
        #self.main_menu_render()
        threading.Thread(target=self.update_code).start()
        self.root.mainloop()

    def init_app_pwd(self):
        data = self.store_data.load(self.file_store)
        pwd_set = False
        if data:
            for i in data:
                if type(i) is dict:
                    pwd_set = True
        if pwd_set:
            self.check_app_pwd_render()
        else:
            self.set_app_pwd_render()                


    def check_app_pwd_render(self):
        def check_app_pwd():
            nonlocal text_entry_pwd
            pwd = str(text_entry_pwd.get())
            data = self.store_data.load(self.file_store)
            if data:
                for i in data:
                    if type(i) is dict:
                        if i['app_pwd'] == pwd:
                            self.main_menu_render()
                        else:
                            messagebox.showerror('Error', 'Password is incorrect!')
            else:
                messagebox.showerror('Error', 'Something went wrong!\nPlease try again later.')
                self.on_closing()
            
        self.clear_frame()
        
        Grid.columnconfigure(self.root, 0, weight=1)
        Grid.columnconfigure(self.root, 1, weight=3)
        
        ttk.Label(self.root, text='Please enter your App Password', anchor='center').grid(column=0, row=0, columnspan=2, sticky='news')
        
        ttk.Label(self.root, text='Password').grid(column=0, row=1, sticky='news')
        text_entry_pwd = StringVar()
        ttk.Entry(self.root, show='*', textvariable=text_entry_pwd).grid(column=1, row=1, sticky='news')
        
        ttk.Button(self.root, text='Unlock', command=check_app_pwd).grid(column=0, row=2, columnspan=2, sticky='news')
        ttk.Button(self.root, text='Close', command=self.on_closing).grid(column=0, row=3, columnspan=2, sticky='news')

    def set_app_pwd_render(self):
        def set_app_pwd():
            nonlocal text_entry_pwd, text_entry_rpwd
            pwd = str(text_entry_pwd.get())
            rpwd = str(text_entry_rpwd.get())
            if pwd != rpwd:
                messagebox.showerror('Error', 'Password does not match!')
                return False
            arr = [{'app_pwd':pwd}]
            if self.store_data.save(arr, self.file_store):
                self.main_menu_render()
            else:
                messagebox.showerror('Error', 'Something went wrong!\nPlease try again later.')
                self.on_closing()
            
        self.clear_frame()
        
        Grid.columnconfigure(self.root, 0, weight=1)
        Grid.columnconfigure(self.root, 1, weight=3)
        
        ttk.Label(self.root, text='You need to set an App Password', anchor='center').grid(column=0, row=0, columnspan=2, sticky='news')
        
        ttk.Label(self.root, text='Password').grid(column=0, row=1, sticky='news')
        text_entry_pwd = StringVar()
        ttk.Entry(self.root, show='*', textvariable=text_entry_pwd).grid(column=1, row=1, sticky='news')
        
        ttk.Label(self.root, text='Repeat Password').grid(column=0, row=2, sticky='news')
        text_entry_rpwd = StringVar()
        ttk.Entry(self.root, show='*', textvariable=text_entry_rpwd).grid(column=1, row=2, sticky='news')
        
        ttk.Button(self.root, text='Submit', command=set_app_pwd).grid(column=0, row=3, columnspan=2, sticky='news')
        ttk.Button(self.root, text='Close', command=self.on_closing).grid(column=0, row=4, columnspan=2, sticky='news')
    

    def change_app_pwd_render(self):
        def change_app_pwd():
            nonlocal text_entry_opwd, text_entry_pwd, text_entry_rpwd
            opwd = str(text_entry_opwd.get())
            pwd = str(text_entry_pwd.get())
            rpwd = str(text_entry_rpwd.get())
            if pwd != rpwd:
                messagebox.showerror('Error', 'Password does not match!')
                return False
            else:
                data = self.store_data.load(self.file_store)
                if data:
                    for i in data:
                        if type(i) is dict:
                            if i['app_pwd'] == opwd:
                                break
                            else:
                                messagebox.showerror('Error', 'Old password is incorrect!')
                                return False
                    arr = [{'app_pwd':pwd}]
                    for i in data:
                        if type(i) is not dict:
                            arr.append(i)
                    if self.store_data.save(arr, self.file_store):
                        messagebox.showinfo('Info', 'App password has been changed!')
                        self.main_menu_render()
                    else:
                        messagebox.showerror('Error', 'Something went wrong!\nPlease try again later.')
                        return False
                else:
                    messagebox.showerror('Error', 'Something went wrong!\nPlease try again later.')
                    return False
                    
        self.clear_frame()
        
        Grid.columnconfigure(self.root, 0, weight=1)
        Grid.columnconfigure(self.root, 1, weight=3)
        
        ttk.Label(self.root, text='Change your App Password', anchor='center').grid(column=0, row=0, columnspan=2, sticky='news')

        ttk.Label(self.root, text='Old Password').grid(column=0, row=1, sticky='news')
        text_entry_opwd = StringVar()
        ttk.Entry(self.root, show='*', textvariable=text_entry_opwd).grid(column=1, row=1, sticky='news')
        
        ttk.Label(self.root, text='New Password').grid(column=0, row=2, sticky='news')
        text_entry_pwd = StringVar()
        ttk.Entry(self.root, show='*', textvariable=text_entry_pwd).grid(column=1, row=2, sticky='news')
        
        ttk.Label(self.root, text='Repeat Password').grid(column=0, row=3, sticky='news')
        text_entry_rpwd = StringVar()
        ttk.Entry(self.root, show='*', textvariable=text_entry_rpwd).grid(column=1, row=3, sticky='news')
        
        ttk.Button(self.root, text='Submit', command=change_app_pwd).grid(column=0, row=4, columnspan=2, sticky='news')
        ttk.Button(self.root, text='Close', command=self.main_menu_render).grid(column=0, row=5, columnspan=2, sticky='news')
        
    def on_closing(self):
        self.terminated = True
        self.root.quit()
        self.root.destroy()
        raise SystemExit

    def clear_frame(self):
        Grid.columnconfigure(self.root, 0, weight=1)
        Grid.columnconfigure(self.root, 1, weight=0)
        for widget in self.root.winfo_children():
            widget.destroy()
            
    def process_secret_key(self, account_name, secret_key, secret_type):
        secret_key = re.sub('[^A-Za-z0-9]+', '', secret_key)
        if secret_type != 'totp' and secret_type != 'hotp':
            messagebox.showerror('Error', 'Invalid key type!')
            return False
        elif len(secret_key) % 2 != 0:
            self.scan_terminated = True
            messagebox.showerror('Error', 'Invalid secret key!')
            return False
        elif secret_key:
            try:
                if secret_type == 'totp':
                    otp = pyotp.TOTP(secret_key).now()
                elif secret_type == 'hotp':
                    self.scan_terminated = True
                    messagebox.showerror('Error', 'We currently only support TOTP 2FA!')
            except:
                self.scan_terminated = True
                messagebox.showerror('Error', 'Invalid secret key!')
                return False
            arr = self.store_data.load(self.file_store)
            if arr != False:
                tmp = [account_name, secret_key, secret_type]
                if tmp not in arr:
                    for e in arr:
                        try:
                            (exist_account_name, _, _) = e
                        except:
                            continue
                        if exist_account_name == account_name:
                            self.scan_terminated = True
                            messagebox.showerror('Error', 'Account already exists.')
                            return False
                    arr.append(tmp)
                else:
                    self.scan_terminated = True
                    messagebox.showerror('Error', 'Account already exists.')
                    return False
                if self.store_data.save(arr, self.file_store):
                    messagebox.showinfo('Info', 'New account added!')
                    return True
                else:
                    self.scan_terminated = True
                    messagebox.showerror('Error', 'Something went wrong!\nPlease try again later.')
                    return False
            else:
                self.scan_terminated = True
                messagebox.showerror('Error', 'Something went wrong!\nPlease try again later.')
                return False

    def process_QR_code(self, codes):
        contain_code = False
        for code in codes:
            if 'otpauth://' in code:
                secret_type = unquote(code[code.find('://')+3:code.find('/', code.find('://')+3)])
                username = unquote(code[code.find('/', code.find('://')+4)+1:code.find('?', code.find('/')+1)])
                info = code[code.find('?', code.find('/')+1)+1:].split('&')
                secret_key = ''
                issuer = ''
                for i in info:
                    if 'secret' in i:
                        secret_key = unquote(i.replace('secret=', ''))
                    elif 'issuer' in i:
                        issuer = unquote(i.replace('issuer=', ''))
                account_name = ''
                if not secret_key:
                    continue
                elif not username:
                    continue
                elif not issuer:
                    account_name = username
                elif issuer and username:
                    account_name = issuer + ' (' + username + ')'
                if account_name:
                    contain_code = True
                    if self.process_secret_key(account_name, secret_key, secret_type):
                        self.main_menu_render()
                        break
                    else:
                        return False
        if contain_code:
            return True
        else:
            messagebox.showerror('Error', 'Invaid QR code!')
            self.scan_terminated = True
            return False
            
        
    def retrieve_data(self):
        data = self.store_data.load(self.file_store)
        if data:
            data_changed = False
            if self.tmp_account_name != data:
                data_changed = True
                self.tmp_account_name = data
                self.listbox_account_name.delete(0, END)
            for i in range(len(data)):
                if type(data[i]) is dict:
                    continue
                account_name = data[i][0]
                secret_key = data[i][1]
                secret_type = data[i][2]
                if secret_type == 'totp':
                    otp = pyotp.TOTP(secret_key)
                    otp_code = str(otp.now())
                    otp_code = ' '.join([otp_code[i:i+3] for i in range(0, len(otp_code), 3)])
                    time_remaining = otp.interval - time.time() % otp.interval
                    if self.is_show_code:
                        self.progbar_show_code['value'] = time_remaining * 100 / otp.interval
                    else:
                        self.progbar_show_code['value'] = 0
                    if self.is_show_code and self.account_show_code == account_name and otp_code != self.text_entry_show_code.get():
                        self.is_show_code = False
                        self.text_entry_show_code.set('*** ***')
                    if data_changed:
                        self.listbox_account_name.insert(END, account_name)
                #whatabout hotp
        elif data == []:
            self.listbox_account_name.delete(0, END)
        else:
            messagebox.showerror('Error', 'Something went wrong!\nPlease try again later.')
            return False

    def update_code(self):
        while not self.terminated:
            try:
                self.retrieve_data()
            except:
                pass
            time.sleep(1)

    def add_scan_menu_render(self):
        def add_scan(): # take screenshot
            self.scan_terminated = False
            def cancel_scan():
                self.scan_terminated = True
                
            self.clear_frame()
            
            ttk.Label(self.root, text='SWITCH TO YOUR BROWSER', anchor=CENTER, background='green', foreground='white').grid(column=0, row=0, sticky='news')
            ttk.Label(self.root, text='We will take screenshot', anchor=CENTER).grid(column=0, row=1, sticky='news')
            ttk.Label(self.root, text='and automatically detect QR code', anchor=CENTER).grid(column=0, row=2, sticky='news')
            btn_cancel = ttk.Button(self.root, text='Cancel', command=cancel_scan)
            btn_cancel.grid(column=0, row=3, sticky='news')

            codes = []
            timer = time.time()
            while not codes and not self.scan_terminated:
                if time.time() - timer >= 1:
                    timer = time.time()
                    codes = ScanQR().scan(0)
                    if codes and self.process_QR_code(codes):
                        self.main_menu_render()
                        break
                    else:
                        codes = []
                self.root.update()
                time.sleep(.1)
            
            if self.scan_terminated:
                self.add_scan_menu_render()
                
        def add_image(): # promt user to open image
            img_path = askopenfilename()
            codes = ScanQR().scan(1, img_path)
            if codes:
                if self.process_QR_code(codes):
                    self.main_menu_render()
            else:
                messagebox.showerror('Error', 'Cannot interpret QR code!')
                return False

        self.clear_frame()
        
        ttk.Button(self.root, text='Take screenshot (Auto detect QR code)', command=add_scan).grid(column=0, row=0, sticky='news')
        ttk.Button(self.root, text='Import image', command=add_image).grid(column=0, row=1, sticky='news')
        ttk.Button(self.root, text='Cancel', command=self.main_menu_render).grid(column=0, row=2, sticky='news')

    def add_key_menu_render(self):
        def add_key(): # entry, enter key
            nonlocal text_entry_acc, text_entry_key
            account_name = text_entry_acc.get()
            secret_key = text_entry_key.get()

            if account_name and secret_key:
                if self.process_secret_key(account_name, secret_key, 'totp'):
                    self.main_menu_render()
                    
        self.clear_frame()
        
        Grid.columnconfigure(self.root, 0, weight=1)
        Grid.columnconfigure(self.root, 1, weight=3)
        
        ttk.Label(self.root, text='Account Name').grid(column=0, row=0, sticky='news')
        text_entry_acc = StringVar()
        ttk.Entry(self.root, textvariable=text_entry_acc).grid(column=1, row=0, sticky='news')
        
        ttk.Label(self.root, text='Secret Key').grid(column=0, row=1, sticky='news')
        text_entry_key = StringVar()
        ttk.Entry(self.root, textvariable=text_entry_key).grid(column=1, row=1, sticky='news')
        
        ttk.Button(self.root, text='Add', command=add_key).grid(column=0, row=2, columnspan=2, sticky='news')
        ttk.Button(self.root, text='Cancel', command=self.main_menu_render).grid(column=0, row=3, columnspan=2, sticky='news')
    
    def url_catcher_menu_render(self):
        def add_url():
            def close_toplevel():
                nonlocal tmp_window
                tmp_window.destroy()
            def add_url():
                nonlocal text_entry_website_name, text_entry_url
                website_name = text_entry_website_name.get()
                url = text_entry_url.get().split(',')
                with open(self.url_list_filename, 'a') as f:
                    f.write(website_name + '|-*-|' + ('|-*-|').join(url) + '\n')
                close_toplevel()
                self.url_catcher_menu_render()
            tmp_window = Toplevel(self.root)
            tmp_window.title("Authenticator - Add URL")
            tmp_window.geometry('800x200+200+200')
            tmp_window.resizable(False, False)
            tmp_window.protocol("WM_DELETE_WINDOW", close_toplevel)

            Grid.columnconfigure(tmp_window, 0, weight=1)
            Grid.columnconfigure(tmp_window, 1, weight=3)
            
            ttk.Label(tmp_window, text='Website Name (Issuer)').grid(column=0, row=0, sticky='news')
            text_entry_website_name = StringVar()
            ttk.Entry(tmp_window, textvariable=text_entry_website_name).grid(column=1, row=0, sticky='news')
            
            ttk.Label(tmp_window, text='URL').grid(column=0, row=1, sticky='news')
            text_entry_url = StringVar()
            ttk.Entry(tmp_window, textvariable=text_entry_url).grid(column=1, row=1, sticky='news')
            
            ttk.Button(tmp_window, text='Add', command=add_url).grid(column=0, row=2, columnspan=2, sticky='news')
            ttk.Button(tmp_window, text='Cancel', command=close_toplevel).grid(column=0, row=3, columnspan=2, sticky='news')

        def modify_url():
            pass

        def remove_url():
            pass
        
        self.clear_frame()
        
        ttk.Label(self.root, text='Website Name - URL', anchor='center').grid(column=0, row=0, columnspan=3, sticky='news')

        listbox_web_url = Listbox(self.root)
        listbox_web_url.grid(column=0, row=1, columnspan=3, sticky='news')

        try:
            for line in open(self.url_list_filename, 'r'):
                line = line.strip().split('|-*-|')
                website_name = line[0]
                url = str(line[1:])
                listbox_web_url.insert(END, website_name + " - " + url)
        except:
            open(self.url_list_filename, 'w').close()
                

        scrollbar = ttk.Scrollbar(self.root, orient="vertical")
        scrollbar.grid(column=4, row=1, sticky='news')
        listbox_web_url.config(yscrollcommand=scrollbar.set)

        ttk.Button(self.root, text='Add', command=add_url).grid(column=0, row=2, sticky='news')
        ttk.Button(self.root, text='Modify', command=modify_url).grid(column=1, row=2, sticky='news')
        ttk.Button(self.root, text='Remove', command=remove_url).grid(column=2, row=2, sticky='news')
        
        ttk.Button(self.root, text='Cancel', command=self.main_menu_render).grid(column=0, row=3, columnspan=3, sticky='news')        
        
    def main_menu_render(self):
        def copy_code():
            account_name = self.listbox_account_name.get(ACTIVE)
            if account_name:
                data = self.store_data.load(self.file_store)
                if data:
                    for i in data:
                        if type(i) is dict:
                            continue
                        if account_name == i[0]:
                            secret_key = i[1]
                            otp = pyotp.TOTP(secret_key)
                            pyperclip.copy(str(otp.now()))
                elif data == False:
                    messagebox.showerror('Error', 'Something went wrong!\nPlease try again later.')
                    
        def show_code():
            account_name = self.listbox_account_name.get(ACTIVE)
            if account_name:
                data = self.store_data.load(self.file_store)
                if data:
                    for i in data:
                        if type(i) is dict:
                            continue
                        if account_name == i[0]:
                            secret_key = i[1]
                            otp = pyotp.TOTP(secret_key)
                            time_remaining = otp.interval - time.time() % otp.interval
                            self.progbar_show_code['value'] = time_remaining * 100 / otp.interval
                            otp_code = str(otp.now())
                            otp_code = ' '.join([otp_code[i:i+3] for i in range(0, len(otp_code), 3)])
                            self.text_entry_show_code.set(otp_code)
                            self.is_show_code = True
                            self.account_show_code = account_name
                elif data == False:
                    messagebox.showerror('Error', 'Something went wrong!\nPlease try again later.')
                
        def show_key():
            account_name = self.listbox_account_name.get(ACTIVE)
            if account_name:
                confirmation = messagebox.askyesno('Warning', 'Are you sure you want to show the secret key of "' + str(account_name) + '"')
                if confirmation:
                    data = self.store_data.load(self.file_store)
                    if data:
                        for i in data:
                            if type(i) is dict:
                                continue
                            if account_name == i[0]:
                                secret_key = i[1]
                                secret_key_spaced = ' '.join([secret_key[i:i+4] for i in range(0, len(secret_key), 4)])
                                def copy_code():
                                    nonlocal secret_key_spaced
                                    pyperclip.copy(str(secret_key_spaced).upper())
                                def close_toplevel():
                                    nonlocal tmp_window
                                    tmp_window.destroy()
                                tmp_window = Toplevel(self.root)
                                tmp_window.title("Authenticator - Secret Key")
                                tmp_window.geometry('500x500+200+200')
                                tmp_window.resizable(False, False)
                                tmp_window.protocol("WM_DELETE_WINDOW", close_toplevel)
                                Grid.rowconfigure(tmp_window, 0, weight=1)
                                Grid.columnconfigure(tmp_window, 0, weight=1)
                                img = qrcode.make('otpauth://totp/' + str(account_name) + '?secret=' + str(secret_key))
                                img = img.resize((350, 350), Image.ANTIALIAS)
                                img = Image.fromarray(np.uint8(img)*255)
                                img = ImageTk.PhotoImage(img)                         
                                canvas = Canvas(tmp_window, width=350, height=350)
                                canvas.grid(column=0, row=0, sticky='news')
                                canvas.create_image(250, 190, image=img)
                                canvas.image = img
                                entry = ttk.Entry(tmp_window, justify='center')
                                entry.insert(0, str(secret_key_spaced).upper())
                                entry.configure(state='readonly')
                                entry.grid(column=0, row=1, sticky='news')
                                ttk.Button(tmp_window, text='Copy', command=copy_code).grid(column=0, row=2, sticky='news')
                                ttk.Button(tmp_window, text='Close', command=close_toplevel).grid(column=0, row=3, sticky='news')
                    elif data == False:
                        messagebox.showerror('Error', 'Something went wrong!\nPlease try again later.')
                        
        def remove_account():
            account_name = self.listbox_account_name.get(ACTIVE)
            if account_name:
                confirmation = messagebox.askyesno('Warning!','Are you sure you want to delete "' + str(account_name) + '"')
                if confirmation:
                    data = self.store_data.load(self.file_store)
                    if data:
                        arr = []
                        for i in data:
                            if type(i) is dict or i[0] != account_name:
                                arr.append(i)
                        self.store_data.save(arr, self.file_store)
                        self.is_show_code = False
                        self.progbar_show_code['value'] = 0
                        self.text_entry_show_code.set('*** ***')
                    elif data == False:
                        messagebox.showerror('Error', 'Something went wrong!\nPlease try again later.')

        def auto_enter_account():
            if self.auto_enter_code: # if ON
                self.btn_enter_code.configure(text='Detect 2FA code: OFF')
                self.auto_enter_code = not self.auto_enter_code
            else: # if OFF
                self.btn_enter_code.configure(text='Detect 2FA code: ON')
                self.auto_enter_code = not self.auto_enter_code

        self.clear_frame()
        self.tmp_account_name = []
        
        ttk.Button(self.root, text='Scan a QR code', command=self.add_scan_menu_render).grid(column=0, row=0, sticky='news')
        ttk.Button(self.root, text='Enter a setup key', command=self.add_key_menu_render).grid(column=0, row=1, sticky='news')
        ttk.Button(self.root, text='URL Catcher', command=self.url_catcher_menu_render).grid(column=0, row=2, sticky='news')
        self.btn_enter_code = ttk.Button(self.root, text='Detect 2FA code: OFF', command=auto_enter_account)
        self.btn_enter_code.grid(column=0, row=3, sticky='news')

        ttk.Button(self.root, text='Change App Password', command=self.change_app_pwd_render).grid(column=0, row=4, sticky='news')
        
        iframe = Frame(self.root)
        iframe.grid(column=0, row=6, sticky='news')
        Grid.rowconfigure(iframe, 0, weight=1)
        Grid.columnconfigure(iframe, 0, weight=1)

        self.listbox_account_name = Listbox(iframe)
        self.listbox_account_name.grid(column=0, row=0, sticky='news')

        scrollbar = ttk.Scrollbar(iframe, orient="vertical")
        scrollbar.grid(column=2, row=0, sticky='news')
        self.listbox_account_name.config(yscrollcommand=scrollbar.set)
        
        iframe = Frame(self.root)
        iframe.grid(column=0, row=7, sticky='news')
        Grid.rowconfigure(iframe, 0, weight=1)
        Grid.columnconfigure(iframe, 0, weight=1)
        Grid.columnconfigure(iframe, 1, weight=1)
        Grid.columnconfigure(iframe, 2, weight=1)
        Grid.columnconfigure(iframe, 3, weight=1)

        self.text_entry_show_code = StringVar()
        self.entry_show_code = ttk.Entry(iframe, textvariable=self.text_entry_show_code, justify='center', state='readonly')
        self.text_entry_show_code.set('*** ***')
        self.entry_show_code.grid(column=0, row=0, columnspan=4, sticky='news')

        self.progbar_show_code = ttk.Progressbar(iframe, orient=HORIZONTAL, length=100, mode='determinate')
        self.progbar_show_code['value'] = 0
        self.progbar_show_code.grid(column=0, row=1, columnspan=4, sticky='news')
        
        ttk.Button(iframe, text='Copy code', command=copy_code).grid(column=0, row=2, sticky='news')
        ttk.Button(iframe, text='Show code', command=show_code).grid(column=1, row=2, sticky='news')
        ttk.Button(iframe, text='Show secret key', command=show_key).grid(column=2, row=2, sticky='news')
        ttk.Button(iframe, text='Remove account', command=remove_account).grid(column=3, row=2, sticky='news')

        self.retrieve_data()


if __name__ == '__main__':
    GUI()
