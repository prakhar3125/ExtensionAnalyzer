<h1 align='center'>SecOps Extension Analyzer</h1>

**SecOps Extension Analyzer** is a locally-hosted, privacy-first security tool designed to deeply analyze browser extensions (Chrome, Firefox, and Edge) for malicious behaviors, hidden indicators of compromise, and vulnerable dependencies. 

By pulling down extensions directly from the web store or analyzing local `.crx`/`.xpi` files, the analyzer unpacks the extension to expose exactly what it does behind the scenes without ever executing its code in your browser.

## What it does
- **Automatic Extraction**: Give it a URL to an extension on the Chrome, Firefox, or Edge web stores, and it will immediately download and unpack the source code.
- **Deep Intel Parsing**: Automatically scans the raw extension code to extract hidden artifacts including URLs, Domains, IPv4/IPv6 Addresses, Bitcoin Addresses, Base64 Encoded Strings, and developer comments.
- **Vulnerability Scanning**: Uses an integrated RetireJS engine to instantly flag outdated or vulnerable JavaScript frameworks bundled in the extension.
- **Manifest Breakdown**: Parses the `manifest.json` file to highlight dangerous required permissions explicitly.
- **Visual Networking**: Automatically maps relationships between extension files and the domains they talk to using interactive GUI graphs.
- **Offline First**: All intelligence gathering and parsing is done 100% locally on your machine without pinging background tracking APIs.

---

## Installation 

Make sure you have Python 3.11+ installed on your system. 

1. Clone the repository to your local machine:
```bash
git clone https://github.com/local/SecOpsAnalyzer.git
cd ExtAnalysis
```

2. Install the necessary Python dependencies:
```bash
pip install -r requirements.txt
```

## Running the Analyzer

To start the analyzer natively, simply run the Python monolith script:

```bash
python extanalyser.py
```

The application will automatically spin up its local server and open your default web browser. If the browser does not open automatically, navigate to `http://127.0.0.1:13337` to access the interface.
