import os
import dis
import marshal
import types
from pathlib import Path
from deepseek_ai import query_ai
from pyinstxtractor import PyInstArchive

def extract_pyc(exe_path):
    print(f"[+] Extracting {exe_path}")
    arch = PyInstArchive(exe_path)
    dest_dir = os.path.join(os.getcwd(), os.path.basename(exe_path) + '_extracted')
    if arch.open():
        if arch.checkFile():
            if arch.getCArchiveInfo():
                arch.parseTOC()
                arch.extractFiles()
                arch.close()
                print(f'[+] Successfully extracted pyinstaller archive: {exe_path} to {dest_dir}')
                return os.path.join(os.getcwd(), os.path.basename(exe_path) + '_extracted')


        arch.close()
    return None


def find_pyc_files(extract_dir):
    return list(Path(extract_dir).rglob("*.pyc"))

def parse_pyc(pyc_file):
    with open(pyc_file, "rb") as f:
        f.read(16)  # skip header
        code_obj = marshal.load(f)
        return code_obj


def get_functions(code_obj):
    funcs = []
    for const in code_obj.co_consts:
        if isinstance(const, types.CodeType):

            # print(f"\n[ {const.co_name} 函数，起始行：{const.co_firstlineno} ]")
            # print(dis.code_info(const))
            # print("\n>>> 指令:")
            # for instr in dis.Bytecode(const):
            #     print(f"{instr.offset:>3}: {instr.opname:<20} {instr.argrepr}")
            funcs.append(const)
            # funcs.extend(get_functions(const))  # 递归查找嵌套函数(这里先不找了)
    return funcs

def bytecode_to_struct(code_obj):
    return dis.Bytecode(code_obj)

def generate_source_from_bytecode(code_obj):
    bytecode_lines = [f"{instr.opname} {instr.argrepr}" for instr in bytecode_to_struct(code_obj)]
    structured_code = "\n".join(bytecode_lines)
    print(f"[AI] Sending bytecode to AI for function: {code_obj.co_name}")
    print(structured_code)
    return query_ai(code_obj.co_name, structured_code)

def rebuild_source(pyc_file):
    code_obj = parse_pyc(pyc_file)
    functions = get_functions(code_obj)
    sources = []
    for func in functions:
        source = generate_source_from_bytecode(func)
        print(f"\n======================\n{func.co_name}:\n{source}\n=====================\n")
        sources.append(f"# Function: {func.co_name}\n{source}\n")
    return "\n".join(sources)

def main(exe_path):
    extract_dir = extract_pyc(exe_path)
    pyc_files = find_pyc_files(extract_dir)
    print(f"pyc_files:{pyc_files}")
    for pyc_file in pyc_files:
        print(f"[+] Processing {pyc_file}")
        full_source = rebuild_source(pyc_file)
        out_file = Path(pyc_file).with_suffix(".recovered.py")
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(full_source)
        print(f"[+] Recovered source written to {out_file}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python exe2py_v2.py <path_to_exe>")
        sys.exit(1)
    main(sys.argv[1])
