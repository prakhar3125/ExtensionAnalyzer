import os

compilation_file = 'frontend_compilation.md'
output_css = 'consolidated.css'

with open(compilation_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

css_blocks = []
in_css = False

for line in lines:
    if line.startswith('### `static/css/') or line.startswith('### `static/css/dark.css'):
        in_css = True
    elif in_css and line.startswith('```css'):
        continue
    elif in_css and line.startswith('```'):
        in_css = False
    elif in_css:
        css_blocks.append(line)

with open(output_css, 'w', encoding='utf-8') as f:
    f.writelines(css_blocks)

print(f"CSS extraction complete: {output_css}")
