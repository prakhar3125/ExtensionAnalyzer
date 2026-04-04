/**
 * ION SecOps Extension Analyzer — main.js
 * Based on ExtAnalysis by Tuhinshubhra (AGPL-3.0)
 * Refactored: ES6+, DRY helpers, custom toast system
 */

'use strict';

// ─── DOM REFS ────────────────────────────────────────────────────────────────
const $ = window.$;
const swal = window.swal;

const el = {
  scanContainer: document.getElementById('scan-container'),
  resultContainer: document.getElementById('result-container'),
  updateContainer: document.getElementById('update-container'),
  aboutContainer: document.getElementById('about-container'),
  onlineScan: document.getElementById('online-scan'),
  localScan: document.getElementById('local-scan'),
  selectScanType: document.getElementById('select-scan-type'),
  uploadExtension: document.getElementById('upload-extension'),
  webstore: document.getElementById('webstore'),
  loading: document.getElementById('loading'),
  modalContent: document.getElementById('modal-content'),
  noscript: document.getElementById('noscript'),
  pageStyle: document.getElementById('pageStyle'),
  localList: document.getElementById('local-list'),
};

const modalElements = $('.modal-overlay, .modal');
const csrftoken = $('meta[name=csrf-token]').attr('content');

// Hide noscript banner immediately
if (el.noscript) el.noscript.style.display = 'none';

// ─── TOAST NOTIFICATION SYSTEM ───────────────────────────────────────────────
(function initToastSystem() {
  const style = document.createElement('style');
  style.textContent = `
    #ion-toast-container {
      position: fixed; top: 1.25rem; right: 1.25rem;
      z-index: 99999; display: flex; flex-direction: column; gap: .6rem;
      pointer-events: none;
    }
    .ion-toast {
      display: flex; align-items: flex-start; gap: .75rem;
      min-width: 280px; max-width: 400px;
      background: #0f1929; border: 1px solid #1c2e45;
      border-radius: 8px; padding: .9rem 1.1rem;
      box-shadow: 0 8px 32px rgba(0,0,0,.5);
      font-family: 'JetBrains Mono', monospace;
      font-size: .75rem; color: #dde6f0;
      pointer-events: all; cursor: pointer;
      animation: toastIn .3s cubic-bezier(.22,1,.36,1) both;
      border-left: 3px solid #1c2e45;
    }
    .ion-toast.success { border-left-color: #00d4aa; }
    .ion-toast.error   { border-left-color: #ef4444; }
    .ion-toast.warning { border-left-color: #f59e0b; }
    .ion-toast.info    { border-left-color: #3b82f6; }
    .ion-toast-icon { font-size: 1rem; flex-shrink: 0; margin-top: .05rem; }
    .ion-toast.success .ion-toast-icon { color: #00d4aa; }
    .ion-toast.error   .ion-toast-icon { color: #ef4444; }
    .ion-toast.warning .ion-toast-icon { color: #f59e0b; }
    .ion-toast.info    .ion-toast-icon { color: #3b82f6; }
    .ion-toast-body { flex: 1; }
    .ion-toast-title { font-weight: 700; letter-spacing: .06em; text-transform: uppercase; font-size: .65rem; margin-bottom: .2rem; }
    .ion-toast-msg { color: #4a6080; line-height: 1.5; font-size: .72rem; }
    .ion-toast.out { animation: toastOut .25s ease forwards; }
    @keyframes toastIn  { from { opacity:0; transform:translateX(16px); } to { opacity:1; transform:translateX(0); } }
    @keyframes toastOut { from { opacity:1; transform:translateX(0); } to { opacity:0; transform:translateX(16px); } }
  `;
  document.head.appendChild(style);

  const container = document.createElement('div');
  container.id = 'ion-toast-container';
  document.body.appendChild(container);
})();

const ICONS = { success: 'fa-check-circle', error: 'fa-times-circle', warning: 'fa-exclamation-triangle', info: 'fa-info-circle' };

function toast(type, title, msg = '', duration = 4000) {
  const container = document.getElementById('ion-toast-container');
  const t = document.createElement('div');
  t.className = `ion-toast ${type}`;
  t.innerHTML = `
    <div class="ion-toast-icon"><i class="fas ${ICONS[type] || ICONS.info}"></i></div>
    <div class="ion-toast-body">
      <div class="ion-toast-title">${title}</div>
      ${msg ? `<div class="ion-toast-msg">${msg}</div>` : ''}
    </div>`;

  const dismiss = () => {
    t.classList.add('out');
    t.addEventListener('animationend', () => t.remove(), { once: true });
  };
  t.addEventListener('click', dismiss);
  container.appendChild(t);
  setTimeout(dismiss, duration);
  return t;
}

// ─── LOADING HELPERS ─────────────────────────────────────────────────────────
function showLoading() { if (el.loading) el.loading.style.display = 'flex'; }
function hideLoading() { if (el.loading) el.loading.style.display = 'none'; }

// ─── MODAL HELPERS ───────────────────────────────────────────────────────────
$('.close-modal').on('click', () => modalElements.removeClass('active'));

function openModal(html) {
  if (el.modalContent) el.modalContent.innerHTML = html;
  modalElements.addClass('active');
}

function modalError(msg) {
  openModal(`
    <div style="text-align:center;padding:1rem;">
      <img src="/static/images/error.png" style="width:180px;margin:1rem;opacity:.8;">
      <h3 style="font-family:'JetBrains Mono',monospace;font-size:.9rem;color:#ef4444;margin-top:.5rem;">${msg}</h3>
    </div>`);
}

function modalSuccess(msg, extraHtml = '') {
  openModal(`
    <div style="text-align:center;padding:1rem;">
      <img src="/static/images/success.png" style="width:180px;margin:1rem;opacity:.85;">
      <h3 style="font-family:'JetBrains Mono',monospace;font-size:.9rem;color:#00d4aa;margin-top:.5rem;">${msg}</h3>
      ${extraHtml}
    </div>`);
}

// ─── FETCH HELPER ────────────────────────────────────────────────────────────
async function api(url, body, { showLoad = true } = {}) {
  if (showLoad) showLoading();
  try {
    const res = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-CSRFToken': csrftoken,
      },
      body,
    });
    return await res.text();
  } catch (err) {
    toast('error', 'Network Error', 'API call failed. Is the analyzer offline?');
    throw err;
  } finally {
    if (showLoad) hideLoading();
  }
}

// ─── RESPONSE HANDLER ────────────────────────────────────────────────────────
function handleresponse(response) {
  try { swal.close(); } catch { }

  if (response.includes('error: ')) {
    const msg = response.split('error:')[1].trim();
    modalError(msg);
    hideLoading();
  } else if (response.includes('Extension analyzed and report saved')) {
    const anal_id = response.split('report saved under ID: ')[1];
    const repLink = `<a href="/analysis/${anal_id}" target="_blank" class="start_scan" style="margin-top:.75rem;display:inline-flex;align-items:center;gap:.4rem;"><i class="fas fa-external-link-alt"></i> View Analysis</a>`;
    modalSuccess(response, repLink);
    hideLoading();
  } else {
    modalSuccess(response);
    hideLoading();
  }
}

// ─── VIEW SWITCHER ───────────────────────────────────────────────────────────
function switchView(showId) {
  ['scan-container', 'result-container', 'update-container', 'about-container'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.style.display = id === showId ? 'block' : 'none';
  });
  const container = document.getElementById('container');
  if (container) { $(container).fadeOut(200, () => $(container).fadeIn(400)); }
}

function showscan() { switchView('scan-container'); }
function showresult() { switchView('result-container'); }
function showupdate() { switchView('update-container'); }
function showabout() { switchView('about-container'); }

// ─── SCAN FUNCTIONS ──────────────────────────────────────────────────────────
function download_and_scan() {
  let ext_id = document.getElementById('extension-id').value.trim();
  if (!ext_id) { toast('warning', 'Empty Value', "Extension ID can't be empty."); return; }
  if (ext_id.includes('chrome.google.com')) {
    ext_id = ext_id.split('://')[1].split('/')[4].split('?')[0];
  }
  handle_download(ext_id);
}

function download_and_scan_firefox() {
  const ext_id = document.getElementById('firefox-addon').value.trim();
  if (!ext_id.match(/addons\.mozilla\.org/)) {
    toast('warning', 'Invalid URL', 'Please provide a valid Firefox add-on URL.');
    return;
  }
  handle_download(ext_id, 'firefoxaddon');
}

function download_and_scan_edge() {
  const ext_id = document.getElementById('edge-addon').value.trim();
  if (!ext_id.match(/microsoftedge\.microsoft\.com/)) {
    toast('warning', 'Invalid URL', 'Please provide a valid Edge add-on URL.');
    return;
  }
  handle_download(ext_id, 'edgeaddon');
}

function handle_download(id, type = 'dlanalysis') {
  showLoading();
  // Automatic naming based on ID (sanitized)
  const safeName = id.replace(/[^a-z0-9]/gi, '_').toLowerCase();
  
  let url = `/api/?extid=${id}&savedir=${safeName}`;
  if (type === 'firefoxaddon' || type === 'edgeaddon') {
    url = `/api/?addonurl=${encodeURIComponent(id)}&savedir=${safeName}`;
  }
  
  api(url, `query=${type}`, { showLoad: false })
    .then(text => {
      handleresponse(text);
    })
    .catch(err => {
      if (err) toast('error', 'Analysis Failed', 'The request failed. Check backend logs.');
      hideLoading();
    });
}

// ─── UPLOAD ──────────────────────────────────────────────────────────────────
function upload_extension() {
  showLoading();
  const formdata = new FormData($('#upload-form')[0]);
  $.ajax({
    url: '/upload/', type: 'POST',
    headers: { 'X-CSRFToken': csrftoken },
    data: formdata,
    success: response => { handleresponse(response); hideLoading(); },
    error: () => { toast('error', 'Upload Failed', 'Something went wrong.'); hideLoading(); },
    cache: false, contentType: false, processData: false,
  });
}

// ─── RESULTS ─────────────────────────────────────────────────────────────────
function result() {
  api('/api/', 'query=results').then(txt => {
    const changeme = document.getElementById('changeme');
    if (changeme) { changeme.innerHTML = txt; $('#result-table').DataTable(); }
    const btn = document.getElementById('load_result');
    if (btn) btn.innerHTML = '<i class="fas fa-sync-alt"></i> Reload Reports';
  }).catch(() => { });
}

function loadresult(result_id) {
  api(`/api/?result=${result_id}`, 'query=showresult').then(txt => {
    openModal(txt);
  }).catch(() => { });
}

function viewResult(id) { window.open(`/analysis/${id}`, '_blank'); }

function deleteResult(id) {
  swal({
    title: `Delete Result: ${id}`,
    text: 'This action cannot be undone.',
    icon: 'warning', buttons: true, dangerMode: true,
  }).then(willDelete => {
    if (!willDelete) { toast('info', 'Cancelled', `Result ${id} was not deleted.`); return; }
    api(`/api/?resultID=${id}`, 'query=deleteResult').then(txt => {
      if (txt === 'success') { toast('success', 'Deleted', `Analysis ${id} successfully deleted.`); result(); }
      else toast('error', 'Error', txt);
    }).catch(() => { });
  });
}

function removeAll() {
  swal({
    title: 'Delete All Analysis?',
    text: 'All results will be permanently removed.',
    icon: 'warning', buttons: true, dangerMode: true,
  }).then(willDelete => {
    if (!willDelete) { toast('info', 'Cancelled', 'Your analysis reports are safe.'); return; }
    api('/api/', 'query=deleteAll').then(txt => {
      if (txt === 'success') { toast('success', 'Cleared', 'All results deleted successfully.'); result(); }
      else toast('error', 'Error', txt);
    }).catch(() => { });
  });
}

// ─── LOCAL EXTENSIONS ────────────────────────────────────────────────────────
function showscantype() {
  if (el.selectScanType) el.selectScanType.style.display = 'block';
  if (el.onlineScan) el.onlineScan.style.display = 'none';
  if (el.localScan) el.localScan.style.display = 'none';
}

function getLocalExtensions(browser) {
  const localList = el.localList;
  if (localList) localList.style.display = 'none';
  showLoading();

  api(`/api/?browser=${browser}`, 'query=getlocalextensions').then(reply => {
    if (reply.includes('error: ')) {
      toast('error', 'Error', reply.split('error: ')[1]);
    } else {
      const names = { googlechrome: 'Google Chrome', firefox: 'Mozilla Firefox' };
      const browserName = names[browser] || browser;
      if (localList) {
        localList.innerHTML = `<h3 class="mid_header">Local ${browserName} Extensions</h3><br>${reply}`;
        $('#result-table').DataTable();
      }
    }
    if (localList) localList.style.display = 'block';
  }).catch(() => { if (localList) localList.style.display = 'block'; });
}

function getLocalOperaExtensions() {
  toast('info', 'Coming Soon', 'Opera local extension support will be added in an upcoming version.');
}

function analyzeLocalExtension(path, browser) {
  api(`/api/?browser=${browser}&path=${path}`, 'query=analyzelocalextension')
    .then(handleresponse)
    .catch(() => { });
}

// ─── LABS & LOGS ─────────────────────────────────────────────────────────────
function clearLab() {
  swal({
    title: 'Clear Lab?',
    text: "This removes all downloaded and extracted extensions. Analysis reports are unaffected.",
    icon: 'warning', buttons: true, dangerMode: true,
  }).then(willDelete => {
    if (!willDelete) { console.log('Lab untouched.'); return; }
    api('/api/', 'query=clearLab').then(handleresponse).catch(() => { });
  });
}

function clearlogs(x) {
  api('/api/', `query=${encodeURIComponent(x)}`).then(handleresponse).catch(() => { });
}

// ─── FILE VIEWER ─────────────────────────────────────────────────────────────
function viewfile(analysis_id, file_id) {
  window.open(`/view-source/${analysis_id}/${file_id}`, '_blank');
}

// ─── INTEL / PERMISSIONS ─────────────────────────────────────────────────────
function view_permission(permission) {
  const permMap = { 'https:': 'https://*/*', 'http:': 'http://*/*', '*': '*://*/*' };
  const p = permMap[permission] || permission;

  api(`/api/?permission=${p}`, 'query=permissionInfo').then(reply => {
    swal('', reply, 'info');
  }).catch(() => { });
}

// ─── NETWORK TOOLS ───────────────────────────────────────────────────────────
function domain_from_url(url) {
  const match = url.match(/^(?:https?:\/\/)?(?:[^@\n]+@)?(?:www\.)?([^:/\n?=]+)/im);
  if (!match) return null;
  const sub = match[1].match(/^[^.]+\.(.+\..+)$/);
  return sub ? sub[1] : match[1];
}

function whois(url) {
  if (!url || url.trim() === '') { toast('warning', 'Invalid URL', 'Please provide a valid URL.'); return; }
  const domain = domain_from_url(url);
  api(`/api/?domain=${domain}`, 'query=whois').then(txt => openModal(txt)).catch(() => { });
}

function domainvt(url, analysis_id) {
  if (!url || url.trim() === '') { toast('warning', 'Invalid Domain', 'Please provide a valid domain.'); return; }

  api(`/api/?domain=${url}&analysis_id=${analysis_id}`, 'query=vtDomainReport').then(txt => {
    if (txt.includes('error: ')) {
      modalError(txt.split('error:')[1].trim());
    } else {
      openModal(`<center><h4 style="font-family:'JetBrains Mono',monospace;font-size:.85rem;color:#00d4aa;margin-bottom:1rem;">VirusTotal — ${url}</h4></center>
        <div id="vt_info" style="overflow:auto;max-height:500px;text-align:left;"></div>`);
      try {
        const data = (() => { try { return JSON.parse(txt); } catch { return txt; } })();
        const tree = jsonTree.create(data, document.getElementById('vt_info'));
        tree.expand(n => n.childNodes.length < 2 || n.label === 'phoneNumbers');
      } catch { handleresponse('error: No valid VirusTotal result found.'); }
    }
  }).catch(() => { });
}

function geoip(ip) {
  if (!ip || ip.trim() === '') { handleresponse('error: Invalid IP Address'); return; }
  api(`/api/?ip=${ip}`, 'query=geoip').then(txt => openModal(txt)).catch(() => { });
}

function retirejsResult(file_id, analysis_id, file_name) {
  if (!file_id || file_id.trim() === '') { handleresponse('error: Invalid File ID'); return; }

  api(`/api/?file=${file_id}&analysis_id=${analysis_id}`, 'query=retirejsResult').then(txt => {
    if (txt.includes('error: ')) {
      modalError(txt.split('error:')[1].trim());
    } else if (txt === 'none') {
      handleresponse(`No vulnerabilities found in <b>${file_name}</b>`);
    } else {
      openModal(`<center><h4 style="font-family:'JetBrains Mono',monospace;font-size:.85rem;color:#f59e0b;margin-bottom:1rem;">RetireJS — ${file_name}</h4></center>
        <div id="rjs_result" style="overflow:auto;max-height:500px;text-align:left;"></div>`);
      try {
        const data = (() => { try { return JSON.parse(txt); } catch { return txt; } })();
        const tree = jsonTree.create(data, document.getElementById('rjs_result'));
        tree.expand(n => n.childNodes.length < 2 || n.label === 'phoneNumbers');
      } catch { handleresponse('error: Failed to parse RetireJS result.'); }
    }
  }).catch(() => { });
}

function getHTTPHeaders(url) {
  if (!url || url.trim() === '') { handleresponse('error: Invalid URL'); return; }
  api(`/api/?url=${url}`, 'query=HTTPHeaders').then(txt => openModal(txt)).catch(() => { });
}

function getSource(url) {
  if (!url || url.trim() === '') { handleresponse('error: Invalid URL'); return; }
  api(`/api/?url=${url}`, 'query=SourceCode').then(txt => openModal(txt)).catch(() => { });
}

// ─── SETTINGS ────────────────────────────────────────────────────────────────
function changeVTapi() {
  const vt_api = document.getElementById('virustotal_api')?.value?.trim();
  if (!vt_api) { toast('error', 'Invalid API', 'VirusTotal API key cannot be empty.'); return; }
  api(`/api/?api=${vt_api}`, 'query=changeVTapi').then(handleresponse).catch(() => { });
}

function changeReportsDir() {
  const dir = document.getElementById('reports_dir')?.value?.trim();
  if (!dir) { toast('error', 'Invalid Path', 'Reports directory path cannot be empty.'); return; }
  api(`/api/?newpath=${dir}`, 'query=changeReportsDir').then(handleresponse).catch(() => { });
}

function changeLabDir() {
  const dir = document.getElementById('lab_dir')?.value?.trim();
  if (!dir) { toast('error', 'Invalid Path', 'Lab directory path cannot be empty.'); return; }
  api(`/api/?newpath=${dir}`, 'query=changelabDir').then(handleresponse).catch(() => { });
}

function updateIntelExtraction() {
  try {
    const fields = ['extract_comments', 'extract_btc_addresses', 'extract_base64_strings',
      'extract_email_addresses', 'extract_ipv4_addresses', 'extract_ipv6_addresses', 'ignore_css'];
    const params = fields.map(f => `${f}=${document.getElementById(f)?.checked ?? false}`).join('&');
    api(`/api/?${params}`, 'query=updateIntelExtraction').then(handleresponse).catch(() => { });
  } catch {
    handleresponse('error: Something went wrong while reading settings.');
  }
}

function update() {
  toast('info', 'Update', 'Run: <code>python3 extanalyser.py --update</code>', 6000);
}

// ─── TOP NAV TABS ────────────────────────────────────────────────────────────
$('.tabs').on('click', 'a', function (e) {
  e.preventDefault();
  $('.tabs a').removeClass('active');
  $(this).addClass('active');
});

// ─── INIT ────────────────────────────────────────────────────────────────────
(function init() {
  // Any extra initialization can go here
})();