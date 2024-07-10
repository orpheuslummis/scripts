import argparse
import os

def merge_markdown_files(input_dir, output_file):
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for root, _, files in os.walk(input_dir):
            for filename in sorted(f for f in files if f.endswith('.md')):
                filepath = os.path.join(root, filename)
                rel_path = os.path.relpath(filepath, input_dir)
                with open(filepath, 'r', encoding='utf-8') as infile:
                    outfile.write(f"# {os.path.splitext(rel_path)[0]}\n\n")
                    outfile.write(infile.read())
                    outfile.write("\n\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge markdown files into a single file.")
    parser.add_argument("input_dir", help="Directory containing markdown files")
    parser.add_argument("output_file", help="Output merged markdown file")
    
    args = parser.parse_args()
    
    merge_markdown_files(args.input_dir, args.output_file)
    print(f"Merged markdown files into {args.output_file}")