import os

# 指定需要搜索的路径
path_to_check = "E:\\"

# 遍历指定路径及其子目录中的所有文件夹
for foldername, subfolders, filenames in os.walk(path_to_check, topdown=False):
    # 如果一个文件夹是空的，就删除它
    if not subfolders and not filenames:
        print(f"Removing empty folder: {foldername}")
        os.rmdir(foldername)
