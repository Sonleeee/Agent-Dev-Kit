import os
import sys
import zipfile
import xml.etree.ElementTree as ET
from html.parser import HTMLParser

# --- Native Parsers (Zero-Dependency) ---

def parse_docx(docx_path):
    try:
        with zipfile.ZipFile(docx_path) as docx:
            xml_content = docx.read('word/document.xml')
    except Exception as e:
        return f"Error reading DOCX: {str(e)}"
        
    root = ET.fromstring(xml_content)
    namespaces = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    
    markdown = []
    
    for paragraph in root.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
        # Check style
        pPr = paragraph.find('w:pPr', namespaces)
        is_heading = False
        heading_level = 0
        if pPr is not None:
            pStyle = pPr.find('w:pStyle', namespaces)
            if pStyle is not None:
                style_val = pStyle.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val')
                if style_val and style_val.startswith('Heading'):
                    is_heading = True
                    try:
                        heading_level = int(style_val.replace('Heading', ''))
                    except:
                        heading_level = 1
        
        # Get text
        text_pieces = []
        for run in paragraph.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}r'):
            t = run.find('w:t', namespaces)
            if t is not None and t.text:
                text_pieces.append(t.text)
        
        p_text = "".join(text_pieces).strip()
        if p_text:
            if is_heading:
                markdown.append(f"\n{'#' * heading_level} {p_text}\n")
            else:
                markdown.append(f"\n{p_text}\n")
                
    return "".join(markdown)

class SimpleHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.markdown = []
        self.in_title = False
        self.in_heading = False
        self.heading_level = 0
        self.in_list = False
        self.in_link = False
        self.link_url = ""

    def handle_starttag(self, tag, attrs):
        if tag == 'title':
            self.in_title = True
        elif tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            self.in_heading = True
            self.heading_level = int(tag[1])
            self.markdown.append("\n" + "#" * self.heading_level + " ")
        elif tag == 'p':
            self.markdown.append("\n")
        elif tag in ['ul', 'ol']:
            self.in_list = True
        elif tag == 'li':
            self.markdown.append("\n- ")
        elif tag == 'a':
            self.in_link = True
            for attr in attrs:
                if attr[0] == 'href':
                    self.link_url = attr[1]

    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False
            self.markdown.append("\n")
        elif tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            self.in_heading = False
            self.markdown.append("\n")
        elif tag == 'p':
            self.markdown.append("\n")
        elif tag in ['ul', 'ol']:
            self.in_list = False
            self.markdown.append("\n")
        elif tag == 'a':
            self.in_link = False

    def handle_data(self, data):
        clean_data = data.strip()
        if not clean_data:
            return
        if self.in_link:
            self.markdown.append(f"[{clean_data}]({self.link_url})")
        else:
            self.markdown.append(clean_data + " ")

def parse_html(html_path):
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except Exception as e:
        return f"Error reading HTML: {str(e)}"
        
    parser = SimpleHTMLParser()
    parser.feed(html_content)
    return "".join(parser.markdown)

# --- Main Driver ---

def main():
    if len(sys.argv) < 3:
        print("Usage: python parser.py <input_path> <output_path>")
        sys.exit(1)
        
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    
    if not os.path.exists(input_path):
        print(f"Error: Input file does not exist at {input_path}")
        sys.exit(1)
        
    _, ext = os.path.splitext(input_path.lower())
    markdown_content = ""
    
    # 1. Native execution for Word & HTML
    if ext == '.docx':
        print(f"[Parser] Running native DOCX parser for {input_path}...")
        markdown_content = parse_docx(input_path)
    elif ext in ['.html', '.htm']:
        print(f"[Parser] Running native HTML parser for {input_path}...")
        markdown_content = parse_html(input_path)
        
    # 2. Hybrid execution (Check MarkItDown for PDF, Excel, PPTX...)
    else:
        print(f"[Parser] Checking MarkItDown for {ext} format...")
        try:
            from markitdown import MarkItDown
            print("[Parser] MarkItDown found. Initializing...")
            
            # Check for API keys to enable LLM-powered OCR and Image Description
            openai_key = os.environ.get("OPENAI_API_KEY")
            gemini_key = os.environ.get("GEMINI_API_KEY")
            md = None
            
            if openai_key:
                try:
                    from openai import OpenAI
                    print("[Parser] OPENAI_API_KEY found. Enabling LLM mode (gpt-4o)...")
                    client = OpenAI(api_key=openai_key)
                    md = MarkItDown(llm_client=client, llm_model="gpt-4o")
                except Exception as ex:
                    print(f"[Parser] Failed to init OpenAI client: {ex}. Falling back to standard mode.")
            
            if not md and gemini_key:
                try:
                    from openai import OpenAI
                    print("[Parser] GEMINI_API_KEY found. Enabling LLM mode (gemini-2.5-flash) via OpenAI endpoint...")
                    client = OpenAI(
                        api_key=gemini_key,
                        base_url="https://generativelanguage.googleapis.com/v1beta/openai"
                    )
                    md = MarkItDown(llm_client=client, llm_model="gemini-2.5-flash")
                except Exception as ex:
                    print(f"[Parser] Failed to init Gemini client: {ex}. Falling back to standard mode.")
                    
            if not md:
                print("[Parser] Running MarkItDown in offline standard mode (no LLM)...")
                md = MarkItDown()
                
            result = md.convert(input_path)
            markdown_content = result.text_content
        except ImportError:
            print(f"\n[!] Cảnh báo: Định dạng '{ext}' yêu cầu thư viện 'markitdown'.")
            print("Để xử lý được file này, vui lòng cài đặt bằng cách chạy lệnh:")
            print("    pip install markitdown")
            print("Hoặc chuyển đổi file sang định dạng Word (.docx) hoặc HTML để parse native không cần dependency.\n")
            sys.exit(1)
        except Exception as e:
            print(f"Error during MarkItDown execution: {str(e)}")
            sys.exit(1)
            
    # Write output
    try:
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        print(f"[Parser] Successfully wrote markdown to {output_path}")
    except Exception as e:
        print(f"Error writing output file: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
