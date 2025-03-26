# 读取报告文件，获得报告中的行号，文件名

import re


import clang.cindex


PATH = '/home/zhangjiangtao/projects/'
def read_and_parse(file_path):
    """
    从指定文件中读取内容，并解析为键值对形式。
    
    :param file_path: 文件路径
    :return: 解析后的键值对字典
    """
    # pattern = r'Global Reach,Carry out further judgment : dereference at : \(CallICFGNode: \{ "ln": (\d+), "cl": \d+, "fl": "([^"]+)" \}\)'
    # pattern = r'CallICFGNode: \((.*?)\)'
    pattern1 = r'"ln": (\d+)'
    pattern2 = r'"fl": "([^"]+)"'

    
    
    result_dict = {}
    
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            match1 = re.search(pattern1, line)
            match2 = re.search(pattern2, line)
            if match1 and match2 and "Global Reach,Carry out further judgment" in line:
                ln = int(match1.group(1))
                fl = match2.group(1)
                # print(ln, fl)
                
                if fl in result_dict:
                    result_dict[fl].append(ln)
                else:
                    result_dict[fl] = [ln]
    
    return result_dict






# if __name__ == "__main__":
#     file_path = 'D:/code/c++/project/malloc_mssa1.txt'  # 替换为你的文件路径
#     parsed_data = read_and_parse(file_path)
    
#     print("解析的数据:", parsed_data)


    


