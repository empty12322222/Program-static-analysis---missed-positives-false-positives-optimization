# 定义要写入文件的内容
# content = "Hello, World!"

# # 指定文件名
# file_name = "test_file.txt"
def print_warning(file_name,content):
    try:
        # 打开文件并追加内容（如果文件不存在则新建）
        with open(file_name, 'a', encoding='utf-8') as file:
            file.write("\n"+content)
        
    except Exception as e:
        print(f"记录日志发生错误：{e}")