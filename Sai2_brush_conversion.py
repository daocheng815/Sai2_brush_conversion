# -*- coding: utf-8 -*-
from tkinter import *
from tkinter.filedialog import askdirectory, askopenfilename
from tkinter import messagebox
import os
from PIL import Image
import shutil
import configparser
import Imaging_conversion
def is_subdirectory(parent, child):
    # 檢查是否子目錄
    parent = os.path.abspath(parent)
    child = os.path.abspath(child)
    return os.path.commonpath([parent]) == os.path.commonpath([parent, child])

def selectPath(path_var, other_path_var):
    path = askdirectory()
    if path != "":
        if is_subdirectory(path, other_path_var.get()):
            messagebox.showerror("錯誤", "設定的位置不能是目標位置的子資料夾！")
        else:
            path_var.set(path.replace("/", "\\"))

def selectFilPath(path_var, other_path_var):
    path = askopenfilename()
    if path != "":
        if is_subdirectory(path, other_path_var.get()):
            messagebox.showerror("錯誤", "設定的位置不能是目標位置的子資料夾！")
        else:
            path_var.set(path.replace("/", "\\"))

def convert(input_path_var, output_path_var, ini_path_var, config):
    input_path = input_path_var.get()
    output_path = output_path_var.get()
    ini_path = ini_path_var.get()

    if is_subdirectory(ini_path, output_path):
        messagebox.showerror("錯誤", "BMP資料夾位置不能設定成INI設定檔的父資料夾！")
        return

    if is_subdirectory(output_path, ini_path):
        messagebox.showerror("錯誤", "INI設定檔位置不能設定成BMP資料夾的子資料夾！")
        return

    if input_path and output_path and ini_path:
        Imaging_conversion.convert_png_to_gray_bmp_with_copy_ini(input_path, output_path, ini_path)
        messagebox.showinfo("轉換成功", "轉換成功，請查看檔案！")
        os.startfile(output_path)  # 打開 BMP 資料夾

        # 保存最後一次使用的路徑
        config['Paths'] = {
            'InputPath': input_path,
            'OutputPath': output_path,
            'IniPath': ini_path
        }
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
    else:
        messagebox.showerror("轉換錯誤", "請選擇正確的資料夾和檔案位置")



# 檢查是否存在配置文件，如果不存在，創建一個新的
config_path = 'config.ini'
if not os.path.exists(config_path):
    # 創建一個新的配置文件
    config = configparser.ConfigParser()
    config.add_section('Paths')
    config['Paths'] = {
        'InputPath': '',
        'OutputPath': '',
        'IniPath': ''
    }
    with open(config_path, 'w') as configfile:
        config.write(configfile)
else:
    # 如果存在，讀取配置文件
    config = configparser.ConfigParser()
    config.read(config_path)

root = Tk()
root.title("SAI筆刷轉換工具")
root.resizable(width=False, height=False)

input_path_var = StringVar(value=config['Paths']['InputPath'])
output_path_var = StringVar(value=config['Paths']['OutputPath'])
ini_path_var = StringVar(value=config['Paths']['IniPath'])

Label(root, text="Png資料夾位置 :").grid(row=0, column=0)
Entry(root, textvariable=input_path_var, state="readonly").grid(row=0, column=1, ipadx=200)
Button(root, text="變更位置", command=lambda: selectPath(input_path_var, output_path_var)).grid(row=0, column=2)

Label(root, text="注意bmp資料夾位置內不能有預設ini設定檔。").grid(row=1, column=1)
Label(root, text="bmp資料夾位置 :").grid(row=2, column=0)
Entry(root, textvariable=output_path_var, state="readonly").grid(row=2, column=1, ipadx=200)
Button(root, text="變更位置", command=lambda: selectPath(output_path_var, ini_path_var)).grid(row=2, column=2)

Label(root, text="注意預設ini設定檔位置不能設置在bmp資料夾位置內。").grid(row=3, column=1)
Label(root, text="預設ini設定檔位置 :").grid(row=4, column=0)
Entry(root, textvariable=ini_path_var, state="readonly").grid(row=4, column=1, ipadx=200)
Button(root, text="變更位置", command=lambda: selectFilPath(ini_path_var, output_path_var)).grid(row=4, column=2)

Button(root, text="PNG轉換BMP", command=lambda: convert(input_path_var, output_path_var, ini_path_var, config)).grid(row=5, column=1)

root.mainloop()