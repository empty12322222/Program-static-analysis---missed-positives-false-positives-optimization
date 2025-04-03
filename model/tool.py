import os
import argparse
from pathlib import Path
from transformers import AutoModelForCausalLM, AutoTokenizer
import re
class MemoryLeakAnalyzer:
    def __init__(self, model_path="codellama/CodeLlama-7b-Instruct-hf"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            device_map="auto"
        )
    
    def analyze_file(self, file_path):
        with open(file_path, 'r') as f:
            code = f.read()
        
        prompt = self._build_prompt(code)
        inputs = self.tokenizer(prompt, return_tensors="pt").to("cuda")
        
        outputs = self.model.generate(
            inputs.input_ids,
            max_new_tokens=512,
            temperature=0.2
        )
        
        return self._parse_result(
            self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        )

    def _build_prompt(self, code):
       
        return f"""<s>[INST]
作为C/C++专家，请分析以下代码的内存管理情况：
1. 识别所有内存分配点
2. 检查对应的释放操作
3. 标记未释放的变量

输出格式：
- [行号] 变量名 (类型) ➔ 状态: [✅释放/❌未释放]

代码片段：
{code}

[/INST]"""

    def _parse_result(self, text):
        
        results = []
        lines = text.split('\n')
        for line in lines:
            if "➔ 状态:" in line:
                parts = line.split('➔')
                var_info = parts[0].strip()
                status = parts[1].split(':')[1].strip()
                
                
                line_num = var_info.split(']')[0].replace('[', '').strip()
                var_type = re.search(r'\((.*?)\)', var_info).group(1)
                var_name = re.search(r'\](.*?)\(', var_info).group(1).strip()
                
                results.append({
                    "line": line_num,
                    "variable": var_name,
                    "type": var_type,
                    "status": status
                })
        return results

def main():
    # 命令行参数解析
    parser = argparse.ArgumentParser(
        description="代码内存泄漏分析工具",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "path",
        type=str,
        help="需要分析的代码路径（文件或目录）"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="codellama/CodeLlama-7b-Instruct-hf",
        help="本地大模型路径"
    )
    args = parser.parse_args()
    # target_path = '/root/code'
    # target_path = Path(target_path)
    # model_path = '/root/autodl-tmp/qwen-7b-grpo'
    # 路径验证
    target_path = Path(args.path)
    if not target_path.exists():
        print(f"错误：路径 {args.path} 不存在")
        return

    #初始化分析器
    analyzer = MemoryLeakAnalyzer(args.model)

    # 执行分析
    if target_path.is_file():
        print(f"分析文件: {target_path}")
        results = analyzer.analyze_file(target_path)
        _print_report(results, target_path)
    else:
        code_files = list(target_path.rglob("*.[c|h|cpp|hpp]"))
        print(f"找到 {len(code_files)} 个代码文件")
        for file in code_files:
            print(f"\n分析文件: {file}")
            results = analyzer.analyze_file(file)
            _print_report(results, file)

def _print_report(results, file_path):
    """打印格式化报告"""
    print(f"\n{'='*40}")
    print(f"内存分析报告: {file_path}")
    print(f"{'='*40}")
    
    if not results:
        print("✅ 未发现内存泄漏风险")
        return
    
    for item in results:
        color = '\033[92m' if "✅" in item["status"] else '\033[91m'
        print(
            f"[行 {item['line']}] {item['variable']} ({item['type']})"
            f" ➔ 状态: {color}{item['status']}\033[0m"
        )

if __name__ == "__main__":
    main()
