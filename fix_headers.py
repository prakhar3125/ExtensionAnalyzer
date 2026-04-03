import os

files_to_fix = {
    'templates/report.html': 'report.html',
    'templates/graph.html': 'graph.html',
    'templates/source.html': 'source.html',
    'templates/sourcecode.html': 'sourcecode.html',
    'templates/error.html': 'error.html'
}

static_files = [
    'static/css/style.css',
    'static/css/result.css',
    'static/css/dark.css',
    'static/js/main.js',
    'static/js/graph.js'
]

license_header = """<!--
ExtAnalysis - Browser Extension Analysis Framework
Copyright (C) 2019 - 2022 Tuhinshubhra

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
-->
"""

def fix_template(filepath, filename):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Try to find the start of the actual HTML to strip the broken header part
    if '<!doctype html>' in content.lower():
        parts = content.lower().split('<!doctype html>', 1)
        actual_content = '<!DOCTYPE html>' + content[len(parts[0]) + 15:]
    elif '<html>' in content.lower():
        parts = content.lower().split('<html>', 1)
        actual_content = content[len(parts[0]):]
    else:
        actual_content = content # Fallback

    new_content = f"<!-- File: {filename} -->\n" + license_header + actual_content
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

def update_static(filepath):
    filename = os.path.basename(filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if content.startswith(f"/* File: {filename} */"):
        return
        
    new_content = f"/* File: {filename} */\n" + content
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

for path, name in files_to_fix.items():
    if os.path.exists(path):
        fix_template(path, name)

for path in static_files:
    if os.path.exists(path):
        update_static(path)

print("Done fixing headers and adding filename comments.")
