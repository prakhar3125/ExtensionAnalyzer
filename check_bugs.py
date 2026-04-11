with open("extanalyser.py", "r", encoding="utf-8") as f:
    text = f.read()

checks = {
    "1. results_dir": "results_dir = core.reports_path",
    "2. analyze(filename)": "anls = analysis.analyze(filename)",
    "3. purge_old_data before if POST": "purge_old_data()\n    if request.method == 'POST':",
    "4. api args vs form": "api_view(query, request.args)",
    "5. get_country shadows geoip": "geoip = gip[1]",
    "6. virustotal stale": "virustotal_api = core.virustotal_api",
    "7. comma split": "data = sub_directory_data.split(',')",
    "8. ri read handle leak": "ri = open(core.report_index",
    "9. manifest load handle leak": "manifest_load = open(manifest_file",
    "10. retirejs leak": "perms = open(perm_file",
    "11. SafeConfigParser": "SafeConfigParser",
    "12. sleep 60": "time.sleep(60)",
    "13. all_reports overwrite": "core.report_index = json.loads(ri)"
}

for k, v in checks.items():
    print(f"{k}: {'FOUND' if v in text else 'NOT FOUND'}")
