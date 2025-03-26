#分析有问题的函数中的全局变量是如何指向
import clang.cindex
# import analyze2

class MyVisitor:
    def __init__(self,global_list):
        self.__in_function = False  # 是否处于函数体内部
        self.__current_function = None  # 当前函数名
        self.__assignments = {}  # 存储函数名和赋值的右侧表达式
        self.__variables = {}
        self.__global_list = global_list



    def visit(self, cursor,function_name):
        # 检查是否是函数声明
        if cursor.kind.name == 'FUNCTION_DECL':
            # 检查函数是否在全局或命名空间的根级别
            if cursor.semantic_parent.kind.name == 'TRANSLATION_UNIT' or cursor.semantic_parent.kind.name == 'NAMESPACE':
                self.__in_function = True  # 进入函数体
                # 打印函数名和位置
                self.__current_function = cursor.spelling
                # print(f"Custom Function: {cursor.spelling} at {cursor.location.file}:{cursor.location.line}")
                if function_name and self.__current_function != function_name:
                    self.__in_function = False
        
        # 如果不在函数体内部以及不是问题函数，不处理
        if not self.__in_function :
            for c in cursor.get_children():
                self.visit(c,function_name)
            return

        if cursor.kind == clang.cindex.CursorKind.BINARY_OPERATOR and any(token.spelling == '=' for token in cursor.get_tokens()):
            children = list(cursor.get_children())
            
                    # 确保子节点列表中有足够的元素
            if len(children) >= 2:
                        lhs = children[0]  # 赋值的左侧表达式
                        rhs = children[1]  # 赋值的右侧表达式
                        # 打印左侧和右侧表达式的拼写
                        if rhs.kind == clang.cindex.CursorKind.CSTYLE_CAST_EXPR:
                            # 获取类型转换表达式的子节点
                            rhs_children = list(rhs.get_children())
                            if rhs_children:
                                # 使用子节点作为实际的右侧表达式
                                rhs = rhs_children[0]
                        if self.__current_function and lhs.spelling in self.__global_list:
                            
                            #记录键为空间，值为当前函数名
                            self.__assignments.setdefault(lhs.spelling, []).append(self.__current_function)
                            #记录键为全局变量，值为指向空间
                            self.__variables.setdefault(lhs.spelling, []).append(rhs.spelling)
                        
                        # print(f"The pointer points to: {lhs.spelling} ---> {rhs.spelling}")




        # 继续遍历子节点
        for c in cursor.get_children():
            self.visit(c,function_name)

        # 检查是否是函数体的结束
        if cursor.kind == clang.cindex.CursorKind.COMPOUND_STMT and self.__in_function:
            self.__in_function = False  # 退出函数体
            self.__current_function = None  # 重置当前函数名


    def get_assignments(self):
        return self.__assignments
    
    def get_variables(self):
        return self.__variables


#调用接口，输入语法树，全局变量的列表和有问题函数列表,返回的是本文件中全局变量指向的空间名是一个字典，键空间名：函数名；第二个返回是 全局变量：指向空间
def global_point(tu,fun_list,global_list):
     visitor = MyVisitor(global_list)
     for value in fun_list:
          visitor.visit(tu.cursor,value)
     return visitor.get_assignments(),visitor.get_variables()

#测试代码
# file_path = 'D:/code/c++/2.cpp'
# index = clang.cindex.Index.create()
# tu = index.parse(file_path)
# report_fun,fun_global = report_analyze.report()


# fun_list = report_fun['2.cpp']
# global_list = fun_global['2.cpp']
# print(global_point(tu,fun_list,global_list))



     
     

     



















# def parse_file(tu):
#     visitor = MyVisitor()
#     visitor.visit(tu.cursor)
#     return visitor


# def Preliminary_judgment(tu):
#     report_fun,fun_global = report_analyze.report()
#     visitor = parse_file(tu)
#     #global_arrival 记录全局变量指向空间
#     global_arrival = visitor.get_variables()
#     #var_fun 记录空间在说的函数名
#     var_fun = visitor.get_assignments()
#     global_arrival = {key: value for key, value in global_arrival.items() if len(value) > 1}
#     print("记录代码中指向空间大于一的全局变量以及他们的指向空间")
#     print(global_arrival)
#     print("记录指向空间所在的函数")
#     print(var_fun)
#     return global_arrival,var_fun

# #需要解耦合
# def release_before(gloabl_arrival,file_path,var_fun):
#     for key, value in gloabl_arrival.items():
#         gloabl_arrival[key].reverse()
#         gloabl_arrival[key].pop(0)
#         #list指的是当前全局变量在哪些函数释放过，是一个函数名列表
#         list = analyze2.analyze_pointer_usage(file_path, key)
#         for i in range(len(value)-1):
#             if var_fun[value[i]] in list:
#                 gloabl_arrival[key].remove(value[i])
        
#         if(len(gloabl_arrival[key])==0):
#             del gloabl_arrival[key]

#     print("把用全局变量指向新的空间之前释放空间了的指向空间删除掉")
#     print(gloabl_arrival)
#     return gloabl_arrival
             
            

# if __name__ == '__main__':
    
#     file_path = 'D:/code/c++/2.cpp'
#     index = clang.cindex.Index.create()
#     tu = index.parse(file_path)    
#     global_arrival,var_fun = Preliminary_judgment(tu)
#     global_arrival = release_before(global_arrival,file_path,var_fun)
#     # print(Preliminary_judgment(tu))
    




