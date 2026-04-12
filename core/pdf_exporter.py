"""
ExtAnalysis PDF Exporter
Uses ReportLab Platypus for structured document layout.
"""

import json
import os
import time
import io

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, cm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame,
    Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.platypus.flowables import Flowable
from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.graphics import renderPDF


# ─── Colour palette ───────────────────────────────────────────────────────────

C_BG        = colors.HexColor('#0f1117')   # page background
C_SURFACE   = colors.HexColor('#1a1d27')   # card / table row bg
C_SURFACE2  = colors.HexColor('#22263a')   # alternate row
C_BORDER    = colors.HexColor('#2e3350')   # table borders
C_TEXT      = colors.HexColor('#d0d4e8')   # body text
C_MUTED     = colors.HexColor('#9ba3c1')   # boosted secondary text for readability
C_ACCENT    = colors.HexColor('#7c6ef5')   # purple accent
C_GREEN     = colors.HexColor('#3ecf8e')
C_AMBER     = colors.HexColor('#fbbf24')
C_RED       = colors.HexColor('#f87171')
C_WHITE     = colors.white

RISK_COLORS = {
    'high':   (colors.HexColor('#3d1515'), C_RED),    # (bg, fg)
    'medium': (colors.HexColor('#3d2a10'), C_AMBER),
    'low':    (colors.HexColor('#1a2e1a'), C_GREEN),
    'none':   (C_SURFACE2,                C_MUTED),
}


# ─── Custom flowables ─────────────────────────────────────────────────────────

class ColoredRect(Flowable):
    """Full-width colored banner — used for section headers."""
    def __init__(self, text, bg=C_ACCENT, fg=C_WHITE, height=22):
        super().__init__()
        self.text   = text
        self.bg     = bg
        self.fg     = fg
        self.height = height
        self.width  = 0  # set by wrap()

    def wrap(self, available_width, available_height):
        self.width = available_width
        return available_width, self.height

    def draw(self):
        c = self.canv
        c.setFillColor(self.bg)
        c.roundRect(0, 0, self.width, self.height, radius=4, fill=1, stroke=0)
        c.setFillColor(self.fg)
        c.setFont('Helvetica-Bold', 10)
        c.drawString(10, 6, self.text)


class StatCard(Flowable):
    """
    Renders a row of summary stat boxes.
    stats = list of (label, value, accent_color) tuples
    """
    CARD_W  = 95
    CARD_H  = 54
    GAP     = 8
    COLS    = 4

    def __init__(self, stats):
        super().__init__()
        self.stats = stats

    def wrap(self, available_width, available_height):
        rows = -(-len(self.stats) // self.COLS)  # ceiling division
        self.av_width = available_width
        total_h = rows * (self.CARD_H + self.GAP) - self.GAP
        return available_width, total_h

    def draw(self):
        c = self.canv
        for i, (label, value, accent) in enumerate(self.stats):
            col = i % self.COLS
            row = i // self.COLS
            # position: cards are laid out L→R, rows top→bottom
            # but ReportLab y=0 is bottom, so we flip
            rows_total = -(-len(self.stats) // self.COLS)
            x = col * (self.CARD_W + self.GAP)
            y_top = (rows_total - row - 1) * (self.CARD_H + self.GAP)

            # card background
            c.setFillColor(C_SURFACE)
            c.roundRect(x, y_top, self.CARD_W, self.CARD_H, radius=6, fill=1, stroke=0)
            # left accent bar
            c.setFillColor(accent)
            c.roundRect(x, y_top, 3, self.CARD_H, radius=1, fill=1, stroke=0)
            # number
            c.setFillColor(accent)
            c.setFont('Helvetica-Bold', 22)
            c.drawString(x + 12, y_top + 28, str(value))
            # label
            c.setFillColor(C_MUTED)
            c.setFont('Helvetica', 8)
            c.drawString(x + 12, y_top + 14, label.upper())


# ─── Page template (header + footer on every page) ────────────────────────────

def _make_page_template(doc, ext_name):
    """Returns a PageTemplate with header bar and footer."""
    W, H = A4

    def on_page(canvas, doc):
        canvas.saveState()

        # --- fill page background so light text is visible globally ---
        canvas.setFillColor(C_BG)
        canvas.rect(0, 0, W, H, fill=1, stroke=0)

        # --- header bar ---
        canvas.setFillColor(C_SURFACE)
        canvas.rect(0, H - 28*mm, W, 28*mm, fill=1, stroke=0)
        canvas.setFillColor(C_ACCENT)
        canvas.rect(0, H - 28*mm, 4, 28*mm, fill=1, stroke=0)  # left accent
        canvas.setFont('Helvetica-Bold', 11)
        canvas.setFillColor(C_WHITE)
        canvas.drawString(20*mm, H - 17*mm, 'ExtAnalysis Security Report')
        canvas.setFont('Helvetica', 9)
        canvas.setFillColor(C_MUTED)
        canvas.drawRightString(W - 20*mm, H - 17*mm, ext_name[:60])

        # --- footer ---
        canvas.setFillColor(C_SURFACE)
        canvas.rect(0, 0, W, 18*mm, fill=1, stroke=0)
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(C_MUTED)
        canvas.drawString(20*mm, 9*mm, f'Generated: {time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime())}')
        canvas.drawRightString(W - 20*mm, 9*mm, f'Page {doc.page}')

        canvas.restoreState()

    frame = Frame(
        20*mm, 22*mm,            # x, y of frame origin
        W - 40*mm, H - 52*mm,   # width, height (leaves room for header+footer)
        leftPadding=0, rightPadding=0,
        topPadding=0,  bottomPadding=0
    )
    return PageTemplate(id='main', frames=[frame], onPage=on_page)


# ─── Style sheet ──────────────────────────────────────────────────────────────

def _styles():
    base = getSampleStyleSheet()
    def s(name, **kw):
        return ParagraphStyle(name, **kw)

    return {
        'title':    s('title',    fontName='Helvetica-Bold', fontSize=26,
                       textColor=C_WHITE,    spaceAfter=4),
        'subtitle': s('subtitle', fontName='Helvetica',      fontSize=13,
                       textColor=C_ACCENT,   spaceAfter=2),
        'meta':     s('meta',     fontName='Helvetica',      fontSize=9,
                       textColor=C_MUTED,    spaceAfter=16),
        'desc':     s('desc',     fontName='Helvetica',      fontSize=10,
                       textColor=C_TEXT,     spaceAfter=20),
        'body':     s('body',     fontName='Helvetica',      fontSize=9,
                       textColor=C_TEXT,     leading=14),
        'mono':     s('mono',     fontName='Courier',        fontSize=8,
                       textColor=C_TEXT,     leading=12, wordWrap='CJK'),
        'muted':    s('muted',    fontName='Helvetica',      fontSize=8,
                       textColor=C_MUTED),
        'th':       s('th',       fontName='Helvetica-Bold', fontSize=8,
                       textColor=C_MUTED),
        'cell':     s('cell',     fontName='Helvetica',      fontSize=8,
                       textColor=C_TEXT,     leading=11, wordWrap='CJK'),
        'code':     s('code',     fontName='Courier',        fontSize=7,
                       textColor=C_TEXT,     leading=10, wordWrap='CJK'),
        'warn':     s('warn',     fontName='Helvetica',      fontSize=8,
                       textColor=C_AMBER),
        'danger':   s('danger',   fontName='Helvetica',      fontSize=8,
                       textColor=C_RED),
        'clean':    s('clean',    fontName='Helvetica',      fontSize=8,
                       textColor=C_GREEN),
        'section_head': s('section_head', fontName='Helvetica-Bold', fontSize=10,
                           textColor=C_WHITE),
    }


# ─── Table builder helpers ────────────────────────────────────────────────────

def _base_table_style(col_widths, header_bg=C_SURFACE2):
    return TableStyle([
        # header row
        ('BACKGROUND',  (0, 0), (-1, 0),  header_bg),
        ('TEXTCOLOR',   (0, 0), (-1, 0),  C_MUTED),
        ('FONTNAME',    (0, 0), (-1, 0),  'Helvetica-Bold'),
        ('FONTSIZE',    (0, 0), (-1, 0),  7),
        ('TOPPADDING',  (0, 0), (-1, 0),  5),
        ('BOTTOMPADDING',(0, 0),(-1, 0),  5),
        # data rows
        ('BACKGROUND',  (0, 1), (-1, -1), C_SURFACE),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [C_SURFACE, C_SURFACE2]),
        ('TEXTCOLOR',   (0, 1), (-1, -1), C_TEXT),
        ('FONTNAME',    (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE',    (0, 1), (-1, -1), 8),
        ('TOPPADDING',  (0, 1), (-1, -1), 4),
        ('BOTTOMPADDING',(0, 1),(-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING',(0, 0), (-1, -1), 8),
        # grid
        ('LINEABOVE',   (0, 1), (-1, 1),  0.5, C_BORDER),
        ('LINEBELOW',   (0, -1),(-1, -1), 0.5, C_BORDER),
        ('VALIGN',      (0, 0), (-1, -1), 'TOP'),
    ])


def _empty_notice(st, msg='No data found.'):
    return Paragraph(f'<i>{msg}</i>', st['muted'])


def _section(title, content_flowables, count=None):
    """Wraps a section header + content in a KeepTogether where feasible."""
    badge = f'  ({count})' if count is not None else ''
    header = ColoredRect(title.upper() + badge, bg=C_ACCENT)
    return [Spacer(1, 10), header, Spacer(1, 6)] + content_flowables


# ─── Section builders ─────────────────────────────────────────────────────────

def _build_permissions(report, st, avail_w):
    perms = report.get('permissions', [])
    if not perms:
        return [_empty_notice(st, 'No permissions declared.')]

    rows = [[
        Paragraph('RISK', st['th']),
        Paragraph('PERMISSION', st['th']),
        Paragraph('DESCRIPTION', st['th']),
        Paragraph('WARNING', st['th']),
    ]]
    for p in perms:
        risk  = p.get('risk', 'none').lower()
        bg, fg = RISK_COLORS.get(risk, RISK_COLORS['none'])
        risk_para = Paragraph(risk.upper(), ParagraphStyle(
            'rp', fontName='Helvetica-Bold', fontSize=7,
            textColor=fg, backColor=bg, borderPadding=3
        ))
        warn = p.get('warning', 'na')
        warn_para = Paragraph(warn if warn != 'na' else '—', st['warn'] if warn != 'na' else st['muted'])
        rows.append([
            risk_para,
            Paragraph(f'<font name="Courier">{p.get("name","")}</font>', st['cell']),
            Paragraph(p.get('description', '—'), st['cell']),
            warn_para,
        ])

    col_w = [avail_w * r for r in [0.10, 0.22, 0.40, 0.28]]
    t = Table(rows, colWidths=col_w, repeatRows=1)
    t.setStyle(_base_table_style(col_w))
    return [t]


def _build_urls(report, st, avail_w):
    urls = report.get('urls', [])
    if not urls:
        return [_empty_notice(st, 'No URLs extracted.')]

    seen = set()
    rows = [[
        Paragraph('URL', st['th']),
        Paragraph('DOMAIN', st['th']),
        Paragraph('FOUND IN FILE', st['th']),
    ]]
    for u in urls:
        url = u.get('url', '')
        if url in seen:
            continue
        seen.add(url)
        rows.append([
            Paragraph(url[:120], st['code']),
            Paragraph(u.get('domain', ''), st['cell']),
            Paragraph(u.get('file', ''), st['muted']),
        ])

    col_w = [avail_w * r for r in [0.52, 0.26, 0.22]]
    t = Table(rows, colWidths=col_w, repeatRows=1)
    t.setStyle(_base_table_style(col_w))
    return [t]


def _build_domains(report, st, avail_w):
    domains = report.get('domains', [])
    if not domains:
        return [_empty_notice(st, 'No domains found.')]

    rows = [[
        Paragraph('DOMAIN', st['th']),
        Paragraph('IP', st['th']),
        Paragraph('COUNTRY', st['th']),
        Paragraph('VT SCORE', st['th']),
    ]]
    for d in domains:
        vt   = d.get('virustotal', {})
        if isinstance(vt, dict) and 'positives' in vt and 'total' in vt:
            pos, tot = vt['positives'], vt['total']
            vt_str  = f'{pos}/{tot}'
            vt_style = st['danger'] if pos > 0 else st['clean']
        else:
            vt_str, vt_style = 'n/a', st['muted']
        rows.append([
            Paragraph(d.get('name', ''), st['cell']),
            Paragraph(d.get('ip', 'unknown'), st['code']),
            Paragraph(f"{d.get('country_code','?').upper()}  {d.get('country','unknown')}", st['cell']),
            Paragraph(vt_str, vt_style),
        ])

    col_w = [avail_w * r for r in [0.36, 0.22, 0.26, 0.16]]
    t = Table(rows, colWidths=col_w, repeatRows=1)
    t.setStyle(_base_table_style(col_w))
    return [t]


def _build_ips(report, st, avail_w):
    v4 = [{'address': i['address'], 'type': 'IPv4', 'file': i['file']}
          for i in report.get('ipv4_addresses', [])]
    v6 = [{'address': i['address'], 'type': 'IPv6', 'file': i['file']}
          for i in report.get('ipv6_addresses', [])]
    combined = v4 + v6
    if not combined:
        return [_empty_notice(st, 'No IP addresses found.')]

    rows = [[Paragraph('ADDRESS', st['th']),
             Paragraph('TYPE',    st['th']),
             Paragraph('FILE',    st['th'])]]
    for i in combined:
        rows.append([
            Paragraph(i['address'], st['code']),
            Paragraph(i['type'],    st['muted']),
            Paragraph(i['file'],    st['muted']),
        ])
    col_w = [avail_w * r for r in [0.40, 0.12, 0.48]]
    t = Table(rows, colWidths=col_w, repeatRows=1)
    t.setStyle(_base_table_style(col_w))
    return [t]


def _build_simple_two_col(items, key1, key2, label1, label2, st, avail_w, empty_msg):
    if not items:
        return [_empty_notice(st, empty_msg)]
    rows = [[Paragraph(label1, st['th']), Paragraph(label2, st['th'])]]
    for item in items:
        rows.append([
            Paragraph(str(item.get(key1, ''))[:120], st['code']),
            Paragraph(item.get(key2, ''), st['muted']),
        ])
    col_w = [avail_w * 0.65, avail_w * 0.35]
    t = Table(rows, colWidths=col_w, repeatRows=1)
    t.setStyle(_base_table_style(col_w))
    return [t]


def _build_source_files(source_data, st, avail_w):
    if not source_data:
        return [_empty_notice(st, 'No source files recorded.')]

    rows = [[
        Paragraph('FILE', st['th']),
        Paragraph('PATH', st['th']),
        Paragraph('SIZE', st['th']),
        Paragraph('RETIREJS', st['th']),
    ]]
    for fid, info in source_data.items():
        rjs = info.get('retirejs_result', [])
        if rjs:
            vuln_names = ', '.join(
                f"{v.get('component','?')} {v.get('version','')}" for v in rjs
            )
            rjs_para = Paragraph(f'⚠ {vuln_names[:80]}', st['danger'])
        else:
            rjs_para = Paragraph('✓ clean', st['clean'])

        rows.append([
            Paragraph(info.get('file_name', ''), st['code']),
            Paragraph(info.get('relative_path', ''), st['muted']),
            Paragraph(info.get('file_size', ''), st['muted']),
            rjs_para,
        ])
    col_w = [avail_w * r for r in [0.22, 0.38, 0.10, 0.30]]
    t = Table(rows, colWidths=col_w, repeatRows=1)
    t.setStyle(_base_table_style(col_w))
    return [t]


def _build_manifest(report, st, avail_w):
    manifest = report.get('manifest', {})
    raw = json.dumps(manifest, indent=2)
    # Break into lines, wrap each as a Paragraph to avoid one giant unbreakable block
    flowables = []
    for line in raw.splitlines():
        flowables.append(Paragraph(line.replace(' ', '&nbsp;'), st['code']))
    # Wrap in a light table for the background
    cell = [[f] for f in flowables]
    bg_table = Table([[Spacer(avail_w, 1)]], colWidths=[avail_w])
    bg_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_SURFACE),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING',(0,0), (-1,-1), 10),
        ('TOPPADDING',  (0,0), (-1,-1), 8),
        ('BOTTOMPADDING',(0,0),(-1,-1), 8),
    ]))
    # Simpler: just wrap in a Table with colored bg
    data = [[Paragraph(line.replace(' ', '&nbsp;'), st['code'])] for line in raw.splitlines()]
    t = Table(data, colWidths=[avail_w])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_SURFACE),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING',(0,0),(-1,-1), 2),
    ]))
    return [t]


# ─── Cover page ───────────────────────────────────────────────────────────────

def _build_cover(report, analysis_id, st, avail_w):
    ext_name    = report.get('name', 'Unknown Extension')
    ext_version = report.get('version', '?')
    ext_author  = report.get('author', 'unknown')
    ext_desc    = report.get('description', '')
    ext_type    = report.get('type', '')

    # summary stat cards
    stats = [
        ('Permissions',   len(report.get('permissions', [])),    C_ACCENT),
        ('URLs',          len(report.get('urls', [])),           C_GREEN),
        ('Domains',       len(report.get('domains', [])),        C_AMBER),
        ('IPv4/6 Addrs',  len(report.get('ipv4_addresses', []))
                        + len(report.get('ipv6_addresses', [])), C_ACCENT),
        ('Emails',        len(report.get('emails', [])),         C_GREEN),
        ('BTC Addresses', len(report.get('bitcoin_addresses',[])),C_RED),
        ('Base64 Strings',len(report.get('base64_strings', [])), C_AMBER),
        ('Comments',      len(report.get('comments', [])),       C_MUTED),
    ]

    return [
        Spacer(1, 30),
        Paragraph(ext_name, st['title']),
        Paragraph(f'v{ext_version}  ·  {ext_type}', st['subtitle']),
        Spacer(1, 4),
        Paragraph(
            f'Author: {ext_author}   ·   Analysis ID: {analysis_id}   ·   '
            f'{time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime())}',
            st['meta']
        ),
        HRFlowable(width='100%', thickness=1, color=C_BORDER, spaceAfter=16),
        Paragraph(ext_desc, st['desc']),
        Spacer(1, 10),
        StatCard(stats),
        PageBreak(),
    ]


# ─── Public entry point ───────────────────────────────────────────────────────

def generate_pdf(report_data: dict, source_data: dict, analysis_id: str) -> bytes:
    """
    Build and return a PDF as bytes.
    Caller is responsible for loading the JSON dicts.

    Usage:
        pdf_bytes = generate_pdf(report_data, source_data, analysis_id)
        return send_file(io.BytesIO(pdf_bytes), mimetype='application/pdf', ...)
    """
    buf = io.BytesIO()
    W, H = A4
    avail_w = W - 40*mm     # matches the frame width in _make_page_template

    doc = BaseDocTemplate(
        buf,
        pagesize=A4,
        leftMargin=20*mm, rightMargin=20*mm,
        topMargin=30*mm,  bottomMargin=22*mm,
    )
    ext_name = report_data.get('name', 'Unknown Extension')
    doc.addPageTemplates([_make_page_template(doc, ext_name)])

    st = _styles()

    story = []

    # --- Cover ---
    story += _build_cover(report_data, analysis_id, st, avail_w)

    # --- Permissions ---
    perms = report_data.get('permissions', [])
    story += _section('Permissions', _build_permissions(report_data, st, avail_w), len(perms))

    # --- URLs ---
    urls = report_data.get('urls', [])
    story += _section('URLs Extracted', _build_urls(report_data, st, avail_w), len(urls))

    # --- Domains ---
    doms = report_data.get('domains', [])
    story += _section('Domains & VirusTotal', _build_domains(report_data, st, avail_w), len(doms))

    # --- IPs ---
    ip_count = len(report_data.get('ipv4_addresses', [])) + len(report_data.get('ipv6_addresses', []))
    story += _section('IP Addresses', _build_ips(report_data, st, avail_w), ip_count)

    # --- Emails ---
    emails = report_data.get('emails', [])
    story += _section('Email Addresses',
        _build_simple_two_col(emails, 'mail', 'file', 'EMAIL', 'FILE', st, avail_w, 'No emails found.'),
        len(emails))

    # --- BTC ---
    btcs = report_data.get('bitcoin_addresses', [])
    story += _section('Bitcoin Addresses',
        _build_simple_two_col(btcs, 'address', 'file', 'BTC ADDRESS', 'FILE', st, avail_w, 'No BTC addresses found.'),
        len(btcs))

    # --- Base64 ---
    b64s = report_data.get('base64_strings', [])
    story += _section('Base64 Strings',
        _build_simple_two_col(b64s, 'string', 'file', 'ENCODED STRING', 'FILE', st, avail_w, 'None found.'),
        len(b64s))

    # --- Comments ---
    cmts = report_data.get('comments', [])
    story += _section('Comments Extracted',
        _build_simple_two_col(cmts, 'comment', 'file', 'COMMENT', 'FILE', st, avail_w, 'No comments found.'),
        len(cmts))

    # --- Source files ---
    story += _section('Source Files & RetireJS', _build_source_files(source_data, st, avail_w))

    # --- Manifest ---
    story += _section('manifest.json', _build_manifest(report_data, st, avail_w))

    doc.build(story)
    return buf.getvalue()
