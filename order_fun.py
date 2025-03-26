#根据行号判断其所在函数的执行顺序
import clang.cindex

class FunctionLocatorVisitor:
    def __init__(self, line_list):
        self.__line_list = line_list
        self.__functions_at_lines = {}  # 存储行号对应的函数名
        self.__execution_order = []  # 存储函数的执行顺序
        self.__global_variables = []

    def find_last_line(self, cursor):
        # 递归查找最后一个子节点的行号
        last_line = cursor.location.line
        for c in cursor.get_children():
            last_line = max(last_line, self.find_last_line(c))
        return last_line

    def visit_FunctionDecl(self, cursor):
        # 获取函数的起始行号和结束行号
        start_line = cursor.location.line
        end_line = self.find_last_line(cursor)
        
        # 检查给定的行号是否在函数的起始和结束位置之间
        for line in self.__line_list:
            if start_line <= line <= end_line:
                # 如果是，则记录这个函数
                self.__functions_at_lines[line] = cursor.spelling

    def visit_CallExpr(self, cursor):
        # 获取函数名
        callee = cursor.referenced
        if callee and callee.kind.name == 'FUNCTION_DECL':
            function_name = callee.spelling
            # 检查这个函数是否在我们记录的函数中
            if function_name in self.__functions_at_lines.values():
                self.__execution_order.append(function_name)
    def visit_VarDecl(self, cursor):
        # 检查当前节点是否是变量声明且在全局作用域
        if (cursor.kind == clang.cindex.CursorKind.VAR_DECL and
                cursor.semantic_parent.kind.name == 'TRANSLATION_UNIT'):
            # 获取变量的名称
            var_name = cursor.spelling
            # 添加到全局变量列表中
            self.__global_variables.append(var_name)

    def get_execution_order(self):
        return self.__execution_order
    
    def get_global_variables(self):
        return self.__global_variables


#调用接口，输入抽象语法树，和列表指的是所在行  返回的是文件里的按执行顺序的行所在的函数名和文件里的全局变量名
def get_function_execution_order(tu, line_list):
    # 创建索引

    visitor = FunctionLocatorVisitor(line_list)
    
    # 遍历AST查找函数声明和函数调用
    for cursor in tu.cursor.walk_preorder():
        if cursor.kind == clang.cindex.CursorKind.FUNCTION_DECL:
            visitor.visit_FunctionDecl(cursor)
        elif cursor.kind == clang.cindex.CursorKind.CALL_EXPR:
            visitor.visit_CallExpr(cursor)
        elif cursor.kind == clang.cindex.CursorKind.VAR_DECL and cursor.semantic_parent.kind.name == 'TRANSLATION_UNIT':
            visitor.visit_VarDecl(cursor)    
    # 返回函数的执行顺序
    return visitor.get_execution_order(), visitor.get_global_variables()

# 测试
# file_path = "D:/code/c++/2.cpp"  # 替换为你的C/C++文件路径
# line_list = [10, 26]  # 替换为你的函数行列表
# index = clang.cindex.Index.create()
#     # 解析文件
# tu = index.parse(file_path)
# # 获取函数的执行顺序
# execution_order, global_vars = get_function_execution_order(tu, line_list)
# print("Custom function execution order:", execution_order)
# print("Global variables:", global_vars)