import os

files_to_include = [
    # Templates
    'templates/index.html',
    'templates/report.html',
    'templates/graph.html',
    'templates/source.html',
    'templates/sourcecode.html',
    'templates/error.html',
    # Stylesheets
    'static/css/style.css',
    'static/css/result.css',
    'static/css/dark.css',
    'static/css/bttn.css',
    'static/css/codemirror.css',
    'static/css/material.css',
    'static/css/hint.min.css',
    # Javascript
    'static/js/main.js',
    'static/js/graph.js',
    'static/js/jsonTree.js'
]

# Note: Large minified libraries are skipped to prevent file size issues:
# jquery.js, vis.min.js, datatables.min.js, sweetalert.min.js, codemirror.js, beautify.js, libopenmpt.js

output_file = 'frontend_compilation.md'

with open(output_file, 'w', encoding='utf-8') as outfile:
    outfile.write("# ExtAnalysis Frontend Compilation\n\n")
    outfile.write("This file contains the core HTML templates, CSS, and Javascript files for the ExtAnalysis frontend.\n")
    outfile.write("*Note: Large third-party minified libraries (jQuery, Vis.js, DataTables, etc.) are excluded to keep this file concise.*\n\n")
    
    current_section = ""
    
    for relative_path in files_to_include:
        if not os.path.exists(relative_path):
            continue
            
        # Determine section
        if 'templates/' in relative_path:
            section = "HTML Templates"
        elif 'static/css/' in relative_path:
            section = "Stylesheets"
        elif 'static/js/' in relative_path:
            section = "Javascript"
        else:
            section = "Other"
            
        if section != current_section:
            outfile.write(f"## {section}\n\n")
            current_section = section
            
        filename = os.path.basename(relative_path)
        ext = filename.split('.')[-1]
        if ext == 'html':
            lang = 'html'
        elif ext == 'css':
            lang = 'css'
        elif ext == 'js':
            lang = 'javascript'
        else:
            lang = ''
            
        outfile.write(f"### `{relative_path}`\n\n")
        outfile.write(f"```{lang}\n")
        with open(relative_path, 'r', encoding='utf-8') as infile:
            outfile.write(infile.read())
        outfile.write("\n```\n\n")

print(f"Compilation complete: {output_file}")
