with open('extanalyser.py', 'r', encoding='utf-8') as f:
    text = f.read()

print('1', text.count("UPLOAD_FOLDER"))
print('2', text.count("query = request.form['query']"))
print('3', text.count("virustotal.pub_vt == []"))
print('4', text.count("def scan_domain(domain):"))
print('5', text.count('xpi_file = f"{xpi_matches[0]}.xpi"'))
print('6', text.count("if ext_name != False or ext_name != None:"))
print('7', text.count("in locale_content:"))
print('8', text.count("ridcnt = open(ridfile"))
print('9', text.count("graph_file_create = open(graph_file"))
print('10', text.count("cnt = open(file,"))
print('11', text.count("new_path = helper.fixpath(result_directory + '/' + file['name'] + '.src')"))
print('12', text.count("source_data[file_id]['retirejs_result'] != []"))

import re
matches = re.findall(r"report\[\'report_directory\'\] = helper\.fixpath.*?replace.*", text)
print('13 count:', len(matches))
for m in matches:
    print("Match:", m)
