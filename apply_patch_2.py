import os

fpath = 'extanalyser.py'
with open(fpath, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. upload_file UPLOAD_FOLDER stale caching
text = text.replace(
    'app.config[\'UPLOAD_FOLDER\']',
    'core.lab_path'
)

# 2. api() missing Form Key (KeyError 400s)
old_api = "        # query = request.args.get('query')\n        query = request.form['query']\n        return api_view(query, request.values)"
new_api = "        query = request.values.get('query', '')\n        if not query:\n            return 'error: Missing query parameter'\n        return api_view(query, request.values)"
text = text.replace(old_api, new_api)

# 3. virustotal_scans assignment before if
old_vt1 = '    if virustotal.pub_vt == []:\n        try:\n            virustotal_scans = virustotal.domain_batch_scan(set(domains))'
new_vt1 = '    virustotal_scans = {}\n    if virustotal.pub_vt == []:\n        try:\n            virustotal_scans = virustotal.domain_batch_scan(set(domains))'
text = text.replace(old_vt1, new_vt1)

# 4. scan_domain IndexError guard
old_vt2 = 'def scan_domain(domain):\n    # Scan the url\n    global pub_vt\n    virustotal_api = core.virustotal_api'
new_vt2 = 'def scan_domain(domain):\n    # Scan the url\n    global pub_vt\n    if not pub_vt: return [False, "VT APIs disabled"]\n    virustotal_api = core.virustotal_api'
text = text.replace(old_vt2, new_vt2)

# 5. Firefox download Double Suffix string issue
text = text.replace('xpi_file = f"{xpi_matches[0]}.xpi"', 'xpi_file = f"{xpi_matches[0]}"')

# 6. Firefox String Check Type error True Override
text = text.replace('if ext_name != False or ext_name != None:', 'if ext_name and ext_name is not False:')

# 7. Array Pointers for manifest dict
text = text.replace('in locale_content:', 'in en_locale_content:')

# 8. Unhandled file locks initreport
old_lock1 = '    ridcnt = open(ridfile, \'r\', encoding=\'utf-8\')\n    ridcnt = ridcnt.read()\n    reportids = json.loads(ridcnt)'
new_lock1 = '    with open(ridfile, \'r\', encoding=\'utf-8\') as f:\n        ridcnt = f.read()\n    reportids = json.loads(ridcnt)'
text = text.replace(old_lock1, new_lock1)

# 9. savereport unhandled leak
old_lock2 = '        graph_file_create = open(graph_file, \'w+\', encoding=\'utf-8\')\n        graph_file_create.write(self.nodes + \'\\n\' + self.edges)'
new_lock2 = '        with open(graph_file, \'w\', encoding=\'utf-8\') as graph_file_create:\n            graph_file_create.write(self.nodes + \'\\n\' + self.edges)'
text = text.replace(old_lock2, new_lock2)

# 10. Thread Loops Intel
old_lock3 = '                cnt = open(file, \'r\', encoding="utf8")\n                contents = cnt.read()'
new_lock3 = '                with open(file, \'r\', encoding="utf8") as cnt:\n                    contents = cnt.read()'
text = text.replace(old_lock3, new_lock3)

# 11. Clobbering Sub-Folder Path Base
text = text.replace(
    'new_path = helper.fixpath(result_directory + \'/\' + file[\'name\'] + \'.src\')',
    'new_path = helper.fixpath(result_directory + \'/\' + file[\'id\'] + \'_\' + file[\'name\'] + \'.src\')'
)

# 12. Dictionary fetch vs index crash
text = text.replace(
    'source_data[file_id][\'retirejs_result\'] != []',
    'source_data[file_id].get(\'retirejs_result\', []) != []'
)

# 13. Dictionary Path Override Fix
old_rep = "        if report['report_id'] == id:\n            report['report_directory'] = helper.fixpath(report['report_directory'].replace('<reports_path>', reports_path).replace('\\\\', '/'))\n            return [True, report]"
new_rep = "        if report['report_id'] == id:\n            rep_copy = dict(report)\n            rep_copy['report_directory'] = helper.fixpath(rep_copy['report_directory'].replace('<reports_path>', reports_path).replace('\\\\', '/'))\n            return [True, rep_copy]"
text = text.replace(old_rep, new_rep)

with open(fpath, 'w', encoding='utf-8') as f:
    f.write(text)

print("Patch 2 Applied.")
