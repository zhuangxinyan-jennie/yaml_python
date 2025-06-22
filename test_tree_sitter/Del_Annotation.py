import re
import argparse

def remove_c_comments(code):
    """Remove C-style comments from the code."""
    # Remove single-line comments
    code = re.sub(r'//.*?\n', '\n', code)
    # Remove multi-line comments
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
    return code

def remove_c_comments_from_file(input_path: str, output_path: str):
    """Remove C-style comments from a file."""
    with open(input_path, 'r') as f:
        code = f.read()

    cleaned_code = remove_c_comments(code)

    with open(output_path, 'w') as f:
        f.write(cleaned_code)
    print(f"Cleaned code saved to {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Remove C-style comments from a C file.")
    parser.add_argument('input_file', help='Path to the input C file')
    parser.add_argument('output_file', help='Path to save the cleaned C file')
    args = parser.parse_args()

    remove_c_comments_from_file(args.input_file, args.output_file)
    
if __name__ == "__main__":
    main()