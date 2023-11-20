from PIL import Image
import os
import shutil

def convert_png_to_gray_bmp_with_copy_ini(png_folder, bmp_folder, ini_file):
    if not os.path.exists(bmp_folder):
        os.makedirs(bmp_folder)

    png_files = [f for f in os.listdir(png_folder) if f.endswith('.png')]

    for png_file in png_files:
        png_path = os.path.join(png_folder, png_file)

        img = Image.open(png_path)

        # 轉換為 "RGBA" 模式以確保透明度信息在 alpha 通道中
        img = img.convert("RGBA")

        # 建立一個新的白色背景圖像
        white_bg = Image.new("RGBA", img.size, (255, 255, 255, 255))

        # 將原始圖像放在白色背景上，這樣透明區域會變成白色
        img = Image.alpha_composite(white_bg, img)

        # 提取 alpha 通道
        alpha = img.split()[3]

        # 將透明度轉換為灰階值
        gray_alpha = alpha.convert("L")

        # 使用 Image.point 來轉換灰階值
        converted_alpha = gray_alpha.point(lambda i: 255 - i)

        # 將新的 alpha 通道放回原始圖像
        img.putalpha(converted_alpha)

        # 進行顏色的黑白互換
        img = Image.eval(img, lambda x: 255 - x)

        # 檢測圖片大小是否大於1024*1024，如果是則等比縮放
        if img.size[0] > 1024 or img.size[1] > 1024:
            img.thumbnail((1024, 1024))

        # 將圖片轉換為 8 位灰度的 BMP 位圖文件
        img = img.convert("L")

        bmp_file = os.path.splitext(png_file)[0] + '.bmp'
        bmp_path = os.path.join(bmp_folder, bmp_file)

        # 將圖片保存
        img.save(bmp_path, 'BMP')

        # 複製 ini 檔案到相同的目錄，檔案名稱相同（替換副檔名）
        ini_name = os.path.splitext(png_file)[0] + '.ini'
        ini_path_src = ini_file
        ini_path_dst = os.path.join(bmp_folder, ini_name)
        shutil.copy2(ini_path_src, ini_path_dst)