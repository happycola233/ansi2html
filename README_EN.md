<p align="center"><a title="中文" href="/README.md">🇨🇳 中文简体</a> | 🇬🇧 English</p>

# ansi2html

ansi2html is a Python program designed to convert text files containing ANSI escape sequences into HTML-styled files. This allows formatted text that is typically only visible in terminals to be displayed directly on web pages. The project supports various ANSI styles and color formats, including 256 colors and true colors, and provides customizable HTML styles to meet different display needs.

## Installation

1. **Dependencies**

   ansi2html requires the following dependencies:
   - Python 3.x
   - tqdm (for displaying progress bars)

   You can install tqdm using the following command:

   ```
   pip install tqdm
   ```

2. **Clone the Repository**

   Clone the repository using the following command:

   ```
   git clone https://github.com/happycola233/ansi2html.git
   cd ansi2html
   ```

## Usage

   Run the `ansi2html.py` script and provide the path to the text file you want to process. The program will automatically convert it into HTML format and save it in the same directory as the original file.

   ```
   python src/English/ansi2html_EN.py
   ```

## Example Demonstrations

Below are examples of ANSI escape sequences and screenshots of the generated HTML output:

### ANSI Escape Sequence Examples

```plaintext
[0mNormal text[0m
[1mBold text[0m
[2mDim text[0m
[3mItalic text[0m
[4mUnderlined text[0m
[5mBlinking text[0m
[7mInverted text[0m
[8mHidden text[0m
[9mStrikethrough text[0m

[38;5;196mForeground color: Red[0m
[48;5;226mBackground color: Light Yellow[0m

[38;2;255;0;0mTrue color foreground: Red[0m
[48;2;0;255;0mTrue color background: Green[0m

[38;2;255;255;255;48;2;0;0;0mForeground and background colors reversed[0m

[4;38;5;39mUnderlined text with foreground color: Cyan[0m
[1;3;4;38;5;208;48;5;51mBold, italic, underlined text with foreground color: Orange and background color: Dark Red[0m
```

### HTML Output Screenshots

![HTML Output](res/example_output_en.png)

## Contributions

If you find any issues or have suggestions for improvement, please feel free to submit an issue or pull request. Your contributions are key to the advancement of this project.

## License

This project is licensed under the MIT License. For more details, please refer to the `LICENSE` file.