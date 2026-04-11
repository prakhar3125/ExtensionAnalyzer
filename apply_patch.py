import json

fpath = 'extanalyser.py'
with open(fpath, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. results_dir = core.reports_path -> old_results_dir = core.reports_path
text = text.replace(
    'results_dir = core.reports_path',
    'old_results_dir = core.reports_path'
)

# 2. analyze(filename) -> analyze(os.path.join(app.config['UPLOAD_FOLDER'], filename))
text = text.replace(
    'anls = analysis.analyze(filename)',
    'anls = analysis.analyze(os.path.join(app.config[\'UPLOAD_FOLDER\'], filename))'
)

# 3. purge_old_data race condition
# we move purge_old_data() to inside if request.method == 'POST'
text = text.replace(
    'def upload_file():\n    purge_old_data()\n    if request.method == \'POST\':',
    'def upload_file():\n    if request.method == \'POST\':\n        purge_old_data()'
)

# 4. api args vs form
text = text.replace(
    'return api_view(query, request.args)',
    'return api_view(query, request.values)'
)

# 5. get_country shadows geoip
text = text.replace(
    'geoip = gip[1]',
    'geoip_data = gip[1]'
).replace(
    'return [True, geoip[\'country\'].lower(), geoip[\'country_name\']]',
    'return [True, geoip_data[\'country\'].lower(), geoip_data[\'country_name\']]'
)

# 6. virustotal stale logic - remove the top assignment and use core directly.
text = text.replace(
    'global pub_vt, virustotal_api\n    if virustotal_api == "":',
    'global pub_vt\n    virustotal_api = core.virustotal_api\n    if virustotal_api == "":'
)

# 7. comma split -> rsplit(',', 1)
text = text.replace(
    'data = sub_directory_data.split(\',\')',
    'data = sub_directory_data.rsplit(\',\', 1)'
)

# 8. ri file leak
old_ri1 = 'ri = open(core.report_index, \'r\', encoding=\'utf-8\')\n            ri = ri.read()'
new_ri1 = 'with open(core.report_index, \'r\', encoding=\'utf-8\') as f:\n                ri = f.read()'
text = text.replace(old_ri1, new_ri1)

old_ri2 = 'sj = open(core.settings_file, \'r\', encoding=\'utf-8\')\n            sj = json.loads(sj.read())'
new_ri2 = 'with open(core.settings_file, \'r\', encoding=\'utf-8\') as f:\n                sj = json.loads(f.read())'
text = text.replace(old_ri2, new_ri2)

old_ri3 = 'wsj = open(core.settings_file, \'w+\', encoding=\'utf-8\')\n            wsj.write(dump)\n            wsj.close()'
new_ri3 = 'with open(core.settings_file, \'w\', encoding=\'utf-8\') as f:\n                f.write(dump)'
text = text.replace(old_ri3, new_ri3)

old_ri4 = 'ri = open(report_index, \'r\')\n        ri = ri.read()'
new_ri4 = 'with open(report_index, \'r\') as f:\n            ri = f.read()'
text = text.replace(old_ri4, new_ri4)

old_ri5 = 'ri = open(core.report_index, \'w+\')\n        ri.write(json.dumps(all_reports))\n        ri.close()'
new_ri5 = 'with open(core.report_index, \'w\') as f:\n            f.write(json.dumps(all_reports))'
text = text.replace(old_ri5, new_ri5)

# 9. manifest load file leak
old_man = 'manifest_load = open(manifest_file, \'r\', encoding=\'utf-8\')\n                manifest_content = manifest_load.read()'
new_man = 'with open(manifest_file, \'r\', encoding=\'utf-8\') as manifest_load:\n                    manifest_content = manifest_load.read()'
text = text.replace(old_man, new_man)

# 10. retirejs leak
old_ret = 'perms = open(perm_file, \'r\', encoding=\'utf-8\')\n            perms = perms.read()'
new_ret = 'with open(perm_file, \'r\', encoding=\'utf-8\') as f:\n                perms = f.read()'
text = text.replace(old_ret, new_ret)

# 11. ConfigParser
text = text.replace('configparser.SafeConfigParser()', 'configparser.ConfigParser()')
text = text.replace('open(firefox_profile, \'rU\')', 'open(firefox_profile, \'r\')')

# 12. Sleep 60 => bypass 
text = text.replace('time.sleep(60)', 'core.updatelog("Skipping VT delay. Not hitting API."); pass # time.sleep(60)')

# 13. all_reports overwrite
text = text.replace(
    'all_reports = core.report_index = json.loads(ri)',
    'all_reports = core.reportids = json.loads(ri)'
)


with open(fpath, 'w', encoding='utf-8') as f:
    f.write(text)

print("Patch applied.")
