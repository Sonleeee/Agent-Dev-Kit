import os
import sys
import re
from html.parser import HTMLParser

class DefuddleCleaner(HTMLParser):
    def __init__(self):
        super().__init__()
        self.output = []
        self.stack = []
        self.ignore_depth = 0
        self.ignored_tags = {
            'script', 'style', 'head', 'nav', 'footer', 'aside', 'header', 
            'form', 'noscript', 'iframe', 'svg', 'button', 'select', 'option'
        }
        
        # Boilerplate class/id keywords to strip
        self.boilerplate_kws = {
            'nav', 'menu', 'footer', 'sidebar', 'social', 'widget', 'banner', 
            'share', 'promo', 'ad-', 'advertisement', 'popup', 'modal', 'header'
        }
        
        # Formatting states
        self.current_link = None
        self.in_pre = False
        self.in_code = False
        self.in_list = False
        
        # Table parsing states
        self.in_table = False
        self.table_data = []
        self.current_row = []
        self.in_cell = False
        self.cell_data = []

    def is_boilerplate_attr(self, attrs):
        for attr, val in attrs:
            if attr in ('class', 'id') and val:
                val_lower = val.lower()
                if any(kw in val_lower for kw in self.boilerplate_kws):
                    return True
        return False

    def handle_starttag(self, tag, attrs):
        # 1. Determine if this tag starts an ignore block
        should_ignore = tag in self.ignored_tags or self.is_boilerplate_attr(attrs)
        
        if should_ignore:
            self.ignore_depth += 1
            self.stack.append((tag, True))
            return
            
        if self.ignore_depth > 0:
            self.stack.append((tag, False))
            return
            
        self.stack.append((tag, False))
        
        # 2. Handle block-level formatting
        if tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            level = int(tag[1])
            self.output.append(f"\n\n{'#' * level} ")
        elif tag in ('p', 'div'):
            # Append paragraph separation if output doesn't already end with a newline
            if self.output and not self.output[-1].endswith('\n'):
                self.output.append('\n\n')
        elif tag == 'br':
            self.output.append('\n')
        elif tag == 'a':
            href = dict(attrs).get('href')
            if href and not href.startswith('#') and not href.startswith('javascript:'):
                self.current_link = href
                self.output.append('[')
        elif tag in ('ul', 'ol'):
            self.in_list = True
            self.output.append('\n')
        elif tag == 'li':
            self.output.append('\n- ')
        elif tag in ('strong', 'b'):
            self.output.append('**')
        elif tag in ('em', 'i'):
            self.output.append('*')
        elif tag == 'code':
            if not self.in_pre:
                self.output.append('`')
                self.in_code = True
        elif tag == 'pre':
            self.output.append('\n\n```\n')
            self.in_pre = True
        elif tag == 'img':
            attrs_dict = dict(attrs)
            src = attrs_dict.get('src')
            alt = attrs_dict.get('alt', 'Image')
            if src:
                self.output.append(f"\n![{alt}]({src})\n")
        elif tag == 'table':
            self.in_table = True
            self.table_data = []
        elif tag == 'tr':
            self.current_row = []
        elif tag in ('td', 'th'):
            self.in_cell = True
            self.cell_data = []

    def handle_endtag(self, tag):
        # Find corresponding start tag in stack
        tag_idx = -1
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                tag_idx = i
                break
                
        if tag_idx == -1:
            # Orphan end tag, ignore
            return
            
        # Pop everything down to the matching start tag
        popped = self.stack[tag_idx:]
        self.stack = self.stack[:tag_idx]
        
        # Check if any popped tags were responsible for starting an ignore block
        for _, was_ignored in popped:
            if was_ignored:
                self.ignore_depth -= 1
                
        if self.ignore_depth > 0 or popped[0][1]:
            # Still in an ignore block or the ended tag itself was ignored
            return
            
        # 3. Handle formatting closure
        if tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            self.output.append('\n')
        elif tag in ('p', 'div'):
            self.output.append('\n')
        elif tag == 'a':
            if self.current_link:
                self.output.append(f"]({self.current_link})")
                self.current_link = None
            else:
                self.output.append(']')
        elif tag in ('ul', 'ol'):
            self.in_list = False
            self.output.append('\n\n')
        elif tag in ('strong', 'b'):
            self.output.append('**')
        elif tag in ('em', 'i'):
            self.output.append('*')
        elif tag == 'code':
            if self.in_code:
                self.output.append('`')
                self.in_code = False
        elif tag == 'pre':
            self.output.append('\n```\n\n')
            self.in_pre = False
        elif tag == 'tr':
            if self.in_table:
                self.table_data.append(self.current_row)
        elif tag in ('td', 'th'):
            self.in_cell = False
            cell_text = "".join(self.cell_data).strip()
            self.current_row.append(cell_text)
        elif tag == 'table':
            self.in_table = False
            self.render_table()

    def handle_data(self, data):
        if self.ignore_depth > 0:
            return
            
        if self.in_pre:
            self.output.append(data)
        elif self.in_cell:
            self.cell_data.append(data)
        else:
            # Clean up excessive whitespaces in inline text
            clean_data = re.sub(r'\s+', ' ', data)
            if clean_data and clean_data != ' ':
                self.output.append(clean_data)

    def render_table(self):
        if not self.table_data:
            return
            
        markdown_table = []
        max_cols = max(len(row) for row in self.table_data)
        
        # Ensure all rows have the same number of columns
        normalized_table = []
        for row in self.table_data:
            row_len = len(row)
            if row_len < max_cols:
                row.extend([''] * (max_cols - row_len))
            normalized_table.append(row)
            
        # Write headers
        headers = normalized_table[0]
        markdown_table.append(f"\n\n| {' | '.join(headers)} |")
        # Write separator
        markdown_table.append(f"| {' | '.join(['---'] * max_cols)} |")
        
        # Write data rows
        for row in normalized_table[1:]:
            markdown_table.append(f"| {' | '.join(row)} |")
            
        markdown_table.append("\n")
        self.output.append("\n".join(markdown_table))

    def get_markdown(self):
        content = "".join(self.output)
        # Post-processing cleanup: strip redundant consecutive newlines
        content = re.sub(r'\n{3,}', '\n\n', content)
        return content.strip()

def main():
    if len(sys.argv) < 3:
        print("Usage: python defuddle_cleaner.py <input_path> <output_path>")
        sys.exit(1)
        
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    
    if not os.path.exists(input_path):
        print(f"Error: Input file does not exist at {input_path}")
        sys.exit(1)
        
    try:
        with open(input_path, 'r', encoding='utf-8', errors='ignore') as f:
            html_content = f.read()
    except Exception as e:
        print(f"Error reading file {input_path}: {e}")
        sys.exit(1)
        
    print(f"[Defuddle Cleaner] Cleaning HTML file: {input_path}...")
    cleaner = DefuddleCleaner()
    cleaner.feed(html_content)
    markdown_content = cleaner.get_markdown()
    
    try:
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        print(f"[Defuddle Cleaner] Cleaned Markdown written to {output_path}")
    except Exception as e:
        print(f"Error writing output file {output_path}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
