import argparse
import report
import sys
import abnormal
def main():
    parser = argparse.ArgumentParser(description="golbalanalyze")
    parser.add_argument("file_path", help="报告路径")
    parser.add_argument("log_path", help="日志路径")
    

    args = parser.parse_args()
    code_path = ".\\"
    report.report(args.file_path, code_path,args.log_path)
if __name__ == "__main__":
    # if len(sys.argv) != 3:
    #     print("Usage: python analyze.py <file_path> <pointer_name>")
    #     sys.exit(1)

    # file_path, code_path = sys.argv[1], sys.argv[2]
    # report.report(file_path, code_path)
    sys.excepthook = abnormal.global_exception_handler
    main()