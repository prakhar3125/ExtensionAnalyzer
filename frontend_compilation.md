# ExtAnalysis Frontend Compilation

This file contains the core HTML templates, CSS, and Javascript files for the ExtAnalysis frontend.
*Note: Large third-party minified libraries (jQuery, Vis.js, DataTables, etc.) are excluded to keep this file concise.*

## HTML Templates

### `templates/index.html`

```html
<!-- File: index.html -->
<!--
ExtAnalysis - Browser Extension Analysis Framework
Copyright (C) 2019 - 2022 Tuhinshubhra

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
-->
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>ExtAnalysis - Analyze browser extensions</title>
    <link id="pageStyle" rel="stylesheet" type="text/css" href="{{ url_for('static',filename='css/style.css') }}">
    <link rel="stylesheet" type="text/css" href="{{ url_for('static',filename='css/bttn.css') }}">
    <link rel="stylesheet" type="text/css" href="{{ url_for('static',filename='css/hint.min.css') }}">
    <link href="{{ url_for('static',filename='images/favicon.png') }}" rel="icon"/>
    <script type="text/javascript" src="{{ url_for('static',filename='js/fontawesome.min.js') }}"></script>
    <link href="{{ url_for('static',filename='css/fontawesome.min.css') }}" rel="stylesheet" type="text/css" />
    <style>
        @font-face {
            font-family: "ocraextended";
            src: url("{{ url_for('static',filename='fonts/ocraextended.ttf') }}") format('truetype');
            font-weight: 400;
            font-style: normal;
        }
        @font-face {
            font-family: "Roboto";
            src: url("{{ url_for('static',filename='fonts/Roboto-Regular.ttf') }}") format('truetype');
            font-weight: 400;
            font-style: normal;
        }
        /* Roboto italic */
        @font-face {
            font-family: "Roboto";
            src: url("{{ url_for('static',filename='fonts/Roboto-Italic.ttf') }}") format('truetype');
            font-weight: 400;
            font-style: italic;
        }
        /* Roboto bold */
        @font-face {
            font-family: "Roboto";
            src: url("{{ url_for('static',filename='fonts/Roboto-Bold.ttf') }}") format('truetype');
            font-weight: 700;
            font-style: normal;
        }
    </style>
</head>

<body>
    <div class="noscript" id="noscript">
            <img src="{{ url_for('static',filename='images/error.png') }}">
            <h1>ExtAnalysis needs javascript enabled to work!</h1>
    </div>
    <div class="wrapper">
        <!--
        <h2>ExtAnalysis</h2>
        <h6>Browser Extension Analysis Toolkit!</h6>
        -->
        <div class="logo-placeholder"><img src="{{ url_for('static',filename='images/logo.png') }}" class="logo"></div>
        <nav class="tabs">
            <div class="selector"></div>
            <a href="#" class="active" onclick="showscan()"><i class="fas fa-bolt"></i> Analyze</a>
            <a href="#" onclick="showresult()"><i class="fas fa-clipboard-list"></i> Analysis Reports</a>
            <a href="#" onclick="showupdate()"><i class="fas fa-cog"></i> Settings</a>
        </nav>
        <a href="#" id="lightSwitchOn" onclick="lightsOn()" class="dmode day" title="Enable Light Mode"><img src="{{ url_for('static',filename='images/light.svg') }}" style="width:27px;"></a>
        <a href="#" id="lightSwitchOff" onclick="lightsOff()" class="dmode night" title="Enable Dark Mode"><img src="{{ url_for('static',filename='images/dark.svg') }}" style="width:27px;"></a>

        <div class="container" id="container">
            <!-- modal -->
        <div class="modal-overlay">
                <div class="modal">
    
                    <a class="close-modal">
                        <svg viewBox="0 0 20 20">
                            <path fill="#ff1424" d="M15.898,4.045c-0.271-0.272-0.713-0.272-0.986,0l-4.71,4.711L5.493,4.045c-0.272-0.272-0.714-0.272-0.986,0s-0.272,0.714,0,0.986l4.709,4.711l-4.71,4.711c-0.272,0.271-0.272,0.713,0,0.986c0.136,0.136,0.314,0.203,0.492,0.203c0.179,0,0.357-0.067,0.493-0.203l4.711-4.711l4.71,4.711c0.137,0.136,0.314,0.203,0.494,0.203c0.178,0,0.355-0.067,0.492-0.203c0.273-0.273,0.273-0.715,0-0.986l-4.711-4.711l4.711-4.711C16.172,4.759,16.172,4.317,15.898,4.045z"></path>
                        </svg>
                    </a>
                    <!-- close modal -->
    
                    <div class="modal-content" id="modal-content">
                        <h3>Some content here</h3>
                    </div>
                    <!-- content -->
    
                </div>
                <!-- modal -->
            </div>
            <!-- overlay -->  
                <div id="loading" style="display: none;">
                        <img src="{{ url_for('static',filename='images/working.gif') }}"><br>
                        <h4>ExtAnalysis is working... Please wait!</h4>
                </div>
            <div class="scan-container" id="scan-container">
                <div id="select-scan-type">
                    <div class="tabscontainer">
                <ul class="result-tabs">
                    <li class="tab-link current" data-tab="tab-0"><i class="fab fa-chrome"></i> Chrome Web Store</li>
                    <li class="tab-link" data-tab="tab-3"><i class="fab fa-firefox"></i> Firefox Add-ons</li>
                    <li class="tab-link" data-tab="tab-4"><i class="fab fa-edge"></i> Edge Add-ons</li>
                    <li class="tab-link" data-tab="tab-1"><i class="fas fa-home"></i> Installed Locally</li>
                    <li class="tab-link" data-tab="tab-2"><i class="fas fa-upload"></i> Upload Extension</li>
                </ul>

                <div id="tab-0" class="tab-content current">
                        <h2 class="header_for_sub">Download and Analyze Google Chrome Extensions</h2>
                        <img src="{{ url_for('static',filename='images/webstore.png') }}" style="margin-bottom: 10px;">
                        <!-- h3 id='dl-header'>Enter extension ID or Chrome WebStore link:</h2>
                        <br>-->
                        <br>
                        <div id="webstore">
                            <input type="text" id="extension-id" class="target_box" placeholder="extension id or chrome webstore url">
                            <button onclick="download_and_scan()" class="start_scan"><i class="fas fa-binoculars"></i> Download & Analyze </button>
                        </div>
                        
                        <br><br>
                        <div class="inline-note">You can either enter the extension id or the full url of the chrome webstore.</div>
                </div>

                <div id="tab-3" class="tab-content">
                    <h2 class="header_for_sub">Download and Analyze firefox add-ons</h2>
                    <img src="{{ url_for('static',filename='images/ffaddons.png') }}" style="margin-bottom: 10px;">
                    <!--<h3 id='dl-header'>Enter firefox add-on link:</h2>
                    <br>-->
                    <br>
                    <div id="webstore">
                        <input type="text" id="firefox-addon" class="target_box" placeholder="firefox add-on link">
                        <button onclick="download_and_scan_firefox()" class="start_scan"><i class="fas fa-binoculars"></i> Download & Analyze </button>
                    </div>
                    
                    <br><br>
                    <div class="inline-note">You can either enter the extension id or the full url of the Firefox Addon listing.</div>
                </div>

                <div id="tab-4" class="tab-content">
                    <h2 class="header_for_sub">Download and Analyze Edge add-ons</h2>
                    <img src="{{ url_for('static',filename='images/edgeaddons.png') }}" style="margin-bottom: 10px;">
                    <!--<h3 id='dl-header'>Enter Edge add-on link:</h2>
                    <br>-->
                    <br>
                    <div id="webstore">
                        <input type="text" id="edge-addon" class="target_box" placeholder="edge add-on link">
                        <button onclick="download_and_scan_edge()" class="start_scan"><i class="fas fa-binoculars"></i> Download & Analyze </button>
                    </div>
                    
                    <br><br>
                    <div class="inline-note">You can either enter the extension id or the full url of the Edge Addon listing.</div>
                </div>

                <div id="tab-1" class="tab-content">
                        <h2 class="header_for_sub">Analyze Local Extensions</h2>
                        <img src="{{ url_for('static',filename='images/local.png') }}" style="margin-bottom: 10px;">
                        <br>
                        <div class="pill-container">
                            <div class="pill gchrome" onclick="getLocalExtensions('googlechrome')"><i class="fab fa-chrome"></i> Google Chrome</div>
                            <div class="pill mfirefox" onclick="getLocalExtensions('firefox')"><i class="fab fa-firefox"></i> Mozilla Firefox</div>
                            <div class="pill opera" onclick="getLocalExtensions('brave')"><i class="fab fa-chrome"></i> Brave Browser</div>
                            <div class="pill opera" onclick="getLocalExtensions('vivaldi')"><i class="fab fa-chrome"></i> Vivaldi Browser</div>
                        </div>
                        
                        <div id="local-list" style="margin-top:5px;"></div>
                        <div class="inline-note">You can scan the extensions that you already have installed!</div>
                </div>

                <div id="tab-2" class="tab-content">
                    <h2 class="header_for_sub">Upload and Analyze</h2>
                    <img src="{{ url_for('static',filename='images/upload.png') }}" style="margin-bottom: 10px;">
                   <!-- h3 id='dl-header'><i class="fas fa-upload"></i> Upload .crx files and analyze</h2>-->
                    <br><br>
                   <div id="upload-extension">
                        <form method=post enctype=multipart/form-data action='/upload/' id="upload-form" style="display:inline-block; margin-right:5px; width: 55%;">
                            <input type=file name=file class="upload-container" id="upload-container">
                        </form>
                        <button class="start_scan" onclick="upload_extension()"><i class="fas fa-bolt"></i> Upload & Analyze</button>
                    </div>
                    <br><br>
                    <div class="inline-note">Allowed file extensions: <b>.crx</b>, <b>.xpi</b>, <b>.zip</b>, <b>.tar</b>, <b>.gzip</b></div>
                </div>
                    
                </div>
                </div>
            </div>

            <div class="result-container" id="result-container" style="display:none;">
                <h2 class="header_for_main">Analysis Reports</h2>
                <div id="scan-input">
                    <br>
                    <button id="load_result" onclick="result()" class="start_scan">Load Reports </button>
                    <button class="delete_button" onclick=removeAll()><i class="fas fa-trash"></i> Remove All Results</button>
                    <br>
                </div>
                <div class="result-dirs" id="changeme">

                </div>
                
            </div>

            <div class="update-container" id="update-container" style="display:none;">
                <h2 class="header_for_main">Settings</h2>
                <div class="option_body">
                    <div class="option_name" style="color:#03A9F4; border-bottom: dotted 1px #03a9f4">Basic Settings</div>
                        <div class="sub-head-settings">Reports Directory</div>
                        <div class="option_description">
                            Select the location where you wish your Analysis reports should be placed. By default ExtAnalysis uses "reports" directory inside the project directory.
                        </div>
                    <input type="text" id="reports_dir" class="settings_textbox" placeholder="~/ExtAnalysis/reports/" value="{{report_dir}}">
                    <button class="start_scan" onclick=changeReportsDir()><i class="fas fa-check"></i> Apply</button>
                    <br>
                    <br>
                    <div class="sub-head-settings">Lab Directory</div>
                        <div class="option_description">
                            Set the location where you wish ExtAnalysis to download and extensions for analysis.
                        </div>
                    <input type="text" id="lab_dir" class="settings_textbox" placeholder="~/ExtAnalysis/reports/" value="{{lab_dir}}">
                    <button class="start_scan" onclick=changeLabDir()><i class="fas fa-check"></i> Apply</button>
                    <br>
                    <br>
                    <div class="sub-head-settings">VirusTotal API</div>
                        <div class="option_description">
                            Set or change your VirusTotal api here. If you don't have one yet get it here: <a class="hreflink" href="https://www.virustotal.com/gui/join-us" target="_blank">VirusTotal Signup</a>
                        </div>
                    <input type="text" id="virustotal_api" class="settings_textbox" placeholder="virustotal api" value="{{virustotal_api}}">
                    <button class="start_scan" onclick=changeVTapi()><i class="fas fa-check"></i> Apply</button>
                    <br>
                    <br>
                </div>

                <div class="option_body">
                    <div class="option_name" style="color:#39bb00; border-bottom: dotted 1px #39bb00;">Scan Options</div>
                    <div class="sub-head-settings">
                        Intel Extraction Settings
                    </div>
                    <div class="option_description">
                        Select what intels you want to be extracted from files.
                    </div>
                    <br>
                    <table style="border-spacing: 4px 9px;">
                        <tr>
                            <td><i class="fas fa-comment-alt"></i> Comments:</td>
                            <td><span class="hint--bottom hint--bounce hint--rounded hint--large" aria-label="Set it to false if you want to skip extracting comments from files"><i class="fas fa-question-circle"></i></span></td>
                            <td>
                                <div class="switch">
                                    <input id="extract_comments" type="checkbox" class="switch-input">
                                    <label for="extract_comments" class="switch-label">Switch</label>
                                </div>
                            </td>
                        </tr>
                        <tr>
                            <td><i class="fab fa-btc"></i> BTC address:</td>
                            <td><span class="hint--bottom hint--bounce hint--rounded hint--large" aria-label="Set this to false if you want to skip extracting bitcoin addresses from files"><i class="fas fa-question-circle"></i></span></td>
                            <td>
                                <div class="switch">
                                    <input id="extract_btc_addresses" type="checkbox" class="switch-input">
                                    <label for="extract_btc_addresses" class="switch-label">Switch</label>
                                </div>
                            </td>
                        </tr>
                        <tr>
                            <td><i class="fas fa-key"></i> Base64 strings:</td>
                            <td><span class="hint--bottom hint--bounce hint--rounded hint--large" aria-label="Set this to false if you want to skip extracting base64 encoded strings from files"><i class="fas fa-question-circle"></i></span></td>
                            <td>
                                <div class="switch">
                                    <input id="extract_base64_strings" type="checkbox" class="switch-input">
                                    <label for="extract_base64_strings" class="switch-label">Switch</label>
                                </div>
                            </td>
                        </tr>
                        <tr>
                            <td><i class="fas fa-at"></i> Email Addresses:</td>
                            <td><span class="hint--bottom hint--bounce hint--rounded hint--large" aria-label="Set this to false to skip extracting email addresses from files!"><i class="fas fa-question-circle"></i></span></td>
                            <td>
                                <div class="switch">
                                    <input id="extract_email_addresses" type="checkbox" class="switch-input">
                                    <label for="extract_email_addresses" class="switch-label">Switch</label>
                                </div>
                            </td>
                        </tr>
                        <tr>
                            <td><i class="fas fa-map-marker-alt"></i> IPv4 addresses:</td>
                            <td><span class="hint--bottom hint--bounce hint--rounded hint--large" aria-label="Set this to false if you want to skip extracting IPv4 addresses from files"><i class="fas fa-question-circle"></i></span></td>
                            <td>
                                <div class="switch">
                                    <input id="extract_ipv4_addresses" type="checkbox" class="switch-input">
                                    <label for="extract_ipv4_addresses" class="switch-label">Switch</label>
                                </div>
                            </td>
                        </tr>
                        <tr>
                            <td><i class="fas fa-map-marker-alt"></i> IPv6 addresses:</td>
                            <td><span class="hint--bottom hint--bounce hint--rounded hint--large" aria-label="set this to false if you want to skip extracting IPv6 addresses from files"><i class="fas fa-question-circle"></i></span></td>
                            <td>
                                <div class="switch">
                                    <input id="extract_ipv6_addresses" type="checkbox" class="switch-input">
                                    <label for="extract_ipv6_addresses" class="switch-label">Switch</label>
                                </div>
                            </td>
                        </tr>
                    </table>
                    <br>
                    <div class="sub-head-settings">
                        Other Scan Settings
                    </div>
                    <div class="option_description">
                        Miscellaneous scan options! 
                    </div>
                    <br>
                    <table style="border-spacing: 4px 9px;">
                        <tr>
                            <td><i class="fab fa-css3-alt"></i> Ignore CSS Files:</td>
                            <td><span class="hint--bottom hint--bounce hint--rounded hint--large" aria-label="Set this to false if you want to analyze css files. Disabled by default as css files contain a lot of junk!"><i class="fas fa-question-circle"></i></span></td>
                            <td>
                                <div class="switch">
                                    <input id="ignore_css" type="checkbox" class="switch-input">
                                    <label for="ignore_css" class="switch-label">Switch</label>
                                </div>
                            </td>
                        </tr>
                    </table>
                    <br>
                    <br>
                    <button class="start_scan" onclick=updateIntelExtraction()><i class="fas fa-check"></i> Save Settings</button>
                </div>

                <div class="option_body">
                    <div class="option_name" style="border-bottom: dotted 1px red;">Delete & Clear</div>
                    <div class="sub-head-settings">Delete All Reports</div>
                    <div class="option_description">
                        Deletes all Analysis directories under the reports directory and clears reports.json file. Essentially deleting all Analysis results.
                    </div>
                    <button class="delete_button" onclick=removeAll()><i class="fas fa-trash"></i> Remove All Results</button>
                    <br>
                    <br>
                    <div class="sub-head-settings">Clear Lab Directory</div>
                    <div class="option_description">
                        "lab" is the directory where all the extensions are extracted for analysis... clearing it deletes all the contents of the lab directory.
                        <b>Clearing Lab doesn't effect your results!</b>
                    </div>
                    <button class="delete_button" onclick=clearLab()><i class="fas fa-broom"></i> Clear Lab</button>
                </div>
                
            </div>
        </div>

        <div id="log" class="log-holder">
        </div>
        <div class="log-actions">
            <button class="clear-logs-button" onclick="clearlogs('clearlogs')"><i class="fas fa-broom"></i> Clear Logs</button>
            <button class="logs-explorer-button"><i class="fas fa-compass"></i> Logs Explorer</button>
            <meta name="csrf-token" content="{{ csrf_token() }}">
        </div>
    </div>
    <script type="text/javascript" src="{{ url_for('static',filename='js/jquery.js') }}"></script>
    <script type="text/javascript" src="{{ url_for('static',filename='js/sweetalert.min.js') }}"></script>
    <script type="text/javascript" src="{{ url_for('static',filename='js/main.js') }}"></script>
    <script type="text/javascript" src="{{ url_for('static',filename='js/datatables.min.js') }}"></script>
</body>
<script>
    function update_log(){
        var logurl = '/log/'
        fetch(logurl).then((response) => {
            response.text().then(logs => {
                $('#log')[0].innerHTML = logs;
            });
        });
    }
    var counter = 0;
    var interval = setInterval(function() { update_log() }, 1000);
    $(document).ready(function(){
            
            $('ul.result-tabs li').click(function(){
                var tab_id = $(this).attr('data-tab');
        
                $('ul.result-tabs li').removeClass('current');
                $('.tab-content').removeClass('current');
        
                $(this).addClass('current');
                $("#"+tab_id).addClass('current');
            });

            // set the settings value
            settings = {{settings_json | safe}};

            if (settings['extract_base64_strings'] === true){
                $('#extract_base64_strings')[0].checked = true;
            }

            if (settings['extract_btc_addresses'] === true){
                $('#extract_btc_addresses')[0].checked = true;
            }

            if (settings['extract_comments'] === true){
                $('#extract_comments')[0].checked = true;
            }

            if (settings['extract_email_addresses'] === true){
                $('#extract_email_addresses')[0].checked = true;
            }

            if (settings['extract_ipv4_addresses'] === true){
                $('#extract_ipv4_addresses')[0].checked = true;
            }

            if (settings['extract_ipv6_addresses'] === true){
                $('#extract_ipv6_addresses')[0].checked = true;
            }

            if (settings['ignore_css'] === true){
                $('#ignore_css')[0].checked = true;
            }

        
    })
</script>

</html>

```

### `templates/report.html`

```html
<!-- File: report.html -->
<!--
ExtAnalysis - Browser Extension Analysis Framework
Copyright (C) 2019 - 2022 Tuhinshubhra

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
-->
<!DOCTYPE html>
<html>
<head>
  <title>{{basic_info[0]}} - Analysis Report | ExtAnalysis</title>
  <link rel="stylesheet" type="text/css" href="{{ url_for('static',filename='css/bttn.css') }}">
  <script type="text/javascript" src="{{ url_for('static',filename='js/vis.min.js') }}"></script>
  <script type="text/javascript" src="{{ url_for('static',filename='js/fontawesome.min.js') }}"></script>
  <link href="{{ url_for('static',filename='css/vis-network.min.css') }}" rel="stylesheet" type="text/css" />
  <link href="{{ url_for('static',filename='css/fontawesome.min.css') }}" rel="stylesheet" type="text/css" />
  <link href="{{ url_for('static',filename='css/result.css') }}" rel="stylesheet" type="text/css" />
  <link id="pageStyle" rel="stylesheet" type="text/css" href="{{ url_for('static',filename='css/style.css') }}">
  <link href="{{ url_for('static',filename='images/favicon.png') }}" rel="icon"/>
  <style>
    @font-face {
        font-family: "ocraextended";
        src: url("{{ url_for('static',filename='fonts/ocraextended.ttf') }}") format('truetype');
        font-weight: 400;
        font-style: normal;
    }
    @font-face {
        font-family: "Roboto";
        src: url("{{ url_for('static',filename='fonts/Roboto-Regular.ttf') }}") format('truetype');
        font-weight: 400;
        font-style: normal;
    }
    /* Roboto italic */
    @font-face {
        font-family: "Roboto";
        src: url("{{ url_for('static',filename='fonts/Roboto-Italic.ttf') }}") format('truetype');
        font-weight: 400;
        font-style: italic;
    }
    /* Roboto bold */
    @font-face {
        font-family: "Roboto";
        src: url("{{ url_for('static',filename='fonts/Roboto-Bold.ttf') }}") format('truetype');
        font-weight: 700;
        font-style: normal;
    }
  </style>
</head>
<body>
  <div class="noscript" id="noscript">
            <img src="{{ url_for('static',filename='images/error.png') }}">
            <h1>ExtAnalysis needs javascript enabled to work!</h1>
  </div>
  <div class="logo-placeholder"><a href='/'><img src="{{ url_for('static',filename='images/logo.png') }}" class="logo" id="logo"></a></div>
  <a href="#" id="lightSwitchOn" onclick="lightsOn()" class="dmode day" title="Enable Light Mode"><img src="{{ url_for('static',filename='images/light.svg') }}" style="width:27px;"></a>
  <a href="#" id="lightSwitchOff" onclick="lightsOff()" class="dmode night" title="Enable Dark Mode"><img src="{{ url_for('static',filename='images/dark.svg') }}" style="width:27px;"></a>
  <div class="result-wrapper">
      <div id="loading" style="display: block;">
          <img src="{{ url_for('static',filename='images/working.gif') }}"><br>
          <h4>ExtAnalysis is working... Please wait!</h4>
        </div>
    <div class="ext-info-main">
      <!--div class="ext-info-img">
        <span class="risk-span">75</span>
      </div>-->
              <!-- modal -->
        <div class="modal-overlay">
            <div class="modal">

                <a class="close-modal">
                    <svg viewBox="0 0 20 20">
                        <path fill="#ff1424" d="M15.898,4.045c-0.271-0.272-0.713-0.272-0.986,0l-4.71,4.711L5.493,4.045c-0.272-0.272-0.714-0.272-0.986,0s-0.272,0.714,0,0.986l4.709,4.711l-4.71,4.711c-0.272,0.271-0.272,0.713,0,0.986c0.136,0.136,0.314,0.203,0.492,0.203c0.179,0,0.357-0.067,0.493-0.203l4.711-4.711l4.71,4.711c0.137,0.136,0.314,0.203,0.494,0.203c0.178,0,0.355-0.067,0.492-0.203c0.273-0.273,0.273-0.715,0-0.986l-4.711-4.711l4.711-4.711C16.172,4.759,16.172,4.317,15.898,4.045z"></path>
                    </svg>
                </a>
                <!-- close modal -->

                <div class="modal-content" id="modal-content">
                    <h3>Some content here</h3>
                </div>
                <!-- content -->

            </div>
            <!-- modal -->
        </div>
        <!-- overlay --> 
      <div class="ext-info-body">
        <div class="ext-info-col1">
          <div class="ext-info-name">
            {{basic_info[0]}}
          </div>
          <div class="ext-info-others">
            <div class="ext-info-description">
                {{basic_info[3]}}
            </div>
              <div class="ext-info-version">
                  <i class="fas fa-code-branch"></i> {{basic_info[1]}}
              </div>
              <div class="ext-info-author">
                  <i class="fas fa-user-astronaut"></i> {{basic_info[2]}}
              </div>
              <div class="ext-info-last-scanned">
                  <i class="fab fa-slack-hash"></i> {{analysis_id}}
              </div>
          </div>
        </div>
        <div class="ext-info-col2">
            {{basic_info[4]}}
        </div>
        <div class="ext-info-col3">
            <button class="bttn-material-circle bttn-xs bttn-primary" style=" margin: 5px; "><i class="fas fa-sync-alt"></i></button>
            <button class="bttn-material-circle bttn-xs bttn-danger" style=" margin: 5px; "><i class="fas fa-trash-alt"></i></button>
        </div>
      </div>
    </div>
    <br><br>
    <div class="tabscontainer">
        <meta name="csrf-token" content="{{ csrf_token() }}">

      <ul class="result-tabs">
        <li class="tab-link current" data-tab="tab-0"><i class="fas fa-tree"></i> Basic Info</li>
        <li class="tab-link" data-tab="tab-3"><i class="fas fa-clone"></i> Files</li>
        <li class="tab-link" data-tab="tab-1"><i class="fas fa-heartbeat"></i> Permissions</li>
        <li class="tab-link" data-tab="tab-2"><i class="fas fa-link"></i> URLs & Domains</li>
        <li class="tab-link" data-tab="tab-4"><i class="fas fa-fingerprint"></i> Gathered Intels</li>
      </ul>


      <div id="tab-0" class="tab-content current">
        <div class="sub_section">
          <div class="mid-head">
            <i class="fas fa-search"></i> Scan Info
          </div>
          <div class="sub_body">
              <span class="stats-qa"><span class="stats-q">Analysis ID: </span> <span class="stats-a">{{analysis_id}}</span></span>
              <span class="stats-qa"><span class="stats-q">Name: </span> <span class="stats-a">{{basic_info[0]}}</span></span>
              <span class="stats-qa"><span class="stats-q">Version: </span> <span class="stats-a">{{basic_info[1]}}</span></span>
              <span class="stats-qa"><span class="stats-q">Author: </span> <span class="stats-a">{{basic_info[2]}}</span></span>
              <span class="stats-qa"><span class="stats-q">Type: </span> <span class="stats-a">{{extension_type | safe}}</span></span>
              <span class="stats-qa"><span class="stats-q">Permissions: </span> <span class="stats-a">{{permissions_count}}</span></span>
              <span class="stats-qa"><span class="stats-q">Unique Domains: </span> <span class="stats-a">{{unique_domains}}</span></span>
              <span class="stats-qa"><span class="stats-q">Extracted URLs: </span> <span class="stats-a">{{urls_count}}</span></span>
              <span class="stats-qa"><span class="stats-q">External JavaScript: </span> <span class="stats-a">{{extjs_count}}</span></span>
          </div>
        </div>
          <div class="sub_section">
              <div class="mid-head">
                  <i class="fas fa-tree"></i> manifest.json
              </div>
              <div class="sub_body">
                  <div id="manifest-content"></div>
                  <br>
              </div>
            </div>
      </div>
      <div id="tab-3" class="tab-content">
        <div class="stats-holder">
          <div class="stats">
              <div class="stats_head"><i class="fas fa-network-wired"></i> Files & URLs Graph</div>
              <div id="resultnetwork"></div>
          </div>
          
          <div class="stats">
            <div class="stats_head"><i class="fas fa-chart-pie"></i> Statistics</div>
            <div class="stats_body">
              <div class="stats_pill">
                  <img src="{{ url_for('static',filename='images/html1.png') }}">
                  <div class="stats_data">{{html_files_count}} File(s)</div>
              </div>
              <div class="stats_pill">
                  <img src="{{ url_for('static',filename='images/js1.png') }}">
                  <div class="stats_data">{{js_files_count}} File(s)</div>
              </div>
              <div class="stats_pill">
                  <img src="{{ url_for('static',filename='images/json1.png') }}">
                  <div class="stats_data">{{json_files_count}} File(s)</div>
              </div>
              <div class="stats_pill">
                  <img src="{{ url_for('static',filename='images/css1.png') }}">
                  <div class="stats_data">{{css_files_count}} File(s)</div>
              </div>
              <div class="stats_pill">
                  <img src="{{ url_for('static',filename='images/static1.png') }}">
                  <div class="stats_data">{{static_files_count}} File(s)</div>
              </div>
              <div class="stats_pill">
                  <img src="{{ url_for('static',filename='images/other1.png') }}">
                  <div class="stats_data">{{other_files_count}} File(s)</div>
              </div>
              <center>
                <button class="start_scan" onclick=viewGraph()><i class="fas fa-external-link-alt"></i> View Large Graph</button>
              </center>
            </div>
          </div>
        </div>
          <br>
          <div class="sub_section">
            <div class="mid-head">
                <i class="fas fa-code"></i> View source code of files!
            </div>
            <div class="sub_body">
                {{files_table | safe}}
                <br>
                <div class="inline-note">Only <b>Javascript</b>, <b>CSS</b>, <b>HTML</b> & <b>JSON</b> Files are saved since they contain all the code!</div>
            </div>
          </div>
      </div>
      <div id="tab-1" class="tab-content">
        <div class="p-holder">
          {{permissions_div | safe}}
        </div>
        <div class="inline-note">Click on the Permission <i class="fas fa-hand-point-up"></i> to learn more about it!</div>
      </div>
      <div id="tab-2" class="tab-content">
          <div class="sub_section">
              <div class="mid-head">
                  <i class="fas fa-globe-asia"></i> Domains!
              </div>
              <div class="sub_body">
                  {{domains_table | safe}}
                  <br>
              </div>
            </div>

          <div class="sub_section">
              <div class="mid-head">
                  <i class="fas fa-link"></i> Extracted URLS from files!
              </div>
              <div class="sub_body">
                  {{urls_table | safe}}
                  <br>
              </div>
          </div>

          <div class="sub_section">
            <div class="mid-head">
              <i class="fab fa-js-square"></i> External JavaScript Files!
            </div>
            <div class="sub_body">
                {{extjs_table | safe}}
                <br>
            </div>
        </div>
         
      </div>
      <div id="tab-4" class="tab-content">
          <div class="sub_section">
              <div class="mid-head">
                  <i class="fas fa-map-marker-alt"></i> Extracted IP Addresses
              </div>
              <div class="sub_body">
                  {{ips_table | safe}}
                  <br>
              </div>
            </div>


            <div class="sub_section">
                <div class="mid-head">
                    <i class="fab fa-btc"></i> Extracted Bitcoin Addresses
                </div>
                <div class="sub_body">
                    {{btc_table | safe}}
                    <br>
                </div>
            </div>


            <div class="sub_section">
              <div class="mid-head">
                  <i class="fas fa-at"></i> Extracted Email Addresses
              </div>
              <div class="sub_body">
                  {{mails_table | safe}}
                  <br>
              </div>
            </div>

            <div class="sub_section">
                <div class="mid-head">
                    <i class="fas fa-comment-alt"></i> Extracted Comments
                </div>
                <div class="sub_body">
                    {{comments_table | safe}}
                    <br>
                </div>
            </div>

            <div class="sub_section">
                <div class="mid-head">
                    <i class="fas fa-key"></i> Extracted Base64 Encoded strings
                </div>
                <div class="sub_body">
                    {{base64_table | safe}}
                    <br>
                </div>
            </div>


      </div>

    </div>

  </div>





<script type="text/javascript">
var imagedir = "{{ url_for('static',filename='images/') }}";

{{graph_data|safe}}
// create a network
  var container = document.getElementById('resultnetwork');
  var data = {
    nodes: nodes,
    edges: edges
  };
  var options = {
    physics: {
        adaptiveTimestep: true,
        barnesHut: {
            gravitationalConstant: -8000,
            springConstant: 0.04,
            springLength: 95
        },
        stabilization: {
            iterations: 987
        }
    },
    layout: {
        randomSeed: 191006,
        improvedLayout: false
    },
    interaction: {
        hideEdgesOnDrag: true,
        tooltipDelay: 200
      },
    edges: {
        smooth: {
            type: 'continuous',
            forceDirection: 'horizontal',
            roundness: 0.4
        }
    },
    nodes: {
      size: 20,
            font: {
                size: 15,
                color: '#89ff00'
            }
    }, 
      groups: {
          extension: {
            shape: 'image',
            image: {
                unselected:imagedir + 'extension0.png',
                selected:imagedir + 'extension1.png'
            },
            /** fixed: true,  **/
            /** physics:false **/
          },
          html: {
            shape: 'image',
            image: {
                unselected:imagedir + 'html0.png',
                selected:imagedir + 'html1.png'
            },
            /** fixed: true,  **/
            /** physics:false **/
          },
          css: {
            shape: 'image',
            image: {
                unselected:imagedir + 'css0.png',
                selected:imagedir + 'css1.png'
            },
            /** fixed: true,  **/
            /** physics:false **/
          },
          static: {
            shape: 'image',
            image: {
                unselected:imagedir + 'static0.png',
                selected:imagedir + 'static1.png'
            },
            /** fixed: true,  **/
            /** physics:false **/
          },
          js: {
            shape: 'image',
            image: {
                unselected:imagedir + 'js0.png',
                selected:imagedir + 'js1.png'
            },
            /** fixed: true,  **/
            /** physics:false **/
          },
          json: {
            shape: 'image',
            image: {
                unselected:imagedir + 'json0.png',
                selected:imagedir + 'json1.png'
            },
            /** fixed: true,  **/
            /** physics:false **/
          },
          other: {
            shape: 'image',
            image: {
                unselected:imagedir + 'other0.png',
                selected:imagedir + 'other1.png'
            },
            /** fixed: true,  **/
            /** physics:false **/
          },
          directory: {
            shape: 'image',
            image: {
                unselected:imagedir + 'directory0.png',
                selected:imagedir + 'directory1.png'
            },
            /** fixed: true,  **/
            /** physics:false **/
          },
          url: {
            shape: 'image',
            image: {
                unselected:imagedir + 'url0.png',
                selected:imagedir + 'url1.png'
            },
            /** fixed: true,  **/
            /** physics:false, **/
            /** font: {size:12, color:'blue', face:'sans', background:'white'} **/
          }
      }
  };
  var network = new vis.Network(container, data, options);
  network.on( 'click', function(properties) {
    var ids = properties.nodes;
    var clickedNodes = nodes.get(ids);
    try{
        if (clickedNodes[0]['group'] === 'url'){
        alert(clickedNodes[0]['label']);
        // add a sweetalert and do shits with the url
        }
        // add edit option for js/html/json and css files
    } catch {
        console.log('Handled exception like a boss! - lame yeah i know i wanna die');
    }

});


</script>
<script type="text/javascript" src="{{ url_for('static',filename='js/jquery.js') }}"></script>
<script type="text/javascript" src="{{ url_for('static',filename='js/sweetalert.min.js') }}"></script>
<script type="text/javascript" src="{{ url_for('static',filename='js/main.js') }}"></script>
<script type="text/javascript" src="{{ url_for('static',filename='js/datatables.min.js') }}"></script>
<script type="text/javascript" src="{{ url_for('static',filename='js/jsonTree.js') }}"></script>
<script>
$(document).ready(function(){

	$('ul.result-tabs li').click(function(){
		var tab_id = $(this).attr('data-tab');

		$('ul.result-tabs li').removeClass('current');
		$('.tab-content').removeClass('current');

		$(this).addClass('current');
		$("#"+tab_id).addClass('current');
  })
  $('#files-table').DataTable();
  $('#urls-table').DataTable();
  $('#domains-table').DataTable();
  $('#ips_table').DataTable();
  $('#mails_table').DataTable();
  $('#btc_table').DataTable();
  $('#comments_table').DataTable();
  $('#base64_table').DataTable();
  $('#extjs_table').DataTable();
});

$(function() {
		$("#loading").fadeOut("slow");;
  });
  $(function(){
	$('.accordion .accordion__question').on('click', function(){
		var answer = $(this).next();
		$('.accordion .accordion__answer:visible').not(answer).slideUp(400);
		answer.slideToggle(400);
	});
});

var wrapper = document.getElementById("manifest-content");
var data = {{manifest_content | safe}}
try {
    var data = JSON.parse(data);
} catch (e) {}
var tree = jsonTree.create(data, wrapper);
tree.expand(function(node) {
   return node.childNodes.length < 2 || node.label === 'phoneNumbers';
});


function viewGraph(){
  var final_url = '/view-graph/' + '{{analysis_id}}';
  window.open(final_url, target = "_blank");
}
</script>
<br><br>
</body>
</html>

```

### `templates/graph.html`

```html
<!-- File: graph.html -->
<!--
ExtAnalysis - Browser Extension Analysis Framework
Copyright (C) 2019 - 2022 Tuhinshubhra

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
-->
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Graph Viewer | ExtAnalysis</title>
    <link rel="stylesheet" type="text/css" href="{{ url_for('static',filename='css/bttn.css') }}">
    <script type="text/javascript" src="{{ url_for('static',filename='js/vis.min.js') }}"></script>
    <script type="text/javascript" src="{{ url_for('static',filename='js/fontawesome.min.js') }}"></script>
    <link href="{{ url_for('static',filename='css/vis-network.min.css') }}" rel="stylesheet" type="text/css" />
    <link href="{{ url_for('static',filename='css/fontawesome.min.css') }}" rel="stylesheet" type="text/css" />
    <link href="{{ url_for('static',filename='css/result.css') }}" rel="stylesheet" type="text/css" />
    <link id="pageStyle" rel="stylesheet" type="text/css" href="{{ url_for('static',filename='css/style.css') }}">
    <link href="{{ url_for('static',filename='images/favicon.png') }}" rel="icon"/>
    <style>
        @font-face {
            font-family: "ocraextended";
            src: url("{{ url_for('static',filename='fonts/ocraextended.ttf') }}") format('truetype');
            font-weight: 400;
            font-style: normal;
        }
        @font-face {
            font-family: "Roboto";
            src: url("{{ url_for('static',filename='fonts/Roboto-Regular.ttf') }}") format('truetype');
            font-weight: 400;
            font-style: normal;
        }
        /* Roboto italic */
        @font-face {
            font-family: "Roboto";
            src: url("{{ url_for('static',filename='fonts/Roboto-Italic.ttf') }}") format('truetype');
            font-weight: 400;
            font-style: italic;
        }
        /* Roboto bold */
        @font-face {
            font-family: "Roboto";
            src: url("{{ url_for('static',filename='fonts/Roboto-Bold.ttf') }}") format('truetype');
            font-weight: 700;
            font-style: normal;
        }
        
    </style>
</head>

<body>
    <div class="noscript" id="noscript">
            <img src="{{ url_for('static',filename='images/error.png') }}">
            <h1>ExtAnalysis needs javascript enabled to work!</h1>
    </div>
    <div class="wrapper">
        <div id="loading" style="display: block;">
            <img src="{{ url_for('static',filename='images/working.gif') }}"><br>
            <h4>Please wait.. plotting graph might take some time!</h4>
        </div>
        <div class="logo-placeholder"><a href='/'><img src="{{ url_for('static',filename='images/logo.png') }}" class="logo" id="logo"></a></div>
        <a href="#" id="lightSwitchOn" onclick="lightsOn()" class="dmode day" title="Enable Light Mode"><img src="{{ url_for('static',filename='images/light.svg') }}" style="width:27px;"></a>
        <a href="#" id="lightSwitchOff" onclick="lightsOff()" class="dmode night" title="Enable Dark Mode"><img src="{{ url_for('static',filename='images/dark.svg') }}" style="width:27px;"></a>

        <div class="graph-container" id="container">
            <div id="large-graph"></div>
            <div class="graph-control">
                <div class="control-title">Controls</div>
                <div class="control-body">
                    <div class="selected-node" id="selected-node">
                        <span class="selected-title">SELECTED NODE</span>
                        ID: <span id="selected-node-id">None</span>
                        <br>
                        Name: <span id="selected-node-label">None</span>
                        <br>
                        Group: <span id="selected-node-group">None</span>
                        <br>
                        Parent: <span id="selected-node-parent">None</span>
                        <br>
                        <!--
                            TODO: add these functions and enable the buttons
                            <button onclick="hideSelectedGroup()" class="control-button"><i class="fas fa-trash"></i> Delete Group</button>
                            <button onclick="hideSelectedNode()" class="control-button"><i class="fas fa-trash-alt"></i> Delete Node</button>
                        -->
                        <button onclick="clusterBySelf()" class="control-button">Parent Cluster</button>
                        <button onclick="clusterBySelf(true)" class="control-button">Cluster by Self</button>
                    </div>
                    <button onclick="resetGraph()" class="control-button"><i class="fas fa-undo"></i> Reset Graph</button>
                </div>
            </div>
        </div>

    </div>
    <script type="text/javascript" src="{{ url_for('static',filename='js/jquery.js') }}"></script>
    <script type="text/javascript" src="{{ url_for('static',filename='js/main.js') }}"></script>
    <script type="text/javascript" src="{{ url_for('static',filename='js/sweetalert.min.js') }}"></script>
    <script>
        var imagedir = "{{ url_for('static',filename='images/') }}";
        {{graph_data|safe}}
    </script>
    <script type="text/javascript" src="{{ url_for('static',filename='js/graph.js') }}"></script>
</body>

</html>

```

### `templates/source.html`

```html
<!-- File: source.html -->
<!--
ExtAnalysis - Browser Extension Analysis Framework
Copyright (C) 2019 - 2022 Tuhinshubhra

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
-->
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{{file_name}} Source | ExtAnalysis</title>
    <link id="pageStyle" rel="stylesheet" type="text/css" href="{{ url_for('static',filename='css/style.css') }}">
    <link rel="stylesheet" type="text/css" href="{{ url_for('static',filename='css/bttn.css') }}">
    <link href="{{ url_for('static',filename='images/favicon.png') }}" rel="icon"/>
    <link rel="stylesheet" href="{{ url_for('static',filename='css/codemirror.css') }}">
    <link rel="stylesheet" href="{{ url_for('static',filename='css/material.css') }}">
    <script type="text/javascript" src="{{ url_for('static',filename='js/fontawesome.min.js') }}"></script>
    <link href="{{ url_for('static',filename='css/fontawesome.min.css') }}" rel="stylesheet" type="text/css" />
    <style>
        @font-face {
            font-family: "ocraextended";
            src: url("{{ url_for('static',filename='fonts/ocraextended.ttf') }}") format('truetype');
            font-weight: 400;
            font-style: normal;
        }
        @font-face {
            font-family: "Roboto";
            src: url("{{ url_for('static',filename='fonts/Roboto-Regular.ttf') }}") format('truetype');
            font-weight: 400;
            font-style: normal;
        }
        /* Roboto italic */
        @font-face {
            font-family: "Roboto";
            src: url("{{ url_for('static',filename='fonts/Roboto-Italic.ttf') }}") format('truetype');
            font-weight: 400;
            font-style: italic;
        }
        /* Roboto bold */
        @font-face {
            font-family: "Roboto";
            src: url("{{ url_for('static',filename='fonts/Roboto-Bold.ttf') }}") format('truetype');
            font-weight: 700;
            font-style: normal;
        }
    </style>
</head>

<body>
    <div class="noscript" id="noscript">
            <img src="{{ url_for('static',filename='images/error.png') }}">
            <h1>ExtAnalysis needs javascript enabled to work!</h1>
    </div>
    <div class="wrapper">
        <!--
        <h2>ExtAnalysis</h2>
        <h6>Browser Extension Analysis Toolkit!</h6>
        -->
        <div class="logo-placeholder"><a href='/'><img src="{{ url_for('static',filename='images/logo.png') }}" class="logo" id="logo"></a></div>
        <a href="#" id="lightSwitchOn" onclick="lightsOn()" class="dmode day" title="Enable Light Mode"><img src="{{ url_for('static',filename='images/light.svg') }}" style="width:27px;"></a>
        <a href="#" id="lightSwitchOff" onclick="lightsOff()" class="dmode night" title="Enable Dark Mode"><img src="{{ url_for('static',filename='images/dark.svg') }}" style="width:27px;"></a>

        <div class="container" id="container">
            <div class="file_info">
                <div class="file_image">
                    {{file_icon | safe}}
                </div>
                <div class="file_body">
                    <div class="file_name">Showing File: {{file_name}}</div>
                    <div class="file_attrs">
                        <div class="file_location">
                            <div class="file_icon">
                                <i class="fas fa-folder"></i>
                            </div>
                            {{file_location}}
                        </div>
                        <div class="file_type">
                            <div class="file_icon">
                                <i class="fas fa-file"></i>
                            </div>
                            {{file_type}} File
                        </div>
                        <div class="file_size">
                            <div class="file_icon">
                                <i class="fas fa-weight"></i> 
                            </div>
                            {{file_size}}
                        </div>
                    </div>
                </div>
            </div>

            <textarea class="source_code" id="editor">
                {{file_source}}
            </textarea>
            <div class="editor_buttons">
                    <button class="format_button" onclick="formatSelection()"><i class="fas fa-hat-wizard"></i> Beautify Selected Code</button>
                    <button class="format_button" onclick="autoFormatSelection()"><i class="fas fa-magic"></i> Beautify Full Code</button>
            </div>
        </div>

    </div>
    <script type="text/javascript" src="{{ url_for('static',filename='js/jquery.js') }}"></script>
    <script type="text/javascript" src="{{ url_for('static',filename='js/main.js') }}"></script>
    <script src="{{ url_for('static',filename='js/codemirror.js') }}"></script>
    <script src="{{ url_for('static',filename='js/javascript.js') }}"></script>
    <script src="{{ url_for('static',filename='js/htmlmixed.js') }}"></script>
    <script src="{{ url_for('static',filename='js/css.js') }}"></script>
    <script src="{{ url_for('static',filename='js/xml.js') }}"></script>
    <script src="{{ url_for('static',filename='js/beautify.js') }}"></script>
</body>
<script>
    code_mode = '{{file_type}}'
    if (code_mode === 'html'){code_type = 'htmlmixed'} else if (code_mode === 'json'){code_type = 'javascript'} else if (code_mode === 'css'){code_type = 'css'} else {code_type = 'javascript'}
    var codemirror = CodeMirror.fromTextArea(document.getElementById('editor'), {
        mode: code_type,
        theme: "material",
        lineNumbers: true,
        readOnly: false
    });
    
    function getSelectedRange() {
        return { from: codemirror.getCursor(true), to: codemirror.getCursor(false) };
      }
    function autoFormatSelection() {
        if (code_type === 'javascript'){
            var currentValue = codemirror.getValue();
            var newval = js_beautify(currentValue);
            codemirror.setValue(newval);
        } 
        totalLines = codemirror.lineCount();
        codemirror.autoFormatRange({line:0, ch:0}, {line:totalLines});

    }
    function formatSelection() {
        var range = getSelectedRange();
        codemirror.autoFormatRange(range.from, range.to);
    }
      (function() {

        CodeMirror.extendMode("css", {
        commentStart: "/*",
        commentEnd: "*/",
        newlineAfterToken: function(type, content) {
            return /^[;{}]$/.test(content);
        }
        });

        CodeMirror.extendMode("javascript", {
        commentStart: "/*",
        commentEnd: "*/",
        // FIXME semicolons inside of for
        newlineAfterToken: function(type, content, textAfter, state) {
            if (this.jsonMode) {
            return /^[\[,{]$/.test(content) || /^}/.test(textAfter);
            } else {
            if (content == ";" && state.lexical && state.lexical.type == ")") return false;
            return /^[;{}]$/.test(content) && !/^;/.test(textAfter);
            }
        }
        });

        CodeMirror.extendMode("xml", {
        commentStart: "<!--",
        commentEnd: "-->",
        newlineAfterToken: function(type, content, textAfter) {
            return type == "tag" && />$/.test(content) || /^</.test(textAfter);
        }
        });

        // Comment/uncomment the specified range
        CodeMirror.defineExtension("commentRange", function (isComment, from, to) {
        var cm = this, curMode = CodeMirror.innerMode(cm.getMode(), cm.getTokenAt(from).state).mode;
        cm.operation(function() {
            if (isComment) { // Comment range
            cm.replaceRange(curMode.commentEnd, to);
            cm.replaceRange(curMode.commentStart, from);
            if (from.line == to.line && from.ch == to.ch) // An empty comment inserted - put cursor inside
                cm.setCursor(from.line, from.ch + curMode.commentStart.length);
            } else { // Uncomment range
            var selText = cm.getRange(from, to);
            var startIndex = selText.indexOf(curMode.commentStart);
            var endIndex = selText.lastIndexOf(curMode.commentEnd);
            if (startIndex > -1 && endIndex > -1 && endIndex > startIndex) {
                // Take string till comment start
                selText = selText.substr(0, startIndex)
                // From comment start till comment end
                + selText.substring(startIndex + curMode.commentStart.length, endIndex)
                // From comment end till string end
                + selText.substr(endIndex + curMode.commentEnd.length);
            }
            cm.replaceRange(selText, from, to);
            }
        });
        });

        // Applies automatic mode-aware indentation to the specified range
        CodeMirror.defineExtension("autoIndentRange", function (from, to) {
        var cmInstance = this;
        this.operation(function () {
            for (var i = from.line; i <= to.line; i++) {
            cmInstance.indentLine(i, "smart");
            }
        });
        });

        // Applies automatic formatting to the specified range
        CodeMirror.defineExtension("autoFormatRange", function (from, to) {
        var cm = this;
        var outer = cm.getMode(), text = cm.getRange(from, to).split("\n");
        var state = CodeMirror.copyState(outer, cm.getTokenAt(from).state);
        var tabSize = cm.getOption("tabSize");

        var out = "", lines = 0, atSol = from.ch == 0;
        function newline() {
            out += "\n";
            atSol = true;
            ++lines;
        }

        for (var i = 0; i < text.length; ++i) {
            var stream = new CodeMirror.StringStream(text[i], tabSize);
            while (!stream.eol()) {
            var inner = CodeMirror.innerMode(outer, state);
            var style = outer.token(stream, state), cur = stream.current();
            stream.start = stream.pos;
            if (!atSol || /\S/.test(cur)) {
                out += cur;
                atSol = false;
            }
            if (!atSol && inner.mode.newlineAfterToken &&
                inner.mode.newlineAfterToken(style, cur, stream.string.slice(stream.pos) || text[i+1] || "", inner.state))
                newline();
            }
            if (!stream.pos && outer.blankLine) outer.blankLine(state);
            if (!atSol) newline();
        }

        cm.operation(function () {
            cm.replaceRange(out, from, to);
            for (var cur = from.line + 1, end = from.line + lines; cur <= end; ++cur)
            cm.indentLine(cur, "smart");
            cm.setSelection(from, cm.getCursor(false));
        });
        });
        })();
</script>
</html>

```

### `templates/sourcecode.html`

```html
<!-- File: sourcecode.html -->
<!--
ExtAnalysis - Browser Extension Analysis Framework
Copyright (C) 2019 - 2022 Tuhinshubhra

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
-->
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Source Code from URL | ExtAnalysis</title>
    <link id="pageStyle" rel="stylesheet" type="text/css" href="{{ url_for('static',filename='css/style.css') }}">
    <link rel="stylesheet" type="text/css" href="{{ url_for('static',filename='css/bttn.css') }}">
    <link href="{{ url_for('static',filename='images/favicon.png') }}" rel="icon"/>
    <link rel="stylesheet" href="{{ url_for('static',filename='css/codemirror.css') }}">
    <link rel="stylesheet" href="{{ url_for('static',filename='css/material.css') }}">
    <script type="text/javascript" src="{{ url_for('static',filename='js/fontawesome.min.js') }}"></script>
    <link href="{{ url_for('static',filename='css/fontawesome.min.css') }}" rel="stylesheet" type="text/css" />
    <style>
        @font-face {
            font-family: "ocraextended";
            src: url("{{ url_for('static',filename='fonts/ocraextended.ttf') }}") format('truetype');
            font-weight: 400;
            font-style: normal;
        }
        @font-face {
            font-family: "Roboto";
            src: url("{{ url_for('static',filename='fonts/Roboto-Regular.ttf') }}") format('truetype');
            font-weight: 400;
            font-style: normal;
        }
        /* Roboto italic */
        @font-face {
            font-family: "Roboto";
            src: url("{{ url_for('static',filename='fonts/Roboto-Italic.ttf') }}") format('truetype');
            font-weight: 400;
            font-style: italic;
        }
        /* Roboto bold */
        @font-face {
            font-family: "Roboto";
            src: url("{{ url_for('static',filename='fonts/Roboto-Bold.ttf') }}") format('truetype');
            font-weight: 700;
            font-style: normal;
        }
    </style>
</head>

<body>
    <div class="noscript" id="noscript">
            <img src="{{ url_for('static',filename='images/error.png') }}">
            <h1>ExtAnalysis needs javascript enabled to work!</h1>
    </div>
    <div class="wrapper">
        <!--
        <h2>ExtAnalysis</h2>
        <h6>Browser Extension Analysis Toolkit!</h6>
        -->
        <div class="logo-placeholder"><a href='/'><img src="{{ url_for('static',filename='images/logo.png') }}" class="logo" id="logo"></a></div>
        <a href="#" id="lightSwitchOn" onclick="lightsOn()" class="dmode day" title="Enable Light Mode"><img src="{{ url_for('static',filename='images/light.svg') }}" style="width:27px;"></a>
        <a href="#" id="lightSwitchOff" onclick="lightsOff()" class="dmode night" title="Enable Dark Mode"><img src="{{ url_for('static',filename='images/dark.svg') }}" style="width:27px;"></a>

        <div class="container" id="container">
            <div class="file_info">
                <div class="file_image">
                    {{url_icon | safe}}
                </div>
                <div class="file_body">
                    <div class="file_name" style="font-size: 14px;letter-spacing: 0.5px;">Target URL: {{target_url}}</div>
                    <div class="file_attrs">
                        <div class="file_location">
                            <div class="file_icon">
                                <i class="fas fa-folder"></i>
                            </div>
                            ...
                        </div>
                        <div class="file_type">
                            <div class="file_icon">
                                <i class="fas fa-file"></i>
                            </div>
                             URL
                        </div>
                        <div class="file_size">
                            <div class="file_icon">
                                <i class="fas fa-weight"></i> 
                            </div>
                            ...
                        </div>
                    </div>
                </div>
            </div>

            <textarea class="source_code" id="editor">
                {{source_code}}
            </textarea>
            <div class="editor_buttons">
                    <button class="format_button" onclick="formatSelection()"><i class="fas fa-hat-wizard"></i> Beautify Selected Code</button>
                    <button class="format_button" onclick="autoFormatSelection()"><i class="fas fa-magic"></i> Beautify Full Code</button>
            </div>
            <div class="inline-note">Use the <b>beautify selected code</b> option in case <b>beautify full code</b> breaks layout!</div>
        </div>

    </div>
    <script type="text/javascript" src="{{ url_for('static',filename='js/jquery.js') }}"></script>
    <script type="text/javascript" src="{{ url_for('static',filename='js/main.js') }}"></script>
    <script src="{{ url_for('static',filename='js/codemirror.js') }}"></script>
    <script src="{{ url_for('static',filename='js/javascript.js') }}"></script>
    <script src="{{ url_for('static',filename='js/htmlmixed.js') }}"></script>
    <script src="{{ url_for('static',filename='js/css.js') }}"></script>
    <script src="{{ url_for('static',filename='js/xml.js') }}"></script>
    <script src="{{ url_for('static',filename='js/beautify.js') }}"></script>
</body>
<script>
    code_mode = '{{file_type}}'
    if (code_mode === 'html'){code_type = 'htmlmixed'} else if (code_mode === 'json'){code_type = 'javascript'} else if (code_mode === 'css'){code_type = 'css'} else {code_type = 'javascript'}
    var codemirror = CodeMirror.fromTextArea(document.getElementById('editor'), {
        mode: code_type,
        theme: "material",
        lineNumbers: true,
        readOnly: false
    });
    
    function getSelectedRange() {
        return { from: codemirror.getCursor(true), to: codemirror.getCursor(false) };
      }
    function autoFormatSelection() {
        if (code_type === 'javascript'){
            var currentValue = codemirror.getValue();
            var newval = js_beautify(currentValue);
            codemirror.setValue(newval);
        } 
        totalLines = codemirror.lineCount();
        codemirror.autoFormatRange({line:0, ch:0}, {line:totalLines});

    }
    function formatSelection() {
        var range = getSelectedRange();
        codemirror.autoFormatRange(range.from, range.to);
    }
      (function() {

        CodeMirror.extendMode("css", {
        commentStart: "/*",
        commentEnd: "*/",
        newlineAfterToken: function(type, content) {
            return /^[;{}]$/.test(content);
        }
        });

        CodeMirror.extendMode("javascript", {
        commentStart: "/*",
        commentEnd: "*/",
        // FIXME semicolons inside of for
        newlineAfterToken: function(type, content, textAfter, state) {
            if (this.jsonMode) {
            return /^[\[,{]$/.test(content) || /^}/.test(textAfter);
            } else {
            if (content == ";" && state.lexical && state.lexical.type == ")") return false;
            return /^[;{}]$/.test(content) && !/^;/.test(textAfter);
            }
        }
        });

        CodeMirror.extendMode("xml", {
        commentStart: "<!--",
        commentEnd: "-->",
        newlineAfterToken: function(type, content, textAfter) {
            return type == "tag" && />$/.test(content) || /^</.test(textAfter);
        }
        });

        // Comment/uncomment the specified range
        CodeMirror.defineExtension("commentRange", function (isComment, from, to) {
        var cm = this, curMode = CodeMirror.innerMode(cm.getMode(), cm.getTokenAt(from).state).mode;
        cm.operation(function() {
            if (isComment) { // Comment range
            cm.replaceRange(curMode.commentEnd, to);
            cm.replaceRange(curMode.commentStart, from);
            if (from.line == to.line && from.ch == to.ch) // An empty comment inserted - put cursor inside
                cm.setCursor(from.line, from.ch + curMode.commentStart.length);
            } else { // Uncomment range
            var selText = cm.getRange(from, to);
            var startIndex = selText.indexOf(curMode.commentStart);
            var endIndex = selText.lastIndexOf(curMode.commentEnd);
            if (startIndex > -1 && endIndex > -1 && endIndex > startIndex) {
                // Take string till comment start
                selText = selText.substr(0, startIndex)
                // From comment start till comment end
                + selText.substring(startIndex + curMode.commentStart.length, endIndex)
                // From comment end till string end
                + selText.substr(endIndex + curMode.commentEnd.length);
            }
            cm.replaceRange(selText, from, to);
            }
        });
        });

        // Applies automatic mode-aware indentation to the specified range
        CodeMirror.defineExtension("autoIndentRange", function (from, to) {
        var cmInstance = this;
        this.operation(function () {
            for (var i = from.line; i <= to.line; i++) {
            cmInstance.indentLine(i, "smart");
            }
        });
        });

        // Applies automatic formatting to the specified range
        CodeMirror.defineExtension("autoFormatRange", function (from, to) {
        var cm = this;
        var outer = cm.getMode(), text = cm.getRange(from, to).split("\n");
        var state = CodeMirror.copyState(outer, cm.getTokenAt(from).state);
        var tabSize = cm.getOption("tabSize");

        var out = "", lines = 0, atSol = from.ch == 0;
        function newline() {
            out += "\n";
            atSol = true;
            ++lines;
        }

        for (var i = 0; i < text.length; ++i) {
            var stream = new CodeMirror.StringStream(text[i], tabSize);
            while (!stream.eol()) {
            var inner = CodeMirror.innerMode(outer, state);
            var style = outer.token(stream, state), cur = stream.current();
            stream.start = stream.pos;
            if (!atSol || /\S/.test(cur)) {
                out += cur;
                atSol = false;
            }
            if (!atSol && inner.mode.newlineAfterToken &&
                inner.mode.newlineAfterToken(style, cur, stream.string.slice(stream.pos) || text[i+1] || "", inner.state))
                newline();
            }
            if (!stream.pos && outer.blankLine) outer.blankLine(state);
            if (!atSol) newline();
        }

        cm.operation(function () {
            cm.replaceRange(out, from, to);
            for (var cur = from.line + 1, end = from.line + lines; cur <= end; ++cur)
            cm.indentLine(cur, "smart");
            cm.setSelection(from, cm.getCursor(false));
        });
        });
        })();
</script>
</html>

```

### `templates/error.html`

```html
<!-- File: error.html -->
<!--
ExtAnalysis - Browser Extension Analysis Framework
Copyright (C) 2019 - 2022 Tuhinshubhra

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
-->
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{{error_title}} | ExtAnalysis</title>
    <link id="pageStyle" rel="stylesheet" type="text/css" href="{{ url_for('static',filename='css/style.css') }}">
    <link rel="stylesheet" type="text/css" href="{{ url_for('static',filename='css/bttn.css') }}">
    <link href="{{ url_for('static',filename='images/favicon.png') }}" rel="icon"/>
    <script type="text/javascript" src="{{ url_for('static',filename='js/fontawesome.min.js') }}"></script>
    <link href="{{ url_for('static',filename='css/fontawesome.min.css') }}" rel="stylesheet" type="text/css" />
    <style>
        @font-face {
            font-family: "ocraextended";
            src: url("{{ url_for('static',filename='fonts/ocraextended.ttf') }}") format('truetype');
            font-weight: 400;
            font-style: normal;
        }
        @font-face {
            font-family: "Roboto";
            src: url("{{ url_for('static',filename='fonts/Roboto-Regular.ttf') }}") format('truetype');
            font-weight: 400;
            font-style: normal;
        }
        /* Roboto italic */
        @font-face {
            font-family: "Roboto";
            src: url("{{ url_for('static',filename='fonts/Roboto-Italic.ttf') }}") format('truetype');
            font-weight: 400;
            font-style: italic;
        }
        /* Roboto bold */
        @font-face {
            font-family: "Roboto";
            src: url("{{ url_for('static',filename='fonts/Roboto-Bold.ttf') }}") format('truetype');
            font-weight: 700;
            font-style: normal;
        }
        @-webkit-keyframes rotation {
		from {
				-webkit-transform: rotate(0deg);
		}
		to {
				-webkit-transform: rotate(359deg);
		}
        }
    </style>
</head>

<body>
    <div class="noscript" id="noscript">
            <img src="{{ url_for('static',filename='images/error.png') }}">
            <h1>ExtAnalysis needs javascript enabled to work!</h1>
    </div>
    <div class="wrapper">
        <!--
        <h2>ExtAnalysis</h2>
        <h6>Browser Extension Analysis Toolkit!</h6>
        -->
        <div class="logo-placeholder"><a href='/'><img src="{{ url_for('static',filename='images/logo.png') }}" class="logo" id="logo"></a></div>
        
        <a href="#" id="lightSwitchOn" onclick="lightsOn()" class="dmode day" title="Enable Light Mode"><img src="{{ url_for('static',filename='images/light.svg') }}" style="width:27px;"></a>
        <a href="#" id="lightSwitchOff" onclick="lightsOff()" class="dmode night" title="Enable Dark Mode"><img src="{{ url_for('static',filename='images/dark.svg') }}" style="width:27px;"></a>

        <div class="container" id="container">
            <div class="error-div">
                <h3>{{error_head}}</h3>
                <br>
                <img src="{{ url_for('static',filename='images/techerror.gif') }}" style="width:200px; -webkit-animation: rotation 20s infinite linear; border-radius: 50%;">
                <br><br>
                {{error_txt | safe}}
                <br>
                <div class="inline-note">Click on the logo to go back to homepage</div>
            </div>
        </div>

    </div>
    <script type="text/javascript" src="{{ url_for('static',filename='js/jquery.js') }}"></script>
    <script type="text/javascript" src="{{ url_for('static',filename='js/main.js') }}"></script>
</body>

</html>

```

## Stylesheets

### `static/css/style.css`

```css
/* File: style.css */
/** @import url("https://fonts.googleapis.com/css?family=Roboto"); **/
button {
  cursor: pointer;
}
button:hover {
  background: #0c4ddb;
}
button:focus {
  outline: none;
}

::-webkit-scrollbar {
  width: 4px;
  height: 4px;
}

::-webkit-scrollbar-track {
background: #BDBDBD;
border-radius: 6px;
}

::-webkit-scrollbar-thumb {background-color: #3e96fa;border-radius: 3px;outline: 1px solid lime;}

@media only screen and (min-width: 40em) {
  .modal-overlay {
    display: flex;
    align-items: center;
    justify-content: center;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 9999;
    background-color: rgba(0, 0, 0, 0.6);
    opacity: 0;
    visibility: hidden;
    -webkit-backface-visibility: hidden;
            backface-visibility: hidden;
    transition: opacity 0.6s cubic-bezier(0.55, 0, 0.1, 1), visibility 0.6s cubic-bezier(0.55, 0, 0.1, 1);
  }
  .modal-overlay.active {
    opacity: 1;
    visibility: visible;
  }
}
/**
 * Modal
 */
.modal {
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  margin: 0 auto;
  background-color: #fff;
  width: 600px;
  max-width: 75rem;
  min-height: 20rem;
  padding: 1rem;
  border-radius: 3px;
  opacity: 0;
  overflow-y: auto;
  visibility: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  -webkit-backface-visibility: hidden;
          backface-visibility: hidden;
  -webkit-transform: scale(1.2);
          transform: scale(1.2);
  transition: all 0.6s cubic-bezier(0.55, 0, 0.1, 1);
}
.modal .close-modal {
  position: absolute;
  cursor: pointer;
  top: 5px;
  right: 15px;
  opacity: 0;
  -webkit-backface-visibility: hidden;
          backface-visibility: hidden;
  transition: opacity 0.6s cubic-bezier(0.55, 0, 0.1, 1), -webkit-transform 0.6s cubic-bezier(0.55, 0, 0.1, 1);
  transition: opacity 0.6s cubic-bezier(0.55, 0, 0.1, 1), transform 0.6s cubic-bezier(0.55, 0, 0.1, 1);
  transition: opacity 0.6s cubic-bezier(0.55, 0, 0.1, 1), transform 0.6s cubic-bezier(0.55, 0, 0.1, 1), -webkit-transform 0.6s cubic-bezier(0.55, 0, 0.1, 1);
  transition-delay: 0.3s;
}
.modal .close-modal svg {
  width: 1.75em;
  height: 1.75em;
}
.modal .modal-content {
  opacity: 0;
  -webkit-backface-visibility: hidden;
          backface-visibility: hidden;
  transition: opacity 0.6s cubic-bezier(0.55, 0, 0.1, 1);
  transition-delay: 0.3s;
}
.modal-content{
  width: 100%;
}
.modal.active {
  visibility: visible;
  opacity: 1;
  -webkit-transform: scale(1);
          transform: scale(1);
}
.modal.active .modal-content {
  opacity: 1;
}
.modal.active .close-modal {
  -webkit-transform: translateY(10px);
          transform: translateY(10px);
  opacity: 1;
}

/**
 * Mobile styling
 */
@media only screen and (max-width: 39.9375em) {
  h1 {
    font-size: 1.5rem;
  }

  .modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    -webkit-overflow-scrolling: touch;
    border-radius: 0;
    -webkit-transform: scale(1.1);
            transform: scale(1.1);
    padding: 0 !important;
  }

  .close-modal {
    right: 20px !important;
  }
}
body {
  font-family: "Roboto", sans-serif;
  min-height: 100%;
  position: relative;
  padding-bottom: 3rem;
  margin: 0;
}

h2 {
  margin: 0px;
}

h6 {
  margin: 0px;
  color: #777;
}
.result-dirs::-webkit-scrollbar {
    width: 1em;
}

.result-dirs::-webkit-scrollbar-track {
  background: #eee;
  border-radius: 6px;
}

.result-dirs::-webkit-scrollbar-thumb {
  background-color: #324a5ebd;
  border-radius: 3px;
  outline: 1px solid #eeeeee;
}
.wrapper {
  text-align: center;
  margin: 50px auto;
}

.tabs {
  margin-top: 50px;
  font-size: 15px;
  padding: 0px;
  list-style: none;
  background: #fff;
  box-shadow: 0px 5px 20px rgba(0, 0, 0, 0.1);
  display: inline-block;
  border-radius: 50px;
  position: relative;
}

.tabs a {
  text-decoration: none;
  color: #777;
  text-transform: uppercase;
  padding: 10px 20px;
  display: inline-block;
  position: relative;
  z-index: 1;
  transition-duration: 0.6s;
}

.tabs a.active {
  color: #fff;
}

.tabs a i {
  margin-right: 5px;
}

.tabs .selector {
  height: 100%;
  display: inline-block;
  position: absolute;
  left: 0px;
  top: 0px;
  z-index: 1;
  border-radius: 50px;
  transition-duration: 0.6s;
  transition-timing-function: cubic-bezier(0.68, -0.55, 0.265, 1.55);
  background: #05abe0;
  background: -moz-linear-gradient(45deg, #05abe0 0%, #8200f4 100%);
  background: -webkit-linear-gradient(45deg, #3e96fa 0%, #05c2ff 100%);
  background: linear-gradient(45deg, #3e96fa 0%, #05c2ff 100%);
  filter: progid:DXImageTransform.Microsoft.gradient(
      startColorstr="#05abe0",
      endColorstr="#8200f4",
      GradientType=1
    );
}
.container{
  width: 900px;
  margin: 0 auto;
  border-radius: 6px;
  box-shadow: 0px 5px 20px rgba(0, 0, 0, 0.18);
  padding: 24px;
  margin-top: 21px;
  border: solid 1px #eee;
  /** overflow: auto; **/
  position: relative;
}
.target_box{
  border: solid 1px #e0e0e0;
  border-radius: 18px;
  background: #ffffff;
  margin: 6px;
  padding: 8px 19px;
  cursor: text;
  outline: none;
  width: 94%;
  color: #6f6f6f;
  text-align: center;
  transition: all 0.2s cubic-bezier(0.55, 0, 0.1, 1);
  }

  .target_box:hover {
    border: solid 1px #3e96faf5;
    box-shadow: 0px 0px 10px 1px #2196f361;
  }

.start_scan{
  background: transparent;
  margin: 0px;
  margin-top: 20px;
  border: solid 1px #3e96fa;
  text-decoration: none;
  padding: 5px 30px;
  letter-spacing: 1px;
  cursor: pointer;
  text-transform: uppercase;
  font-size: 12px;
  color: #3e96fa;
  border-radius: 18px;
}
.start_scan:hover{
  background: #3e96fa;
  color: #fff;
  box-shadow: 0px 2px 6px #3e96fa85;
}
.avatar{
  width: 82px;
  border-radius: 100px;
  display: table-cell;
}
.avatar-placeholder{
  width: 30%;
  display: inline-block;
  float: left;
}
.bio-placeholder{
  width: 100%;
  line-height: 25px;
  text-align: center;
  overflow: hidden;
  font-size: 15px;
  letter-spacing: 1px;
}
.result-dirs{
  padding: 7px;
    text-align: left;
    max-height: 800px;
    margin: 14px;
    overflow: auto;
}
.result-single {
      border: solid 1px #324a5e;
      background-image: url(/static/result.svg);
      padding: 6px 44px;
      font-size: 15px;
      margin-bottom: 10px;
      border-radius: 24px;
      background-size: 28px;
      cursor: pointer;
      background-repeat: no-repeat;
      background-position: left;
      background-position-x: 2px;
  }

.result-single:hover{
  background-color: #324a5e;
  color: white;
  transition-timing-function: ease;
  transition: all 0.2s ease-in;
  border: solid 1px #fff;
}

.upload-container{
  background: #eee;
    padding: 4px;
    border-radius: 4px;
    font-size: 15px;
    width: 97%;
    font-weight: bold;
    color: #6b6b6b;
}

.log-holder{
  width: 800px;
  margin: 0 auto;
  margin-top: 34px;
  background: black;
  font-size: 13px;
  font-family: ocraextended;
  color: lime;
  padding: 24px;
  border-top-right-radius: 5px;
  border-top-left-radius: 5px;
  max-height: 230px;
  overflow: auto;
  text-align: left;
}

.mainbut {
  width: 47%;
  display: inline-block;
  font-size: 24px;
  padding: 5px;
  border: solid 1px;
  box-shadow: 0px 2px 8px 1px #86878859;
  cursor: pointer;
  border-radius: 4px;
  margin: 4px;
}

.mainbut img{
  width: 50px;
}

.butlocal{
  background: #ffd15c17;
  border: solid 2px #f3705a;
  color: black;
}

.butremote{
  background: #324a5e17;
  border: solid 2px #324a5e;
  color: #12414c;
}

.butremote:hover{
  background: #324a5e;
  color: white;
  box-shadow: 0px 2px 8px 1px #324a5e6b;
  transition: all 0.1s cubic-bezier(0.55, 0, 0.1, 1);
}

.butlocal:hover{
  background: #f3705a;
  box-shadow: 0px 2px 8px 1px #f3705a6b;
  color: white;
  transition: all 0.1s cubic-bezier(0.55, 0, 0.1, 1);
}

.butdesc{
  font-size: 13px;
  padding: 0 !important;
  margin: inherit;
  text-transform: uppercase;
}

#lightSwitchOff{ display:inline; }
#lightSwitchOn{ display:none; }

.log-holder::-webkit-scrollbar {
  width: 7px;
}

.log-holder::-webkit-scrollbar-track {
background: #000;
border-radius: 6px;
}

.log-holder::-webkit-scrollbar-thumb {
background-color: #89ff00;
border-radius: 3px;
outline: 1px solid lime;
}

.dmode{
  position: fixed;
  bottom: 20px;
  right: 20px;
  border-radius: 100%;
  height: 27px;
  width: 27px;
  padding: 10px;
  z-index: 10;
  -webkit-transition: -webkit-transform .8s ease-in-out;
  transition:         transform .8s ease-in-out;
}

.dmode:hover{
  -webkit-transform: rotate(360deg);
  transform: rotate(360deg);
}
.day{
  background: #fff;
  box-shadow: 0px 0px 20px 1px #ffffff73;
}

.night{
  background: #000;
  box-shadow: 0px 0px 20px 1px #000000;
}

a.paginate_button.current {
  background: #3e96fa;
  color: white;
  cursor: not-allowed;
}

table.result-table{
	width: 100%;
	/* padding: 6px; */
  border-collapse: collapse;
  text-align: left;
}

table.result-table th{
  text-align: left;
  background: #e0e0e0;
  padding: 5px;
  color: #000000;
}

table.result-table tr{
  background: transparent;
  border: solid 1px #e0e0e0;
  color: #6b6b6b;
}

table.result-table tr:hover{
  box-shadow: 1px 1px 6px 0px #9898988f;
  color: #000000;
  background: #ffffff;
  border: solid 1px #ffffff;
  transition: all ease 0.2s;
}

table.result-table td{
  padding: 8px 5px !important;
  max-width: 500px;
  font-size: 14px;
  word-break: break-all;
}

div#result-table_wrapper {
}

.dataTables_length{
    width: 50%;
    float: left;
    padding: 10px;
    padding-left: 0px;
    font-weight: bold;
    text-align: left;
    color: gray;
}
.dataTables_length select{
  border: solid 1px #3e96fa;
  padding: 2px;
  background: #3e96fa;
  color: #ffffff;
}
.dataTables_length select:hover{
    border: solid 1px #676767;
    transition: all ease 0.2s;
}
.dataTables_filter{
    width: 44%;
    float: right;
    padding: 10px;
    /* font-weight: bold; */
    padding-right: 0px;
    text-align: right;
    color: black;
}

.dataTables_filter input{
  background: #ffffff;
  padding: 4px;
  border-radius: 21px;
  border: solid 1px #bdbdbd;
  color: #3e96fa;
  outline: none;
  margin-left: 5px;
}
.dataTables_filter input:hover{
  border: solid 1px #3e96fa96;
  transition: all ease 0.2s;
}
.dataTables_info{
    padding: 7px;
    font-weight: 500;
    margin-top: 15px;
    color: #3c3c3c;
    text-align: left;
    width: 40%;
    display: inline-block;
    float: left;
}
.paginate_button{
  background: transparent;
  color: #3e96fa;
  border: solid 1px #3e96fa;
  padding: 3px 7px;
  border-radius: 2px;
  width: 100%;
  margin: 2px;
  cursor: pointer;
  font-weight: bold;
  text-transform: uppercase;
}
.paginate_button:hover{
  background: #3e96fa;
  color: white;
  transition: all ease 0.2s;
}
.dataTables_paginate{
	margin-top: 20px;
	text-align: right;
	display: inline-block;
	width: 50%;
}
.paginate_button .current, .disabled{
  background: #757575;
  color: #ffffff;
  border: solid 2px #757575;
  cursor: not-allowed;
}
.paginate_button .current, .disabled:hover{
	background: black;
	color: gray;
	cursor: not-allowed;
}
.querybox{
    background: #272727;
    padding: 5px 15px;
    color: #109be1;
    width: fit-content;
    border-radius: 5px;
}
th.sorting_asc {
  border-bottom: solid 1px #109be1;
  color: #109be1 !important;
}
th.sorting_desc {
    border-top: solid 1px #109be1;
    color: #109be1 !important;
}
.logo-placeholder{
  text-align: center;
}
.inline-note{
  padding: 13px 8px;
  font-size: 14px;
  background: #ffffff;
  margin-top: 19px;
  color: #3e96fa;
  border-radius: 5px;
  border: solid 1px #3e96fa;
  border-left: solid 5px #3e96fa;
  border-bottom-left-radius: 0px;
  border-top-left-radius: 0px;
}

.result-header{
  color: #28b78d;
  margin-bottom: 16px;
  text-transform: uppercase;
  letter-spacing: 1ch;
}

.permission{
  display: inline-block;
  padding: 5px 12px;
  margin: 3px;
  border-radius: 3px;
  color: #fff;
  cursor: pointer;
  background: #3e96fa;
  box-shadow: 0px 0px 4px 2px #13131330;
}

.permission:hover {
  box-shadow: 0px 0px 9px 2px #3e96fa7a;
  background: #fff;
  color: #3e96fa;
}

.fstats {
  display: inline-block;
  width: 15%;
  background: #00ff48;
  padding: 8px 4px;
  border-radius: 4px;
  box-shadow: 0px 0px 1px 0px #0006;
}

ul.result-tabs{
  margin: 0px;
  width: 100%;
  /* border-spacing: 7px; */
  border-collapse: separate;
  display: table;
  padding: 0;
  padding-bottom: 0px;
  list-style: none;
}
ul.result-tabs li{
  /* background: #e6e6e6; */
  color: #000000;
  display: table-cell;
  padding: 10px 6px;
  cursor: pointer;
  margin-bottom: -17px;
  border-bottom: solid 2px #c8c8c8;
  text-transform: uppercase;
  letter-spacing: 2px;
  font-size: 12px;
}

ul.result-tabs li.current{
  border-bottom: solid 2px #3e96fa;
  color: #3e96fa;
}

ul.result-tabs li:hover {
  border-bottom: solid 2px #000000;
}

.tab-content{
  display: none;
  border-radius: 7px;
  margin: 13px 0px;
  box-shadow: 0px 3px 6px 0px #dedede;
  background: #fafafa;
  padding: 15px;
}

.tab-content.current{
  display: inherit;
}

html {
  height: 100%;
  box-sizing: border-box;
}

.footer {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  width: 100%;
  text-transform: uppercase;
  font-size: 12px;
  background-color: #ffffff;
  letter-spacing: 3px;
  color: #000000;
  box-shadow: 0px -2px 9px 0px #0c0c0c26;
  text-align: center;
}

img.cat-image {
  width: 100px;
  margin-bottom: 10px;
}

.pill {
  display: table-cell;
  text-align: center;
  border: solid 1px;
  padding: 7px;
  cursor: pointer;
  border-radius: 5px;
}

.gchrome {
  border: solid 2px #FF9800;
  color: #FF9800;
}

.mfirefox {
  border: solid 2px #FF5722;
  color: #FF5722;
}

.mfirefox:hover {
  background: #FF5722;
  color: white;
  transition: all 0.2s;
  box-shadow: 0px 0px 6px 1px #ff00005e;
}

.gchrome:hover {
  background: #FF9800;
  color: white;
  transition: all 0.2s;
  box-shadow: 0px 0px 6px 1px #ff00005e;
}

.pill-container {
  display: table;
  width: 100%;
  border-collapse: separate;
  border-spacing: 5px;
}

.opera {
  border: solid 2px red;
  color: red;
}

.opera:hover {
  background: red;
  color: white;
  transition: all 0.2s;
  box-shadow: 0px 0px 6px 1px #ff00005e;
}

::-moz-selection { 
  color: #fff;
  background: #3e96fa;
}

::selection {
  color: #fff;
  background: #000000;
}

div#loading {
  width: 100%;
  height: 100%;
  left: 0;
  padding-top: 10%;
  letter-spacing: 5px;
  top: 0;
  font-family: ocraextended;
  z-index: 99999;
  position: fixed;
  background: #000000eb;
  color: #fff;
}

.ext-info-body {
  width: 100%;
  display: inline-block;
  padding: 9px;
  vertical-align: middle;
  z-index: 1;
  position: relative;
  border-radius: 6px;
  box-shadow: 0px 0px 15px 0px #797979;
  background: #177cef;
  color: #fff;
}

.ext-info-img {
  display: inline-block;
  width: 50px;
  height: 50px;
  text-align: center;
  background: #fff;
  padding: 19px;
  vertical-align: middle;
  border: solid 7px #F44336;
  border-radius: 50%;
  font-size: 28px;
  color: red;
  font-weight: bold;
  box-shadow: inset 0px 0px 3px 2px #00000047;
  letter-spacing: 4px;
  line-height: 50px;
  position: relative;
  z-index: 55;
}

.ext-info-col1 {
  width: 65%;
  display: inline-block;
  text-align: left;
  vertical-align: middle;
}

.ext-info-col2 {
  display: inline-block;
  width: 10%;
  border-left: solid 2px #464545;
  font-size: 13px;
  vertical-align: middle;
  padding: 7px;
}

.ext-info-col3 {
  display: inline-block;
  width: 17%;
  border-left: solid 2px #464545;
  font-size: 13px;
  vertical-align: middle;
  padding-left: 8px;
}

.ext-info-name {
  width: 100%;
  display: inline-block;
  font-size: 22px;
}

.ext-info-version {
  display: inline-block;
  margin: 5px;
  margin-left: 0px;
  padding: 3px 10px;
  background: #ffffff;
  color: #177cef;
  border-radius: 3px;
  font-size: 13px;
}

.ext-info-author {
  display: inline-block;
  margin: 5px;
  padding: 3px 10px;
  background: #FFEB3B;
  color: #000;
  font-size: 13px;
  border-radius: 3px;
}

.ext-info-main {
/**  background: #e6e6e6; **/
}

.ext-info-description {
  font-size: 13px;
  margin-top: 5px;
}

.ext-info-last-scanned{
  display: inline-block;
  margin: 5px;
  padding: 3px 10px;
  background: #000000;
  color: #fff;
  font-size: 13px;
  border-radius: 3px;
}

.ext-info-img img {
  width: 50%;
}

.log-actions {
  width: 800px;
  background: black;
  margin: 0 auto;
  padding: 15px 24px;
  border-bottom-left-radius: 5px;
  border-bottom-right-radius: 5px;
  padding-bottom: 20px;
}

.clear-logs-button {
  border: solid 1px red;
  background: transparent;
  color: red;
  font-weight: bold;
  font-size: 15px;
  font-family: ocraextended;
  border-radius: 3px;
  padding: 6px 23px;
  display: inline-block;
  width: 40%;
}

.logs-explorer-button {
  border: solid 1px #03A9F4;
  background: transparent;
  font-family: ocraextended;
  color: #03A9F4;
  border-radius: 3px;
  padding: 6px 23px;
  display: inline-block;
  width: 40%;
  font-weight: bold;
  font-size: 15px;
}

.clear-logs-button:hover {
  background: red;
  color: black;
}

.logs-explorer-button:hover {
  color: black;
  background: #03A9F4;
}

.perm {
  background: #ffffff;
  margin-bottom: 9px;
  color: #3e96fa;
  box-shadow: 0px 0px 4px 0px #afafaf;
  border-radius: 4px;
  text-align: left;
  display: table-cell;
  border-spacing: 5px;
}

.perm-desc {
  padding: 10px;
  color: #000000;
  border-radius: 4px;
  margin: 5px 0px;
}

.perm-warn {
  padding: 10px;
  background: transparent;
  color: #f70a2a;
  border-radius: 4px;
  margin: 5px 0px;
  font-weight: bold;
}

.perm-name {
  text-align: center;
  font-size: 20px;
  color: white;
  background: #3e96fa;
  /* font-weight: bold; */
  border-top-left-radius: 4px;
  border-top-right-radius: 4px;
}
.permissions-holder {
  display: table;
  border-spacing: 5px;
}

.file_name {
  width: 100%;
  text-align: left;
  font-size: 21px;
  margin-bottom: 5px;
}

.file_location {
  display: inline-block;
  font-size: 12px;
  background: #ccc;
  padding: 3px 9px;
  border-radius: 2px;
}

.file_attrs {
  text-align: left;
  font-size: 12px;
}

.file_type {
  display: inline-block;
  background: #05abe0;
  font-weight: bold;
  border-radius: 2px;
  color: white;
  padding: 3px 6px;
}

.file_size {
  display: inline-block;
  background: #28b78d;
  font-weight: bold;
  border-radius: 2px;
  color: white;
  padding: 3px 6px;
}

.file_info {
  border: solid 1px #eee;
  padding: 7px;
  background: #eee;
  border-radius: 3px;
}

.file_icon {
  display: inline-block;
  padding-right: 12px;
  text-align: left;
  float: left;
}

.source_code {
  height: 430px;
  overflow-y: scroll;
  text-align: left;
  width: 95%;
  border: solid 1px #3e96fa;
  padding: 8px;
  background: #ffffff;
  color: #3e96fa;
  margin-top: 20px;
}

.CodeMirror {
  margin-top: 24px;
  text-align: left;
  height: 450px !important;
}

.editor_buttons {
  margin-top: 10px;
}

.format_button {
  border: solid 1px #1d89ff;
  background: transparent;
  color: #1d89ff;
  font-size: 15px;
  padding: 7px 23px;
  letter-spacing: 2px;
  border-radius: 3px;
  box-shadow: 0px 0px 9px 1px #1d89ff54;
}

.format_button:hover{
  background: #1d89ff;
  color: #fff;
}

.file_image {
  float: left;
  margin-right: 22px;
  display: inline-block;
}

.file_body {
  width: 90%;
  display: inline-block;
}

.file_image img {
  width: 44px;
}

.header_for_main{
  color: #ffffff;
  background: #3e96fa;
  border-bottom: solid 1px #3e96fa;
  margin: -25px;
  margin-bottom: 28px;
  padding: 6px;
  font-weight: normal;
  font-size: 16px;
  letter-spacing: 5px;
  text-transform: uppercase;
}

.header_for_sub{
  color: #ffffff;
  background: #3e96fa;
  border-bottom: solid 1px #3e96fa;
  margin: -15px;
  margin-bottom: 28px;
  padding: 6px;
  font-size: 14px;
  letter-spacing: 3px;
  text-transform: uppercase;
  font-weight: normal;
  border-top-left-radius: 5px;
  border-top-right-radius: 5px;
}

.option_body {
  padding: 8px;
  text-align: left;
  padding-left: 13px;
  /* border: solid 1px #d6d6d6; */
  margin-bottom: 17px;
}

.option_name {
  text-align: left;
  font-size: 16px;
  text-transform: uppercase;
  letter-spacing: 3px;
  margin: 0px;
  margin-bottom: 7px;
  color: #ff3d00;
  padding-bottom: 6px;
  border-bottom: solid 1px #d6d6d6;
}

.option_description {
  text-align: left;
  color: #616060;
  font-size: 13px;
  letter-spacing: 0.5px;
}

.delete_button {
  border: solid 1px #ff5964;
  background: transparent;
  color: #ff5964;
  box-shadow: 0px 0px 7px 0px #ff596459;
  border-radius: 18px;
  text-transform: uppercase;
  min-width: 225px;
  margin-top: 6px;
  padding: 5px 30px;
  font-size: 12px;
  letter-spacing: 1px;
}

.delete_button:hover {
  background: red;
  color: white;
  border: solid 1px red;
  box-shadow: 0px 2px 6px #ff5964c2;
}

#musicButton {
  position: fixed;
  bottom: 83px;
  right: 20px;
  color: white;
  background: #E91E63;
  border-radius: 100%;
  height: 27px;
  width: 27px;
  padding: 10px;
  z-index: 10;
  -webkit-transition: -webkit-transform .8s ease-in-out;
  transition:         transform .8s ease-in-out;
  box-shadow: 0px 0px 10px 0px #E91E63;
}

#musicButton:hover, .change_music:hover, .play_pause:hover {
  -webkit-transform: rotate(360deg);
  transform: rotate(360deg);
}
.accordion__item {
  width: 100%;
}
.accordion__question:after {
  content: "   ▼";
  text-align: right;
  float: right;
}
.accordion__answer {
  display: none;
  font-size: 14px;
  line-height: 19px;
  margin-top: 6px;
  border-top: solid 1px #3e96fa;
  padding-top: 10px;
}

.accordion {
  width: 98%;
  text-align: left;
  background: #ffffff;
  border: solid 1px #dedede;
  border-radius: 3px;
  color: #000;
  padding: 11px;
  margin-bottom: 7px;
  cursor: pointer;
}

.accordion__question {
  color: #656565;
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 4px;
  width: 100%;
}

.accordion__question:hover {
  color: #3e96fa;
}

.accordion:hover {
  box-shadow: 0px 0px 7px 0px #c8c8c896;
}

.accordion:active {
  box-shadow: 0px 0px 7px 0px #c8c8c896;
}

.accordion__question:active {
  color: #3e96fa;
}
.stats {
  display: inline-block;
  height: 381px;
  padding: 11px;
  vertical-align: top;
  width: 43%;
  text-align: left;
  background: white;
  box-shadow: 0px 0px 8px 0px #ccc;
  border-radius: 6px;
  margin: 0px 10px;
}
.stats_head {
  margin: -11px;
  margin-bottom: 12px;
  border-top: solid 3px #000;
  color: #000;
  font-size: 15px;
  text-transform: uppercase;
  text-align: center;
  letter-spacing: 2px;
  border-top-left-radius: 5px;
  border-top-right-radius: 5px;
  padding: 6px;
}

.stats_body {
  line-height: 30px;
  text-align: center;
}

.stats_pill {
  display: inline-block;
  margin: 15px;
  width: 23%;
  padding: 6px 1px;
  align-self: center;
  background: #ccc;
  border-radius: 5px;
  text-align: center;
}

.stats_pill img {
  width: 52px;
}

.stats_data {
  background: #000;
  color: white;
  letter-spacing: 1px;
  font-size: 12px;
  margin: -6px -1px;
  border-bottom-left-radius: 5px;
  border-bottom-right-radius: 5px;
}

.stats_pill:hover {
  box-shadow: 0px 0px 12px 0px #00000063;
}

.mid-head {
  background: #fff !important;
  color: #000 !important;
}

.sub_body {
  box-shadow: 0px 7px 8px 0px #ccccccd4 !important;
}


.graph-container {
  width: 90%;
  background: #ffffff;
  padding: 20px;
  box-shadow: 0px 0px 14px 0px #00000045;
  margin: 0 auto;
  border-radius: 5px;
  text-align: left;
  margin-top: 20px;
}

div#large-graph {
  height: 700px;
  background: #000;
  width: 87%;
  padding-right: 5px;
  border-radius: 5px;
  display: inline-block;
  border-top-right-radius: 0px;
  border-top: solid 3px #4eeeb2;
  border-bottom-right-radius: 0px;
}

.graph-control {
  display: inline-block;
  width: 11%;
  background: #171717;
  border-left: dotted 1px #4eeeb2;
  float: right;
  height: 700px;
  border-top: solid 3px #4eeeb2;
  padding: 0px 7px;
  border-top-right-radius: 5px;
  overflow: hidden;
  margin-left: -5px;
  border-bottom-right-radius: 5px;
}

.control-title {
  font-size: 15px;
  text-transform: uppercase;
  letter-spacing: 2px;
  color: #4eeeb2;
  padding-top: 3px;
  text-align: center;
  margin-bottom: 8px;
}

.control-body {
  font-size: 15px;
}


.jsontree_bg {
  background: #FFF;
}

/* Styles for the container of the tree (e.g. fonts, margins etc.) */
.jsontree_tree {
  padding: 15px;
  border-radius: 5px;
  list-style-type: none;
  font-size: 14px;
  color: #000;
  background: #ffffff;
}

/* Styles for a list of child nodes */
.jsontree_child-nodes {
  display: none;
  /* margin-left: 35px; */
  border-left: dotted 1px #6d6d6d;
  margin-top: 5px;
  line-height: 21px;
}
.jsontree_node_expanded > .jsontree_value-wrapper > .jsontree_value > .jsontree_child-nodes {
  display: block;
  list-style-type: none;
}

/* Styles for labels */
.jsontree_label-wrapper {
  float: left;
  font-weight: bold;
  margin-right: 8px;
}
.jsontree_label {
  font-weight: normal;
  vertical-align: top;
  margin-left: 1px;
  position: relative;
  border-bottom: solid 2px transparent;
  padding: 1px 5px;
  letter-spacing: 3px;
  text-transform: uppercase;
  color: #009688;
  cursor: default;
  transition: all 0.2s ease-in;
}
.jsontree_node_marked > .jsontree_label-wrapper > .jsontree_label {
  background: #fff2aa;
}

/* Styles for values */
.jsontree_value-wrapper {
  display: block;
  overflow: hidden;
}
.jsontree_node_complex > .jsontree_value-wrapper {
  overflow: inherit;
}
.jsontree_value {
  vertical-align: top;
  display: inline;
}
.jsontree_value_null {
  color: #c8c8c8;
  font-weight: bold;
}
.jsontree_value_string {
  color: #424242;
  padding: 1px 5px;
  transition: all 0.2s ease-in;
  border-radius: 2px;
  letter-spacing: 1px;
}
.jsontree_value_number {
  color: #FF9800;
  font-weight: bold;
}
.jsontree_value_boolean {
  color: #ff0300;
  font-weight: bold;
}

/* Styles for active elements */
.jsontree_expand-button {
  position: absolute;
  top: 3px;
  left: -15px;
  display: block;
  width: 11px;
  height: 11px;
  background-image: url('../images/vectorpaint.svg');
}
.jsontree_node_expanded > .jsontree_label-wrapper > .jsontree_label > .jsontree_expand-button {
  background-position: 0 -11px;
}
.jsontree_show-more {
  cursor: pointer;
}
.jsontree_node_expanded > .jsontree_value-wrapper > .jsontree_value > .jsontree_show-more {
  display: none;
}
.jsontree_node_empty > .jsontree_label-wrapper > .jsontree_label > .jsontree_expand-button,
.jsontree_node_empty > .jsontree_value-wrapper > .jsontree_value > .jsontree_show-more {
  display: none !important;
}
.jsontree_node_complex > .jsontree_label-wrapper > .jsontree_label {
  cursor: pointer;
}
.jsontree_node_empty > .jsontree_label-wrapper > .jsontree_label {
  cursor: default !important;
}

div#manifest-content {
  text-align: left;
  box-shadow: 0px 0px 5px 3px #eee;
  font-size: 12px !important;
}

li.jsontree_node {
  margin-bottom: 5px;
}

.jsontree_label:hover {
  text-shadow: 0px 0px 1px #009688;
  border-bottom: solid 1px #009688;
}

.jsontree_value_string:hover {
  color: #000;
  background: #fff;
  text-shadow: 0px 0px 1px #777;
}

.jsontree_child-nodes:hover {
  border-left: dotted 1px #03A9F4;
}

.stats-q {
  color: #000000;
  font-size: 14px;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 2px;
}

.stats-a {
  font-size: 14px;
  color: #4a4949;
}

.nothing{
  background: #cacaca;
  padding: 12px;
  border-radius: 7px;
  color: #404040;
  text-transform: uppercase;
  letter-spacing: 2px;
  font-size: 15px;
  font-weight: 100;
}

.sub-head-settings {
  text-align: left;
  color: #000;
  font-weight: bold;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 1px;
  display: inline-block;
  padding-bottom: 5px;
}

.settings_textbox {
  background: #ffffff;
  border: solid 1px #bdbdbd;
  padding: 5px 11px;
  letter-spacing: 1px;
  font-size: 13px;
  color: #000000;
  outline: none;
  width: 400px;
  border-radius: 16px;
}

.settings_textbox:focus, .dataTables_filter input:focus {
  color: #3e96fa;
  border: solid 1px #3e96fa;
  box-shadow: 0px 0px 8px 0px #2196f361;
}

.target_box:focus {
    color: #3e96fa;
    border: solid 1px #fffffff5;
    box-shadow: 0px 0px 10px 1px #2196f361;
}

.change_music {
  position: fixed;
  bottom: 83px;
  right: 130px;
  color: white;
  background: #03A9F4;
  border-radius: 100%;
  height: 27px;
  width: 27px;
  padding: 10px;
  z-index: 10;
  box-shadow: 0px 0px 10px 0px #03a9f4;
}

.play_pause {
  position: fixed;
  bottom: 83px;
  right: 75px;
  color: white;
  background: #9C27B0;
  border-radius: 100%;
  height: 27px;
  width: 27px;
  padding: 10px;
  z-index: 10;
  box-shadow: 0px 0px 10px 0px #9C27B0;
}

div#music_buttons {
  position: fixed;
  bottom: 77px;
  right: 35px;
  color: white;
  background: #ffffff;
  width: 130px;
  height: 37px;
  border-radius: 73px;
  padding: 10px;
  border-top-right-radius: 76px;
  border-bottom-right-radius: 76px;
  z-index: 9;
  box-shadow: 0px 0px 13px 0px #0000001f;
}

.settings_textbox:hover {
    border: solid 1px #3e96faa1;
}

.ext_url {
  text-decoration: none;
  color: inherit;
  font-weight: normal;
  font-size: inherit;
}

.ext_url:hover {
  border-bottom: dotted 1px #3e96fa;
  padding-bottom: 4px;
}

.mid_header{
  background: #27272f;
  color: #ffffff;
  text-transform: uppercase;
  font-size: 13px;
  padding: 2px;
  letter-spacing: 2px;
  font-weight: normal;
  border-radius: 18px;
  margin-top: 15px;
}

.license {
  width: 100%;
  height: 300px;
  background: #cccccc;
  border: none;
  border-radius: 4px;
  color: #000;
  text-align: center;
}

.author_info {
  display: table-cell;
  float: right;
  width: 80%;
  text-align: left;
}

a#change_music:hover {
  background: #00BCD4;
}

a#play_pause:hover {
  background: #cf07f1;
}

a.hreflink {
  text-decoration: none;
  color: #03A9F4;
  border-bottom: dotted 1px #03a9f4;
}

.noscript {
  display: flex;
  align-items: center;
  justify-content: center;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 9999;
  background-color: rgb(255, 90, 90);
  color: #ffffff;
  letter-spacing: 2px;
}

.sub-head-settingss {
  display: inline-block;
  color: #d0d0d0;
  letter-spacing: 1px;
  text-transform: capitalize;
}

.switch {
  position: relative;
  margin-left: 5px;
  display: inline-block;
}

.switch-input {
  display: none;
}

.switch-label {
  display: block;
  width: 44px;
  height: 14px;
  cursor: pointer;
  padding-top: 2px;
  text-indent: -150%;
  clip: rect(0 0 0 0);
  color: transparent;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
}
.switch-label:before,
.switch-label:after {
  content: "";
  display: block;
  position: absolute;
  cursor: pointer;
}
.switch-label:before {
  width: 100%;
  height: 100%;
  background-color: #b5b5b5;
  border-radius: 9999em;
  transition: background-color 0.25s ease;
}
.switch-label:after {
  top: 0;
  left: 0;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background-color: #fff;
  box-shadow: 0 0 2px rgba(0, 0, 0, 0.45);
  transition: left 0.25s ease;
}

.switch-input:checked + .switch-label:before {
  background-color: #39bb00;
}
.switch-input:checked + .switch-label:after {
  left: 24px;
}
```

### `static/css/result.css`

```css
/* File: result.css */

#resultnetwork{
    width: 100%;
    height: 342px;
    background: #1f1f27;
    border-radius: 5px;
    display: inline-block;
    border: 1px solid #000000;
}

.result-info{
    width: 100%;
    margin-bottom: 21px;
}

.result-wrapper{
    width: 80%;
    text-align: center;
    align-items: center;
    margin-left: 10%;
}

.fs-head img{
    width: 63px;
}

.risk-pill {
    display: inline-block;
    margin-left: 12px;
    background: #000;
    color: #fff;
    padding: 3px;
    padding-left: 5px;
    font-size: 8px;
    border-radius: 2px;
  }
  
  .none {
    background: #28b78d;
  }
  
  .high {
    background: #FF5722;
  }
  
  .critical {
    background: #d61522;
  }
  
  .low {
    background: #7d9a0f;
  }
  
  .medium {
    background: #FF9800;
  }
  
  .warning {
    margin-top: 5px;
    color: #FF5722;
    border-left: solid 6px;
    padding-left: 8px;
  }

  .clear {
    clear: both;
}
.clearfix:after {
    content: ".";
    display: block;
    clear: both;
    visibility: hidden;
    line-height: 0;
    height: 0;
}
.jsontree_bg {
    background: #FFF;
}

/* Styles for the container of the tree (e.g. fonts, margins etc.) */
.jsontree_tree {
    padding: 15px;
    border-radius: 5px;
    list-style-type: none;
    font-size: 14px;
    color: #fff;
    background: #2c2c33;
}

/* Styles for a list of child nodes */
.jsontree_child-nodes {
    display: none;
    /* margin-left: 35px; */
    border-left: dotted 1px #6d6d6d;
    margin-top: 5px;
    line-height: 21px;
}
.jsontree_node_expanded > .jsontree_value-wrapper > .jsontree_value > .jsontree_child-nodes {
    display: block;
    list-style-type: none;
}

/* Styles for labels */
.jsontree_label-wrapper {
    float: left;
    font-weight: bold;
    margin-right: 8px;
}
.jsontree_label {
    font-weight: normal;
    vertical-align: top;
    margin-left: 1px;
    position: relative;
    border-bottom: solid 2px transparent;
    padding: 1px 5px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #4eeeb2;
    cursor: default;
    transition: all 0.2s ease-in;
}
.jsontree_node_marked > .jsontree_label-wrapper > .jsontree_label {
    background: #fff2aa;
}

/* Styles for values */
.jsontree_value-wrapper {
    display: block;
    overflow: hidden;
}
.jsontree_node_complex > .jsontree_value-wrapper {
    overflow: inherit;
}
.jsontree_value {
    vertical-align: top;
    display: inline;
}
.jsontree_value_null {
    color: #c8c8c8;
    font-weight: bold;
}
.jsontree_value_string {
    color: #ffffff;
    padding: 1px 5px;
    transition: all 0.2s ease-in;
    border-radius: 2px;
    letter-spacing: 1px;
}
.jsontree_value_number {
    color: #fff900;
    font-weight: bold;
}
.jsontree_value_boolean {
    color: #ff0300;
    font-weight: bold;
}

/* Styles for active elements */
.jsontree_expand-button {
    position: absolute;
    top: 3px;
    left: -15px;
    display: block;
    width: 11px;
    height: 11px;
    background-image: url('../images/vectorpaint.svg');
}
.jsontree_node_expanded > .jsontree_label-wrapper > .jsontree_label > .jsontree_expand-button {
    background-position: 0 -11px;
}
.jsontree_show-more {
    cursor: pointer;
}
.jsontree_node_expanded > .jsontree_value-wrapper > .jsontree_value > .jsontree_show-more {
    display: none;
}
.jsontree_node_empty > .jsontree_label-wrapper > .jsontree_label > .jsontree_expand-button,
.jsontree_node_empty > .jsontree_value-wrapper > .jsontree_value > .jsontree_show-more {
    display: none !important;
}
.jsontree_node_complex > .jsontree_label-wrapper > .jsontree_label {
    cursor: pointer;
}
.jsontree_node_empty > .jsontree_label-wrapper > .jsontree_label {
    cursor: default !important;
}

div#manifest-content {
    text-align: left;
    font-size: 12px !important;
}

li.jsontree_node {
    margin-bottom: 5px;
}

.jsontree_label:hover {
    text-shadow: 0px 0px 6px #398e6e;
    border-bottom: solid 1px #4eeeb2;
}

.jsontree_value_string:hover {
    background: #000000;
    color: #fff;
}

.mid-head {
    padding: 11px 25px;
    display: inline-block;
    box-shadow: 0px 0px 8px 0px #ccc;
    width: 88%;
    background: #33333d;
    color: #4eeeb2;
    border-top: solid 4px;
    font-size: 15px;
    text-transform: uppercase;
    letter-spacing: 3px;
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
    margin: 0px 10px;
}

.sub_section {
    margin-top: 20px;
    width: 100%;
    text-align: center;
    align-items: center;
    align-content: center;
}

.sub_body {
    width: 88%;
    display: inline-block;
    background: #fff;
    padding: 11px 25px;
    border-radius: 5px;
    border-top-left-radius: 0px;
    border-top-right-radius: 0px;
    box-shadow: 0px 3px 8px 0px #ccc;
    margin: 0px 10px;
}

div#selected-node {
    border-bottom: solid 1px #4eeeb2;
    color: #4eeeb2;
    font-size: 12px;
    padding: 6px 3px;
    line-height: 19px;
    letter-spacing: 0.5px;
}

.selected-title {
    width: 100%;
    display: inline-block;
    margin: 0px -3px;
    padding: 0px 3px;
    text-align: center;
    color: #000000;
    background: #4eeeb2;
    font-size: 12px;
    font-weight: bold;
    letter-spacing: 1px;
    margin-bottom: 4px;
}

#selected-node-label, #selected-node-id, #selected-node-parent {
    color: #fff;
}

#selected-node-group {
    color: #fff;
}

.control-button {
    width: 100%;
    margin: 2px 0px;
    background: #00ff9f24;
    font-size: 12px;
    text-transform: uppercase;
    color: #00ff9f;
    border: solid 1px #00ff9f;
    letter-spacing: 1px;
    border-radius: 2px;
}

.control-button:hover {
    color: #000000;
    background: #0cff9f;
}

.vis-button {
    background: #000;
}

.stats-qa {
    width: 100%;
    display: inline-block;
    text-align: left;
    margin-bottom: 10px;
}

.stats-q {
    color: #4eeeb2;
    font-size: 14px;
    text-transform: uppercase;
    letter-spacing: 2px;
}

.stats-a {
    font-size: 14px;
}

.jsontree_child-nodes:hover {
    border-left: dotted 1px white;
}

.country_flag {
    width: 15px;
    height: 15px;
    border-radius: 50%;
    vertical-align: middle;
}

.ft_icon {
    width: 16px;
    vertical-align: middle;
}
```

### `static/css/dark.css`

```css
/* File: dark.css */
/** @import url("https://fonts.googleapis.com/css?family=Roboto"); **/
button {
  cursor: pointer;
}
button:hover {
  background: #0c4ddb;
}
button:focus {
  outline: none;
}

/**
 * Overlay
 * -- only show for tablet and up
 */
@media only screen and (min-width: 40em) {
  .modal-overlay {
    display: flex;
    align-items: center;
    justify-content: center;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 9999;
    background-color: rgba(0, 0, 0, 0.6);
    opacity: 0;
    visibility: hidden;
    -webkit-backface-visibility: hidden;
            backface-visibility: hidden;
    transition: opacity 0.6s cubic-bezier(0.55, 0, 0.1, 1), visibility 0.6s cubic-bezier(0.55, 0, 0.1, 1);
  }
  .modal-overlay.active {
    opacity: 1;
    visibility: visible;
  }
}
/**
 * Modal
 */
.modal {
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  margin: 0 auto;
  background-color: #2b2b2b;
  width: 600px;
  max-width: 75rem;
  min-height: 20rem;
  padding: 1rem;
  border-radius: 3px;
  opacity: 0;
  overflow-y: auto;
  visibility: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  -webkit-backface-visibility: hidden;
          backface-visibility: hidden;
  -webkit-transform: scale(1.2);
          transform: scale(1.2);
  transition: all 0.6s cubic-bezier(0.55, 0, 0.1, 1);
}
.modal .close-modal {
  position: absolute;
  cursor: pointer;
  top: 5px;
  right: 15px;
  opacity: 0;
  -webkit-backface-visibility: hidden;
          backface-visibility: hidden;
  transition: opacity 0.6s cubic-bezier(0.55, 0, 0.1, 1), -webkit-transform 0.6s cubic-bezier(0.55, 0, 0.1, 1);
  transition: opacity 0.6s cubic-bezier(0.55, 0, 0.1, 1), transform 0.6s cubic-bezier(0.55, 0, 0.1, 1);
  transition: opacity 0.6s cubic-bezier(0.55, 0, 0.1, 1), transform 0.6s cubic-bezier(0.55, 0, 0.1, 1), -webkit-transform 0.6s cubic-bezier(0.55, 0, 0.1, 1);
  transition-delay: 0.3s;
}
.modal .close-modal svg {
  width: 1.75em;
  height: 1.75em;
}
.modal .modal-content {
  opacity: 0;
  -webkit-backface-visibility: hidden;
          backface-visibility: hidden;
  transition: opacity 0.6s cubic-bezier(0.55, 0, 0.1, 1);
  transition-delay: 0.3s;
}
.modal.active {
  visibility: visible;
  opacity: 1;
  -webkit-transform: scale(1);
          transform: scale(1);
}
.modal.active .modal-content {
  opacity: 1;
  text-align: left;
  width: 100%;
}
.modal.active .close-modal {
  -webkit-transform: translateY(10px);
          transform: translateY(10px);
  opacity: 1;
}

/**
 * Mobile styling
 */
@media only screen and (max-width: 39.9375em) {
  h1 {
    font-size: 1.5rem;
  }

  .modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    -webkit-overflow-scrolling: touch;
    border-radius: 0;
    -webkit-transform: scale(1.1);
            transform: scale(1.1);
    padding: 0 !important;
  }

  .close-modal {
    right: 20px !important;
  }
}
body {
  font-family: "Roboto", sans-serif;
  min-height: 100%;
  background: #424250;
  color: #adadb1;
  position: relative;
  padding-bottom: 3rem;
  margin: 0;
}

h2 {
  margin: 0px;
  color: #eee;
}

h6 {
  margin: 0px;
  color: #777;
}
.result-dirs::-webkit-scrollbar {
    width: 1em;
}

.result-dirs::-webkit-scrollbar-track {
  background: #eee;
  border-radius: 6px;
}

.result-dirs::-webkit-scrollbar-thumb {
  background-color: #324a5ebd;
  border-radius: 3px;
  outline: 1px solid #eeeeee;
}

::-webkit-scrollbar {
  width: 4px;
  height: 4px;
}

::-webkit-scrollbar-track {
background: #000;
border-radius: 6px;
}

::-webkit-scrollbar-thumb {background-color: #4eeeb2;border-radius: 3px;outline: 1px solid lime;}

.wrapper {
  text-align: center;
  margin: 50px auto;
}

.tabs {
  margin-top: 50px;
  font-size: 15px;
  padding: 0px;
  list-style: none;
  background: #33333d;
  box-shadow: 0px 5px 20px rgba(0, 0, 0, 0.1);
  display: inline-block;
  border-radius: 50px;
  position: relative;
}

.tabs a {
  text-decoration: none;
  color: #fff;
  text-transform: uppercase;
  padding: 10px 20px;
  display: inline-block;
  position: relative;
  z-index: 1;
  transition-duration: 0.6s;
}

.tabs a.active {
  color: #fff;
}

.tabs a i {
  margin-right: 5px;
}

.tabs .selector {
  height: 100%;
  display: inline-block;
  position: absolute;
  left: 0px;
  top: 0px;
  z-index: 1;
  border-radius: 50px;
  transition-duration: 0.6s;
  transition-timing-function: cubic-bezier(0.68, -0.55, 0.265, 1.55);
  background: #05abe0;
  background: -moz-linear-gradient(45deg, #05abe0 0%, #8200f4 100%);
  background: -webkit-linear-gradient(45deg, #04b97f 0%, #0ed093 100%);
  background: linear-gradient(45deg, #04b97f 0%, #0ed093 100%);
  filter: progid:DXImageTransform.Microsoft.gradient(
      startColorstr="#05abe0",
      endColorstr="#8200f4",
      GradientType=1
    );
}
.container{
  width: 800px;
  margin: 0 auto;
  border-radius: 6px;
  box-shadow: 0px 5px 20px rgba(0, 0, 0, 0.18);
  padding: 24px;
  margin-top: 21px;
  background: #33333d;
  border: solid 1px #313131;
  /** overflow: auto; **/
  position: relative;
}
.target_box{
  border: solid 1px #262629;
  border-radius: 18px;
  margin: 5px;
  width: 94%;
  background: #2f2f35;
  padding: 8px 19px;
  font-weight: bold;
  transition: all 0.2s cubic-bezier(0.55, 0, 0.1, 1);
  outline: none;
  color: #ffffff;
  text-align: center;
  }
  .target_box:hover {
    border: solid 1px #4eeeb2;
    box-shadow: 0px 0px 9px 0px #4eeeb24a;
  }
  .start_scan{
    background: transparent;
    margin: 0px;
    margin-top: 20px;
    border: solid 1px #4eeeb2;
    padding: 5px 30px;
    cursor: pointer;
    letter-spacing: 1px;
    text-decoration: none;
    text-transform: uppercase;
    font-size: 12px;
    color: #4eeeb2;
    border-radius: 18px;
  }
  .start_scan:hover{
    background: #4eeeb2;
    color: #000;
    box-shadow: 0px 2px 6px #4eeeb28c;
  }
.avatar{
  width: 82px;
  border-radius: 100px;
  display: table-cell;
}
.avatar-placeholder{
  width: 30%;
  display: inline-block;
  float: left;
}
.bio-placeholder{
  width: 100%;
  line-height: 25px;
  text-align: center;
  overflow: hidden;
  font-size: 15px;
  letter-spacing: 1px;
}
.result-dirs{
  padding: 7px;
    text-align: left;
    max-height: 800px;
    margin: 14px;
    overflow: auto;
}
.result-single {
      border: solid 1px #324a5e;
      background-image: url(/static/result.svg);
      padding: 6px 44px;
      font-size: 15px;
      margin-bottom: 10px;
      border-radius: 24px;
      background-size: 28px;
      cursor: pointer;
      background-repeat: no-repeat;
      background-position: left;
      background-position-x: 2px;
  }

.result-single:hover{
  background-color: #324a5e;
  color: black;
  transition-timing-function: ease;
  transition: all 0.2s ease-in;
  border: solid 1px #fff;
}

.upload-container{
  background: #000;
  padding: 4px;
  border-radius: 4px;
  font-size: 15px;
  width: 97%;
  font-weight: bold;
  color: #d0d0d0;
}

.log-holder{
  width: 800px;
  font-family: ocraextended;
  margin: 0 auto;
  margin-top: 34px;
  background: #27272f;
  font-size: 13px;
  color: #89ff00;
  padding: 24px;
  border-top-right-radius: 5px;
  border-top-left-radius: 5px;
  max-height: 230px;
  overflow: auto;
  text-align: left;
}

.mainbut {
  width: 47%;
  display: inline-block;
  font-size: 24px;
  padding: 5px;
  border: solid 1px;
  box-shadow: 0px 2px 8px 1px #00000059;
  cursor: pointer;
  border-radius: 4px;
  margin: 4px;
}

.mainbut img{
  width: 50px;
}

.butlocal{
  background: #ffd15c17;
  border: solid 2px #f3705a;
  color: white;
}

.butremote{
  background: #324a5e17;
  border: solid 2px #324a5e;
  color: #ffffff;
}

.butremote:hover{
  background: #324a5e;
  color: white;
  box-shadow: 0px 2px 8px 1px #324a5e6b;
  transition: all 0.1s cubic-bezier(0.55, 0, 0.1, 1);
}

.butlocal:hover{
  background: #f3705a;
  box-shadow: 0px 2px 8px 1px #f3705a6b;
  color: white;
  transition: all 0.1s cubic-bezier(0.55, 0, 0.1, 1);
}

.butdesc{
  font-size: 13px;
  padding: 0 !important;
  margin: inherit;
  text-transform: uppercase;
}

#lightSwitchOff{ display:none; }
#lightSwitchOn{ display:inline; }

.dmode{
  position: fixed;
  bottom: 20px;
  right: 20px;
  border-radius: 100%;
  height: 27px;
  width: 27px;
  padding: 10px;
  z-index: 10;
  -webkit-transition: -webkit-transform .8s ease-in-out;
  transition:         transform .8s ease-in-out;
}

.dmode:hover{
  -webkit-transform: rotate(360deg);
  transform: rotate(360deg);
}

.day{
  background: #fff;
  box-shadow: 0px 0px 20px 1px #ffffff73;
}

.night{
  background: #000;
  box-shadow: 0px 0px 20px 1px #000000;
}

a.paginate_button.current {
  background: #4eeeb2;
  color: black;
  cursor: not-allowed;
}

table.result-table{
	width: 100%;
	/* padding: 6px; */
  border-collapse: collapse;
  text-align: left;
}

table.result-table th{
    text-align: left;
    background: #27272f;
    padding: 5px;
    color: #a2a2a2;
}

table.result-table tr{
	background: transparent;
	border: solid 1px #000;
}

table.result-table tr:hover{
  background: #27272f;
  color: #ffffff;
  box-shadow: 0px 0px 6px 1px #272727;
  transition: all ease 0.2s;
}

table.result-table td{
  word-break: break-all;
  padding: 8px 5px !important;
  max-width: 500px;
  font-size: 14px;
}

.dataTables_length{
    width: 50%;
    float: left;
    padding: 10px;
    padding-left: 0px;
    font-weight: bold;
    text-align: left;
    color: gray;
}
.dataTables_length select{
	border: solid 1px #272727;
    padding: 2px;
    background: #2d2d2c;
    color: white;
}
.dataTables_length select:hover{
    border: solid 1px #676767;
    transition: all ease 0.2s;
}
.dataTables_filter{
    width: 44%;
    float: right;
    padding: 10px;
    font-weight: bold;
    padding-right: 0px;
    text-align: right;
    color: gray;
}

.dataTables_filter input{
    background: #27272f;
    padding: 3px 8px;
    border-radius: 19px;
    margin-left: 4px;
    outline: none;
    border: solid 1px #272727;
    color: white;
}
.dataTables_filter input:hover{
    border: solid 1px #4eeeb2;
    box-shadow: 0px 0px 9px 0px #4eeeb24a;
    color: #4eeeb2;
    transition: all ease 0.2s;
}
.dataTables_info{
    padding: 7px;
    text-align: left;
    padding-left: 0px;
    color: #928b8b;
    width: 35%;
    display: inline-block;
    float: left;
}
.paginate_button{
  background: transparent;
  color: #4eeeb2;
  border: solid 1px #4eeeb2;
  padding: 0px 5px;
  border-radius: 2px;
  width: 100%;
  margin: 2px;
  cursor: pointer;
  text-transform: uppercase;
}
.paginate_button:hover{
  background: #4eeeb2;
  color: black;
  transition: all ease 0.2s;
}
.dataTables_paginate{
	margin-top: 10px;
	display: inline-block;
	width: 60%;
	text-align: right;
	/* float: right; */
	padding: 7px;
	padding-right: 0px;
}
.paginate_button .current, .disabled{
  background: #212121;
  color: gray;
  border: solid 2px #212121;
  cursor: not-allowed;
}
.paginate_button .current, .disabled:hover{
	background: #212121;
	color: gray;
	cursor: not-allowed;
}
.querybox{
    background: #272727;
    padding: 5px 15px;
    color: #109be1;
    width: fit-content;
    border-radius: 5px;
}
th.sorting_asc {
    border-bottom: solid 1px #4deeae;
}
th.sorting_desc {
    border-top: solid 1px #4eeeb2;
}
.logo-placeholder{
  text-align: center;
}

.inline-note{
  padding: 13px 8px;
  font-size: 14px;
  background: #27272f96;
  margin-top: 19px;
  color: #adadb1;
  border-radius: 5px;
  letter-spacing: 1px;
  border-left: solid 5px #59595d;
  border-bottom-left-radius: 0px;
  border-top-left-radius: 0px;
}

.result-header{
  color: #00fd47;
  margin-bottom: 16px;
  text-transform: uppercase;
  letter-spacing: 1ch;
}

.permission{
    display: inline-block;
    padding: 5px 12px;
    margin: 3px;
    border-radius: 3px;
    color: #000;
    cursor: pointer;
    background: #89ff00;
    box-shadow: 0px 0px 9px 2px #131313ab;
}

.permission:hover {
  box-shadow: 0px 0px 9px 2px #89ff006e;
  background: #000;
  color: #89ff00;
}

.fstats {
  display: inline-block;
  width: 15%;
  background: #1b1a1a;
  padding: 8px 4px;
  border-radius: 4px;
  box-shadow: 0px 0px 1px 0px #0006;
}

ul.result-tabs{
  margin: 0px;
  width: 100%;
  /* border-spacing: 7px; */
  border-collapse: separate;
  display: table;
  padding: 0px;
  list-style: none;
}
ul.result-tabs li{
  color: #adadb1;
  display: table-cell;
  padding: 10px 15px;
  font-size: 12px;
  cursor: pointer;
  margin-bottom: 9px;
  border-bottom: solid 2px #adadb1;
  text-transform: uppercase;
  letter-spacing: 2px;
}

ul.result-tabs li.current{
  border-bottom: solid 2px #ffffff;
  color: #ffffff;
  text-shadow: 0px 0px 7px #989898;
}

.tab-content{
  display: none;
  border-radius: 7px;
  margin: 15px 0px;
  box-shadow: 0px 3px 6px 0px #13131399;
  background: #373740;
  padding: 15px;
}

.tab-content.current{
  display: inherit;
}

ul.result-tabs li:hover {
  border-bottom: solid 2px #ffffff;
}

html {
  height: 100%;
  box-sizing: border-box;
}

.footer {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  width: 100%;
  font-size: 12px;
  text-transform: uppercase;
  background-color: #000000;
  letter-spacing: 4px;
  color: #a2a2a2;
  box-shadow: 0px -2px 9px 0px #0c0c0c69;
  text-align: center;
}

img.cat-image {
  width: 100px;
  margin-bottom: 10px;
}

.pill {
  display: table-cell;
  text-align: center;
  border: solid 1px;
  padding: 7px;
  cursor: pointer;
  border-radius: 5px;
}

.gchrome {
  border: solid 2px #FF9800;
  color: #FF9800;
}

.mfirefox {
  border: solid 2px #FF5722;
  color: #FF5722;
}

.mfirefox:hover {
  background: #FF5722;
  color: white;
  box-shadow: 0px 0px 6px 1px #ff00005e;
  transition: all 0.2s;
}

.gchrome:hover {
  background: #FF9800;
  color: white;
  box-shadow: 0px 0px 6px 1px #ff00005e;
  transition: all 0.2s;
}

.pill-container {
  display: table;
  width: 100%;
  border-collapse: separate;
  border-spacing: 5px;
}

.opera {
  border: solid 2px red;
  color: red;
}

.opera:hover {
  background: red;
  color: white;
  box-shadow: 0px 0px 6px 1px #ff00005e;
  transition: all 0.2s;
}

::-moz-selection { 
  color: #000;
  background: #fffffff2;
}

::selection {
  color: #000;
  background: #fffffff2;
}

.ext-info-body {
  width: 100%;
  display: inline-block;
  background: #000000;
  padding: 9px;
  color: #dedede;
  vertical-align: middle;
  z-index: 1;
  position: relative;
  border-radius: 6px;
  /* border: dotted 1px black; */
  box-shadow: 0px 0px 13px 0px #0000004d;
}

.ext-info-img {
  display: inline-block;
  width: 50px;
  height: 50px;
  text-align: center;
  background: #373740;
  position: relative;
  padding: 19px;
  vertical-align: middle;
  z-index: 99;
  border: solid 7px #F44336;
  border-radius: 50%;
  font-size: 28px;
  color: red;
  font-weight: bold;
  box-shadow: inset 0 0 8px 0px #0000007a;
  letter-spacing: 4px;
  line-height: 50px;
}

.ext-info-col1 {
  width: 65%;
  display: inline-block;
  text-align: left;
  vertical-align: middle;
}

.ext-info-col2 {
  display: inline-block;
  width: 10%;
  border-left: solid 2px #464545;
  font-size: 13px;
  vertical-align: middle;
  padding: 7px;
}

.ext-info-col3 {
  display: inline-block;
  width: 17%;
  border-left: solid 2px #464545;
  font-size: 13px;
  vertical-align: middle;
  padding-left: 8px;
}

.ext-info-name {
  width: 100%;
  display: inline-block;
  font-size: 22px;
}

.ext-info-others {}

.ext-info-version {
  display: inline-block;
  margin: 5px;
  margin-left: 0px;
  padding: 3px 10px;
  background: #03A9F4;
  color: #fff;
  border-radius: 3px;
  font-size: 13px;
}

.ext-info-author {
  display: inline-block;
  margin: 5px;
  padding: 3px 10px;
  background: #FFC107;
  color: #000;
  font-size: 13px;
  border-radius: 3px;
}

.ext-info-main {
  /* background: #1f1e1e; */
}

.ext-info-description {
  font-size: 13px;
  margin-top: 5px;
  margin-bottom: 5px;
}

.ext-info-last-scanned{
  display: inline-block;
  margin: 5px;
  padding: 3px 10px;
  background: #e91e63;
  color: #fff;
  font-size: 13px;
  border-radius: 3px;
}

.ext-info-img img {
  width: 50%;
}

div#loading {
  width: 100%;
  height: 100%;
  left: 0;
  padding-top: 10%;
  letter-spacing: 5px;
  top: 0;
  font-family: ocraextended;
  z-index: 99999;
  position: fixed;
  background: #000000eb;
}

.swal-overlay {
  background-color: rgba(43, 165, 137, 0.45);
}

.log-actions {
  width: 800px;
  background: #27272f;
  margin: 0 auto;
  padding: 15px 24px;
  border-bottom-left-radius: 5px;
  border-bottom-right-radius: 5px;
  padding-bottom: 20px;
}

.clear-logs-button {
  border: solid 1px red;
  background: transparent;
  color: red;
  font-weight: bold;
  font-size: 15px;
  font-family: ocraextended;
  border-radius: 3px;
  padding: 6px;
  display: inline-block;
  width: 40%;
}

.logs-explorer-button {
  border: solid 1px #03A9F4;
  background: transparent;
  font-family: ocraextended;
  color: #03A9F4;
  border-radius: 3px;
  padding: 6px 23px;
  display: inline-block;
  width: 40%;
  font-weight: bold;
  font-size: 15px;
}

.clear-logs-button:hover {
  background: red;
  color: black;
}

.logs-explorer-button:hover {
  color: black;
  background: #03A9F4;
}

.perm {
  background: #2b2b2b;
  margin-bottom: 9px;
  color: #3e96fa;
  /* padding: 10px 9px; */
  border-radius: 4px;
  text-align: left;
  display: table-cell;
  border-spacing: 5px;
}

.perm-desc {
  padding: 10px;
  background: #2b2b2b;
  color: #c8c8c8;
  border-radius: 4px;
  margin: 5px 0px;
  /* box-shadow: 0px 0px 3px 0px #3e96fab5; */
}

.perm-warn {
  padding: 10px;
  background: transparent;
  color: #f70a2a;
  border-radius: 4px;
  margin: 5px 0px;
  font-weight: bold;
}

.perm-name {
  text-align: center;
  font-size: 20px;
  color: white;
  background: #3e96fa;
  /* font-weight: bold; */
  border-top-left-radius: 4px;
  border-top-right-radius: 4px;
}

.permissions-holder {
  display: table;
  border-spacing: 5px;
}

.file_name {
  width: 100%;
  text-align: left;
  font-size: 21px;
  margin-bottom: 5px;
}

.file_location {
  display: inline-block;
  font-size: 12px;
  background: #000;
  color: #b7b6b6;
  padding: 3px 9px;
  border-radius: 2px;
}

.file_attrs {
  text-align: left;
  font-size: 12px;
}

.file_type {
  display: inline-block;
  background: #1d89ff;
  font-weight: bold;
  border-radius: 2px;
  color: white;
  padding: 3px 6px;
}

.file_size {
  display: inline-block;
  background: #89ff00;
  font-weight: bold;
  border-radius: 2px;
  color: black;
  padding: 3px 6px;
}

.file_info {
  border: solid 1px #252525;
  padding: 7px;
  background: #252525;
  border-radius: 3px;
}
.file_icon {
  display: inline-block;
  padding-right: 12px;
  text-align: left;
  float: left;
}

.source_code {
  height: 430px;
  overflow-y: scroll;
  text-align: left;
  width: 95%;
  border: solid 1px #4eeeb2;
  padding: 8px;
  background: #1a1a20;
  color: #28b78d;
  margin-top: 20px;
}

.CodeMirror {
  margin-top: 24px;
  text-align: left;
  height: 450px !important;
}

.editor_buttons {
  margin-top: 15px;
}

.format_button {
  border: solid 1px #000000;
  background: transparent;
  color: #b3b3b3;
  font-size: 15px;
  padding: 7px 23px;
  letter-spacing: 2px;
  border-radius: 3px;
  box-shadow: 0px 0px 9px 1px #00000054;
}

.format_button:hover{
  background: #000000;
  color: #fff;
}

.file_image {
  float: left;
  margin-right: 22px;
  display: inline-block;
}

.file_body {
  width: 90%;
  display: inline-block;
}

.file_image img {
  width: 44px;
}

.header_for_main{
  color: #4eeeb2;
  background: #27272f;
  border-bottom: solid 1px #4eeeb2;
  margin: -25px;
  margin-bottom: 28px;
  padding: 6px;
  font-weight: normal;
  font-size: 16px;
  letter-spacing: 5px;
  text-transform: uppercase;
}

.header_for_sub{
  color: #4eeeb2;
  background: #27272f;
  border-bottom: solid 1px #4eeeb2;
  margin: -15px;
  margin-bottom: 28px;
  padding: 6px;
  font-size: 14px;
  letter-spacing: 3px;
  text-transform: uppercase;
  font-weight: normal;
  border-top-left-radius: 5px;
  border-top-right-radius: 5px;
}

.option_body {
  padding: 8px;
  padding-left: 13px;
  text-align: left;
  background: #33333d;
  margin-bottom: 17px;
}

.option_name {
  text-align: left;
  font-size: 16px;
  text-transform: uppercase;
  letter-spacing: 3px;
  margin: 0px;
  margin-bottom: 8px;
  border-bottom: solid 1px #44444e;
  color: #FF5722;
  padding-bottom: 8px;
}

.option_description {
  text-align: left;
  color: #c3c3c3;
  font-size: 13px;
  letter-spacing: 0.5px;
}

.delete_button {
  border: solid 1px #ff1424;
  background: transparent;
  color: #ff1424;
  box-shadow: 0px 0px 7px 0px #ff596475;
  border-radius: 18px;
  text-transform: uppercase;
  min-width: 225px;
  letter-spacing: 1px;
  margin-top: 7px;
  font-size: 12px;
  padding: 5px 30px;
}

.delete_button:hover {
  background: red;
  color: white;
  border: solid 1px red;
  box-shadow: 0px 2px 6px #ff00009c;
}

#musicButton {
  position: fixed;
  bottom: 83px;
  right: 20px;
  color: white;
  background: #E91E63;
  border-radius: 100%;
  height: 27px;
  width: 27px;
  padding: 10px;
  z-index: 10;
  -webkit-transition: -webkit-transform .8s ease-in-out;
  transition:         transform .8s ease-in-out;
  box-shadow: 0px 0px 10px 0px #E91E63;
}

#musicButton:hover, .change_music:hover, .play_pause:hover {
  -webkit-transform: rotate(360deg);
  transform: rotate(360deg);
}
.accordion__item {
  width: 100%;
}
.accordion__question:after {
  content: "   ▼";
  text-align: right;
  float: right;
}
.accordion__answer {
  display: none;
  font-size: 14px;
  line-height: 19px;
  margin-top: 6px;
  border-top: solid 1px #adadb1;
  padding-top: 10px;
}

.accordion {
  width: 98%;
  text-align: left;
  background: #24242b;
  border-radius: 3px;
  padding: 7px;
  margin-bottom: 7px;
}

.accordion__question {
  color: #a2a7a5;
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 4px;
  width: 100%;
  cursor: pointer;
}

.accordion__question:hover {
  color: #4eeeb2;
}

.stats {
  display: inline-block;
  padding: 11px;
  vertical-align: top;
  height: 381px;
  width: 43%;
  text-align: left;
  background: #33333d;
  box-shadow: 0px 0px 8px 0px #00000080;
  border-radius: 6px;
  margin: 0px 10px;
  /* border-bottom: solid 3px #4eeeb2; */
}

.stats_head {
  margin: -11px;
  margin-bottom: 12px;
  background: #33333d;
  color: #4eeeb2;
  border-top: solid 3px;
  font-size: 15px;
  text-transform: uppercase;
  text-align: center;
  letter-spacing: 2px;
  border-top-left-radius: 5px;
  border-top-right-radius: 5px;
  padding: 6px;
}

.stats_body {
  line-height: 30px;
  text-align: center;
}

.stats_pill {
  display: inline-block;
  margin: 15px;
  width: 23%;
  padding: 6px 1px;
  align-self: center;
  background: #1f1f27;
  border-radius: 5px;
  text-align: center;
}

.stats_pill img {
  width: 52px;
}

.stats_data {
  background: #000;
  color: white;
  letter-spacing: 1px;
  font-size: 12px;
  margin: -6px -1px;
  border-bottom-left-radius: 5px;
  border-bottom-right-radius: 5px;
}

.stats_pill:hover {
  box-shadow: 0px 0px 12px 0px #00000063;
}

.sub_body, .mid-head{
  box-shadow: 0px 6px 8px 0px #00000050 !important;
}
.sub_body{
  background: #33333d !important;
}

.graph-container {
  width: 90%;
  background: #33333d;
  padding: 20px;
  box-shadow: 0px 0px 14px 0px #0000007a;
  margin: 0 auto;
  border-radius: 5px;
  text-align: left;
  margin-top: 20px;
}

div#large-graph {
  height: 700px;
  background: #1f1f27;
  width: 87%;
  padding-right: 5px;
  border-radius: 5px;
  display: inline-block;
  border-top-right-radius: 0px;
  border-top: solid 3px #4eeeb2;
  border-bottom-right-radius: 0px;
}

.graph-control {
  display: inline-block;
  width: 11%;
  float: right;
  background: #1f1f27;
  border-left: dotted 1px #4eeeb2;
  height: 700px;
  border-top: solid 3px #4eeeb2;
  padding: 0px 7px;
  border-top-right-radius: 5px;
  margin-left: -5px;
  border-bottom-right-radius: 5px;
  overflow: hidden;
}

.control-title {
  font-size: 15px;
  text-transform: uppercase;
  letter-spacing: 2px;
  color: #4eeeb2;
  padding-top: 3px;
  text-align: center;
  margin-bottom: 8px;
}

.control-body {
  font-size: 15px;
}

.nothing {
  background: #424250;
  padding: 12px;
  border-radius: 7px;
  color: #b0b0e2;
  text-transform: uppercase;
  letter-spacing: 2px;
  font-size: 15px;
  font-weight: 100;
}

.sub-head-settings {
  text-align: left;
  color: #ffffff;
  font-size: 14px;
  text-transform: uppercase;
  display: inline-block;
  letter-spacing: 2px;
  padding-bottom: 5px;
  font-weight: bold;
}

.settings_textbox {
  background: #00000021;
  border: solid 1px #33333d;
  padding: 6px 11px;
  letter-spacing: 1px;
  outline: none;
  font-size: 13px;
  color: #a5a5a5;
  width: 400px;
  border-radius: 27px;
}

.settings_textbox:focus {border: solid 1px #4eeeb2;box-shadow: 0px 0px 9px 0px #4eeeb24a;color: #4eeeb2;}

.target_box:focus {
    border: solid 1px #4eeeb2;
    box-shadow: 0px 0px 9px 0px #4eeeb24a;
    color: #4eeeb2;
}

.change_music {
  position: fixed;
  bottom: 83px;
  right: 130px;
  color: white;
  background: #03A9F4;
  border-radius: 100%;
  height: 27px;
  width: 27px;
  padding: 10px;
  z-index: 10;
  box-shadow: 0px 0px 10px 0px #03a9f4;
}

.play_pause {
  position: fixed;
  bottom: 83px;
  right: 75px;
  color: white;
  background: #9C27B0;
  border-radius: 100%;
  height: 27px;
  width: 27px;
  padding: 10px;
  z-index: 10;
  box-shadow: 0px 0px 10px 0px #9C27B0;
}

#music_buttons {
  position: fixed;
  bottom: 77px;
  right: 35px;
  color: white;
  background: #141415;
  width: 130px;
  height: 37px;
  border-radius: 73px;
  padding: 10px;
  border-top-right-radius: 76px;
  border-bottom-right-radius: 76px;
  z-index: 9;
  box-shadow: 0px 0px 13px 0px #00000091;
}
.dataTables_filter input:focus {
    border: solid 1px #4eeeb2;
    box-shadow: 0px 0px 9px 0px #4eeeb24a;
    color: #4eeeb2;
}

.settings_textbox:hover {
    border: solid 1px #00ff9f70;
}

.ext_url {
  text-decoration: none;
  color: inherit;
  font-weight: normal;
  font-size: inherit;
}

.ext_url:hover {
  border-bottom: dotted 1px #4eeeb2;
  color: #4eeeb2;
  padding-bottom: 4px;
}

.mid_header{
  background: #27272f;
  color: #ffffff;
  text-transform: uppercase;
  font-size: 13px;
  padding: 1px;
  letter-spacing: 2px;
  font-weight: normal;
  /* margin: 0px -6px; */
  border-radius: 12px;
  margin-top: 15px;
  margin-bottom: 10px;
}

.license {
  width: 100%;
  height: 300px;
  background: #424250;
  border: none;
  border-radius: 4px;
  color: #fff;
  text-align: center;
}

.author_info {
    display: table-cell;
    float: right;
    width: 85%;
    text-align: left;
}
a#change_music:hover {
  background: #00BCD4;
}

a#play_pause:hover {
  background: #cf07f1;
}

a.hreflink {
  text-decoration: none;
  color: #03A9F4;
  border-bottom: dotted 1px #03a9f4;
}

.sub-head-settingss {
  display: inline-block;
  color: #d0d0d0;
  letter-spacing: 1px;
  text-transform: capitalize;
}


.switch {
  margin-left: 5px;
  position: relative;
  display: inline-block;
}

.switch-input {
  display: none;
}

.switch-label {
  display: block;
  width: 44px;
  height: 14px;
  cursor: pointer;
  padding-top: 2px;
  text-indent: -150%;
  clip: rect(0 0 0 0);
  color: transparent;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
}
.switch-label:before,
.switch-label:after {
  content: "";
  display: block;
  position: absolute;
  cursor: pointer;
}
.switch-label:before {
  width: 100%;
  height: 100%;
  background-color: #424250;
  border-radius: 9999em;
  transition: background-color 0.25s ease;
}
.switch-label:after {
  top: 0;
  left: 0;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background-color: #fff;
  box-shadow: 0 0 2px rgba(0, 0, 0, 0.45);
  transition: left 0.25s ease;
}
.switch-input:checked + .switch-label:before {
  background-color: #39bb00;
}
.switch-input:checked + .switch-label:after {
  left: 24px;
}

```

### `static/css/bttn.css`

```css
/*!
 *
 * bttn.css - https://ganapativs.github.io/bttn.css
 * Version - 0.2.4
 * Demo: https://bttn.surge.sh
 *
 * Licensed under the MIT license - http://opensource.org/licenses/MIT
 *
 * Copyright (c) 2016 Ganapati V S (@ganapativs)
 *
 */.bttn-default{color:#fff}.bttn,.bttn-lg,.bttn-md,.bttn-primary,.bttn-sm,.bttn-xs{color:#1d89ff}.bttn-warning{color:#feab3a}.bttn-danger{color:#ff5964}.bttn-success{color:#28b78d}.bttn-royal{color:#bd2df5}.bttn,.bttn-lg,.bttn-md,.bttn-sm,.bttn-xs{margin:0;padding:0;border-width:0;border-color:transparent;background:transparent;font-weight:400;cursor:pointer;position:relative}.bttn-lg{padding:8px 15px;font-size:24px}.bttn-lg,.bttn-md{font-family:inherit}.bttn-md{font-size:20px;padding:5px 12px}.bttn-sm{padding:4px 10px;font-size:16px}.bttn-sm,.bttn-xs{font-family:inherit}.bttn-xs{padding:3px 8px;font-size:12px}.bttn-gradient,.bttn-simple{margin:0;padding:0;border-color:transparent;background:transparent;font-weight:400;cursor:pointer;position:relative;font-size:20px;font-family:inherit;padding:5px 12px;overflow:hidden;border-width:0;border-radius:4px;background:hsla(0,0%,100%,.4);color:#fff;-webkit-transition:all .3s cubic-bezier(.02,.01,.47,1);transition:all .3s cubic-bezier(.02,.01,.47,1)}.bttn-gradient:focus,.bttn-gradient:hover,.bttn-simple:focus,.bttn-simple:hover{opacity:.75}.bttn-gradient.bttn-xs,.bttn-simple.bttn-xs{padding:3px 8px;font-size:12px;font-family:inherit}.bttn-gradient.bttn-sm,.bttn-simple.bttn-sm{padding:4px 10px;font-size:16px;font-family:inherit}.bttn-gradient.bttn-md,.bttn-simple.bttn-md{font-size:20px;font-family:inherit;padding:5px 12px}.bttn-gradient.bttn-lg,.bttn-simple.bttn-lg{padding:8px 15px;font-size:24px;font-family:inherit}.bttn-gradient.bttn-default,.bttn-simple.bttn-default{background:hsla(0,0%,100%,.4)}.bttn-gradient.bttn-primary,.bttn-simple.bttn-primary{background:#1d89ff}.bttn-gradient.bttn-warning,.bttn-simple.bttn-warning{background:#feab3a}.bttn-gradient.bttn-danger,.bttn-simple.bttn-danger{background:#ff5964}.bttn-gradient.bttn-success,.bttn-simple.bttn-success{background:#28b78d}.bttn-gradient.bttn-royal,.bttn-simple.bttn-royal{background:#bd2df5}.bttn-bordered{margin:0;padding:0;border-width:0;border-color:transparent;font-weight:400;cursor:pointer;position:relative;font-size:20px;font-family:inherit;padding:5px 12px;overflow:hidden;border:1px solid hsla(0,0%,100%,.4);border-radius:4px;background:transparent;color:#fff;-webkit-transition:all .3s cubic-bezier(.02,.01,.47,1);transition:all .3s cubic-bezier(.02,.01,.47,1)}.bttn-bordered:focus,.bttn-bordered:hover{border-color:hsla(0,0%,100%,.7)}.bttn-bordered.bttn-xs{padding:3px 8px;font-size:12px;font-family:inherit}.bttn-bordered.bttn-sm{padding:4px 10px;font-size:16px;font-family:inherit}.bttn-bordered.bttn-md{font-size:20px;font-family:inherit;padding:5px 12px}.bttn-bordered.bttn-lg{padding:8px 15px;font-size:24px;font-family:inherit}.bttn-bordered.bttn-default{border-color:hsla(0,0%,100%,.4);color:#fff}.bttn-bordered.bttn-default:focus,.bttn-bordered.bttn-default:hover{border-color:hsla(0,0%,100%,.7)}.bttn-bordered.bttn-primary{border-color:rgba(29,137,255,.4);color:#1d89ff}.bttn-bordered.bttn-primary:focus,.bttn-bordered.bttn-primary:hover{border-color:rgba(29,137,255,.7)}.bttn-bordered.bttn-warning{border-color:rgba(254,171,58,.4);color:#feab3a}.bttn-bordered.bttn-warning:focus,.bttn-bordered.bttn-warning:hover{border-color:rgba(254,171,58,.7)}.bttn-bordered.bttn-danger{border-color:rgba(255,89,100,.4);color:#ff5964}.bttn-bordered.bttn-danger:focus,.bttn-bordered.bttn-danger:hover{border-color:rgba(255,89,100,.7)}.bttn-bordered.bttn-success{border-color:rgba(40,183,141,.4);color:#28b78d}.bttn-bordered.bttn-success:focus,.bttn-bordered.bttn-success:hover{border-color:rgba(40,183,141,.7)}.bttn-bordered.bttn-royal{border-color:rgba(189,45,245,.4);color:#bd2df5}.bttn-bordered.bttn-royal:focus,.bttn-bordered.bttn-royal:hover{border-color:rgba(189,45,245,.7)}.bttn-gradient{border-radius:100px;box-shadow:0 1px 2px rgba(0,0,0,.25);text-shadow:0 1px 0 hsla(0,0%,100%,.25)}.bttn-gradient,.bttn-gradient.bttn-default{background-image:-webkit-gradient(linear,left top,left bottom,color-stop(0,#fff),color-stop(1,#d6e3ff));background-image:-webkit-linear-gradient(top,#fff,#d6e3ff);background-image:linear-gradient(180deg,#fff 0,#d6e3ff);background-image:-webkit-linear-gradient(93deg,#d6e3ff,#fff);color:#1d89ff}.bttn-gradient.bttn-primary{background-image:-webkit-gradient(linear,left top,left bottom,color-stop(0,#00bbd4),color-stop(1,#3f51b5));background-image:-webkit-linear-gradient(top,#00bbd4,#3f51b5);background-image:linear-gradient(180deg,#00bbd4 0,#3f51b5);background-image:-webkit-linear-gradient(93deg,#3f51b5,#00bbd4);color:#fff}.bttn-gradient.bttn-warning{background-image:-webkit-gradient(linear,left top,left bottom,color-stop(0,#feab3a),color-stop(1,#f35626));background-image:-webkit-linear-gradient(top,#feab3a,#f35626);background-image:linear-gradient(180deg,#feab3a 0,#f35626);background-image:-webkit-linear-gradient(93deg,#f35626,#feab3a);color:#fff}.bttn-gradient.bttn-danger{background-image:-webkit-gradient(linear,left top,left bottom,color-stop(0,#ff97c2),color-stop(1,#e91e63));background-image:-webkit-linear-gradient(top,#ff97c2,#e91e63);background-image:linear-gradient(180deg,#ff97c2 0,#e91e63);background-image:-webkit-linear-gradient(93deg,#e91e63,#ff97c2);color:#fff}.bttn-gradient.bttn-success{background-image:-webkit-gradient(linear,left top,left bottom,color-stop(0,#9ccc65),color-stop(1,#009688));background-image:-webkit-linear-gradient(top,#9ccc65,#009688);background-image:linear-gradient(180deg,#9ccc65 0,#009688);background-image:-webkit-linear-gradient(93deg,#009688,#9ccc65);color:#fff}.bttn-gradient.bttn-royal{background-image:-webkit-gradient(linear,left top,left bottom,color-stop(0,#9c27b0),color-stop(1,#512da8));background-image:-webkit-linear-gradient(top,#9c27b0,#512da8);background-image:linear-gradient(180deg,#9c27b0 0,#512da8);background-image:-webkit-linear-gradient(93deg,#512da8,#9c27b0);color:#fff}.bttn-minimal{margin:0;padding:0;border-color:transparent;font-weight:400;cursor:pointer;position:relative;font-size:20px;font-family:inherit;padding:5px 12px;overflow:hidden;border-width:0;border-radius:4px;background:transparent;color:#fff;-webkit-transition:all .5s cubic-bezier(.02,.01,.47,1);transition:all .5s cubic-bezier(.02,.01,.47,1)}.bttn-minimal:after,.bttn-minimal:before{position:absolute;bottom:0;left:10px;width:calc(100% - 20px);height:1px;background:currentColor;content:'';opacity:.65;-webkit-transition:opacity .5s cubic-bezier(.02,.01,.47,1),-webkit-transform .5s cubic-bezier(.02,.01,.47,1);transition:opacity .5s cubic-bezier(.02,.01,.47,1),-webkit-transform .5s cubic-bezier(.02,.01,.47,1);transition:transform .5s cubic-bezier(.02,.01,.47,1),opacity .5s cubic-bezier(.02,.01,.47,1);transition:transform .5s cubic-bezier(.02,.01,.47,1),opacity .5s cubic-bezier(.02,.01,.47,1),-webkit-transform .5s cubic-bezier(.02,.01,.47,1)}.bttn-minimal:focus,.bttn-minimal:hover{opacity:.9}.bttn-minimal:focus:after,.bttn-minimal:hover:after{opacity:1;-webkit-transform:translateX(-10px) rotate(.001deg);transform:translateX(-10px) rotate(.001deg)}.bttn-minimal:focus:before,.bttn-minimal:hover:before{opacity:1;-webkit-transform:translateX(10px) rotate(.001deg);transform:translateX(10px) rotate(.001deg)}.bttn-minimal.bttn-xs{padding:3px 8px;font-size:12px;font-family:inherit}.bttn-minimal.bttn-sm{padding:4px 10px;font-size:16px;font-family:inherit}.bttn-minimal.bttn-md{font-size:20px;font-family:inherit;padding:5px 12px}.bttn-minimal.bttn-lg{padding:8px 15px;font-size:24px;font-family:inherit}.bttn-minimal.bttn-default{color:#fff}.bttn-minimal.bttn-primary{color:#1d89ff}.bttn-minimal.bttn-warning{color:#feab3a}.bttn-minimal.bttn-danger{color:#ff5964}.bttn-minimal.bttn-success{color:#28b78d}.bttn-minimal.bttn-royal{color:#bd2df5}.bttn-stretch{margin:0;padding:0;border-color:transparent;font-weight:400;cursor:pointer;position:relative;font-size:20px;font-family:inherit;padding:5px 12px;overflow:hidden;border-width:0;border-radius:0;background:transparent;color:#fff;letter-spacing:0}.bttn-stretch,.bttn-stretch:after,.bttn-stretch:before{-webkit-transition:all .2s cubic-bezier(.02,.01,.47,1);transition:all .2s cubic-bezier(.02,.01,.47,1)}.bttn-stretch:after,.bttn-stretch:before{position:absolute;left:0;width:100%;height:1px;background:currentColor;content:'';opacity:.65;-webkit-transform:scaleX(0);transform:scaleX(0)}.bttn-stretch:after{top:0}.bttn-stretch:before{bottom:0}.bttn-stretch:focus,.bttn-stretch:hover{letter-spacing:2px;opacity:.9;-webkit-transition:all .3s cubic-bezier(.02,.01,.47,1);transition:all .3s cubic-bezier(.02,.01,.47,1)}.bttn-stretch:focus:after,.bttn-stretch:focus:before,.bttn-stretch:hover:after,.bttn-stretch:hover:before{opacity:1;-webkit-transition:all .3s cubic-bezier(.02,.01,.47,1);transition:all .3s cubic-bezier(.02,.01,.47,1);-webkit-transform:scaleX(1);transform:scaleX(1)}.bttn-stretch.bttn-xs{padding:3px 8px;font-size:12px;font-family:inherit}.bttn-stretch.bttn-sm{padding:4px 10px;font-size:16px;font-family:inherit}.bttn-stretch.bttn-md{font-size:20px;font-family:inherit;padding:5px 12px}.bttn-stretch.bttn-lg{padding:8px 15px;font-size:24px;font-family:inherit}.bttn-stretch.bttn-default{color:#fff}.bttn-stretch.bttn-primary{color:#1d89ff}.bttn-stretch.bttn-warning{color:#feab3a}.bttn-stretch.bttn-danger{color:#ff5964}.bttn-stretch.bttn-success{color:#28b78d}.bttn-stretch.bttn-royal{color:#bd2df5}.bttn-jelly{margin:0;padding:0;border-width:0;border-color:transparent;background:transparent;font-weight:400;cursor:pointer;position:relative;font-size:20px;font-family:inherit;padding:5px 12px;overflow:hidden;background:#fff;color:#1d89ff}.bttn-jelly,.bttn-jelly:before{border-radius:50px;-webkit-transition:all .2s cubic-bezier(.02,.01,.47,1);transition:all .2s cubic-bezier(.02,.01,.47,1)}.bttn-jelly:before{position:absolute;top:0;left:0;width:100%;height:100%;background:currentColor;content:'';z-index:-1;opacity:0;-webkit-transform:scale(.2);transform:scale(.2)}.bttn-jelly:focus,.bttn-jelly:hover{box-shadow:0 1px 8px rgba(58,51,53,.4);-webkit-transform:scale(1.1);transform:scale(1.1)}.bttn-jelly:focus,.bttn-jelly:focus:before,.bttn-jelly:hover,.bttn-jelly:hover:before{-webkit-transition:all .3s cubic-bezier(.02,.01,.47,1);transition:all .3s cubic-bezier(.02,.01,.47,1)}.bttn-jelly:focus:before,.bttn-jelly:hover:before{opacity:.15;-webkit-transform:scale(1);transform:scale(1)}.bttn-jelly.bttn-xs{padding:3px 8px;font-size:12px;font-family:inherit}.bttn-jelly.bttn-xs:focus,.bttn-jelly.bttn-xs:hover{box-shadow:0 1px 4px rgba(58,51,53,.4)}.bttn-jelly.bttn-sm{padding:4px 10px;font-size:16px;font-family:inherit}.bttn-jelly.bttn-sm:focus,.bttn-jelly.bttn-sm:hover{box-shadow:0 1px 6px rgba(58,51,53,.4)}.bttn-jelly.bttn-md{font-size:20px;font-family:inherit;padding:5px 12px}.bttn-jelly.bttn-md:focus,.bttn-jelly.bttn-md:hover{box-shadow:0 1px 8px rgba(58,51,53,.4)}.bttn-jelly.bttn-lg{padding:8px 15px;font-size:24px;font-family:inherit}.bttn-jelly.bttn-lg:focus,.bttn-jelly.bttn-lg:hover{box-shadow:0 1px 10px rgba(58,51,53,.4)}.bttn-jelly.bttn-default{background:#fff;color:#1d89ff}.bttn-jelly.bttn-primary{background:#1d89ff;color:#fff}.bttn-jelly.bttn-warning{background:#feab3a;color:#fff}.bttn-jelly.bttn-danger{background:#ff5964;color:#fff}.bttn-jelly.bttn-success{background:#28b78d;color:#fff}.bttn-jelly.bttn-royal{background:#bd2df5;color:#fff}.bttn-fill{border-radius: 2px;margin:0;padding:0;border-width:0;border-color:transparent;background:transparent;font-weight:400;cursor:pointer;position:relative;font-size:20px;font-family:inherit;padding:5px 12px;z-index:0;border:none;background:#fff;color:#1d89ff;-webkit-transition:all .3s cubic-bezier(.02,.01,.47,1);transition:all .3s cubic-bezier(.02,.01,.47,1);}.bttn-fill:before{position:absolute;bottom:0;left:0;width:100%;height:100%;background:#1d89ff;content:'';opacity:0;-webkit-transition:opacity .15s ease-out,-webkit-transform .15s ease-out;transition:opacity .15s ease-out,-webkit-transform .15s ease-out;transition:transform .15s ease-out,opacity .15s ease-out;transition:transform .15s ease-out,opacity .15s ease-out,-webkit-transform .15s ease-out;z-index:-1;-webkit-transform:scaleX(0);transform:scaleX(0)}.bttn-fill:focus,.bttn-fill:hover{box-shadow:0 1px 8px rgba(58,51,53,.3);color:#fff;-webkit-transition:all .5s cubic-bezier(.02,.01,.47,1);transition:all .5s cubic-bezier(.02,.01,.47,1)}.bttn-fill:focus:before,.bttn-fill:hover:before{opacity:1;-webkit-transition:opacity .2s ease-in,-webkit-transform .2s ease-in;transition:opacity .2s ease-in,-webkit-transform .2s ease-in;transition:transform .2s ease-in,opacity .2s ease-in;transition:transform .2s ease-in,opacity .2s ease-in,-webkit-transform .2s ease-in;-webkit-transform:scaleX(1);transform:scaleX(1)}.bttn-fill.bttn-xs{padding:3px 8px;font-size:12px;font-family:inherit}.bttn-fill.bttn-xs:focus,.bttn-fill.bttn-xs:hover{box-shadow:0 1px 4px rgba(58,51,53,.3)}.bttn-fill.bttn-sm{padding:4px 10px;font-size:16px;font-family:inherit}.bttn-fill.bttn-sm:focus,.bttn-fill.bttn-sm:hover{box-shadow:0 1px 6px rgba(58,51,53,.3)}.bttn-fill.bttn-md{font-size:20px;font-family:inherit;padding:5px 12px}.bttn-fill.bttn-md:focus,.bttn-fill.bttn-md:hover{box-shadow:0 1px 8px rgba(58,51,53,.3)}.bttn-fill.bttn-lg{padding:8px 15px;font-size:24px;font-family:inherit}.bttn-fill.bttn-lg:focus,.bttn-fill.bttn-lg:hover{box-shadow:0 1px 10px rgba(58,51,53,.3)}.bttn-fill.bttn-default{background:#fff;color:#1d89ff}.bttn-fill.bttn-default:focus,.bttn-fill.bttn-default:hover{color:#fff}.bttn-fill.bttn-default:before{background:#1d89ff}.bttn-fill.bttn-primary{background:#1d89ff;color:#fff}.bttn-fill.bttn-primary:focus,.bttn-fill.bttn-primary:hover{color:#1d89ff}.bttn-fill.bttn-primary:before{background:#fff}.bttn-fill.bttn-warning{background:#feab3a;color:#fff}.bttn-fill.bttn-warning:focus,.bttn-fill.bttn-warning:hover{color:#feab3a}.bttn-fill.bttn-warning:before{background:#fff}.bttn-fill.bttn-danger{background:#ff5964;color:#fff}.bttn-fill.bttn-danger:focus,.bttn-fill.bttn-danger:hover{color:#ff5964}.bttn-fill.bttn-danger:before{background:#fff}.bttn-fill.bttn-success{background:#28b78d;color:#fff}.bttn-fill.bttn-success:focus,.bttn-fill.bttn-success:hover{color:#28b78d}.bttn-fill.bttn-success:before{background:#fff}.bttn-fill.bttn-royal{background:#bd2df5;color:#fff}.bttn-fill.bttn-royal:focus,.bttn-fill.bttn-royal:hover{color:#bd2df5}.bttn-fill.bttn-royal:before{background:#fff}.bttn-material-circle{margin:0;padding:0;border-color:transparent;background:transparent;font-weight:400;cursor:pointer;position:relative;font-size:20px;font-family:inherit;padding:5px 12px;overflow:hidden;border-width:0;border-radius:50%;background:#fff;box-shadow:0 2px 5px 0 rgba(0,0,0,.18),0 1px 5px 0 rgba(0,0,0,.15);color:#1d89ff;-webkit-transition:all .25s cubic-bezier(.02,.01,.47,1);transition:all .25s cubic-bezier(.02,.01,.47,1);-webkit-transform:translateZ(0);transform:translateZ(0)}.bttn-material-circle:focus,.bttn-material-circle:hover{box-shadow:0 5px 11px 0 rgba(0,0,0,.18),0 4px 15px 0 rgba(0,0,0,.15);-webkit-transition:box-shadow .4s ease-out;transition:box-shadow .4s ease-out}.bttn-material-circle.bttn-xs{padding:3px 8px;font-size:12px;font-family:inherit;width:28px;height:28px;line-height:24px}.bttn-material-circle.bttn-sm{padding:4px 10px;font-size:16px;font-family:inherit;width:36px;height:36px;line-height:30px}.bttn-material-circle.bttn-md{font-size:20px;font-family:inherit;padding:5px 12px;width:44px;height:44px;line-height:38px}.bttn-material-circle.bttn-lg{padding:8px 15px;font-size:24px;font-family:inherit;width:54px;height:54px;line-height:44px}.bttn-material-circle.bttn-default{background:#fff;color:#1d89ff}.bttn-material-circle.bttn-primary{background:#1d89ff;color:#fff}.bttn-material-circle.bttn-warning{background:#feab3a;color:#fff}.bttn-material-circle.bttn-danger{background:#ff5964;color:#fff}.bttn-material-circle.bttn-success{background:#28b78d;color:#fff}.bttn-material-circle.bttn-royal{background:#bd2df5;color:#fff}.bttn-material-flat{margin:0;padding:0;border-color:transparent;background:transparent;font-weight:400;cursor:pointer;position:relative;font-size:20px;font-family:inherit;padding:5px 12px;overflow:hidden;border-width:0;border-radius:2px;background:#fff;box-shadow:0 2px 5px 0 rgba(0,0,0,.18),0 1px 5px 0 rgba(0,0,0,.15);color:#1d89ff;text-transform:none;-webkit-transition:all .25s cubic-bezier(.02,.01,.47,1);transition:all .25s cubic-bezier(.02,.01,.47,1);-webkit-transform:translateZ(0);transform:translateZ(0)}.bttn-material-flat:focus,.bttn-material-flat:hover{box-shadow:0 5px 11px 0 rgba(0,0,0,.18),0 4px 15px 0 rgba(0,0,0,.15);-webkit-transition:box-shadow .4s ease-out;transition:box-shadow .4s ease-out}.bttn-material-flat.bttn-xs{padding:3px 8px;font-size:12px;font-family:inherit}.bttn-material-flat.bttn-sm{padding:4px 10px;font-size:16px;font-family:inherit}.bttn-material-flat.bttn-md{font-size:20px;font-family:inherit;padding:5px 12px}.bttn-material-flat.bttn-lg{padding:8px 15px;font-size:24px;font-family:inherit}.bttn-material-flat.bttn-default{background:#fff;color:#1d89ff}.bttn-material-flat.bttn-primary{background:#1d89ff;color:#fff}.bttn-material-flat.bttn-warning{background:#feab3a;color:#fff}.bttn-material-flat.bttn-danger{background:#ff5964;color:#fff}.bttn-material-flat.bttn-success{background:#28b78d;color:#fff}.bttn-material-flat.bttn-royal{background:#bd2df5;color:#fff}.bttn-pill{margin:0;padding:0;border-width:0;border-color:transparent;background:transparent;font-weight:400;cursor:pointer;position:relative;font-size:20px;font-family:inherit;padding:5px 12px;z-index:0;overflow:hidden;border:none;border-radius:100px;background:#fff;color:#1d89ff;-webkit-transition:all .3s cubic-bezier(.02,.01,.47,1);transition:all .3s cubic-bezier(.02,.01,.47,1)}.bttn-pill:after,.bttn-pill:before{position:absolute;right:0;bottom:0;width:100px;height:100px;border-radius:50%;background:#1d89ff;content:'';opacity:0;-webkit-transition:opacity .15s cubic-bezier(.02,.01,.47,1),-webkit-transform .15s cubic-bezier(.02,.01,.47,1);transition:opacity .15s cubic-bezier(.02,.01,.47,1),-webkit-transform .15s cubic-bezier(.02,.01,.47,1);transition:transform .15s cubic-bezier(.02,.01,.47,1),opacity .15s cubic-bezier(.02,.01,.47,1);transition:transform .15s cubic-bezier(.02,.01,.47,1),opacity .15s cubic-bezier(.02,.01,.47,1),-webkit-transform .15s cubic-bezier(.02,.01,.47,1);z-index:-1;-webkit-transform:translate(100%,-25%) translateZ(0);transform:translate(100%,-25%) translateZ(0)}.bttn-pill:focus,.bttn-pill:hover{box-shadow:0 1px 8px rgba(58,51,53,.3);color:#fff;-webkit-transition:all .5s cubic-bezier(.02,.01,.47,1);transition:all .5s cubic-bezier(.02,.01,.47,1);-webkit-transform:scale(1.1) translateZ(0);transform:scale(1.1) translateZ(0)}.bttn-pill:focus:before,.bttn-pill:hover:before{opacity:.15;-webkit-transition:opacity .2s cubic-bezier(.02,.01,.47,1),-webkit-transform .2s cubic-bezier(.02,.01,.47,1);transition:opacity .2s cubic-bezier(.02,.01,.47,1),-webkit-transform .2s cubic-bezier(.02,.01,.47,1);transition:transform .2s cubic-bezier(.02,.01,.47,1),opacity .2s cubic-bezier(.02,.01,.47,1);transition:transform .2s cubic-bezier(.02,.01,.47,1),opacity .2s cubic-bezier(.02,.01,.47,1),-webkit-transform .2s cubic-bezier(.02,.01,.47,1);-webkit-transform:translate3d(50%,0,0) scale(.9);transform:translate3d(50%,0,0) scale(.9)}.bttn-pill:focus:after,.bttn-pill:hover:after{opacity:.25;-webkit-transition:opacity .2s cubic-bezier(.02,.01,.47,1) .05s,-webkit-transform .2s cubic-bezier(.02,.01,.47,1) .05s;transition:opacity .2s cubic-bezier(.02,.01,.47,1) .05s,-webkit-transform .2s cubic-bezier(.02,.01,.47,1) .05s;transition:transform .2s cubic-bezier(.02,.01,.47,1) .05s,opacity .2s cubic-bezier(.02,.01,.47,1) .05s;transition:transform .2s cubic-bezier(.02,.01,.47,1) .05s,opacity .2s cubic-bezier(.02,.01,.47,1) .05s,-webkit-transform .2s cubic-bezier(.02,.01,.47,1) .05s;-webkit-transform:translate(50%) scale(1.1);transform:translate(50%) scale(1.1)}.bttn-pill.bttn-xs{padding:3px 8px;font-size:12px;font-family:inherit}.bttn-pill.bttn-xs:focus,.bttn-pill.bttn-xs:hover{box-shadow:0 1px 4px rgba(58,51,53,.3)}.bttn-pill.bttn-sm{padding:4px 10px;font-size:16px;font-family:inherit}.bttn-pill.bttn-sm:focus,.bttn-pill.bttn-sm:hover{box-shadow:0 1px 6px rgba(58,51,53,.3)}.bttn-pill.bttn-md{font-size:20px;font-family:inherit;padding:5px 12px}.bttn-pill.bttn-md:focus,.bttn-pill.bttn-md:hover{box-shadow:0 1px 8px rgba(58,51,53,.3)}.bttn-pill.bttn-lg{padding:8px 15px;font-size:24px;font-family:inherit}.bttn-pill.bttn-lg:focus,.bttn-pill.bttn-lg:hover{box-shadow:0 1px 10px rgba(58,51,53,.3)}.bttn-pill.bttn-default{background:#fff;color:#1d89ff}.bttn-pill.bttn-default:focus,.bttn-pill.bttn-default:hover{color:#1d89ff}.bttn-pill.bttn-default:after,.bttn-pill.bttn-default:before{background:#1d89ff}.bttn-pill.bttn-primary{background:#1d89ff;color:#fff}.bttn-pill.bttn-primary:focus,.bttn-pill.bttn-primary:hover{color:#fff}.bttn-pill.bttn-primary:after,.bttn-pill.bttn-primary:before{background:#fff}.bttn-pill.bttn-warning{background:#feab3a;color:#fff}.bttn-pill.bttn-warning:focus,.bttn-pill.bttn-warning:hover{color:#fff}.bttn-pill.bttn-warning:after,.bttn-pill.bttn-warning:before{background:#fff}.bttn-pill.bttn-danger{background:#ff5964;color:#fff}.bttn-pill.bttn-danger:focus,.bttn-pill.bttn-danger:hover{color:#fff}.bttn-pill.bttn-danger:after,.bttn-pill.bttn-danger:before{background:#fff}.bttn-pill.bttn-success{background:#28b78d;color:#fff}.bttn-pill.bttn-success:focus,.bttn-pill.bttn-success:hover{color:#fff}.bttn-pill.bttn-success:after,.bttn-pill.bttn-success:before{background:#fff}.bttn-pill.bttn-royal{background:#bd2df5;color:#fff}.bttn-pill.bttn-royal:focus,.bttn-pill.bttn-royal:hover{color:#fff}.bttn-pill.bttn-royal:after,.bttn-pill.bttn-royal:before{background:#fff}.bttn-float{margin:0;padding:0;border-width:0;border-color:transparent;background:transparent;font-weight:400;cursor:pointer;position:relative;font-size:20px;font-family:inherit;padding:5px 12px;overflow:hidden;border:1px dotted #fff;border-radius:4px;background:hsla(0,0%,100%,.4);color:#fff;-webkit-transition:opacity .3s cubic-bezier(.02,.01,.47,1),box-shadow .2s cubic-bezier(.02,.01,.47,1),-webkit-transform .3s cubic-bezier(.02,.01,.47,1);transition:opacity .3s cubic-bezier(.02,.01,.47,1),box-shadow .2s cubic-bezier(.02,.01,.47,1),-webkit-transform .3s cubic-bezier(.02,.01,.47,1);transition:transform .3s cubic-bezier(.02,.01,.47,1),opacity .3s cubic-bezier(.02,.01,.47,1),box-shadow .2s cubic-bezier(.02,.01,.47,1);transition:transform .3s cubic-bezier(.02,.01,.47,1),opacity .3s cubic-bezier(.02,.01,.47,1),box-shadow .2s cubic-bezier(.02,.01,.47,1),-webkit-transform .3s cubic-bezier(.02,.01,.47,1)}.bttn-float:focus,.bttn-float:hover{box-shadow:0 30px 30px rgba(0,0,0,.16);opacity:.85;-webkit-transition:opacity .2s cubic-bezier(.02,.01,.47,1),box-shadow .4s cubic-bezier(.02,.01,.47,1),-webkit-transform .2s cubic-bezier(.02,.01,.47,1);transition:opacity .2s cubic-bezier(.02,.01,.47,1),box-shadow .4s cubic-bezier(.02,.01,.47,1),-webkit-transform .2s cubic-bezier(.02,.01,.47,1);transition:transform .2s cubic-bezier(.02,.01,.47,1),opacity .2s cubic-bezier(.02,.01,.47,1),box-shadow .4s cubic-bezier(.02,.01,.47,1);transition:transform .2s cubic-bezier(.02,.01,.47,1),opacity .2s cubic-bezier(.02,.01,.47,1),box-shadow .4s cubic-bezier(.02,.01,.47,1),-webkit-transform .2s cubic-bezier(.02,.01,.47,1)}.bttn-float.bttn-xs{padding:3px 8px;font-size:12px;font-family:inherit}.bttn-float.bttn-xs:focus,.bttn-float.bttn-xs:hover{-webkit-transform:translateY(-6px);transform:translateY(-6px)}.bttn-float.bttn-sm{padding:4px 10px;font-size:16px;font-family:inherit}.bttn-float.bttn-sm:focus,.bttn-float.bttn-sm:hover{-webkit-transform:translateY(-8px);transform:translateY(-8px)}.bttn-float.bttn-md{font-size:20px;font-family:inherit;padding:5px 12px}.bttn-float.bttn-md:focus,.bttn-float.bttn-md:hover{-webkit-transform:translateY(-10px);transform:translateY(-10px)}.bttn-float.bttn-lg{padding:8px 15px;font-size:24px;font-family:inherit}.bttn-float.bttn-lg:focus,.bttn-float.bttn-lg:hover{-webkit-transform:translateY(-12px);transform:translateY(-12px)}.bttn-float.bttn-default{border-color:#fff;background:hsla(0,0%,100%,.4);color:#fff}.bttn-float.bttn-primary{border-color:#1d89ff;background:rgba(29,137,255,.4);color:#1d89ff}.bttn-float.bttn-warning{border-color:#feab3a;background:rgba(254,171,58,.4);color:#feab3a}.bttn-float.bttn-danger{border-color:#ff5964;background:rgba(255,89,100,.4);color:#ff5964}.bttn-float.bttn-success{border-color:#28b78d;background:rgba(40,183,141,.4);color:#28b78d}.bttn-float.bttn-royal{border-color:#bd2df5;background:rgba(189,45,245,.4);color:#bd2df5}.bttn-unite{margin:0;padding:0;border-width:0;border-color:transparent;background:transparent;font-weight:400;cursor:pointer;position:relative;font-size:20px;font-family:inherit;padding:5px 12px;z-index:0;overflow:hidden;border:1px solid #1d89ff;border-radius:100px;background:#fff;color:#1d89ff;-webkit-transition:color .3s cubic-bezier(.02,.01,.47,1),border-color .3s cubic-bezier(.02,.01,.47,1);transition:color .3s cubic-bezier(.02,.01,.47,1),border-color .3s cubic-bezier(.02,.01,.47,1)}.bttn-unite:before{background:#d6e3ff;-webkit-transform:translate3d(-110%,-10%,0) skewX(-20deg);transform:translate3d(-110%,-10%,0) skewX(-20deg)}.bttn-unite:after,.bttn-unite:before{position:absolute;top:0;left:0;width:100%;height:120%;content:'';opacity:0;z-index:-1;-webkit-transition:opacity .15s cubic-bezier(.02,.01,.47,1),-webkit-transform .15s cubic-bezier(.02,.01,.47,1);transition:opacity .15s cubic-bezier(.02,.01,.47,1),-webkit-transform .15s cubic-bezier(.02,.01,.47,1);transition:transform .15s cubic-bezier(.02,.01,.47,1),opacity .15s cubic-bezier(.02,.01,.47,1);transition:transform .15s cubic-bezier(.02,.01,.47,1),opacity .15s cubic-bezier(.02,.01,.47,1),-webkit-transform .15s cubic-bezier(.02,.01,.47,1)}.bttn-unite:after{background:rgba(214,227,255,.7);-webkit-transform:translate3d(110%,-10%,0) skewX(-20deg);transform:translate3d(110%,-10%,0) skewX(-20deg)}.bttn-unite:focus,.bttn-unite:hover{box-shadow:0 1px 8px rgba(58,51,53,.3);color:#1d89ff;-webkit-transition:all .5s cubic-bezier(.02,.01,.47,1);transition:all .5s cubic-bezier(.02,.01,.47,1)}.bttn-unite:focus:before,.bttn-unite:hover:before{-webkit-transform:translate3d(-50%,-10%,0) skewX(-20deg);transform:translate3d(-50%,-10%,0) skewX(-20deg)}.bttn-unite:focus:after,.bttn-unite:focus:before,.bttn-unite:hover:after,.bttn-unite:hover:before{opacity:1;-webkit-transition:opacity .25s cubic-bezier(.02,.01,.47,1),-webkit-transform .25s cubic-bezier(.02,.01,.47,1);transition:opacity .25s cubic-bezier(.02,.01,.47,1),-webkit-transform .25s cubic-bezier(.02,.01,.47,1);transition:transform .25s cubic-bezier(.02,.01,.47,1),opacity .25s cubic-bezier(.02,.01,.47,1);transition:transform .25s cubic-bezier(.02,.01,.47,1),opacity .25s cubic-bezier(.02,.01,.47,1),-webkit-transform .25s cubic-bezier(.02,.01,.47,1)}.bttn-unite:focus:after,.bttn-unite:hover:after{-webkit-transform:translate3d(50%,-10%,0) skewX(-20deg);transform:translate3d(50%,-10%,0) skewX(-20deg)}.bttn-unite.bttn-xs{padding:3px 8px;font-size:12px;font-family:inherit}.bttn-unite.bttn-xs:focus,.bttn-unite.bttn-xs:hover{box-shadow:0 1px 4px rgba(58,51,53,.3)}.bttn-unite.bttn-sm{padding:4px 10px;font-size:16px;font-family:inherit}.bttn-unite.bttn-sm:focus,.bttn-unite.bttn-sm:hover{box-shadow:0 1px 6px rgba(58,51,53,.3)}.bttn-unite.bttn-md{font-size:20px;font-family:inherit;padding:5px 12px}.bttn-unite.bttn-md:focus,.bttn-unite.bttn-md:hover{box-shadow:0 1px 8px rgba(58,51,53,.3)}.bttn-unite.bttn-lg{padding:8px 15px;font-size:24px;font-family:inherit}.bttn-unite.bttn-lg:focus,.bttn-unite.bttn-lg:hover{box-shadow:0 1px 10px rgba(58,51,53,.3)}.bttn-unite.bttn-default{border-color:#1d89ff;color:#1d89ff}.bttn-unite.bttn-default:focus,.bttn-unite.bttn-default:hover{background:#d6e3ff;color:#1d89ff}.bttn-unite.bttn-default:before{background:#a7c3ff}.bttn-unite.bttn-default:after{background:#d6e3ff}.bttn-unite.bttn-primary{border-color:#1d89ff;color:#1d89ff}.bttn-unite.bttn-primary:focus,.bttn-unite.bttn-primary:hover{background:#1d89ff;color:#fff}.bttn-unite.bttn-primary:before{background:#006de3}.bttn-unite.bttn-primary:after{background:#1d89ff}.bttn-unite.bttn-warning{border-color:#feab3a;color:#feab3a}.bttn-unite.bttn-warning:focus,.bttn-unite.bttn-warning:hover{background:#feab3a;color:#fff}.bttn-unite.bttn-warning:before{background:#f89001}.bttn-unite.bttn-warning:after{background:#feab3a}.bttn-unite.bttn-danger{border-color:#ff5964;color:#ff5964}.bttn-unite.bttn-danger:focus,.bttn-unite.bttn-danger:hover{background:#ff5964;color:#fff}.bttn-unite.bttn-danger:before{background:#ff1424}.bttn-unite.bttn-danger:after{background:#ff5964}.bttn-unite.bttn-success{border-color:#28b78d;color:#28b78d}.bttn-unite.bttn-success:focus,.bttn-unite.bttn-success:hover{background:#28b78d;color:#fff}.bttn-unite.bttn-success:before{background:#209271}.bttn-unite.bttn-success:after{background:#28b78d}.bttn-unite.bttn-royal{border-color:#bd2df5;color:#bd2df5}.bttn-unite.bttn-royal:focus,.bttn-unite.bttn-royal:hover{background:#bd2df5;color:#fff}.bttn-unite.bttn-royal:before{background:#a20bdd}.bttn-unite.bttn-royal:after{background:#bd2df5}.bttn-slant{margin:0;padding:0;border-width:0;border-color:transparent;font-weight:400;cursor:pointer;position:relative;font-size:20px;font-family:inherit;padding:5px 12px;z-index:0;border:none;border-radius:0;background:transparent;color:#1d89ff;-webkit-transition:color .3s cubic-bezier(.02,.01,.47,1),-webkit-transform .3s cubic-bezier(.02,.01,.47,1);transition:color .3s cubic-bezier(.02,.01,.47,1),-webkit-transform .3s cubic-bezier(.02,.01,.47,1);transition:color .3s cubic-bezier(.02,.01,.47,1),transform .3s cubic-bezier(.02,.01,.47,1);transition:color .3s cubic-bezier(.02,.01,.47,1),transform .3s cubic-bezier(.02,.01,.47,1),-webkit-transform .3s cubic-bezier(.02,.01,.47,1)}.bttn-slant:before{width:100%;background:#fafafa;-webkit-transition:box-shadow .2s cubic-bezier(.02,.01,.47,1);transition:box-shadow .2s cubic-bezier(.02,.01,.47,1)}.bttn-slant:after,.bttn-slant:before{position:absolute;top:0;left:0;z-index:-1;height:100%;content:'';-webkit-transform:skewX(20deg);transform:skewX(20deg)}.bttn-slant:after{width:0;background:hsla(0,0%,98%,.3);opacity:0;-webkit-transition:opacity .2s cubic-bezier(.02,.01,.47,1),width .15s cubic-bezier(.02,.01,.47,1);transition:opacity .2s cubic-bezier(.02,.01,.47,1),width .15s cubic-bezier(.02,.01,.47,1)}.bttn-slant:focus,.bttn-slant:hover{-webkit-transform:translateX(5px);transform:translateX(5px)}.bttn-slant:focus:after,.bttn-slant:hover:after{width:5px;opacity:1}.bttn-slant:focus:before,.bttn-slant:hover:before{box-shadow:inset 0 -1px 0 #a7c3ff,inset 0 1px 0 #a7c3ff,inset -1px 0 0 #a7c3ff}.bttn-slant.bttn-xs{padding:3px 8px;font-size:12px;font-family:inherit}.bttn-slant.bttn-sm{padding:4px 10px;font-size:16px;font-family:inherit}.bttn-slant.bttn-md{font-size:20px;font-family:inherit;padding:5px 12px}.bttn-slant.bttn-lg{padding:8px 15px;font-size:24px;font-family:inherit}.bttn-slant.bttn-default{color:#1d89ff}.bttn-slant.bttn-default:focus:before,.bttn-slant.bttn-default:hover:before{box-shadow:inset 0 -1px 0 #a7c3ff,inset 0 1px 0 #a7c3ff,inset -1px 0 0 #a7c3ff}.bttn-slant.bttn-default:before{background:#fff}.bttn-slant.bttn-default:after{background:#a7c3ff}.bttn-slant.bttn-primary{color:#fff}.bttn-slant.bttn-primary:focus:before,.bttn-slant.bttn-primary:hover:before{box-shadow:inset 0 -1px 0 #006de3,inset 0 1px 0 #006de3,inset -1px 0 0 #006de3}.bttn-slant.bttn-primary:before{background:#1d89ff}.bttn-slant.bttn-primary:after{background:#006de3}.bttn-slant.bttn-warning{color:#fff}.bttn-slant.bttn-warning:focus:before,.bttn-slant.bttn-warning:hover:before{box-shadow:inset 0 -1px 0 #f89001,inset 0 1px 0 #f89001,inset -1px 0 0 #f89001}.bttn-slant.bttn-warning:before{background:#feab3a}.bttn-slant.bttn-warning:after{background:#f89001}.bttn-slant.bttn-danger{color:#fff}.bttn-slant.bttn-danger:focus:before,.bttn-slant.bttn-danger:hover:before{box-shadow:inset 0 -1px 0 #ff1424,inset 0 1px 0 #ff1424,inset -1px 0 0 #ff1424}.bttn-slant.bttn-danger:before{background:#ff5964}.bttn-slant.bttn-danger:after{background:#ff1424}.bttn-slant.bttn-success{color:#fff}.bttn-slant.bttn-success:focus:before,.bttn-slant.bttn-success:hover:before{box-shadow:inset 0 -1px 0 #209271,inset 0 1px 0 #209271,inset -1px 0 0 #209271}.bttn-slant.bttn-success:before{background:#28b78d}.bttn-slant.bttn-success:after{background:#209271}.bttn-slant.bttn-royal{color:#fff}.bttn-slant.bttn-royal:focus:before,.bttn-slant.bttn-royal:hover:before{box-shadow:inset 0 -1px 0 #a20bdd,inset 0 1px 0 #a20bdd,inset -1px 0 0 #a20bdd}.bttn-slant.bttn-royal:before{background:#bd2df5}.bttn-slant.bttn-royal:after{background:#a20bdd}.bttn-block{display:block;width:100%}.bttn-no-outline,.bttn-no-outline:active,.bttn-no-outline:focus,.bttn-no-outline:hover{outline:none}

```

### `static/css/codemirror.css`

```css
/* BASICS */

.CodeMirror {
  /* Set height, width, borders, and global font properties here */
  font-family: monospace;
  height: 300px;
  color: black;
  direction: ltr;
}

/* PADDING */

.CodeMirror-lines {
  padding: 4px 0; /* Vertical padding around content */
}
.CodeMirror pre {
  padding: 0 4px; /* Horizontal padding of content */
}

.CodeMirror-scrollbar-filler, .CodeMirror-gutter-filler {
  background-color: white; /* The little square between H and V scrollbars */
}

/* GUTTER */

.CodeMirror-gutters {
  border-right: 1px solid #ddd;
  background-color: #f7f7f7;
  white-space: nowrap;
}
.CodeMirror-linenumbers {}
.CodeMirror-linenumber {
  padding: 0 3px 0 5px;
  min-width: 20px;
  text-align: right;
  color: #999;
  white-space: nowrap;
}

.CodeMirror-guttermarker { color: black; }
.CodeMirror-guttermarker-subtle { color: #999; }

/* CURSOR */

.CodeMirror-cursor {
  border-left: 1px solid black;
  border-right: none;
  width: 0;
}
/* Shown when moving in bi-directional text */
.CodeMirror div.CodeMirror-secondarycursor {
  border-left: 1px solid silver;
}
.cm-fat-cursor .CodeMirror-cursor {
  width: auto;
  border: 0 !important;
  background: #7e7;
}
.cm-fat-cursor div.CodeMirror-cursors {
  z-index: 1;
}
.cm-fat-cursor-mark {
  background-color: rgba(20, 255, 20, 0.5);
  -webkit-animation: blink 1.06s steps(1) infinite;
  -moz-animation: blink 1.06s steps(1) infinite;
  animation: blink 1.06s steps(1) infinite;
}
.cm-animate-fat-cursor {
  width: auto;
  border: 0;
  -webkit-animation: blink 1.06s steps(1) infinite;
  -moz-animation: blink 1.06s steps(1) infinite;
  animation: blink 1.06s steps(1) infinite;
  background-color: #7e7;
}
@-moz-keyframes blink {
  0% {}
  50% { background-color: transparent; }
  100% {}
}
@-webkit-keyframes blink {
  0% {}
  50% { background-color: transparent; }
  100% {}
}
@keyframes blink {
  0% {}
  50% { background-color: transparent; }
  100% {}
}

/* Can style cursor different in overwrite (non-insert) mode */
.CodeMirror-overwrite .CodeMirror-cursor {}

.cm-tab { display: inline-block; text-decoration: inherit; }

.CodeMirror-rulers {
  position: absolute;
  left: 0; right: 0; top: -50px; bottom: -20px;
  overflow: hidden;
}
.CodeMirror-ruler {
  border-left: 1px solid #ccc;
  top: 0; bottom: 0;
  position: absolute;
}

/* DEFAULT THEME */

.cm-s-default .cm-header {color: blue;}
.cm-s-default .cm-quote {color: #090;}
.cm-negative {color: #d44;}
.cm-positive {color: #292;}
.cm-header, .cm-strong {font-weight: bold;}
.cm-em {font-style: italic;}
.cm-link {text-decoration: underline;}
.cm-strikethrough {text-decoration: line-through;}

.cm-s-default .cm-keyword {color: #708;}
.cm-s-default .cm-atom {color: #219;}
.cm-s-default .cm-number {color: #164;}
.cm-s-default .cm-def {color: #00f;}
.cm-s-default .cm-variable,
.cm-s-default .cm-punctuation,
.cm-s-default .cm-property,
.cm-s-default .cm-operator {}
.cm-s-default .cm-variable-2 {color: #05a;}
.cm-s-default .cm-variable-3, .cm-s-default .cm-type {color: #085;}
.cm-s-default .cm-comment {color: #a50;}
.cm-s-default .cm-string {color: #a11;}
.cm-s-default .cm-string-2 {color: #f50;}
.cm-s-default .cm-meta {color: #555;}
.cm-s-default .cm-qualifier {color: #555;}
.cm-s-default .cm-builtin {color: #30a;}
.cm-s-default .cm-bracket {color: #997;}
.cm-s-default .cm-tag {color: #170;}
.cm-s-default .cm-attribute {color: #00c;}
.cm-s-default .cm-hr {color: #999;}
.cm-s-default .cm-link {color: #00c;}

.cm-s-default .cm-error {color: #f00;}
.cm-invalidchar {color: #f00;}

.CodeMirror-composing { border-bottom: 2px solid; }

/* Default styles for common addons */

div.CodeMirror span.CodeMirror-matchingbracket {color: #0b0;}
div.CodeMirror span.CodeMirror-nonmatchingbracket {color: #a22;}
.CodeMirror-matchingtag { background: rgba(255, 150, 0, .3); }
.CodeMirror-activeline-background {background: #e8f2ff;}

/* STOP */

/* The rest of this file contains styles related to the mechanics of
   the editor. You probably shouldn't touch them. */

.CodeMirror {
  position: relative;
  overflow: hidden;
  background: white;
}

.CodeMirror-scroll {
  overflow: scroll !important; /* Things will break if this is overridden */
  /* 30px is the magic margin used to hide the element's real scrollbars */
  /* See overflow: hidden in .CodeMirror */
  margin-bottom: -30px; margin-right: -30px;
  padding-bottom: 30px;
  height: 100%;
  outline: none; /* Prevent dragging from highlighting the element */
  position: relative;
}
.CodeMirror-sizer {
  position: relative;
  border-right: 30px solid transparent;
}

/* The fake, visible scrollbars. Used to force redraw during scrolling
   before actual scrolling happens, thus preventing shaking and
   flickering artifacts. */
.CodeMirror-vscrollbar, .CodeMirror-hscrollbar, .CodeMirror-scrollbar-filler, .CodeMirror-gutter-filler {
  position: absolute;
  z-index: 6;
  display: none;
}
.CodeMirror-vscrollbar {
  right: 0; top: 0;
  overflow-x: hidden;
  overflow-y: scroll;
}
.CodeMirror-hscrollbar {
  bottom: 0; left: 0;
  overflow-y: hidden;
  overflow-x: scroll;
}
.CodeMirror-scrollbar-filler {
  right: 0; bottom: 0;
}
.CodeMirror-gutter-filler {
  left: 0; bottom: 0;
}

.CodeMirror-gutters {
  position: absolute; left: 0; top: 0;
  min-height: 100%;
  z-index: 3;
}
.CodeMirror-gutter {
  white-space: normal;
  height: 100%;
  display: inline-block;
  vertical-align: top;
  margin-bottom: -30px;
}
.CodeMirror-gutter-wrapper {
  position: absolute;
  z-index: 4;
  background: none !important;
  border: none !important;
}
.CodeMirror-gutter-background {
  position: absolute;
  top: 0; bottom: 0;
  z-index: 4;
}
.CodeMirror-gutter-elt {
  position: absolute;
  cursor: default;
  z-index: 4;
}
.CodeMirror-gutter-wrapper ::selection { background-color: transparent }
.CodeMirror-gutter-wrapper ::-moz-selection { background-color: transparent }

.CodeMirror-lines {
  cursor: text;
  min-height: 1px; /* prevents collapsing before first draw */
}
.CodeMirror pre {
  /* Reset some styles that the rest of the page might have set */
  -moz-border-radius: 0; -webkit-border-radius: 0; border-radius: 0;
  border-width: 0;
  background: transparent;
  font-family: inherit;
  font-size: inherit;
  margin: 0;
  white-space: pre;
  word-wrap: normal;
  line-height: inherit;
  color: inherit;
  z-index: 2;
  position: relative;
  overflow: visible;
  -webkit-tap-highlight-color: transparent;
  -webkit-font-variant-ligatures: contextual;
  font-variant-ligatures: contextual;
}
.CodeMirror-wrap pre {
  word-wrap: break-word;
  white-space: pre-wrap;
  word-break: normal;
}

.CodeMirror-linebackground {
  position: absolute;
  left: 0; right: 0; top: 0; bottom: 0;
  z-index: 0;
}

.CodeMirror-linewidget {
  position: relative;
  z-index: 2;
  padding: 0.1px; /* Force widget margins to stay inside of the container */
}

.CodeMirror-widget {}

.CodeMirror-rtl pre { direction: rtl; }

.CodeMirror-code {
  outline: none;
}

/* Force content-box sizing for the elements where we expect it */
.CodeMirror-scroll,
.CodeMirror-sizer,
.CodeMirror-gutter,
.CodeMirror-gutters,
.CodeMirror-linenumber {
  -moz-box-sizing: content-box;
  box-sizing: content-box;
}

.CodeMirror-measure {
  position: absolute;
  width: 100%;
  height: 0;
  overflow: hidden;
  visibility: hidden;
}

.CodeMirror-cursor {
  position: absolute;
  pointer-events: none;
}
.CodeMirror-measure pre { position: static; }

div.CodeMirror-cursors {
  visibility: hidden;
  position: relative;
  z-index: 3;
}
div.CodeMirror-dragcursors {
  visibility: visible;
}

.CodeMirror-focused div.CodeMirror-cursors {
  visibility: visible;
}

.CodeMirror-selected { background: #d9d9d9; }
.CodeMirror-focused .CodeMirror-selected { background: #d7d4f0; }
.CodeMirror-crosshair { cursor: crosshair; }
.CodeMirror-line::selection, .CodeMirror-line > span::selection, .CodeMirror-line > span > span::selection { background: #d7d4f0; }
.CodeMirror-line::-moz-selection, .CodeMirror-line > span::-moz-selection, .CodeMirror-line > span > span::-moz-selection { background: #d7d4f0; }

.cm-searching {
  background-color: #ffa;
  background-color: rgba(255, 255, 0, .4);
}

/* Used to force a border model for a node */
.cm-force-border { padding-right: .1px; }

@media print {
  /* Hide the cursor when printing */
  .CodeMirror div.CodeMirror-cursors {
    visibility: hidden;
  }
}

/* See issue #2901 */
.cm-tab-wrap-hack:after { content: ''; }

/* Help users use markselection to safely style text background */
span.CodeMirror-selectedtext { background: none; }

```

### `static/css/material.css`

```css
/*

    Name:       material
    Author:     Michael Kaminsky (http://github.com/mkaminsky11)

    Original material color scheme by Mattia Astorino (https://github.com/equinusocio/material-theme)

*/

.cm-s-material.CodeMirror {
  background-color: #263238;
  color: rgba(233, 237, 237, 1);
}
.cm-s-material .CodeMirror-gutters {
  background: #263238;
  color: rgb(83,127,126);
  border: none;
}
.cm-s-material .CodeMirror-guttermarker, .cm-s-material .CodeMirror-guttermarker-subtle, .cm-s-material .CodeMirror-linenumber { color: rgb(83,127,126); }
.cm-s-material .CodeMirror-cursor { border-left: 1px solid #f8f8f0; }
.cm-s-material div.CodeMirror-selected { background: rgba(255, 255, 255, 0.15); }
.cm-s-material.CodeMirror-focused div.CodeMirror-selected { background: rgba(255, 255, 255, 0.10); }
.cm-s-material .CodeMirror-line::selection, .cm-s-material .CodeMirror-line > span::selection, .cm-s-material .CodeMirror-line > span > span::selection { background: rgba(255, 255, 255, 0.10); }
.cm-s-material .CodeMirror-line::-moz-selection, .cm-s-material .CodeMirror-line > span::-moz-selection, .cm-s-material .CodeMirror-line > span > span::-moz-selection { background: rgba(255, 255, 255, 0.10); }

.cm-s-material .CodeMirror-activeline-background { background: rgba(0, 0, 0, 0); }
.cm-s-material .cm-keyword { color: rgba(199, 146, 234, 1); }
.cm-s-material .cm-operator { color: rgba(233, 237, 237, 1); }
.cm-s-material .cm-variable-2 { color: #80CBC4; }
.cm-s-material .cm-variable-3, .cm-s-material .cm-type { color: #82B1FF; }
.cm-s-material .cm-builtin { color: #DECB6B; }
.cm-s-material .cm-atom { color: #F77669; }
.cm-s-material .cm-number { color: #F77669; }
.cm-s-material .cm-def { color: rgba(233, 237, 237, 1); }
.cm-s-material .cm-string { color: #C3E88D; }
.cm-s-material .cm-string-2 { color: #80CBC4; }
.cm-s-material .cm-comment { color: #546E7A; }
.cm-s-material .cm-variable { color: #82B1FF; }
.cm-s-material .cm-tag { color: #80CBC4; }
.cm-s-material .cm-meta { color: #80CBC4; }
.cm-s-material .cm-attribute { color: #FFCB6B; }
.cm-s-material .cm-property { color: #80CBAE; }
.cm-s-material .cm-qualifier { color: #DECB6B; }
.cm-s-material .cm-variable-3, .cm-s-material .cm-type { color: #DECB6B; }
.cm-s-material .cm-tag { color: rgba(255, 83, 112, 1); }
.cm-s-material .cm-error {
  color: rgba(255, 255, 255, 1.0);
  background-color: #EC5F67;
}
.cm-s-material .CodeMirror-matchingbracket {
  text-decoration: underline;
  color: white !important;
}

```

### `static/css/hint.min.css`

```css
/*! Hint.css - v2.6.0 - 2019-04-27
* http://kushagragour.in/lab/hint/
* Copyright (c) 2019 Kushagra Gour */

[class*=hint--]{position:relative;display:inline-block;color: #a9a9a9;text-transform: none;font-weight: normal;letter-spacing: normal;font-size: inherit;}[class*=hint--]:after,[class*=hint--]:before{position:absolute;-webkit-transform:translate3d(0,0,0);-moz-transform:translate3d(0,0,0);transform:translate3d(0,0,0);visibility:hidden;opacity:0;z-index:1000000;pointer-events:none;-webkit-transition:.3s ease;-moz-transition:.3s ease;transition:.3s ease;-webkit-transition-delay:0s;-moz-transition-delay:0s;transition-delay:0s}[class*=hint--]:hover:after,[class*=hint--]:hover:before{visibility:visible;opacity:1;-webkit-transition-delay:.1s;-moz-transition-delay:.1s;transition-delay:.1s}[class*=hint--]:before{content:'';position:absolute;background:0 0;border:6px solid transparent;z-index:1000001}[class*=hint--]:after{background: #424250;color:#fff;padding:8px 10px;font-size:12px;font-family:"Helvetica Neue",Helvetica,Arial,sans-serif;line-height:12px;white-space:nowrap;text-shadow:0 -1px 0 #000;box-shadow: 0px 0px 4px 1px #0000007a;}[class*=hint--][aria-label]:after{content:attr(aria-label)}[class*=hint--][data-hint]:after{content:attr(data-hint)}[aria-label='']:after,[aria-label='']:before,[data-hint='']:after,[data-hint='']:before{display:none!important}.hint--top-left:before,.hint--top-right:before,.hint--top:before{border-top-color:#383838}.hint--bottom-left:before,.hint--bottom-right:before,.hint--bottom:before{border-bottom-color: #424250;}.hint--top:after,.hint--top:before{bottom:100%;left:50%}.hint--top:before{margin-bottom:-11px;left:calc(50% - 6px)}.hint--top:after{-webkit-transform:translateX(-50%);-moz-transform:translateX(-50%);transform:translateX(-50%)}.hint--top:hover:before{-webkit-transform:translateY(-8px);-moz-transform:translateY(-8px);transform:translateY(-8px)}.hint--top:hover:after{-webkit-transform:translateX(-50%) translateY(-8px);-moz-transform:translateX(-50%) translateY(-8px);transform:translateX(-50%) translateY(-8px)}.hint--bottom:after,.hint--bottom:before{top:100%;left:50%}.hint--bottom:before{margin-top:-11px;left:calc(50% - 6px)}.hint--bottom:after{-webkit-transform:translateX(-50%);-moz-transform:translateX(-50%);transform:translateX(-50%)}.hint--bottom:hover:before{-webkit-transform:translateY(8px);-moz-transform:translateY(8px);transform:translateY(8px)}.hint--bottom:hover:after{-webkit-transform:translateX(-50%) translateY(8px);-moz-transform:translateX(-50%) translateY(8px);transform:translateX(-50%) translateY(8px)}.hint--right:before{border-right-color:#383838;margin-left:-11px;margin-bottom:-6px}.hint--right:after{margin-bottom:-14px}.hint--right:after,.hint--right:before{left:100%;bottom:50%}.hint--right:hover:after,.hint--right:hover:before{-webkit-transform:translateX(8px);-moz-transform:translateX(8px);transform:translateX(8px)}.hint--left:before{border-left-color:#383838;margin-right:-11px;margin-bottom:-6px}.hint--left:after{margin-bottom:-14px}.hint--left:after,.hint--left:before{right:100%;bottom:50%}.hint--left:hover:after,.hint--left:hover:before{-webkit-transform:translateX(-8px);-moz-transform:translateX(-8px);transform:translateX(-8px)}.hint--top-left:after,.hint--top-left:before{bottom:100%;left:50%}.hint--top-left:before{margin-bottom:-11px;left:calc(50% - 6px)}.hint--top-left:after{-webkit-transform:translateX(-100%);-moz-transform:translateX(-100%);transform:translateX(-100%);margin-left:12px}.hint--top-left:hover:before{-webkit-transform:translateY(-8px);-moz-transform:translateY(-8px);transform:translateY(-8px)}.hint--top-left:hover:after{-webkit-transform:translateX(-100%) translateY(-8px);-moz-transform:translateX(-100%) translateY(-8px);transform:translateX(-100%) translateY(-8px)}.hint--top-right:after,.hint--top-right:before{bottom:100%;left:50%}.hint--top-right:before{margin-bottom:-11px;left:calc(50% - 6px)}.hint--top-right:after{-webkit-transform:translateX(0);-moz-transform:translateX(0);transform:translateX(0);margin-left:-12px}.hint--top-right:hover:after,.hint--top-right:hover:before{-webkit-transform:translateY(-8px);-moz-transform:translateY(-8px);transform:translateY(-8px)}.hint--bottom-left:after,.hint--bottom-left:before{top:100%;left:50%}.hint--bottom-left:before{margin-top:-11px;left:calc(50% - 6px)}.hint--bottom-left:after{-webkit-transform:translateX(-100%);-moz-transform:translateX(-100%);transform:translateX(-100%);margin-left:12px}.hint--bottom-left:hover:before{-webkit-transform:translateY(8px);-moz-transform:translateY(8px);transform:translateY(8px)}.hint--bottom-left:hover:after{-webkit-transform:translateX(-100%) translateY(8px);-moz-transform:translateX(-100%) translateY(8px);transform:translateX(-100%) translateY(8px)}.hint--bottom-right:after,.hint--bottom-right:before{top:100%;left:50%}.hint--bottom-right:before{margin-top:-11px;left:calc(50% - 6px)}.hint--bottom-right:after{-webkit-transform:translateX(0);-moz-transform:translateX(0);transform:translateX(0);margin-left:-12px}.hint--bottom-right:hover:after,.hint--bottom-right:hover:before{-webkit-transform:translateY(8px);-moz-transform:translateY(8px);transform:translateY(8px)}.hint--large:after,.hint--medium:after,.hint--small:after{white-space:normal;line-height:1.4em;word-wrap:break-word}.hint--small:after{width:80px}.hint--medium:after{width:150px}.hint--large:after{width:300px}.hint--error:after{background-color:#b34e4d;text-shadow:0 -1px 0 #592726}.hint--error.hint--top-left:before,.hint--error.hint--top-right:before,.hint--error.hint--top:before{border-top-color:#b34e4d}.hint--error.hint--bottom-left:before,.hint--error.hint--bottom-right:before,.hint--error.hint--bottom:before{border-bottom-color:#b34e4d}.hint--error.hint--left:before{border-left-color:#b34e4d}.hint--error.hint--right:before{border-right-color:#b34e4d}.hint--warning:after{background-color:#c09854;text-shadow:0 -1px 0 #6c5328}.hint--warning.hint--top-left:before,.hint--warning.hint--top-right:before,.hint--warning.hint--top:before{border-top-color:#c09854}.hint--warning.hint--bottom-left:before,.hint--warning.hint--bottom-right:before,.hint--warning.hint--bottom:before{border-bottom-color:#c09854}.hint--warning.hint--left:before{border-left-color:#c09854}.hint--warning.hint--right:before{border-right-color:#c09854}.hint--info:after{background-color:#3986ac;text-shadow:0 -1px 0 #1a3c4d}.hint--info.hint--top-left:before,.hint--info.hint--top-right:before,.hint--info.hint--top:before{border-top-color:#3986ac}.hint--info.hint--bottom-left:before,.hint--info.hint--bottom-right:before,.hint--info.hint--bottom:before{border-bottom-color:#3986ac}.hint--info.hint--left:before{border-left-color:#3986ac}.hint--info.hint--right:before{border-right-color:#3986ac}.hint--success:after{background-color:#458746;text-shadow:0 -1px 0 #1a321a}.hint--success.hint--top-left:before,.hint--success.hint--top-right:before,.hint--success.hint--top:before{border-top-color:#458746}.hint--success.hint--bottom-left:before,.hint--success.hint--bottom-right:before,.hint--success.hint--bottom:before{border-bottom-color:#458746}.hint--success.hint--left:before{border-left-color:#458746}.hint--success.hint--right:before{border-right-color:#458746}.hint--always:after,.hint--always:before{opacity:1;visibility:visible}.hint--always.hint--top:before{-webkit-transform:translateY(-8px);-moz-transform:translateY(-8px);transform:translateY(-8px)}.hint--always.hint--top:after{-webkit-transform:translateX(-50%) translateY(-8px);-moz-transform:translateX(-50%) translateY(-8px);transform:translateX(-50%) translateY(-8px)}.hint--always.hint--top-left:before{-webkit-transform:translateY(-8px);-moz-transform:translateY(-8px);transform:translateY(-8px)}.hint--always.hint--top-left:after{-webkit-transform:translateX(-100%) translateY(-8px);-moz-transform:translateX(-100%) translateY(-8px);transform:translateX(-100%) translateY(-8px)}.hint--always.hint--top-right:after,.hint--always.hint--top-right:before{-webkit-transform:translateY(-8px);-moz-transform:translateY(-8px);transform:translateY(-8px)}.hint--always.hint--bottom:before{-webkit-transform:translateY(8px);-moz-transform:translateY(8px);transform:translateY(8px)}.hint--always.hint--bottom:after{-webkit-transform:translateX(-50%) translateY(8px);-moz-transform:translateX(-50%) translateY(8px);transform:translateX(-50%) translateY(8px)}.hint--always.hint--bottom-left:before{-webkit-transform:translateY(8px);-moz-transform:translateY(8px);transform:translateY(8px)}.hint--always.hint--bottom-left:after{-webkit-transform:translateX(-100%) translateY(8px);-moz-transform:translateX(-100%) translateY(8px);transform:translateX(-100%) translateY(8px)}.hint--always.hint--bottom-right:after,.hint--always.hint--bottom-right:before{-webkit-transform:translateY(8px);-moz-transform:translateY(8px);transform:translateY(8px)}.hint--always.hint--left:after,.hint--always.hint--left:before{-webkit-transform:translateX(-8px);-moz-transform:translateX(-8px);transform:translateX(-8px)}.hint--always.hint--right:after,.hint--always.hint--right:before{-webkit-transform:translateX(8px);-moz-transform:translateX(8px);transform:translateX(8px)}.hint--rounded:after{border-radius:4px}.hint--no-animate:after,.hint--no-animate:before{-webkit-transition-duration:0s;-moz-transition-duration:0s;transition-duration:0s}.hint--bounce:after,.hint--bounce:before{-webkit-transition:opacity .3s ease,visibility .3s ease,-webkit-transform .3s cubic-bezier(.71,1.7,.77,1.24);-moz-transition:opacity .3s ease,visibility .3s ease,-moz-transform .3s cubic-bezier(.71,1.7,.77,1.24);transition:opacity .3s ease,visibility .3s ease,transform .3s cubic-bezier(.71,1.7,.77,1.24)}.hint--no-shadow:after,.hint--no-shadow:before{text-shadow:initial;box-shadow:initial}
```

## Javascript

### `static/js/main.js`

```javascript
/* File: main.js */
/**
ExtAnalysis - Browser Extension Analysis Framework
Copyright (C) 2019 - 2022 Tuhinshubhra

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/
var scan_container = document.getElementById("scan-container");
var result_container = document.getElementById("result-container");
var update_container = document.getElementById("update-container");
var about_container = document.getElementById("about-container");
var online_scan_container = document.getElementById("online-scan");
var local_scan_container = document.getElementById("local-scan");
var select_scan_contaienr = document.getElementById("select-scan-type");
var upload_container = document.getElementById("upload-extension");
var webstore_container = document.getElementById("webstore");
var upload_button = document.getElementById("upload-instead");
var upload_box = document.getElementById("upload-contaienr");
var logo = document.getElementById("logo");
var loading_div = document.getElementById("loading");
var elements = $(".modal-overlay, .modal");
$(".close-modal").click(function () {
  elements.removeClass("active");
});
var csrftoken = $("meta[name=csrf-token]").attr("content");

document.getElementById("noscript").style.display = "none";

function showscan() {
  if (scan_container.style.display === "none") {
    $("#container").fadeOut(300);
    $("#result-container").fadeOut(300);
    $("#update-container").fadeOut(300);
    $("#about-container").fadeOut(300);
    $("#container").fadeIn(600);
    $("#scan-container").fadeIn(600);
  }
}

function showabout() {
  if (about_container.style.display === "none") {
    $("#container").fadeOut(300);
    $("#result-container").fadeOut(300);
    $("#update-container").fadeOut(300);
    $("#scan-container").fadeOut(300);
    $("#container").fadeIn(600);
    $("#about-container").fadeIn(600);
  }
}

function showresult() {
  if (result_container.style.display === "none") {
    $("#container").fadeOut(300);
    $("#scan-container").fadeOut(300);
    $("#update-container").fadeOut(300);
    $("#about-container").fadeOut(300);
    $("#container").fadeIn(600);
    $("#result-container").fadeIn(600);
  }
}

function showupdate() {
  if (update_container.style.display === "none") {
    $("#container").fadeOut(300);
    $("#result-container").fadeOut(300);
    $("#scan-container").fadeOut(300);
    $("#about-container").fadeOut(300);
    $("#container").fadeIn(600);
    $("#update-container").fadeIn(600);
  }
}

function loadOnline() {
  select_scan_contaienr.style.display = "none";
  online_scan_container.style.display = "block";
}

function download_and_scan() {
  loading_div.style.display = "block";
  ext_id = document.getElementById("extension-id").value;
  if (ext_id.match(/chrome\.google\.com/)) {
    ext_id = ext_id.split("://")[1].split("/")[4].split("?")[0];
    handle_download(ext_id);
    loading_div.style.display = "none";
  } else if (ext_id === "" || ext_id === " ") {
    swal("Empty Value", "Extension ID value can't be empty!", "warning");
    loading_div.style.display = "none";
  } else {
    handle_download(ext_id);
    loading_div.style.display = "none";
  }
  queryurl = "" + ext_id;
}

function download_and_scan_firefox() {
  ext_id = document.getElementById("firefox-addon").value;
  loading_div.style.display = "block";
  if (ext_id.match(/addons\.mozilla\.org/)) {
    fetch(`/api/?addonurl=${ext_id}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", // otherwise $_POST is empty
        "X-CSRFToken": csrftoken,
      },
      body: "query=firefoxaddon",
    })
      .then((response) => {
        response.text().then((resptxt) => {
          handleresponse(resptxt);
          loading_div.style.display = "none";
        });
      })
      .catch((err) => {
        swal(
          "Error!",
          "Something went wrong! Check logs for more information",
          "error"
        );
        loading_div.style.display = "none";
      });
  } else {
    swal(
      "Invalid URL",
      "Please provide a valid firefox add-on URL!",
      "warning"
    );
    loading_div.style.display = "none";
  }
  queryurl = "" + ext_id;
}

function download_and_scan_edge() {
  ext_id = document.getElementById("edge-addon").value;
  loading_div.style.display = "block";
  if (ext_id.match(/microsoftedge\.microsoft\.com/)) {
    fetch(`/api/?addonurl=${ext_id}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", // otherwise $_POST is empty
        "X-CSRFToken": csrftoken,
      },
      body: "query=edgeaddon",
    })
      .then((response) => {
        response.text().then((resptxt) => {
          handleresponse(resptxt);
          loading_div.style.display = "none";
        });
      })
      .catch((err) => {
        swal(
          "Error!",
          "Something went wrong! Check logs for more information",
          "error"
        );
        loading_div.style.display = "none";
      });
  } else {
    swal("Invalid URL", "Please provide a valid Edge add-on URL!", "warning");
    loading_div.style.display = "none";
  }
  queryurl = "" + ext_id;
}

function handle_download(id) {
  swal({
    text: "Save Extension as (no need to enter file extension):",
    content: "input",
    button: {
      text: "Download & Analyze",
      closeModal: false,
    },
  })
    .then((name) => {
      if (!name) throw null;
      loading_div.style.display = "block";
      return fetch(`/api/?extid=${id}&savedir=${name}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", // otherwise $_POST is empty
          "X-CSRFToken": csrftoken,
        },
        body: "query=dlanalysis",
      });
    })
    .then((results) => {
      return results.text();
    })
    .then((text) => {
      handleresponse(text);
    })
    .catch((err) => {
      if (err) {
        swal("Oh noes!", "The AJAX request failed!", "error");
      } else {
        swal.stopLoading();
        swal.close();
      }
    });
}

function handleresponse(response) {
  button = document.getElementById("modal-content");
  try {
    swal.close();
  } catch {}
  if (response.match(/error: /)) {
    var msg = response.split("error:")[1];
    var inner_html =
      '<center><img src="/static/images/error.png" style="width: 283px; margin: 11px;"><br><h3>' +
      msg +
      "</h3>";
    button.innerHTML = inner_html;
    elements.addClass("active");
    loading_div.style.display = "none";
  } else if (response.match(/Extension analyzed and report saved/)) {
    var anal_id = response.split("report saved under ID: ")[1];
    var rep_href = `<a href='/analysis/${anal_id}' target="_blank" class="start_scan"><i class="fas fa-external-link-alt"></i> View Analysis</a>`;
    var inner_html =
      '<center><img src="/static/images/success.png" style="width: 283px; margin: 11px;"><br><h3>' +
      response +
      "<br><br>" +
      rep_href +
      "</h3>";
    button.innerHTML = inner_html;
    elements.addClass("active");
    loading_div.style.display = "none";
  } else {
    var inner_html =
      '<center><img src="/static/images/success.png" style="width: 283px; margin: 11px;"><br><h3>' +
      response +
      "</h3>";
    button.innerHTML = inner_html;
    elements.addClass("active");
    loading_div.style.display = "none";
  }
}

function upload_extension() {
  loading_div.style.display = "block";
  var formdata = new FormData($("#upload-form")[0]);
  $.ajax({
    url: "/upload/",
    type: "POST",
    headers: {
      "X-CSRFToken": csrftoken,
    },
    data: formdata,
    success: (response) => {
      handleresponse(response);
      loading_div.style.display = "none";
    },
    cache: false,
    contentType: false,
    processData: false,
  });
}

function result() {
  //path = document.getElementById('result_path').value;
  // checkurl = '/api/?query=results';
  fetch("/api/", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", // otherwise $_POST is empty
      "X-CSRFToken": csrftoken,
    },
    body: "query=results",
  }).then((resp) => {
    resp.text().then((txt) => {
      button = document.getElementById("changeme");
      button.innerHTML = txt;
      $("#result-table").DataTable();
    });
  });
  document.getElementById("load_result").innerHTML =
    '<i class="fas fa-sync-alt"></i> Reload Reports';
}

function loadresult(result) {
  checkurl = "/api/?result=" + result;
  fetch(checkurl, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", // otherwise $_POST is empty
      "X-CSRFToken": csrftoken,
    },
    body: "query=showresult",
  }).then((resp) => {
    resp.text().then((txt) => {
      button = document.getElementById("modal-content");
      button.innerHTML = txt;
      elements.addClass("active");
    });
  });
}

var tabs = $(".tabs");
var items = $(".tabs").find("a").length;
var selector = $(".tabs").find(".selector");
var activeItem = tabs.find(".active");
var activeWidth = activeItem.innerWidth();
$(".selector").css({
  left: activeItem.position.left + "px",
  width: activeWidth + "px",
});

$(".tabs").on("click", "a", function (e) {
  e.preventDefault();
  $(".tabs a").removeClass("active");
  $(this).addClass("active");
  var activeWidth = $(this).innerWidth();
  var itemPos = $(this).position();
  $(".selector").css({
    left: itemPos.left + "px",
    width: activeWidth + "px",
  });
});

function showscantype() {
  select_scan_contaienr.style.display = "block";
  online_scan_container.style.display = "none";
  local_scan_container.style.display = "none";
}

var style = document.getElementById("pageStyle");
function getCookie(cname) {
  var name = cname + "=";
  var ca = document.cookie.split(";");
  for (var i = 0; i < ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == " ") {
      c = c.substring(1);
    }
    if (c.indexOf(name) === 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

function checkCookie() {
  var nightmode = getCookie("lights");
  if (nightmode == "off") {
    lightsOff();
  } else {
    lightsOn();
  }
}

function lightsOff() {
  document.cookie = "lights = off;  expires = Fri, 31 Dec 9999 23:59:59 GMT";
  style.setAttribute("href", "/static/css/dark.css");
}

function lightsOn() {
  document.cookie = "lights = on;  expires = Fri, 31 Dec 9999 23:59:59 GMT";
  style.setAttribute("href", "/static/css/style.css");
}

checkCookie();

function view_permission(permission) {
  if (permission === "https:") {
    permission = "https://*/*";
  } else if (permission === "http:") {
    permission = "http://*/*";
  } else if (permission === "*") {
    permission = "*://*/*";
  }

  fetch("/api/?permission=" + permission, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", // otherwise $_POST is empty
      "X-CSRFToken": csrftoken,
    },
    body: "query=permissionInfo",
  })
    .then((response) => {
      response.text().then((reply) => {
        swal("", reply, "info");
      });
    })
    .catch((err) => {
      swal("Error!", "Something went wrong!", "error");
    });
}

function viewResult(id) {
  result_url = "/analysis/" + id;
  window.open(result_url, (target = "_blank"));
}

function deleteResult(id) {
  console.log("delete result " + id);
  swal({
    title: "Delete Result ID: " + id,
    text: "Once deleted, you will not be able to recover the result!",
    icon: "warning",
    buttons: true,
    dangerMode: true,
  }).then((willDelete) => {
    if (willDelete) {
      loading_div.style.display = "block";
      fetch("/api/?resultID=" + id, {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", // otherwise $_POST is empty
          "X-CSRFToken": csrftoken,
        },
        body: "query=deleteResult",
      })
        .then((response) => {
          response.text().then((resptxt) => {
            if (resptxt === "success") {
              swal("Analysis " + id + " has been successfully deleted!", {
                icon: "success",
              });
              result();
              loading_div.style.display = "none";
            } else {
              swal(resptxt, {
                icon: "error",
                title: "error",
              });
              loading_div.style.display = "none";
            }
          });
        })
        .catch((err) => {
          swal(
            "Something went wrong... Please check log for more information",
            {
              icon: "error",
              title: "error",
            }
          );
          loading_div.style.display = "none";
        });
    } else {
      swal("Result " + id + " was not deleted!");
    }
  });
}

function getLocalExtensions(browser) {
  local_list = document.getElementById("local-list");
  loading_div.style.display = "block";
  local_list.style.display = "none";
  fetch("/api/?browser=" + browser, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", // otherwise $_POST is empty
      "X-CSRFToken": csrftoken,
    },
    body: "query=getlocalextensions",
  })
    .then((response) => {
      response.text().then((reply) => {
        if (reply.match(/error: /)) {
          var msg = reply.split("error: ")[1];
          swal("Error!", msg, "error");
        } else {
          if (browser === "googlechrome") {
            browser_name = "Google Chrome";
          } else if (browser === "firefox") {
            browser_name = "Mozilla Firefox";
          } else {
            browser_name = browser;
          }
          local_list.innerHTML =
            "<h3 class='mid_header'>Local " +
            browser_name +
            " Extensions</h3><br>" +
            reply;
          $("#result-table").DataTable();
        }
        loading_div.style.display = "none";
        local_list.style.display = "block";
      });
    })
    .catch((err) => {
      swal(
        "Error!",
        "Something went wrong! Check logs for more information",
        "error"
      );
      loading_div.style.display = "none";
      local_list.style.display = "block";
    });
}

function getLocalOperaExtensions() {
  swal(
    "Coming Soon!",
    "Support for local Opera extensions will be added in an upcoming version... Keep updating for new stuffs and improvements."
  );
}

function analyzeLocalExtension(path, browser) {
  loading_div.style.display = "block";
  fetch("/api/?browser=" + browser + "&path=" + path, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", // otherwise $_POST is empty
      "X-CSRFToken": csrftoken,
    },
    body: "query=analyzelocalextension",
  })
    .then((response) => {
      response.text().then((reply) => {
        handleresponse(reply);
        loading_div.style.display = "none";
      });
    })
    .catch((err) => {
      console.log(err);
      swal(
        "Error!",
        "Something went wrong! Check logs for more information",
        "error"
      );
      loading_div.style.display = "none";
    });
}

function removeAll() {
  swal({
    title: "Delete All Analysis?",
    text: "Once deleted, you will not be able to recover the results!",
    icon: "warning",
    buttons: true,
    dangerMode: true,
  }).then((willDelete) => {
    if (willDelete) {
      loading_div.style.display = "block";
      fetch("/api/", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", // otherwise $_POST is empty
          "X-CSRFToken": csrftoken,
        },
        body: "query=deleteAll",
      })
        .then((response) => {
          response.text().then((resptxt) => {
            if (resptxt === "success") {
              swal("All the results has successfully been deleted", {
                icon: "success",
              });
              result();
              loading_div.style.display = "none";
            } else {
              swal(resptxt, {
                icon: "error",
                title: "error",
              });
              loading_div.style.display = "none";
            }
          });
        })
        .catch((err) => {
          swal(
            "Something went wrong... Please check log for more information",
            {
              icon: "error",
              title: "error",
            }
          );
          loading_div.style.display = "none";
        });
    } else {
      swal("Info", "Your Analysis Reports Are Safe!", "info");
    }
  });
}

function clearLab() {
  swal({
    title: "Clear Lab?",
    text: "Once deleted, you will loose all the deleted and extracted extensions! P.S: It doesn't effect your analysis reports.",
    icon: "warning",
    buttons: true,
    dangerMode: true,
  }).then((willDelete) => {
    if (willDelete) {
      loading_div.style.display = "block";
      fetch("/api/", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", // otherwise $_POST is empty
          "X-CSRFToken": csrftoken,
        },
        body: "query=clearLab",
      })
        .then((response) => {
          response.text().then((resptxt) => {
            handleresponse(resptxt);
          });
        })
        .catch((err) => {
          swal(
            "Something went wrong... Please check log for more information",
            {
              icon: "error",
              title: "error",
            }
          );
          loading_div.style.display = "none";
        });
    } else {
      console.log("Lab is untouched!");
    }
  });
}

function domain_from_url(url) {
  var result;
  var match;
  if (
    (match = url.match(
      /^(?:https?:\/\/)?(?:[^@\n]+@)?(?:www\.)?([^:\/\n\?\=]+)/im
    ))
  ) {
    result = match[1];
    if ((match = result.match(/^[^\.]+\.(.+\..+)$/))) {
      result = match[1];
    }
  }
  return result;
}

function whois(url) {
  loading_div.style.display = "block";
  if (url !== "" && url !== " ") {
    domain = domain_from_url(url);
    console.log(domain);
    fetch(`/api/?domain=${domain}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", // otherwise $_POST is empty
        "X-CSRFToken": csrftoken,
      },
      body: "query=whois",
    })
      .then((response) => {
        response.text().then((resptxt) => {
          button = document.getElementById("modal-content");
          button.innerHTML = resptxt;
          elements.addClass("active");
          loading_div.style.display = "none";
        });
      })
      .catch((err) => {
        swal(
          "Error!",
          "Something went wrong! Check logs for more information",
          "error"
        );
        loading_div.style.display = "none";
      });
  } else {
    swal("Invalid URL", "Invalid URL!", "warning");
    loading_div.style.display = "none";
  }
}

function domainvt(url, analysis_id) {
  loading_div.style.display = "block";
  if (url !== "" && url !== " ") {
    fetch(`/api/?domain=${url}&analysis_id=${analysis_id}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", // otherwise $_POST is empty
        "X-CSRFToken": csrftoken,
      },
      body: "query=vtDomainReport",
    })
      .then((response) => {
        response.text().then((resptxt) => {
          if (resptxt.match(/error: /)) {
            button = document.getElementById("modal-content");
            var msg = resptxt.split("error:")[1];
            var inner_html =
              '<center><img src="/static/images/error.png" style="width: 283px; margin: 11px;"><br><h3>' +
              msg +
              "</h3>";
            button.innerHTML = inner_html;
            elements.addClass("active");
            loading_div.style.display = "none";
          } else {
            button = document.getElementById("modal-content");
            button.innerHTML =
              "<center><h4>VirusTotal Results For " +
              url +
              '</h4></center><br><div id="vt_info" style="overflow: scroll; max-height:500px; text-align: left;"></div>';
            var wrp1 = document.getElementById("vt_info");
            try {
              var data1 = resptxt;
              try {
                var data1 = JSON.parse(resptxt);
              } catch (e) {}
              var tree1 = jsonTree.create(data1, wrp1);
              tree1.expand(function (node) {
                return (
                  node.childNodes.length < 2 || node.label === "phoneNumbers"
                );
              });
              elements.addClass("active");
              loading_div.style.display = "none";
            } catch (e) {
              handleresponse("error: No valid VirusTotal result found!");
            }
          }
        });
      })
      .catch((err) => {
        swal("Error!", "The api call failed! is ExtAnalysis offline?", "error");
        loading_div.style.display = "none";
      });
  } else {
    swal("Error", "Invalid Domain!", "warning");
    loading_div.style.display = "none";
  }
}

function clearlogs(x) {
  loading_div.style.display = "block";
  fetch("/api/", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", // otherwise $_POST is empty
      "X-CSRFToken": csrftoken,
    },
    body: "query=" + encodeURIComponent(x),
  })
    .then((response) => {
      response.text().then((resptxt) => {
        handleresponse(resptxt);
        loading_div.style.display = "none";
      });
    })
    .catch((err) => {
      swal(
        "Error!",
        "Something went wrong! Check logs for more information",
        "error"
      );
      loading_div.style.display = "none";
    });
}

function viewfile(analysis_id, file_id) {
  var final_url = "/view-source/" + analysis_id + "/" + file_id;
  console.log(analysis_id + ' " ' + file_id);
  window.open(final_url, (target = "_blank"));
}

function changeReportsDir() {
  report_dir = document.getElementById("reports_dir").value;
  if (report_dir === "" || report_dir === " ") {
    swal("Error!", "Invalid/Empty path!", "error");
  } else {
    loading_div.style.display = "block";
    apiurl = "/api/?newpath=" + report_dir;
    fetch(apiurl, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", // otherwise $_POST is empty
        "X-CSRFToken": csrftoken,
      },
      body: "query=changeReportsDir",
    })
      .then((resp) => {
        resp.text().then((resptxt) => {
          handleresponse(resptxt);
          loading_div.style.display = "none";
        });
      })
      .catch((err) => {
        swal(
          "Error!",
          "Something went wrong with the api call! is ExtAnalysis offline?",
          "warning"
        );
        loading_div.style.display = "none";
      });
  }
}

function changeLabDir() {
  lab_dir = document.getElementById("lab_dir").value;
  if (lab_dir === "" || lab_dir === " ") {
    swal("Error!", "Invalid/Empty path!", "error");
  } else {
    loading_div.style.display = "block";
    apiurl = "/api/?newpath=" + lab_dir;
    fetch(apiurl, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", // otherwise $_POST is empty
        "X-CSRFToken": csrftoken,
      },
      body: "query=changelabDir",
    })
      .then((resp) => {
        resp.text().then((resptxt) => {
          handleresponse(resptxt);
          loading_div.style.display = "none";
        });
      })
      .catch((err) => {
        swal(
          "Error!",
          "Something went wrong with the api call! is ExtAnalysis offline?",
          "warning"
        );
        loading_div.style.display = "none";
      });
  }
}

function changeVTapi() {
  vt_api = document.getElementById("virustotal_api").value;
  if (vt_api === "" || vt_api === " ") {
    swal("Error!", "Invalid API!", "error");
  } else {
    loading_div.style.display = "block";
    apiurl = "/api/?api=" + vt_api;
    fetch(apiurl, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", // otherwise $_POST is empty
        "X-CSRFToken": csrftoken,
      },
      body: "query=changeVTapi",
    })
      .then((resp) => {
        resp.text().then((resptxt) => {
          handleresponse(resptxt);
          loading_div.style.display = "none";
        });
      })
      .catch((err) => {
        swal(
          "Error!",
          "Something went wrong with the api call! is ExtAnalysis offline?",
          "warning"
        );
        loading_div.style.display = "none";
      });
  }
}

function geoip(ip) {
  loading_div.style.display = "block";
  if (ip !== "" && ip !== " ") {
    fetch(`/api/?ip=${ip}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", // otherwise $_POST is empty
        "X-CSRFToken": csrftoken,
      },
      body: "query=geoip",
    })
      .then((response) => {
        response.text().then((resptxt) => {
          button = document.getElementById("modal-content");
          button.innerHTML = resptxt;
          elements.addClass("active");
          loading_div.style.display = "none";
        });
      })
      .catch((err) => {
        swal("Error!", "API Call failed! is ExtAnalysis offline?", "error");
        loading_div.style.display = "none";
      });
  } else {
    handleresponse("error: Invalid IP Address");
    loading_div.style.display = "none";
  }
}

function retirejsResult(file_id, analysis_id, file_name) {
  loading_div.style.display = "block";
  if (file_id !== "" && file_id !== " ") {
    fetch(`/api/?file=${file_id}&analysis_id=${analysis_id}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", // otherwise $_POST is empty
        "X-CSRFToken": csrftoken,
      },
      body: "query=retirejsResult",
    })
      .then((response) => {
        response.text().then((resptxt) => {
          if (resptxt.match(/error: /)) {
            button = document.getElementById("modal-content");
            var msg = resptxt.split("error:")[1];
            var inner_html =
              '<center><img src="/static/images/error.png" style="width: 283px; margin: 11px;"><br><h3>' +
              msg +
              "</h3>";
            button.innerHTML = inner_html;
            elements.addClass("active");
            loading_div.style.display = "none";
          } else if (resptxt === "none") {
            /**
                        button = document.getElementById('modal-content');
                        button.innerHTML = '<center><h4>RetireJS Vuln Report for '+file_name+'</h4></center><br><div id="rjs_result" style="overflow: scroll; max-height:500px; text-align: left;">No vulnerabilites found!</div>';
                        elements.addClass('active');
                        loading_div.style.display = 'none';
                         */
            handleresponse(
              "No vulnerabilities found in <b>" + file_name + "</b>"
            );
          } else {
            button = document.getElementById("modal-content");
            button.innerHTML =
              "<center><h4>RetireJS Vulnerabily Report for " +
              file_name +
              '</h4></center><br><div id="rjs_result" style="overflow: scroll; max-height:500px; text-align: left;"></div>';
            var wrp1 = document.getElementById("rjs_result");
            var data1 = resptxt;
            try {
              var data1 = JSON.parse(resptxt);
            } catch (e) {}
            var tree1 = jsonTree.create(data1, wrp1);
            tree1.expand(function (node) {
              return (
                node.childNodes.length < 2 || node.label === "phoneNumbers"
              );
            });
            elements.addClass("active");
            loading_div.style.display = "none";
          }
        });
      })
      .catch((err) => {
        swal("Error!", "API Call failed! is ExtAnalysis offline?", "error");
        loading_div.style.display = "none";
      });
  } else {
    handleresponse("error: Invalid File ID");
    loading_div.style.display = "none";
  }
}

function getHTTPHeaders(url) {
  loading_div.style.display = "block";
  if (url !== "" && url !== " ") {
    fetch(`/api/?url=${url}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", // otherwise $_POST is empty
        "X-CSRFToken": csrftoken,
      },
      body: "query=HTTPHeaders",
    })
      .then((response) => {
        response.text().then((resptxt) => {
          button = document.getElementById("modal-content");
          button.innerHTML = resptxt;
          elements.addClass("active");
          loading_div.style.display = "none";
        });
      })
      .catch((err) => {
        swal("Error!", "API Call failed! is ExtAnalysis offline?", "error");
        loading_div.style.display = "none";
      });
  } else {
    handleresponse("error: Invalid url parameter");
    loading_div.style.display = "none";
  }
}

function getSource(url) {
  loading_div.style.display = "block";
  if (url !== "" && url !== " ") {
    fetch(`/api/?url=${url}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", // otherwise $_POST is empty
        "X-CSRFToken": csrftoken,
      },
      body: "query=SourceCode",
    })
      .then((response) => {
        response.text().then((resptxt) => {
          button = document.getElementById("modal-content");
          button.innerHTML = resptxt;
          elements.addClass("active");
          loading_div.style.display = "none";
        });
      })
      .catch((err) => {
        swal("Error!", "API Call failed! is ExtAnalysis offline?", "error");
        loading_div.style.display = "none";
      });
  } else {
    handleresponse("error: Invalid url parameter");
    loading_div.style.display = "none";
  }
}

function update() {
  swal(
    "Update Extanalysis",
    'Use the command "python3 extanalysis.py --update" to check for updates!',
    "info"
  );
}

function updateIntelExtraction() {
  // Get all the values
  try {
    var extract_comments = $("#extract_comments")[0].checked;
    var extract_btc_addresses = $("#extract_btc_addresses")[0].checked;
    var extract_base64_strings = $("#extract_base64_strings")[0].checked;
    var extract_email_addresses = $("#extract_email_addresses")[0].checked;
    var extract_ipv4_addresses = $("#extract_ipv4_addresses")[0].checked;
    var extract_ipv6_addresses = $("#extract_ipv6_addresses")[0].checked;
    var ignore_css = $("#ignore_css")[0].checked;
    var requrl = `/api/?extract_comments=${extract_comments}&extract_btc_addresses=${extract_btc_addresses}&extract_base64_strings=${extract_base64_strings}&extract_email_addresses=${extract_email_addresses}&extract_ipv4_addresses=${extract_ipv4_addresses}&extract_ipv6_addresses=${extract_ipv6_addresses}&ignore_css=${ignore_css}`;
    loading_div.style.display = "block";
    fetch(requrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", // otherwise $_POST is empty
        "X-CSRFToken": csrftoken,
      },
      body: "query=updateIntelExtraction",
    })
      .then((response) => {
        response.text().then((resptxt) => {
          handleresponse(resptxt);
          loading_div.style.display = "none";
        });
      })
      .catch((err) => {
        swal("Error!", "API Call failed! is ExtAnalysis offline?", "error");
        loading_div.style.display = "none";
      });
  } catch {
    handleresponse("error: Something went wrong while getting settings value");
  }
}

```

### `static/js/graph.js`

```javascript
/* File: graph.js */
/**
ExtAnalysis - Browser Extension Analysis Framework
Copyright (C) 2019 - 2022 Tuhinshubhra

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/

    var selected_node_label = document.getElementById('selected-node-label');
    var selected_node_group = document.getElementById('selected-node-group');
    var selected_node_parent = document.getElementById('selected-node-parent');
    var selected_node_id = document.getElementById('selected-node-id');
    var currentNode = 'None';
    var currentCid = 'None'
    // create a network
      var container = document.getElementById('large-graph');
      var data = {
        nodes: nodes,
        edges: edges
      };
      var options = {
        physics: {
            adaptiveTimestep: true,
            barnesHut: {
                gravitationalConstant: -8000,
                springConstant: 0.04,
                springLength: 95
            },
            stabilization: {
                iterations: 987
            }
        },
        interaction: {
            hideEdgesOnDrag: true,
            tooltipDelay: 200,
            navigationButtons: true,
            keyboard: true
          },
        edges: {
            smooth: {
                type: 'continuous',
                forceDirection: 'horizontal',
                roundness: 0.4
            }
        },
        nodes: {
          size: 20,
                font: {
                    size: 15,
                    color: '#89ff00'
                }
        }, 
          groups: {
              extension: {
                shape: 'image',
                image: {
                    unselected:imagedir + 'extension0.png',
                    selected:imagedir + 'extension1.png'
                },
                /** fixed: true,  **/
                /** physics:false **/
              },
              html: {
                shape: 'image',
                image: {
                    unselected:imagedir + 'html0.png',
                    selected:imagedir + 'html1.png'
                },
                /** fixed: true,  **/
                /** physics:false **/
              },
              css: {
                shape: 'image',
                image: {
                    unselected:imagedir + 'css0.png',
                    selected:imagedir + 'css1.png'
                },
                /** fixed: true,  **/
                /** physics:false **/
              },
              static: {
                shape: 'image',
                image: {
                    unselected:imagedir + 'static0.png',
                    selected:imagedir + 'static1.png'
                },
                /** fixed: true,  **/
                /** physics:false **/
              },
              js: {
                shape: 'image',
                image: {
                    unselected:imagedir + 'js0.png',
                    selected:imagedir + 'js1.png'
                },
                /** fixed: true,  **/
                /** physics:false **/
              },
              json: {
                shape: 'image',
                image: {
                    unselected:imagedir + 'json0.png',
                    selected:imagedir + 'json1.png'
                },
                /** fixed: true,  **/
                /** physics:false **/
              },
              other: {
                shape: 'image',
                image: {
                    unselected:imagedir + 'other0.png',
                    selected:imagedir + 'other1.png'
                },
                /** fixed: true,  **/
                /** physics:false **/
              },
              directory: {
                shape: 'image',
                image: {
                    unselected:imagedir + 'directory0.png',
                    selected:imagedir + 'directory1.png'
                },
                /** fixed: true,  **/
                /** physics:false **/
              },
              url: {
                shape: 'image',
                image: {
                    unselected:imagedir + 'url0.png',
                    selected:imagedir + 'url1.png'
                },
                /** fixed: true,  **/
                /** physics:false, **/
                /** font: {size:12, color:'blue', face:'sans', background:'white'} **/
              }
          }
      };
      var network = new vis.Network(container, data, options);
      network.on("doubleClick", function(params) {
        if (params.nodes.length == 1) {
            if (network.isCluster(params.nodes[0]) == true) {
                network.openCluster(params.nodes[0]);
            }
        }
    });
      network.on( 'click', function(properties) {
          try {
            var ids = properties.nodes;
            var clickedNodes = nodes.get(ids);
            console.log(clickedNodes);
            var NodeGroup = clickedNodes[0]['group'];
            var NodeLabel = clickedNodes[0]['label'];
            currentNode = clickedNodes[0]['id'];
            currentCid = clickedNodes[0]['cid']

            selected_node_group.innerText = NodeGroup;
            selected_node_label.innerText = NodeLabel;
            selected_node_id.innerText = currentNode;
            selected_node_parent.innerText = currentCid;
          } catch {
              console.log('.');
          }
    });
    $(function() {
		$("#loading").fadeOut("slow");;
    });
    
    function hideSelectedGroup(){
        selected_group = selected_node_group.innerText;
        if (selected_group === 'None'){
            swal("No Node Selected!", "Select a node first! To select a node just click on it.", 'error');
        } else {
            console.log('Hiding Group: ' + selected_group)
        }
    }

    function hideSelectedNode(){
        selected_label = selected_node_label.innerText;
        if (selected_label === 'None'){
            swal("No Node Selected!", "Select a node first! To select a node just click on it.", 'error');
        } else {
            console.log('Hiding label: ' + selected_label)
        }
    }

    function clusterBySelf(selfid=false){
        if (!selfid){
            if (currentCid === 'None' || currentCid === undefined){
                swal("No Node Selected!", "Select a node first! To select a node just click on it.", 'error');
            } else {
                network.setData(data);
                var clusterOptionsByData = {
                    joinCondition:function(childOptions) {
                        return childOptions.cid == currentCid;
                    },
                    clusterNodeProperties: {
                        id:'cidCluster', 
                        shape: 'image',
                        label: 'Cluster of ' + currentCid,
                        image: {
                            unselected:imagedir + 'cluster1.png',
                            selected:imagedir + 'cluster0.png'
                        },
                    }
                };
                network.cluster(clusterOptionsByData);
            }
        } else {
            if (currentNode === 'None'){
                swal("No Node Selected!", "Select a node first! To select a node just click on it.", 'error');
            } else {
                network.setData(data);
                var clusterOptionsByData = {
                    joinCondition:function(childOptions) {
                        return childOptions.cid == currentNode;
                    },
                    clusterNodeProperties: {
                        id:'cidCluster', 
                        shape: 'image',
                        label: 'Cluster of ' + currentNode,
                        image: {
                            unselected:imagedir + 'cluster1.png',
                            selected:imagedir + 'cluster0.png'
                        },
                    }
                };
                network.cluster(clusterOptionsByData);
            }
        }
    }

    function resetGraph(){
        network.setData(data);
    }
```

### `static/js/jsonTree.js`

```javascript
/**
 * JSON Tree library (a part of jsonTreeViewer)
 * http://github.com/summerstyle/jsonTreeViewer
 *
 * Copyright 2017 Vera Lobacheva (http://iamvera.com)
 * Released under the MIT license (LICENSE.txt)
 */

var jsonTree = (function() {
    
    /* ---------- Utilities ---------- */
    var utils = {
        
        /*
         * Returns js-"class" of value
         * 
         * @param val {any type} - value
         * @returns {string} - for example, "[object Function]"
         */
        getClass : function(val) {
            return Object.prototype.toString.call(val);
        },
        
        /**
         * Checks for a type of value (for valid JSON data types).
         * In other cases - throws an exception
         * 
         * @param val {any type} - the value for new node
         * @returns {string} ("object" | "array" | "null" | "boolean" | "number" | "string")
         */
        getType : function(val) {
            if (val === null) {
                return 'null';
            }
            
            switch (typeof val) {
                case 'number':
                    return 'number';
                
                case 'string':
                    return 'string';
                
                case 'boolean':
                    return 'boolean';
            }
            
            switch(utils.getClass(val)) {
                case '[object Array]':
                    return 'array';
                
                case '[object Object]':
                    return 'object';
            }
            
            throw new Error('Bad type: ' + utils.getClass(val));
        },
        
        /**
         * Applies for each item of list some function
         * and checks for last element of the list
         * 
         * @param obj {Object | Array} - a list or a dict with child nodes
         * @param func {Function} - the function for each item
         */
        forEachNode : function(obj, func) {
            var type = utils.getType(obj),
                isLast;
        
            switch (type) {
                case 'array':
                    isLast = obj.length - 1;
                    
                    obj.forEach(function(item, i) {
                        func(i, item, i === isLast);
                    });
                    
                    break;
                
                case 'object':
                    var keys = Object.keys(obj).sort();
                    
                    isLast = keys.length - 1;
                    
                    keys.forEach(function(item, i) {
                        func(item, obj[item], i === isLast);
                    });
                    
                    break;
            }
            
        },
        
        /**
         * Implements the kind of an inheritance by
         * using parent prototype and
         * creating intermediate constructor
         * 
         * @param Child {Function} - a child constructor
         * @param Parent {Function} - a parent constructor
         */
        inherits : (function() {
            var F = function() {};
            
            return function(Child, Parent) {
                F.prototype = Parent.prototype;
                Child.prototype = new F();
                Child.prototype.constructor = Child;
            };
        })(),
        
        /*
         * Checks for a valid type of root node*
         *
         * @param {any type} jsonObj - a value for root node
         * @returns {boolean} - true for an object or an array, false otherwise
         */
        isValidRoot : function(jsonObj) {
            switch (utils.getType(jsonObj)) {
                case 'object':
                case 'array':
                    return true;
                default:
                    return false;
            }
        },

        /**
         * Extends some object
         */
        extend : function(targetObj, sourceObj) {
            for (var prop in sourceObj) {
                if (sourceObj.hasOwnProperty(prop)) {
                    targetObj[prop] = sourceObj[prop];
                }
            }
        }
    };
    
    
    /* ---------- Node constructors ---------- */
    
    /**
     * The factory for creating nodes of defined type.
     * 
     * ~~~ Node ~~~ is a structure element of an onject or an array
     * with own label (a key of an object or an index of an array)
     * and value of any json data type. The root object or array
     * is a node without label.
     * {...
     * [+] "label": value,
     * ...}
     * 
     * Markup:
     * <li class="jsontree_node [jsontree_node_expanded]">
     *     <span class="jsontree_label-wrapper">
     *         <span class="jsontree_label">
     *             <span class="jsontree_expand-button" />
     *             "label"
     *         </span>
     *         :
     *     </span>
     *     <(div|span) class="jsontree_value jsontree_value_(object|array|boolean|null|number|string)">
     *         ...
     *     </(div|span)>
     * </li>
     *
     * @param label {string} - key name
     * @param val {Object | Array | string | number | boolean | null} - a value of node
     * @param isLast {boolean} - true if node is last in list of siblings
     * 
     * @return {Node}
     */
    function Node(label, val, isLast) {
        var nodeType = utils.getType(val);
        
        if (nodeType in Node.CONSTRUCTORS) {
            return new Node.CONSTRUCTORS[nodeType](label, val, isLast);
        } else {
            throw new Error('Bad type: ' + utils.getClass(val));
        }
    }
    
    Node.CONSTRUCTORS = {
        'boolean' : NodeBoolean,
        'number'  : NodeNumber,
        'string'  : NodeString,
        'null'    : NodeNull,
        'object'  : NodeObject,
        'array'   : NodeArray  
    };
    
    
    /*
     * The constructor for simple types (string, number, boolean, null)
     * {...
     * [+] "label": value,
     * ...}
     * value = string || number || boolean || null
     *
     * Markup:
     * <li class="jsontree_node">
     *     <span class="jsontree_label-wrapper">
     *         <span class="jsontree_label">"age"</span>
     *         :
     *     </span>
     *     <span class="jsontree_value jsontree_value_(number|boolean|string|null)">25</span>
     *     ,
     * </li>
     *
     * @abstract
     * @param label {string} - key name
     * @param val {string | number | boolean | null} - a value of simple types
     * @param isLast {boolean} - true if node is last in list of parent childNodes
     */
    function _NodeSimple(label, val, isLast) {
        if (this.constructor === _NodeSimple) {
            throw new Error('This is abstract class');
        }
        
        var self = this,
            el = document.createElement('li'),
            labelEl,
            template = function(label, val) {
                var str = '\
                    <span class="jsontree_label-wrapper">\
                        <span class="jsontree_label">"' +
                            label +
                        '"</span> : \
                    </span>\
                    <span class="jsontree_value-wrapper">\
                        <span class="jsontree_value jsontree_value_' + self.type + '">' +
                            val +
                        '</span>' +
                        (!isLast ? ',' : '') + 
                    '</span>';
    
                return str;
            };
            
        self.label = label;
        self.isComplex = false;
    
        el.classList.add('jsontree_node');
        el.innerHTML = template(label, val);
    
        self.el = el;

        labelEl = el.querySelector('.jsontree_label');
    
        labelEl.addEventListener('click', function(e) {
            if (e.altKey) {
                self.toggleMarked();
                return;
            }

            if (e.shiftKey) {
                document.getSelection().removeAllRanges();
                alert(self.getJSONPath());
                return;
            }
        }, false);
    }

    _NodeSimple.prototype = {
        constructor : _NodeSimple,

        /**
         * Mark node
         */
        mark : function() {
            this.el.classList.add('jsontree_node_marked');    
        },

        /**
         * Unmark node
         */
        unmark : function() {
            this.el.classList.remove('jsontree_node_marked');    
        },

        /**
         * Mark or unmark node
         */
        toggleMarked : function() {
            this.el.classList.toggle('jsontree_node_marked');    
        },

        /**
         * Expands parent node of this node
         *
         * @param isRecursive {boolean} - if true, expands all parent nodes
         *                                (from node to root)
         */
        expandParent : function(isRecursive) {
            if (!this.parent) {
                return;
            }
               
            this.parent.expand(); 
            this.parent.expandParent(isRecursive);
        },

        /**
         * Returns JSON-path of this 
         * 
         * @param isInDotNotation {boolean} - kind of notation for returned json-path
         *                                    (by default, in bracket notation)
         * @returns {string}
         */
        getJSONPath : function(isInDotNotation) {
            if (this.isRoot) {
                return "$";
            }

            var currentPath;

            if (this.parent.type === 'array') {
                currentPath = "[" + this.label + "]";
            } else {
                currentPath = isInDotNotation ? "." + this.label : "['" + this.label + "']";
            }

            return this.parent.getJSONPath(isInDotNotation) + currentPath; 
        }
    };
    
    
    /*
     * The constructor for boolean values
     * {...
     * [+] "label": boolean,
     * ...}
     * boolean = true || false
     *
     * @constructor
     * @param label {string} - key name
     * @param val {boolean} - value of boolean type, true or false
     * @param isLast {boolean} - true if node is last in list of parent childNodes
     */
    function NodeBoolean(label, val, isLast) {
        this.type = "boolean";
    
        _NodeSimple.call(this, label, val, isLast);
    }
    utils.inherits(NodeBoolean,_NodeSimple);
    
    
    /*
     * The constructor for number values
     * {...
     * [+] "label": number,
     * ...}
     * number = 123
     *
     * @constructor
     * @param label {string} - key name
     * @param val {number} - value of number type, for example 123
     * @param isLast {boolean} - true if node is last in list of parent childNodes
     */
    function NodeNumber(label, val, isLast) {
        this.type = "number";
    
        _NodeSimple.call(this, label, val, isLast);
    }
    utils.inherits(NodeNumber,_NodeSimple);
    
    
    /*
     * The constructor for string values
     * {...
     * [+] "label": string,
     * ...}
     * string = "abc"
     *
     * @constructor
     * @param label {string} - key name
     * @param val {string} - value of string type, for example "abc"
     * @param isLast {boolean} - true if node is last in list of parent childNodes
     */
    function NodeString(label, val, isLast) {
        this.type = "string";
    
        _NodeSimple.call(this, label, '"' + val + '"', isLast);
    }
    utils.inherits(NodeString,_NodeSimple);
    
    
    /*
     * The constructor for null values
     * {...
     * [+] "label": null,
     * ...}
     *
     * @constructor
     * @param label {string} - key name
     * @param val {null} - value (only null)
     * @param isLast {boolean} - true if node is last in list of parent childNodes
     */
    function NodeNull(label, val, isLast) {
        this.type = "null";
    
        _NodeSimple.call(this, label, val, isLast);
    }
    utils.inherits(NodeNull,_NodeSimple);
    
    
    /*
     * The constructor for complex types (object, array)
     * {...
     * [+] "label": value,
     * ...}
     * value = object || array
     *
     * Markup:
     * <li class="jsontree_node jsontree_node_(object|array) [expanded]">
     *     <span class="jsontree_label-wrapper">
     *         <span class="jsontree_label">
     *             <span class="jsontree_expand-button" />
     *             "label"
     *         </span>
     *         :
     *     </span>
     *     <div class="jsontree_value">
     *         <b>{</b>
     *         <ul class="jsontree_child-nodes" />
     *         <b>}</b>
     *         ,
     *     </div>
     * </li>
     *
     * @abstract
     * @param label {string} - key name
     * @param val {Object | Array} - a value of complex types, object or array
     * @param isLast {boolean} - true if node is last in list of parent childNodes
     */
    function _NodeComplex(label, val, isLast) {
        if (this.constructor === _NodeComplex) {
            throw new Error('This is abstract class');
        }
        
        var self = this,
            el = document.createElement('li'),
            template = function(label, sym) {
                var comma = (!isLast) ? ',' : '',
                    str = '\
                        <div class="jsontree_value-wrapper">\
                            <div class="jsontree_value jsontree_value_' + self.type + '">\
                                <b>' + sym[0] + '</b>\
                                <span class="jsontree_show-more">&hellip;</span>\
                                <ul class="jsontree_child-nodes"></ul>\
                                <b>' + sym[1] + '</b>' +
                            '</div>' + comma +
                        '</div>';
    
                if (label !== null) {
                    str = '\
                        <span class="jsontree_label-wrapper">\
                            <span class="jsontree_label">' +
                                '<span class="jsontree_expand-button"></span>' +
                                '"' + label +
                            '"</span> : \
                        </span>' + str;
                }
    
                return str;
            },
            childNodesUl,
            labelEl,
            moreContentEl,
            childNodes = [];
    
        self.label = label;
        self.isComplex = true;
    
        el.classList.add('jsontree_node');
        el.classList.add('jsontree_node_complex');
        el.innerHTML = template(label, self.sym);
    
        childNodesUl = el.querySelector('.jsontree_child-nodes');
    
        if (label !== null) {
            labelEl = el.querySelector('.jsontree_label');
            moreContentEl = el.querySelector('.jsontree_show-more');
    
            labelEl.addEventListener('click', function(e) {
                if (e.altKey) {
                    self.toggleMarked();
                    return;
                }

                if (e.shiftKey) {
                    document.getSelection().removeAllRanges();
                    alert(self.getJSONPath());
                    return;
                }

                self.toggle(e.ctrlKey || e.metaKey);
            }, false);
            
            moreContentEl.addEventListener('click', function(e) {
                self.toggle(e.ctrlKey || e.metaKey);
            }, false);
    
            self.isRoot = false;
        } else {
            self.isRoot = true;
            self.parent = null;
    
            el.classList.add('jsontree_node_expanded');
        }
    
        self.el = el;
        self.childNodes = childNodes;
        self.childNodesUl = childNodesUl;
    
        utils.forEachNode(val, function(label, node, isLast) {
            self.addChild(new Node(label, node, isLast));
        });
    
        self.isEmpty = !Boolean(childNodes.length);
        if (self.isEmpty) {
            el.classList.add('jsontree_node_empty');
        }
    }

    utils.inherits(_NodeComplex, _NodeSimple);
    
    utils.extend(_NodeComplex.prototype, {
        constructor : _NodeComplex,
        
        /*
         * Add child node to list of child nodes
         *
         * @param child {Node} - child node
         */
        addChild : function(child) {
            this.childNodes.push(child);
            this.childNodesUl.appendChild(child.el);
            child.parent = this;
        },
    
        /*
         * Expands this list of node child nodes
         *
         * @param isRecursive {boolean} - if true, expands all child nodes
         */
        expand : function(isRecursive){
            if (this.isEmpty) {
                return;
            }
            
            if (!this.isRoot) {
                this.el.classList.add('jsontree_node_expanded');
            }
    
            if (isRecursive) {
                this.childNodes.forEach(function(item, i) {
                    if (item.isComplex) {
                        item.expand(isRecursive);
                    }
                });
            }
        },
    
        /*
         * Collapses this list of node child nodes
         *
         * @param isRecursive {boolean} - if true, collapses all child nodes
         */
        collapse : function(isRecursive) {
            if (this.isEmpty) {
                return;
            }
            
            if (!this.isRoot) {
                this.el.classList.remove('jsontree_node_expanded');
            }
    
            if (isRecursive) {
                this.childNodes.forEach(function(item, i) {
                    if (item.isComplex) {
                        item.collapse(isRecursive);
                    }
                });
            }
        },
    
        /*
         * Expands collapsed or collapses expanded node
         *
         * @param {boolean} isRecursive - Expand all child nodes if this node is expanded
         *                                and collapse it otherwise
         */
        toggle : function(isRecursive) {
            if (this.isEmpty) {
                return;
            }
            
            this.el.classList.toggle('jsontree_node_expanded');
            
            if (isRecursive) {
                var isExpanded = this.el.classList.contains('jsontree_node_expanded');
                
                this.childNodes.forEach(function(item, i) {
                    if (item.isComplex) {
                        item[isExpanded ? 'expand' : 'collapse'](isRecursive);
                    }
                });
            }
        },

        /**
         * Find child nodes that match some conditions and handle it
         * 
         * @param {Function} matcher
         * @param {Function} handler
         * @param {boolean} isRecursive
         */
        findChildren : function(matcher, handler, isRecursive) {
            if (this.isEmpty) {
                return;
            }
            
            this.childNodes.forEach(function(item, i) {
                if (matcher(item)) {
                    handler(item);
                }

                if (item.isComplex && isRecursive) {
                    item.findChildren(matcher, handler, isRecursive);
                }
            });
        }
    });
    
    
    /*
     * The constructor for object values
     * {...
     * [+] "label": object,
     * ...}
     * object = {"abc": "def"}
     *
     * @constructor
     * @param label {string} - key name
     * @param val {Object} - value of object type, {"abc": "def"}
     * @param isLast {boolean} - true if node is last in list of siblings
     */
    function NodeObject(label, val, isLast) {
        this.sym = ['{', '}'];
        this.type = "object";
    
        _NodeComplex.call(this, label, val, isLast);
    }
    utils.inherits(NodeObject,_NodeComplex);
    
    
    /*
     * The constructor for array values
     * {...
     * [+] "label": array,
     * ...}
     * array = [1,2,3]
     *
     * @constructor
     * @param label {string} - key name
     * @param val {Array} - value of array type, [1,2,3]
     * @param isLast {boolean} - true if node is last in list of siblings
     */
    function NodeArray(label, val, isLast) {
        this.sym = ['[', ']'];
        this.type = "array";
    
        _NodeComplex.call(this, label, val, isLast);
    }
    utils.inherits(NodeArray, _NodeComplex);
    
    
    /* ---------- The tree constructor ---------- */
    
    /*
     * The constructor for json tree.
     * It contains only one Node (Array or Object), without property name.
     * CSS-styles of .tree define main tree styles like font-family,
     * font-size and own margins.
     *
     * Markup:
     * <ul class="jsontree_tree clearfix">
     *     {Node}
     * </ul>
     *
     * @constructor
     * @param jsonObj {Object | Array} - data for tree
     * @param domEl {DOMElement} - DOM-element, wrapper for tree
     */
    function Tree(jsonObj, domEl) {
        this.wrapper = document.createElement('ul');
        this.wrapper.className = 'jsontree_tree clearfix';
        
        this.rootNode = null;
        
        this.sourceJSONObj = jsonObj;

        this.loadData(jsonObj);
        this.appendTo(domEl);
    }
    
    Tree.prototype = {
        constructor : Tree,
        
        /**
         * Fill new data in current json tree
         *
         * @param {Object | Array} jsonObj - json-data
         */
        loadData : function(jsonObj) {
            if (!utils.isValidRoot(jsonObj)) {
                alert('The root should be an object or an array');
                console.log(utils.getType(jsonObj));
                return;
            }

            this.sourceJSONObj = jsonObj;
            
            this.rootNode = new Node(null, jsonObj, 'last');
            this.wrapper.innerHTML = '';
            this.wrapper.appendChild(this.rootNode.el);
        },
        
        /**
         * Appends tree to DOM-element (or move it to new place)
         *
         * @param {DOMElement} domEl 
         */
        appendTo : function(domEl) {
            domEl.appendChild(this.wrapper);
        },
        
        /**
         * Expands all tree nodes (objects or arrays) recursively
         *
         * @param {Function} filterFunc - 'true' if this node should be expanded
         */
        expand : function(filterFunc) {
            if (this.rootNode.isComplex) {
                if (typeof filterFunc == 'function') {
                    this.rootNode.childNodes.forEach(function(item, i) {
                        if (item.isComplex && filterFunc(item)) {
                            item.expand();
                        }
                    });
                } else {
                    this.rootNode.expand('recursive');
                }
            }
        },
       
        /**
         * Collapses all tree nodes (objects or arrays) recursively
         */
        collapse : function() {
            if (typeof this.rootNode.collapse === 'function') {
                this.rootNode.collapse('recursive');
            }
        },

        /**
         * Returns the source json-string (pretty-printed)
         * 
         * @param {boolean} isPrettyPrinted - 'true' for pretty-printed string
         * @returns {string} - for exemple, '{"a":2,"b":3}'
         */
        toSourceJSON : function(isPrettyPrinted) {
            if (!isPrettyPrinted) {
                return JSON.stringify(this.sourceJSONObj);
            }

            var DELIMETER = "[%^$#$%^%]",
                jsonStr = JSON.stringify(this.sourceJSONObj, null, DELIMETER);

            jsonStr = jsonStr.split("\n").join("<br />");
            jsonStr = jsonStr.split(DELIMETER).join("&nbsp;&nbsp;&nbsp;&nbsp;");

            return jsonStr;
        },

        /**
         * Find all nodes that match some conditions and handle it
         */
        findAndHandle : function(matcher, handler) {
            this.rootNode.findChildren(matcher, handler, 'isRecursive');
        },

        /**
         * Unmark all nodes
         */
        unmarkAll : function() {
            this.rootNode.findChildren(function(node) {
                return true;
            }, function(node) {
                node.unmark();
            }, 'isRecursive');
        }
    };

    
    /* ---------- Public methods ---------- */
    return {
        /**
         * Creates new tree by data and appends it to the DOM-element
         * 
         * @param jsonObj {Object | Array} - json-data
         * @param domEl {DOMElement} - the wrapper element
         * @returns {Tree}
         */
        create : function(jsonObj, domEl) {
            return new Tree(jsonObj, domEl);
        }
    };
})();

```

