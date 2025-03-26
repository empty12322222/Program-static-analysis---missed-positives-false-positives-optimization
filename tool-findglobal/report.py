#测试主函数
import analyze_fie
import order_fun
import global_point
import clang.cindex
import Preliminary_sifting
import is_free_befor
import other_point
import print_warning
def report(file_path,code_path,log_file):
    # file_path = 'D:/code/c++/project/malloc_mssa1.txt'  # 替换为你的文件路径
    # path = 'D:/code/c++/'
    file_path = file_path
    path = code_path
    try:
      parsed_data = analyze_fie.read_and_parse(file_path)
        
    except FileNotFoundError:
        print(f"Report a path{file_path} error!")
    for key in parsed_data:
        path_key = path +key
        index = clang.cindex.Index.create()
        try:
          tu = index.parse(path_key)
        except clang.cindex.TranslationUnitLoadError as e:
            print(f"The source file{path_key} doesn't exist!")
        execution_order,gloabal_ = order_fun.get_function_execution_order(tu, parsed_data[key])
        point_fun,glo_point=global_point.global_point(tu,execution_order,gloabal_)

        #初步过筛
        glo_point = Preliminary_sifting.Preliminary_sifting(glo_point)
        point_fun =Preliminary_sifting.Preliminary_sifting(point_fun)
        for global_name in glo_point:
            list_point = glo_point[global_name][::-1]
            list_funname = point_fun[global_name][::-1]
            for i in range(len(list_point)):
                # print(f"分析函数{list_funname[i]}")
                if i<len(list_point) -1 and (is_free_befor.analyze_pointer_usage(tu,global_name,list_point[i],list_funname[i])==False or other_point.analyze_pointer_other(tu,global_name,list_funname[i])==False):
                    #告警，需要告警————————————————————————————————————————————————
                    context = f"在文件{key}中函数{list_funname[i]}，使用全局指针{global_name}前未得到有效释放，也就是在{list_funname[i+1]}这个函数中申请的空间传递给了全局变量，但是没有释放"
                    print_warning.print_warning(log_file,context)
                    print(f"在文件{key}中函数{list_funname[i]}，使用全局指针{global_name}前未得到有效释放，也就是在{list_funname[i+1]}这个函数中申请的空间传递给了全局变量，但是没有释放")
                if i == len(list_point) -1 and other_point.analyze_pointer_other(tu,global_name,list_funname[i]):
                     context = f"在文件{key}中函数{list_funname[i]}，改变了全局变量的指向，造成了内存泄漏"
                     print_warning.print_warning(log_file,context)
                     print(f"在文件{key}中函数{list_funname[i]}，改变了全局变量的指向，造成了内存泄漏")




        
        

    return point_fun,glo_point


