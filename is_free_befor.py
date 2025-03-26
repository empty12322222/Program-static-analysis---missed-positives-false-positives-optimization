#判断指向空间前是否释放之前的空间
import clang.cindex


class PointerVisitor:
        def __init__(self):
            self.__pointer_freed = False
            self.__current_function = None
            self.__in_function = False

        def visit(self, cursor,pointer_name,point_by,function_name):
            # 检查是否是函数声明
            if cursor.kind.name == 'FUNCTION_DECL':
                # 如果是自定义函数（不在任何其他函数内部），则记录函数名
                if cursor.semantic_parent.kind.name == 'TRANSLATION_UNIT' or cursor.semantic_parent.kind.name == 'NAMESPACE':
                  self.__in_function = True  # 进入函数体
                # 打印函数名和位置
                  self.__current_function = cursor.spelling
                # print(f"Custom Function: {cursor.spelling} at {cursor.location.file}:{cursor.location.line}")
                if function_name and self.__current_function != function_name:
                    self.__in_function = False
            
            # 如果不在自定义函数内部，不处理
            if not self.__in_function :
                for c in cursor.get_children():
                    self.visit(c,pointer_name,point_by,function_name)
                return
            
            # 检查是否是指向该空间之前
            if cursor.kind == clang.cindex.CursorKind.BINARY_OPERATOR and any(token.spelling == '=' for token in cursor.get_tokens()):
                children = list(cursor.get_children())
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
                        if lhs.spelling == pointer_name and rhs.spelling == point_by:
                             return
                                
                                
                        


            # 检查是否是free()函数调用
            elif cursor.kind.name == 'CALL_EXPR':

                for arg in cursor.get_arguments():
                   if arg.kind.name == 'UNEXPOSED_EXPR' and any(token.spelling == 'free' for token in cursor.get_tokens()) and any(token.spelling == pointer_name for token in cursor.get_tokens()):
                        self.__pointer_freed = True
                        # print(self.pointer_freed)
                        break

            for c in cursor.get_children():
               self.visit(c,pointer_name,point_by,function_name)
            if cursor.kind == clang.cindex.CursorKind.COMPOUND_STMT and self.__in_function:
                self.__in_function = False  # 退出函数体
                self.__current_function = None  # 重置当前函数名
        def get_pointer_freed(self):
             return self.__pointer_freed






#检查在function_name中全局变量在指向新空间之前有无被释放
def analyze_pointer_usage(tu, pointer_name,point_by,function_name):
    visitor = PointerVisitor()
    
    visitor.visit(tu.cursor,pointer_name,point_by,function_name)
    # print(visitor.get_pointer_freed())
    return visitor.get_pointer_freed() 
# 检查指针是否在重新赋值前被释放


# --------------------------------------测试--------------------------------------

# file_path = 'D:/code/c++/1.cpp'
# pointer_name = 'globalContent'  
# point_by = 'localPtr2'
# function_name = 'reallocateAndStore'
# index = clang.cindex.Index.create()

#     # 解析文件
# tu = index.parse(file_path)
# print(analyze_pointer_usage(tu, pointer_name,point_by,function_name))