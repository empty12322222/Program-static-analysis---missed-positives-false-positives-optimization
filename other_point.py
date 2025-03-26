#用来分析别名中是否有被释放的

import clang.cindex


class PointerVisitor:
        def __init__(self,):
            self.__pointer_freed = False
            self.__current_function = None
            self.__aliases = {}
            self.__in_function = False

        def visit(self, cursor,pointer_name,function_name):
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
            
            # 如果不在函数体内部，不处理
            if not self.__in_function:
                for c in cursor.get_children():
                    self.visit(c,pointer_name,function_name)
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
                            if self.__current_function:
                                #记录键为空间，值为当前函数名
                                if(rhs.spelling == pointer_name or rhs.spelling in self.__aliases.get(pointer_name,[])):
                                     if lhs.spelling not in self.__aliases.get(pointer_name,[]):
                                        self.__aliases.setdefault(pointer_name, []).append(lhs.spelling)
                                
                            # print(f"The pointer points to: {lhs.spelling} ---> {rhs.spelling}")
            elif cursor.kind.name == 'CALL_EXPR':
                 for arg in cursor.get_arguments():
                      if arg.kind.name == 'UNEXPOSED_EXPR' and any(token.spelling == 'free' for token in cursor.get_tokens()):
                           aliases = self.__aliases.get(pointer_name)
                           if aliases and any(token.spelling in aliases for token in cursor.get_tokens()):
                                #之前的空间其实得到了释放
                                self.__pointer_freed = True
                                del self.__aliases[pointer_name]



            # 继续遍历子节点
            for c in cursor.get_children():
                self.visit(c,pointer_name,function_name)

            # 检查是否是函数体的结束
            if cursor.kind == clang.cindex.CursorKind.COMPOUND_STMT and self.__in_function:
                self.in_function = False  # 退出函数体
                self.__current_function = None  # 重置当前函数名
        def get_point_freed(self):
             return self.__pointer_freed



#别名分析，分析当前函数中，是否出现了别的指针指向了全局变量并释放了之前的空间
def analyze_pointer_other(tu, pointer_name,function_name):
    # 创建索引


    
    visitor = PointerVisitor()
    
    visitor.visit(tu.cursor,pointer_name,function_name)
    # print(visitor.get_point_freed())
    return visitor.get_point_freed()
# file_path = 'D:/code/c++/3.cpp'
# pointer_name = 'globalContent'  # 假设我们要检查的指针名为'oldPointer'
# function_name ='allocateAndStore'
# index = clang.cindex.Index.create()

#     # 解析文件
# tu = index.parse(file_path)
# print(analyze_pointer_other(tu, pointer_name,function_name))