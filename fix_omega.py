import os

JSX_CONTENT = r'''
import React, { useState, useEffect, useRef, useMemo } from 'react';

/**
 * ExtAnalysis - Ω MEGA MASTER INTEGRATION
 * High-Fidelity 1:1 React Port of the entire frontend.
 */

const ALL_STYLES = `
[PASTE_FULL_CSS_HERE]
`;

// --- UTILITIES ---

const jsonTree = (function() {
    var utils = {
        getClass : function(val) { return Object.prototype.toString.call(val); },
        getType : function(val) {
            if (val === null) return 'null';
            switch (typeof val) {
                case 'number': return 'number';
                case 'string': return 'string';
                case 'boolean': return 'boolean';
            }
            switch(utils.getClass(val)) {
                case '[object Array]': return 'array';
                case '[object Object]': return 'object';
            }
            return 'string';
        },
        forEachNode : function(obj, func) {
            var type = utils.getType(obj), isLast;
            if (type === 'array') {
                isLast = obj.length - 1;
                obj.forEach((item, i) => func(i, item, i === isLast));
            } else if (type === 'object') {
                var keys = Object.keys(obj).sort();
                isLast = keys.length - 1;
                keys.forEach((item, i) => func(item, obj[item], i === isLast));
            }
        },
        inherits : (function() {
            var F = function() {};
            return function(Child, Parent) {
                F.prototype = Parent.prototype;
                Child.prototype = new F();
                Child.prototype.constructor = Child;
            };
        })()
    };

    function Node(label, val, isLast) {
        var nodeType = utils.getType(val);
        const Const = {
            'boolean': NodeBoolean, 'number': NodeNumber, 'string': NodeString,
            'null': NodeNull, 'object': NodeObject, 'array': NodeArray
        }[nodeType] || NodeString;
        return new Const(label, val, isLast);
    }

    function _NodeSimple(label, val, isLast) {
        var self = this, el = document.createElement('li');
        self.label = label; self.isComplex = false;
        el.classList.add('jsontree_node');
        el.innerHTML = `<span class="jsontree_label-wrapper"><span class="jsontree_label">"${label}"</span> : </span><span class="jsontree_value-wrapper"><span class="jsontree_value jsontree_value_${this.type}">${val}</span>${!isLast ? ',' : ''}</span>`;
        self.el = el;
    }
    _NodeSimple.prototype = {
        mark: function() { this.el.classList.add('jsontree_node_marked'); },
        unmark: function() { this.el.classList.remove('jsontree_node_marked'); },
        toggleMarked: function() { this.el.classList.toggle('jsontree_node_marked'); }
    };

    function NodeBoolean(label, val, isLast) { this.type = "boolean"; _NodeSimple.call(this, label, val, isLast); }
    utils.inherits(NodeBoolean, _NodeSimple);
    function NodeNumber(label, val, isLast) { this.type = "number"; _NodeSimple.call(this, label, val, isLast); }
    utils.inherits(NodeNumber, _NodeSimple);
    function NodeString(label, val, isLast) { this.type = "string"; _NodeSimple.call(this, label, '"' + val + '"', isLast); }
    utils.inherits(NodeString, _NodeSimple);
    function NodeNull(label, val, isLast) { this.type = "null"; _NodeSimple.call(this, label, val, isLast); }
    utils.inherits(NodeNull, _NodeSimple);

    function _NodeComplex(label, val, isLast) {
        var self = this, el = document.createElement('li');
        self.label = label; self.isComplex = true;
        self.sym = (this.constructor === NodeArray) ? ['[', ']'] : ['{', '}'];
        self.type = (this.constructor === NodeArray) ? "array" : "object";
        
        el.classList.add('jsontree_node', 'jsontree_node_complex');
        let html = '';
        if (label !== null) {
            html += `<span class="jsontree_label-wrapper"><span class="jsontree_label"><span class="jsontree_expand-button"></span>"${label}"</span> : </span>`;
        }
        html += `<div class="jsontree_value-wrapper"><div class="jsontree_value jsontree_value_${self.type}"><b>${self.sym[0]}</b><span class="jsontree_show-more">&hellip;</span><ul class="jsontree_child-nodes"></ul><b>${self.sym[1]}</b></div>${!isLast ? ',' : ''}</div>`;
        el.innerHTML = html;

        self.el = el;
        self.childNodesUl = el.querySelector('.jsontree_child-nodes');
        self.childNodes = [];
        utils.forEachNode(val, function(l, n, last) {
            var child = new Node(l, n, last);
            self.childNodes.push(child);
            self.childNodesUl.appendChild(child.el);
            child.parent = self;
        });

        if (label !== null) {
            el.querySelector('.jsontree_label').addEventListener('click', (e) => self.toggle(e.ctrlKey));
            el.querySelector('.jsontree_show-more').addEventListener('click', (e) => self.toggle(e.ctrlKey));
        } else {
            self.isRoot = true;
            el.classList.add('jsontree_node_expanded');
        }
    }
    utils.inherits(_NodeComplex, _NodeSimple);
    _NodeComplex.prototype.expand = function(rec) { 
        this.el.classList.add('jsontree_node_expanded');
        if(rec) this.childNodes.forEach(c => c.isComplex && c.expand(rec));
    };
    _NodeComplex.prototype.collapse = function(rec) {
        this.el.classList.remove('jsontree_node_expanded');
        if(rec) this.childNodes.forEach(c => c.isComplex && c.collapse(rec));
    };
    _NodeComplex.prototype.toggle = function(rec) {
        this.el.classList.toggle('jsontree_node_expanded');
        if(rec) {
            let exp = this.el.classList.contains('jsontree_node_expanded');
            this.childNodes.forEach(c => c.isComplex && (exp ? c.expand(rec) : c.collapse(rec)));
        }
    };

    function NodeObject(label, val, isLast) { _NodeComplex.call(this, label, val, isLast); }
    utils.inherits(NodeObject, _NodeComplex);
    function NodeArray(label, val, isLast) { _NodeComplex.call(this, label, val, isLast); }
    utils.inherits(NodeArray, _NodeComplex);

    return {
        create: function(data, el) {
            let wrapper = document.createElement('ul');
            wrapper.className = 'jsontree_tree clearfix';
            let root = new Node(null, data, true);
            wrapper.appendChild(root.el);
            el.innerHTML = '';
            el.appendChild(wrapper);
            return root;
        }
    };
})();

// --- COMPONENTS ---

const JsonTree = ({ data, expanded = true }) => {
    const containerRef = useRef(null);
    useEffect(() => {
        if (containerRef.current && data) {
            const tree = jsonTree.create(data, containerRef.current);
            if (expanded) tree.expand('recursive');
        }
    }, [data, expanded]);
    return <div ref={containerRef} className="json-tree-container" />;
};

const DataTable = ({ columns, data, id }) => {
    useEffect(() => {
        const table = window.$(`#${id}`).DataTable({ destroy: true });
        return () => table.destroy();
    }, [data, id]);

    return (
        <table id={id} className="result-table display" style={{ width: '100%' }}>
            <thead>
                <tr>{columns.map(c => <th key={c}>{c}</th>)}</tr>
            </thead>
            <tbody>
                {data.map((row, i) => (
                    <tr key={i}>{row.map((cell, j) => <td key={j}>{cell}</td>)}</tr>
                ))}
            </tbody>
        </table>
    );
};

const VisGraph = ({ data, height = "400px" }) => {
    const containerRef = useRef(null);
    useEffect(() => {
        if (!containerRef.current || !data) return;
        const options = {
            physics: { barnesHut: { gravitationalConstant: -2000, springLength: 95 } },
            nodes: { size: 20, font: { color: '#89ff00' } },
            groups: {
                extension: { shape: 'image', image: '/static/images/extension0.png' },
                js: { shape: 'image', image: '/static/images/js0.png' },
                url: { shape: 'image', image: '/static/images/url0.png' }
            }
        };
        const network = new window.vis.Network(containerRef.current, data, options);
        return () => network.destroy();
    }, [data]);
    return <div ref={containerRef} style={{ height, width: '100%', background: '#1f1f27' }} />;
};

// --- SUB-VIEWS ---

const ReportDetail = ({ report, onBack }) => {
    const [activeTab, setActiveTab] = useState('info');

    const tabs = [
        { id: 'info', label: 'Info', icon: 'fa-info-circle' },
        { id: 'files', label: 'Files', icon: 'fa-file-code' },
        { id: 'perms', label: 'Permissions', icon: 'fa-shield-alt' },
        { id: 'urls', label: 'URLs & Domains', icon: 'fa-globe' },
        { id: 'intel', label: 'Intel', icon: 'fa-brain' }
    ];

    return (
        <div id="result-detail">
            <button onClick={onBack} className="start_scan" style={{marginBottom: '20px'}}>
                <i className="fas fa-arrow-left"></i> Back to Reports
            </button>
            
            <div className="ext-info-body">
                <div className="ext-info-img">
                    {report.icon ? <img src={report.icon} alt="Ext" /> : report.name[0]}
                </div>
                <div className="ext-info-col1">
                    <span className="ext-info-name">{report.name}</span>
                    <div className="ext-info-description">{report.description}</div>
                    <div className="ext-info-others">
                        <span className="ext-info-version">v{report.version}</span>
                        <span className="ext-info-author">By {report.author}</span>
                    </div>
                </div>
            </div>

            <ul className="result-tabs">
                {tabs.map(t => (
                    <li key={t.id} className={activeTab === t.id ? 'current' : ''} onClick={() => setActiveTab(t.id)}>
                        <i className={`fas ${t.icon}`}></i> {t.label}
                    </li>
                ))}
            </ul>

            <div className="tab-content current">
                {activeTab === 'info' && (
                    <div className="info-tab">
                        <h4 className="mid_header">Manifest.json Overview</h4>
                        <JsonTree data={report.manifest || {}} />
                        <h4 className="mid_header" style={{marginTop:'20px'}}>Analysis Metadata</h4>
                        <div className="stats_body">
                            <div className="stats_pill"><div className="stats_data">ID: {report.id}</div></div>
                            <div className="stats_pill"><div className="stats_data">Date: {report.date}</div></div>
                        </div>
                    </div>
                )}

                {activeTab === 'files' && (
                    <div className="files-tab">
                        <h4 className="mid_header">Extension Network Graph</h4>
                        <VisGraph data={report.graph_data} height="500px" />
                        <h4 className="mid_header">File Statistics</h4>
                        <div className="stats_body">
                           {['HTML','JS','CSS','JSON','Images','Other'].map(cat => (
                               <div className="stats_pill" key={cat}>
                                   <div className="stats_data">{cat}: {report.stats?.[cat.toLowerCase()] || 0}</div>
                               </div>
                           ))}
                        </div>
                    </div>
                )}

                {activeTab === 'perms' && (
                    <div className="perms-tab">
                        <h4 className="mid_header">Permission Risks</h4>
                        <div className="permissions-holder">
                            {(report.permissions || []).map(p => (
                                <div className="perm" key={p.name}>
                                    <div className="perm-name" style={{background: p.risk === 'high' ? 'red' : '#3e96fa'}}>{p.name}</div>
                                    <div className="perm-desc">{p.description}</div>
                                    {p.warning && <div className="perm-warn">{p.warning}</div>}
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                {activeTab === 'urls' && (
                    <div className="urls-tab">
                        <h4 className="mid_header">Extracted URLs</h4>
                        <DataTable id="urls-table" columns={['URL','Domain','Source File']} data={report.urls || []} />
                        <h4 className="mid_header" style={{marginTop:'30px'}}>Target Domains</h4>
                        <DataTable id="domains-table" columns={['Domain','Analysis','Whois']} data={report.domains || []} />
                    </div>
                )}

                {activeTab === 'intel' && (
                    <div className="intel-tab">
                        <h4 className="mid_header">Intel & Indicators</h4>
                        <DataTable id="ip-table" columns={['Type','Value','GeoIP']} data={report.ips || []} />
                        <h4 className="mid_header" style={{marginTop:'20px'}}>Crypto Addresses</h4>
                        <DataTable id="btc-table" columns={['Type','Address']} data={report.crypto || []} />
                        <h4 className="mid_header" style={{marginTop:'20px'}}>Emails</h4>
                        <DataTable id="mail-table" columns={['Email','File']} data={report.emails || []} />
                    </div>
                )}
            </div>
        </div>
    );
};

// --- MAIN APPLICATION ---

const ExtAnalysisApp = () => {
    const [view, setView] = useState('dashboard');
    const [theme, setTheme] = useState('dark');
    const [reports, setReports] = useState([]);
    const [selectedReport, setSelectedReport] = useState(null);
    const [logs, setLogs] = useState(["[SYSTEM] ExtAnalysis initialized...", "[SYSTEM] Mode: Omega React Master"]);

    useEffect(() => {
        const styleTag = document.createElement('style');
        styleTag.id = "omega-master-styles";
        styleTag.innerHTML = ALL_STYLES;
        document.head.appendChild(styleTag);
        return () => {
            const el = document.getElementById("omega-master-styles");
            if (el) el.remove();
        };
    }, []);

    const toggleTheme = () => setTheme(theme === 'dark' ? 'light' : 'dark');

    const handleViewReport = (report) => {
        setSelectedReport(report);
        setView('detail');
    };

    return (
        <div className={`wrapper ${theme}-mode`}>
            <div id="loading" style={{display: 'none'}}>
                <img src="/static/images/working.gif" alt="working" /><br />
                <h4>Processing Analysis...</h4>
            </div>

            <div className="logo-placeholder">
                <img src="/static/images/logo.png" className="logo" alt="ExtAnalysis" />
            </div>
            
            <nav className="tabs">
                <div className="selector" style={{ 
                    left: view === 'dashboard' ? '0px' : (view === 'reports' || view === 'detail') ? '106px' : '212px',
                    width: '106px' 
                }}></div>
                <a href="#" className={view === 'dashboard' ? 'active' : ''} onClick={() => setView('dashboard')}>
                    <i className="fas fa-bolt"></i> Analyze
                </a>
                <a href="#" className={(view === 'reports' || view === 'detail') ? 'active' : ''} onClick={() => setView('reports')}>
                    <i className="fas fa-clipboard-list"></i> Reports
                </a>
                <a href="#" className={view === 'settings' ? 'active' : ''} onClick={() => setView('settings')}>
                    <i className="fas fa-cog"></i> Settings
                </a>
            </nav>

            <a href="#" onClick={toggleTheme} className={`dmode ${theme === 'dark' ? 'day' : 'night'}`} title="Toggle Mode">
                <img src={`/static/images/${theme === 'dark' ? 'light.svg' : 'dark.svg'}`} style={{width:27px}} alt="theme" />
            </a>

            <div className="container" id="container">
                {view === 'dashboard' && (
                    <div id="scan-container">
                        <div id="select-scan-type">
                            <div className="mainbut butremote">
                                <img src="/static/images/webstore.png" alt="webstore" /><br />
                                <span className="butdesc">WebStore Analyze</span>
                            </div>
                            <div className="mainbut butlocal">
                                <img src="/static/images/folder.png" alt="folder" /><br />
                                <span className="butdesc">Local Analyze</span>
                            </div>
                            <div style={{marginTop:'20px'}}>
                                <span className="butdesc">Or </span>
                                <a href="#" className="hreflink">Upload Archive (.zip/.crx)</a>
                            </div>
                        </div>
                    </div>
                )}

                {view === 'reports' && (
                    <div id="result-container">
                        <h3 className="mid_header">Historical Analysis Reports</h3>
                        <DataTable 
                            id="result-table" 
                            columns={['ID', 'Name', 'Version', 'Date', 'Action']}
                            data={reports.map(r => [
                                r.id, r.name, r.version, r.date, 
                                <button className="start_scan" onClick={() => handleViewReport(r)}>View</button>
                            ])}
                        />
                    </div>
                )}

                {view === 'detail' && selectedReport && (
                    <ReportDetail report={selectedReport} onBack={() => setView('reports')} />
                )}

                {view === 'settings' && (
                    <div id="update-container">
                        <h3 className="mid_header">General Settings</h3>
                        <div className="option_body">
                            <p className="option_name">Storage Locations</p>
                            <p className="option_description">Reports: <input className="settings_textbox" defaultValue="./reports" /></p>
                            <p className="option_description">Archives: <input className="settings_textbox" defaultValue="./lab" /></p>
                        </div>
                        <div className="option_body">
                            <p className="option_name">Extraction Parameters</p>
                            <div className="switch"><input type="checkbox" id="c1" className="switch-input" defaultChecked /><label htmlFor="c1" className="switch-label">Comments</label></div>
                            <div className="switch"><input type="checkbox" id="c2" className="switch-input" defaultChecked /><label htmlFor="c2" className="switch-label">Crypto Indicators</label></div>
                        </div>
                    </div>
                )}
            </div>

            <div className="log-holder">
                {logs.map((log, i) => <div key={i}>{log}</div>)}
            </div>

            <div className="footer">
                EXTANALYSIS Ω - BROWSER EXTENSION ANALYSIS FRAMEWORK
            </div>
        </div>
    );
};

export default ExtAnalysisApp;
'''

import sys

def main():
    target = r'c:\Users\prakh\Projects\Dashboard\ExtAnalysis-master\ExtAnalysis.jsx'
    css_file = r'c:\Users\prakh\Projects\Dashboard\ExtAnalysis-master\consolidated.css'
    
    with open(css_file, 'r', encoding='utf-8') as f:
        full_css = f.read()
    
    # Escape backticks and dollar signs in the CSS to prevent breaking the template literal
    full_css = full_css.replace('`', '\\`').replace('$', '\\$')
    
    final_jsx = JSX_CONTENT.replace('[PASTE_FULL_CSS_HERE]', full_css)
    
    with open(target, 'w', encoding='utf-8') as f:
        f.write(final_jsx)
    
    print(f"Successfully wrote {len(final_jsx)} characters to {target}")

if __name__ == "__main__":
    main()
