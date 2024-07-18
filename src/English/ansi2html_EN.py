import re  # Import the regular expression package
import os
from tqdm.rich import tqdm  # Progress bar support
from tqdm import TqdmExperimentalWarning
import warnings

# Ignore TqdmExperimentalWarning because tqdm's rich integration is still experimental
warnings.filterwarnings("ignore", category=TqdmExperimentalWarning)

# Use RGB color values to map ANSI color codes
foreground_color_map = {
    # Standard colors
    '30': 'rgb(12, 12, 12)',    # Black
    '31': 'rgb(197, 15, 31)',   # Red
    '32': 'rgb(19, 161, 14)',   # Green
    '33': 'rgb(193, 156, 0)',   # Yellow
    '34': 'rgb(0, 55, 218)',    # Blue
    '35': 'rgb(136, 23, 152)',  # Deep Purple
    '36': 'rgb(58, 150, 221)',  # Light Blue
    '37': 'rgb(204, 204, 204)', # Light Gray
    # Bright colors
    '90': 'rgb(118, 118, 118)', # Dark Gray
    '91': 'rgb(231, 72, 86)',   # Dark Red
    '92': 'rgb(22, 198, 12)',   # Dark Green
    '93': 'rgb(249, 241, 165)', # Light Yellow
    '94': 'rgb(59, 120, 255)',  # Light Blue
    '95': 'rgb(180, 0, 158)',   # Plum
    '96': 'rgb(97, 214, 214)',  # Cyan
    '97': 'rgb(242, 242, 242)', # White
    # Default foreground color
    '39': 'rgb(204, 204, 204)', # Default
}

background_color_map = {
    # Standard background colors
    '40': 'rgb(12, 12, 12)',     # Black
    '41': 'rgb(197, 15, 31)',    # Red
    '42': 'rgb(19, 161, 14)',    # Green
    '43': 'rgb(193, 156, 0)',    # Yellow
    '44': 'rgb(0, 55, 218)',     # Blue
    '45': 'rgb(136, 23, 152)',   # Deep Purple
    '46': 'rgb(58, 150, 221)',   # Light Blue
    '47': 'rgb(204, 204, 204)',  # Light Gray
    # Bright background colors
    '100': 'rgb(118, 118, 118)', # Dark Gray
    '101': 'rgb(231, 72, 86)',   # Dark Red
    '102': 'rgb(22, 198, 12)',   # Dark Green
    '103': 'rgb(249, 241, 165)', # Light Yellow
    '104': 'rgb(59, 120, 255)',  # Light Blue
    '105': 'rgb(180, 0, 158)',   # Plum
    '106': 'rgb(97, 214, 214)',  # Cyan
    '107': 'rgb(242, 242, 242)', # White
    # Default background color
    '49': 'rgb(12, 12, 12)',     # Default
}

# Convert ANSI 256 color code to RGB format
def ansi_256_to_rgb(ansi_code):
    basic_colors = [
        'rgb(12, 12, 12)',    # Black
        'rgb(197, 15, 31)',   # Red
        'rgb(19, 161, 14)',   # Green
        'rgb(193, 156, 0)',   # Yellow
        'rgb(0, 55, 218)',    # Blue
        'rgb(136, 23, 152)',  # Deep Purple
        'rgb(58, 150, 221)',  # Light Blue
        'rgb(204, 204, 204)', # Light Gray
        'rgb(118, 118, 118)', # Dark Gray
        'rgb(231, 72, 86)',   # Dark Red
        'rgb(22, 198, 12)',   # Dark Green
        'rgb(249, 241, 165)', # Light Yellow
        'rgb(59, 120, 255)',  # Light Blue
        'rgb(180, 0, 158)',   # Plum
        'rgb(97, 214, 214)',  # Cyan
        'rgb(242, 242, 242)', # White
    ]
    
    if ansi_code < 16:
        return basic_colors[ansi_code]
    elif ansi_code < 232:
        ansi_code -= 16
        r = (ansi_code // 36) * 51
        g = ((ansi_code // 6) % 6) * 51
        b = (ansi_code % 6) * 51
        return f'rgb({r}, {g}, {b})'
    else:
        gray = (ansi_code - 232) * 10 + 8
        return f'rgb({gray}, {gray}, {gray})'

# Parse ANSI codes and convert to HTML tags
def ansi_to_html(match):
    codes = match.group(1).split(';')  # Style codes
    text = match.group(2)  # Text after style codes
    
    global foreground_color, background_color, bold, dim, italic, underlined, blinked, inversed, hidden, line_through
    
    i = 0
    while i < len(codes):
        code = codes[i]
        if code == '0':
            foreground_color = foreground_color_map['39']  # Default foreground color
            background_color = background_color_map['49']  # Default background color
            bold = False
            dim = False
            italic = False
            underlined = False
            blinked = False
            inversed = False
            hidden = False
            line_through = False
        elif code in foreground_color_map:
            foreground_color = foreground_color_map[code]
        elif code in background_color_map:
            background_color = background_color_map[code]
        elif code == '38' and i + 2 < len(codes) and codes[i + 1] == '5':
            foreground_color = ansi_256_to_rgb(int(codes[i + 2]))
            i += 2
        elif code == '38' and i + 4 < len(codes) and codes[i + 1] == '2':
            foreground_color = f'rgb({codes[i + 2]}, {codes[i + 3]}, {codes[i + 4]})'
            i += 4
        elif code == '48' and i + 2 < len(codes) and codes[i + 1] == '5':
            background_color = ansi_256_to_rgb(int(codes[i + 2]))
            i += 2
        elif code == '48' and i + 4 < len(codes) and codes[i + 1] == '2':
            background_color = f'rgb({codes[i + 2]}, {codes[i + 3]}, {codes[i + 4]})'
            i += 4
        elif code == '1':
            bold = True
        elif code == '2':
            dim = True
        elif code == '3':
            italic = True
        elif code == '4':
            underlined = True
        elif code == '5':
            blinked = True
        elif code == '7':
            inversed = True
        elif code == '8':
            hidden = True
        elif code == '9':
            line_through = True
        elif code == '21':
            underlined = 'double'
        elif code == '22':
            bold = False
            dim = False
        elif code == '23':
            italic = False
        elif code == '24':
            underlined = False
        elif code == '25':
            blinked = False
        elif code == '27':
            inversed = False
        elif code == '28':
            hidden = False
        elif code == '29':
            line_through = False
        i += 1
    
    if not text:
        return ''
    
    styles = []
    classNames = []
    
    styles.append(f'color: {background_color if inversed else foreground_color};')
    styles.append(f'background-color: {foreground_color if inversed else background_color};')
    
    if bold:
        classNames.append('bold')
    
    if dim:
        classNames.append('dim')
    
    if italic:
        classNames.append('italic')
    
    if underlined:
        classNames.append('underlined')
    
    if blinked:
        classNames.append('blinked')
    
    if hidden:
        classNames.append('hidden')
    
    if line_through:
        classNames.append('line-through')
    
    style_str = ' '.join(styles)
    className_str = ' '.join(classNames)
    return f'<span style="{style_str}" class="{className_str}">{text}</span>'

foreground_color = foreground_color_map['39']  # Default foreground color
background_color = background_color_map['49']  # Default background color
bold = False
dim = False
italic = False
underlined = False
blinked = False
inversed = False
hidden = False
line_through = False

def convert_to_html(file_path):
    html_content = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Console</title>
    <style>
        body {
            background-color: #000;
            color: #b0b0b0;
            text-underline-position: under;
            text-underline-offset: -1px;
        }
        
        pre {
            white-space: pre-wrap;
            word-wrap: break-word;
            font-family: 'Cascadia Mono', Consolas, 'Courier New', '黑体', '等线', '微软雅黑', monospace;
        }
        
        .bold {
            font-weight: bold;
        }
        
        .dim {
            opacity: 0.5;
        }
        
        .italic {
            font-style: italic;
        }
        
        .underlined {
            text-decoration-line: underline;
        }
        
        .blinked {
            animation: 1s steps(2, jump-none) infinite alternate blink;
        }
        
        .hidden {
            opacity: 0;
        }
        
        .line-through {
            text-decoration-line: line-through;
        }
        
        .underlined.line-through {
            text-decoration-line: underline line-through;
        }
        
        @keyframes blink {
            from {
                opacity: 1;
            }
            to {
                opacity: 0;
            }
        }
    </style>
</head>

<body>
    <pre>'''
    
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in tqdm(file.readlines(), desc="Processing"):  # Use tqdm for progress bar
            line = re.sub(r'\x1b\[([\d;]+)m(.*?)(?=\x1b\[|$)', ansi_to_html, line, flags=re.DOTALL)
            html_content += line
    
    html_content += '</pre></body></html>'
    return html_content

def save_file(content, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(content)

def get_unique_output_filename(directory, base_name="output", extension=".html"):
    counter = 0
    while True:
        if counter == 0:
            unique_name = f"{base_name}{extension}"
        else:
            unique_name = f"{base_name}({counter}){extension}"
        unique_path = os.path.join(directory, unique_name)
        if not os.path.exists(unique_path):
            return unique_path
        counter += 1

def file_exists(file_path):
    return os.path.exists(file_path) and os.path.isfile(file_path)

def prompt_for_file_path(prompt_message="Please enter the file path to process: "):
    while True:
        file_path = input(prompt_message)
        if file_exists(file_path):
            return file_path
        else:
            print("File does not exist. Please enter a valid file path.")

# Main program
input_file = prompt_for_file_path()
output_directory = os.path.dirname(input_file)
output_file = get_unique_output_filename(output_directory)

html_content = convert_to_html(input_file)
save_file(html_content, output_file)

print(f"File saved to: {output_file}")
os.popen("pause")
