import re

with open('extanalyser.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace scan_url
url_pattern = re.compile(r'def scan_url\(url\):.*?def scan_domain\(domain\):', re.DOTALL)
text = url_pattern.sub('def scan_url(url):\n    return [False, "VirusTotal API disabled."]\n\n\ndef scan_domain(domain):', text)

# Replace scan_domain
domain_pattern = re.compile(r'def scan_domain\(domain\):.*?def domain_batch_scan\(domains\):', re.DOTALL)
text = domain_pattern.sub('def scan_domain(domain):\n    return [False, "VirusTotal API disabled."]\n\n\ndef domain_batch_scan(domains):', text)

# Replace domain_batch_scan
batch_pattern = re.compile(r'def domain_batch_scan\(domains\):.*?# ==========================================\n# FROM: core/localextensions.py', re.DOTALL)
text = batch_pattern.sub('def domain_batch_scan(domains):\n    batch_result = {}\n    for _domain in domains:\n        batch_result[_domain] = [False, "VirusTotal API disabled."]\n    return batch_result\n\n\n# ==========================================\n# FROM: core/localextensions.py', text)

with open('extanalyser.py', 'w', encoding='utf-8') as f:
    f.write(text)

print('Disabled all VT API backend functions.')
