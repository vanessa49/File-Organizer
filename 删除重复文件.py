import os
import hashlib

# 指定需要搜索的路径
path_to_check = "E:\\"

# 创建一个字典来存储已经找到的文件的哈希值和文件名
hashes = {}

# 遍历指定路径及其子目录中的所有文件
for foldername, subfolders, filenames in os.walk(path_to_check):
    # 忽略 "$RECYCLE.BIN" 文件夹
    if "$RECYCLE.BIN" in foldername.upper():
        continue

    for filename in filenames:
        # 忽略".inf"等后缀的文件
        if filename.lower() == "desktop.ini" or filename.lower().endswith(".inf") \
                or filename.lower().endswith(".txt") or filename.lower().endswith(".ax") \
                or filename.lower().endswith(".fli") or filename.lower().endswith(".ay") \
                or filename.lower().endswith(".mul") or filename.lower().endswith(".inc") \
                or filename.lower() == "qvinfo" or filename.lower().endswith(".qv")\
                or filename.lower().endswith(".mtd"):
            continue

        # 获取文件的全路径
        full_path = os.path.join(foldername, filename)

        # 计算文件的MD5哈希值
        hasher = hashlib.md5()
        with open(full_path, 'rb') as file:
            buf = file.read()
            hasher.update(buf)
        file_hash = hasher.hexdigest()

        # 创建一个键，该键包含文件的哈希值和文件名
        key = (file_hash, filename)

        # 如果这个键已经在字典中，那么这个文件是重复的
        if key in hashes:
            # 将重复的文件添加到键对应的列表中
            hashes[key].append(full_path)

            # 列出所有哈希值和文件名都相同的文件
            print(f"Duplicate files:")
            for i, duplicate_file in enumerate(hashes[key]):
                print(f"{i + 1}: {duplicate_file}")

            # 自动删除 "原备份" 文件夹中的文件
            original_files = [f for f in hashes[key] if "原备份" in f]
            if original_files:
                # 如果所有的重复文件都在 "原备份" 文件夹中，只保留一个
                if all("原备份" in f for f in hashes[key]):
                    for f in original_files[1:]:
                        os.remove(f)
                        print(f"Removed: {f}")
                        hashes[key].remove(f)  # 更新哈希字典，移除已经被删除的文件
                else:
                    for f in original_files:
                        os.remove(f)
                        print(f"Removed: {f}")
                        hashes[key].remove(f)  # 更新哈希字典，移除已经被删除的文件


            # 如果没有 "原备份" 文件夹中的文件，询问用户要保留哪些文件
            elif len(hashes[key]) > 1:
                files_to_keep = input("Which files do you want to keep? (enter the numbers separated by comma) ")
                files_to_keep = [int(num) - 1 for num in files_to_keep.split(",")]

                # 删除除了用户选择保留的文件以外的所有文件
                for i, duplicate_file in enumerate(hashes[key]):
                    if i not in files_to_keep:
                        os.remove(duplicate_file)
                        hashes[key].remove(duplicate_file)  # 更新哈希字典，移除已经被删除的文件
        else:
            # 如果这个键不在字典中，那么将它添加到字典中
            hashes[key] = [full_path]




