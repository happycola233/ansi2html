import re # 导入正则表达式包
import os
from tqdm.rich import tqdm # 进度条支持
from tqdm import TqdmExperimentalWarning
import warnings


# 忽略 TqdmExperimentalWarning 警告，这是因为tqdm的rich集成仍处于实验阶段
warnings.filterwarnings("ignore", category=TqdmExperimentalWarning)


# 使用 RGB 颜色值映射 ANSI 颜色代码
foreground_color_map = { # 文本颜色
    # 标准颜色
    '30': 'rgb(12, 12, 12)',    # 黑色
    '31': 'rgb(197, 15, 31)',   # 红色
    '32': 'rgb(19, 161, 14)',   # 绿色
    '33': 'rgb(193, 156, 0)',   # 黄色
    '34': 'rgb(0, 55, 218)',    # 蓝色
    '35': 'rgb(136, 23, 152)',  # 深紫色
    '36': 'rgb(58, 150, 221)',  # 浅蓝色
    '37': 'rgb(204, 204, 204)', # 浅灰色
    # 亮色
    '90': 'rgb(118, 118, 118)', # 深灰色
    '91': 'rgb(231, 72, 86)',   # 暗红色
    '92': 'rgb(22, 198, 12)',   # 暗绿色
    '93': 'rgb(249, 241, 165)', # 浅黄色
    '94': 'rgb(59, 120, 255)',  # 亮蓝色
    '95': 'rgb(180, 0, 158)',   # 梅红色
    '96': 'rgb(97, 214, 214)',  # 青色
    '97': 'rgb(242, 242, 242)', # 白色
    # 默认前景色
    '39': 'rgb(204, 204, 204)', # 默认色
}

background_color_map = { # 背景颜色
    # 标准背景色
    '40': 'rgb(12, 12, 12)',     # 黑色
    '41': 'rgb(197, 15, 31)',    # 红色
    '42': 'rgb(19, 161, 14)',    # 绿色
    '43': 'rgb(193, 156, 0)',    # 黄色
    '44': 'rgb(0, 55, 218)',     # 蓝色
    '45': 'rgb(136, 23, 152)',   # 深紫色
    '46': 'rgb(58, 150, 221)',   # 浅蓝色
    '47': 'rgb(204, 204, 204)',  # 浅灰色
    # 亮色背景
    '100': 'rgb(118, 118, 118)', # 深灰色
    '101': 'rgb(231, 72, 86)',   # 暗红色
    '102': 'rgb(22, 198, 12)',   # 暗绿色
    '103': 'rgb(249, 241, 165)', # 浅黄色
    '104': 'rgb(59, 120, 255)',  # 亮蓝色
    '105': 'rgb(180, 0, 158)',   # 梅红色
    '106': 'rgb(97, 214, 214)',  # 青色
    '107': 'rgb(242, 242, 242)', # 白色
    # 默认背景色
    '49': 'rgb(12, 12, 12)',     # 默认色
}

# 将 256 色的 ANSI 代码转换成 RGB 格式
def ansi_256_to_rgb(ansi_code):
    # 基本颜色直接映射
    basic_colors = [
        'rgb(12, 12, 12)',    # 黑色
        'rgb(197, 15, 31)',   # 红色
        'rgb(19, 161, 14)',   # 绿色
        'rgb(193, 156, 0)',   # 黄色
        'rgb(0, 55, 218)',    # 蓝色
        'rgb(136, 23, 152)',  # 深紫色
        'rgb(58, 150, 221)',  # 浅蓝色
        'rgb(204, 204, 204)', # 浅灰色
        'rgb(118, 118, 118)', # 深灰色
        'rgb(231, 72, 86)',   # 暗红色
        'rgb(22, 198, 12)',   # 暗绿色
        'rgb(249, 241, 165)', # 浅黄色
        'rgb(59, 120, 255)',  # 亮蓝色
        'rgb(180, 0, 158)',   # 梅红色
        'rgb(97, 214, 214)',  # 青色
        'rgb(242, 242, 242)', # 白色
    ]
    
    if ansi_code < 16:
        # 16 种基本颜色
        return basic_colors[ansi_code]
    elif ansi_code < 232:
        # 6×6×6 立方体色彩
        ansi_code -= 16
        r = (ansi_code // 36) * 51
        g = ((ansi_code // 6) % 6) * 51
        b = (ansi_code % 6) * 51
        return f'rgb({r}, {g}, {b})'
    else:
        # 灰度渐变
        gray = (ansi_code - 232) * 10 + 8
        return f'rgb({gray}, {gray}, {gray})'

# 解析 ANSI 代码并转换为 HTML 标签
def ansi_to_html(match):
    codes = match.group(1).split(';') # 样式代码
    text = match.group(2) # 样式代码后的文本
    
    # 使用全局变量来追踪样式状态
    global foreground_color, background_color, bold, dim, italic, underlined, blinked, inversed, hidden, line_through
    
    i = 0
    while i < len(codes):
        code = codes[i]
        if code == '0': # 正常（重置所有样式）
            foreground_color = foreground_color_map['39'] # 默认前景色
            background_color = background_color_map['49'] # 默认背景色
            bold = False     # 文本不是粗体的
            dim = False      # 文本未弱化
            italic = False   # 文本不是斜体的
            underlined = False   # 文本无下划线
            blinked = False  # 文本不是闪烁的
            inversed = False # 颜色未反转
            hidden = False   # 文本未隐藏
            line_through = False # 文本无删除线
        # 处理颜色代码
        elif code in foreground_color_map:
            foreground_color = foreground_color_map[code]
        elif code in background_color_map:
            background_color = background_color_map[code]
        elif code == '38' and i + 2 < len(codes) and codes[i + 1] == '5': # 前景色 256 色
            foreground_color = ansi_256_to_rgb(int(codes[i + 2]))
            i += 2
        elif code == '38' and i + 4 < len(codes) and codes[i + 1] == '2': # 前景色真彩色
            foreground_color = f'rgb({codes[i + 2]}, {codes[i + 3]}, {codes[i + 4]})'
            i += 4
        elif code == '48' and i + 2 < len(codes) and codes[i + 1] == '5': # 背景色 256 色
            background_color = ansi_256_to_rgb(int(codes[i + 2]))
            i += 2
        elif code == '48' and i + 4 < len(codes) and codes[i + 1] == '2': # 背景色真彩色
            background_color = f'rgb({codes[i + 2]}, {codes[i + 3]}, {codes[i + 4]})'
            i += 4
        # 处理其他样式代码
        elif code == '1': # 粗体
            bold = True
        elif code == '2': # 弱化
            dim = True
        elif code == '3': # 斜体
            italic = True
        elif code == '4': # 下划线
            underlined = True
        elif code == '5': # 闪烁
            blinked = True
        elif code == '7': # 反显
            inversed = True
        elif code == '8': # 隐藏
            hidden = True
        elif code == '9': # 删除线
            line_through = True
        elif code == '21': # 双下划线
            underlined = 'double'
        elif code == '22': # 取消粗体、弱化
            bold = False
            dim = False
        elif code == '23': # 取消斜体
            italic = False
        elif code == '24': # 取消下划线、双下划线
            underlined = False
        elif code == '25': # 取消闪烁
            blinked = False
        elif code == '27': # 取消反显
            inversed = False
        elif code == '28': # 取消隐藏
            hidden = False
        elif code == '29': # 取消删除线
            line_through = False
        i += 1
    
    # 对于样式代码后无文本的，只改变样式的状态，返回空字符串
    if not text:
        return ''
    
    # 应用当前的前景色、背景色和其他样式
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

# 在使用ansi_to_html函数之前，初始化样式为默认值
foreground_color = foreground_color_map['39'] # 默认前景色
background_color = background_color_map['49'] # 默认背景色
bold = False     # 文本不是粗体的
dim = False      # 文本未弱化
italic = False   # 文本不是斜体的
underlined = False   # 文本无下划线
blinked = False  # 文本不是闪烁的
inversed = False # 颜色未反转
hidden = False   # 文本未隐藏
line_through = False # 文本无删除线

# 转换到 HTML
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
            white-space: pre-wrap; /* 自动换行 */
            word-wrap: break-word; /* 在长单词或 URL 地址内部进行换行 */
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
        # for line in file:
        for line in tqdm(file.readlines(), desc="处理中"):  # 使用tqdm添加进度条
            line = re.sub(r'\x1b\[([\d;]+)m(.*?)(?=\x1b\[|$)', ansi_to_html, line, flags=re.DOTALL)
            html_content += line
    
    html_content += '</pre></body></html>'
    return html_content

def save_file(content, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(content)


def get_unique_output_filename(directory, base_name="output", extension=".html"):
    """
    生成唯一的输出文件名。
    如果目录中已存在相同名称的文件，则增加计数后缀（例如 output(1).html）。

    :param directory: 输出文件所在的目录
    :param base_name: 输出文件的基本名称，默认为"output"
    :param extension: 输出文件的扩展名，默认为".html"
    :return: 唯一的完整文件路径
    """
    counter = 0  # 计数器，用于生成唯一的文件名
    while True:
        if counter == 0:
            unique_name = f"{base_name}{extension}"
        else:
            unique_name = f"{base_name}({counter}){extension}"
        unique_path = os.path.join(directory, unique_name)
        if not os.path.exists(unique_path):  # 如果文件名唯一，则返回该路径
            return unique_path
        counter += 1  # 如果文件已存在，增加计数并重试

def file_exists(file_path):
    """
    检查指定路径的文件是否存在。

    :param file_path: 要检查的文件路径
    :return: 如果文件存在且不是目录，则返回True；否则返回False
    """
    return os.path.exists(file_path) and os.path.isfile(file_path)

def prompt_for_file_path(prompt_message="请输入要处理的文件路径："):
    """
    循环提示用户输入文件路径，直到输入的路径指向一个实际存在的文件。

    :param prompt_message: 提示信息，默认为"请输入要处理的文件路径："
    :return: 用户输入的有效文件路径
    """
    while True:
        file_path = input(prompt_message)
        if file_exists(file_path):
            return file_path  # 如果文件存在，返回该路径
        else:
            print("文件不存在，请重新输入。")


# 主程序
input_file = prompt_for_file_path()  # 获取一个有效的输入文件路径
output_directory = os.path.dirname(input_file)  # 获取输入文件所在的目录
output_file = get_unique_output_filename(output_directory)  # 获取唯一的输出文件名

html_content = convert_to_html(input_file)  # 将ANSI转换为HTML内容
save_file(html_content, output_file)  # 保存HTML内容到输出文件

print(f"文件已保存至：{output_file}")  # 向用户显示文件已保存的位置
os.popen("pause")