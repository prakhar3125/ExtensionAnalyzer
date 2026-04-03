# Monolithic ExtAnalysis - auto-compiled
from flask import Flask, request, render_template, redirect, url_for, send_from_directory
from flask import render_template
from flask import render_template, url_for
from flask_wtf.csrf import CSRFProtect
from pathlib import Path
from typing import Optional
from urllib.parse import parse_qsl, urlparse, parse_qs
from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
import argparse
import base64
import certifi
import configparser
import json
import logging
import logging, traceback
import logging,traceback
import os
import plugins.retirejs as retirejs
import random
import re
import requests
import shutil
import signal
import socket
import ssl
import subprocess
import sys
import tarfile
import tempfile
import time
import traceback
import urllib.request
import webbrowser
import zipfile

import sys
_m = sys.modules[__name__]
_m.core = _m
_m.helper = _m
_m.analysis = _m
_m.virustotal = _m
_m.settings = _m
_m.download_extension = _m
_m.scan = _m
_m.processapi = _m
_m.viewgraph = _m
_m.viewfile = _m
_m.vs = _m
_m.viewResult = _m
_m.updater = _m
_m.ip2country = _m
_m.intel = _m
_m.localextensions = _m
_m.result = _m
_m.saveresult = _m


# ==========================================
# FROM: core/helper.py
# ==========================================

"""
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
"""


def escape(html):
    return(html.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;'))

def fixpath(path):
    # i have a bad issue of hardcoding path this saves some troubles
    return os.path.abspath(os.path.expanduser(path))

# ==========================================
# FROM: core/settings.py
# ==========================================

"""
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
"""


def init_settings():
    # Check if reports file exist if not create an empty one
    if not os.path.isfile(core.report_index):
        rif = open(core.report_index, 'w+', encoding='utf-8')
        empty_reports = {"reports": []}
        rif.write(json.dumps(empty_reports, indent=4))
        rif.close()
        core.updatelog('Created empty reports file')

    # Check if settings file exist if not get the contents from github and create one
    if not os.path.isfile(core.settings_file):
        core.updatelog('Could not find settings.json file. Downloading it from github...')
        try:
            import urllib.request
            raw_settings = 'https://raw.githubusercontent.com/Tuhinshubhra/ExtAnalysis/master/settings.json'
            urllib.request.urlretrieve(raw_settings, core.settings_file)
            core.updatelog('New settings file successfully generated!')
        except Exception as e:
            core.updatelog('Error {0} encountered while getting settings file from github... Please download a clean version of ExtAnalysis from github.'.format(str(e)))
            logging.error(traceback.format_exc())
            core.handle_exit()


    if os.path.isfile(core.settings_file):
        try:
            with open(core.settings_file, 'r', encoding='utf-8') as sc:
                settings = json.loads(sc.read())

            '''
            INIT VIRUSTOTAL API
            '''
            if settings['virustotal_api'] != '':
                core.virustotal_api = settings['virustotal_api']
            else:
                core.updatelog('Virustotal api was not specified... Files won\'t be scanned')
            
           
            '''
            INIT REPORT DIRECTORY...
            '''
            new_results_dir = settings['results_directory_path']
            old_results_dir = settings['old_result_directory']
            if new_results_dir == '':
                new_results_dir = core.reports_path
            if old_results_dir == '':
                old_results_dir = core.reports_path
            ### Check if the results directory have changed... if yes we have to change paths
            if new_results_dir != old_results_dir:
                core.updatelog('Reports path change detected! fixing old paths and updating report index...')
                path_changed(old_results_dir, new_results_dir)
            # set it
            if core.reports_path != new_results_dir:
                if os.path.isdir(new_results_dir):
                    core.reports_path = new_results_dir
                else:
                    core.updatelog('Invalid results_directory_path specified in settings.json! using default path: {0}'.format(core.reports_path))
            
            
            '''
            INIT LAB DIRECTORY
            '''
            lab_dir = settings['lab_directory_path']
            if lab_dir != '' and lab_dir != core.lab_path:
                if os.path.isdir(lab_dir):
                    core.lab_path = lab_dir
                else:
                    core.updatelog('Invalid lab_directory_path specified in settings.json! using default lab path: {0}'.format(core.lab_path))
            elif lab_dir == '' and not os.path.isdir(core.lab_path):
                core.updatelog('Creating lab directory: ' + core.lab_path)
                try:
                    os.mkdir(core.lab_path)
                except:
                    core.updatelog('Something went wrong while creating lab directory!')
                    logging.error(traceback.format_exc())
                    core.handle_exit()
            
            '''
            CHECK IGNORE CSS VAR
            '''
            if not settings['ignore_css']:
                core.ignore_css = False
                core.updatelog('CSS files will not be ignored!')

            '''
            ALL THE INTEL EXTRACTION SETTINGS GO HERE
            '''
            if not settings['extract_comments']:
                # comment extraction set to false
                core.extract_comments = False
                core.updatelog('Skipping comments extraction')


            if not settings['extract_btc_addresses']:
                # BTC Address extraction set to false
                core.extract_btc_addresses = False
                core.updatelog('Skipping Bitcoin address extraction')

            if not settings['extract_base64_strings']:
                # Base64 encoded strings extraction set to false
                core.extract_base64_strings = False
                core.updatelog('Skipping Base64 strings extraction')

            if not settings['extract_email_addresses']:
                # Comments extraction set to false
                core.extract_email_addresses = False
                core.updatelog('Skipping email address extraction')

            if not settings['extract_ipv4_addresses']:
                # IPv4 address extraction set to false
                core.extract_ipv4_addresses = False
                core.updatelog('Skipping IPv4 address extraction')

            if not settings['extract_ipv6_addresses']:
                # IPv6 address extraction set to false
                core.extract_ipv6_addresses = False
                core.updatelog('Skipping IPv6 address extraction')

            return [True, 'All settings loaded']
        
        
        except Exception as e:
            core.updatelog('Something went wrong while reading settings file. Error: ' + str(e))
            logging.error(traceback.format_exc())
            return [False, 'error reading settings file']
    else:
        core.updatelog('Settings file not found... Some features might not work as intended')
        return [False, 'settings.json not found']

def path_changed(old_path, new_path):
    # Change '<reports_path>' to absolute path in results file

    if core.reportids == {}:
        ri = open(core.report_index, 'r', encoding='utf-8')
        ri = ri.read()
        core.reportids = json.loads(ri)
    reports = core.reportids
    for report in reports['reports']:
        if '<reports_path>' in report['report_directory']:
            core.updatelog('[Updating reports index] Chainging <report_index> to: ' + old_path)
            report['report_directory'] = report['report_directory'].replace('<reports_path>', old_path)
    
    core.reportids = reports
    ri = open(core.report_index, 'w+', encoding='utf-8')
    ri.write(json.dumps(reports, indent=4, sort_keys=True))
    ri.close()
    core.updatelog('Report index updated successfully')
    core.updatelog('Updating settings.json')
    sj = open(core.settings_file, 'r', encoding='utf-8')
    sj = json.loads(sj.read())
    sj['old_result_directory'] = new_path
    wsj = open(core.settings_file, 'w+', encoding='utf-8')
    wsj.write(json.dumps(sj, indent=4, sort_keys=False))
    wsj.close()
    core.updatelog('Updated settings.json successfully')

def changedir(newpath):
    '''
    change the results_directory_path in settings.json
    response [True/False, 'message']
    '''
    if os.path.isdir(newpath):
        core.updatelog('Setting results directory to: ' + newpath)
        settings = open(core.settings_file, 'r', encoding='utf-8')
        settings = json.loads(settings.read())
        old_reports_path = settings['results_directory_path']
        if old_reports_path == '':
            old_reports_path = core.reports_path
        if newpath == old_reports_path:
            return[False, 'Please provide a different path, not the current one!']
        settings['results_directory_path'] = newpath
        core.updatelog('Updating settings.json')
        try:
            ws = open(core.settings_file, 'w+', encoding='utf-8')
            ws.write(json.dumps(settings, indent=4, sort_keys=False))
            ws.close()
            core.updatelog('File successfully updated! rewriting variables and fixing old paths...')
            core.reports_path = newpath
            path_changed(old_reports_path, newpath)
            return[True, 'Analysis report directory updated successfully!']
        except Exception as e:
            logging.error(traceback.format_exc())
            return[False, 'Error while writing settings file: ' + str(e)]
    else:
        return [False, 'invalid path']

def changelabdir(newpath):
    '''
    change the results_directory_path in settings.json
    response [True/False, 'message']
    '''
    if os.path.isdir(newpath):
        core.updatelog('Setting lab directory to: ' + newpath)
        settings = open(core.settings_file, 'r', encoding='utf-8')
        settings = json.loads(settings.read())
        old_reports_path = settings['lab_directory_path']
        if old_reports_path == '':
            old_reports_path = core.lab_path
        if newpath == old_reports_path:
            return[False, 'Please provide a different path, not the current one!']
        settings['lab_directory_path'] = newpath
        core.updatelog('Updating settings.json')
        try:
            ws = open(core.settings_file, 'w+', encoding='utf-8')
            ws.write(json.dumps(settings, indent=4, sort_keys=False))
            ws.close()
            core.updatelog('File successfully updated! rewriting variables and fixing old paths...')
            core.lab_path = newpath
            return[True, 'Lab directory updated successfully!']
        except Exception as e:
            logging.error(traceback.format_exc())
            return[False, 'Error while writing settings file: ' + str(e)]
    else:
        return [False, 'invalid path']


def change_vt_api(api):
    '''
    change virustotal api!
    parameters needed = api = new api
    '''
    if api != core.virustotal_api:
        # Not the same api
        core.updatelog('Setting new virustotal api!')
        settings = open(core.settings_file, 'r')
        settings = json.loads(settings.read())
        settings['virustotal_api'] = api
        try:
            ws = open(core.settings_file, 'w+')
            ws.write(json.dumps(settings, indent=4, sort_keys=False))
            ws.close()
            core.virustotal_api = api
            core.updatelog('New virustotal api set successfully! new api: ' + api)
            return[True, 'New virustotal api set successfully!']
        except Exception as e:
            logging.error(traceback.format_exc())
            return[False, 'Error while writing settings file: ' + str(e)]

    else:
        return [False, 'This api is already in use. Nothing changed!']

def update_settings_batch(settings_dict):
    '''
    FUNCTION TO UPDATE SETTINGS KEYS THAT HAVE TRUE/FALSE VALUES
    NEEDED PARAMETERS:
    settings_dict = DICT WITH NAME AND VALUES.. ex: {"extract_comment":"true"}
    '''
    update_type = '' # 0 = failed, 1 = success, 2 = some updated some not!
    try:
        settings = open(core.settings_file, 'r')
        settings = json.loads(settings.read())

        for the_setting in settings_dict:
            try:
                if type(settings[the_setting]) == bool:
                    # okay settings key is good...
                    if str(settings_dict[the_setting]).lower() == 'true':
                        # set to true
                        settings[the_setting] = True
                        core.updatelog('Set the value of {0} to True successfully'.format(the_setting))
                        # set update type
                        if update_type == '':
                            update_type = '1'
                        elif update_type == '0':
                            update_type = '2'
                    elif str(settings_dict[the_setting]).lower() == 'false':
                        # set to false
                        settings[the_setting] = False
                        core.updatelog('Set the value of {0} to False successfully'.format(the_setting))
                        # set update type
                        if update_type == '':
                            update_type = '1'
                        elif update_type == '0':
                            update_type = '2'
                    else:
                        core.updatelog('Invalid value: {1} for setting {0}'.format(the_setting, str(settings_dict[the_setting])))
                        # set update type
                        if update_type == '':
                            update_type = '0'
                        elif update_type == '1':
                            update_type = '2'
            except Exception as e:
                logging.error(traceback.format_exc())
                if update_type == '':
                    update_type = '0'
                elif update_type == '1':
                    update_type = '2'
        try:
            ws = open(core.settings_file, 'w+')
            ws.write(json.dumps(settings, indent=4, sort_keys=False))
            ws.close()
            core.updatelog('Settings written to file successfully! Restart ExtAnalysis for them to take effect')
        except Exception as e:
            core.updatelog('Error {0} occured while writing settings.json file'.format(str(e)))
            logging.error(traceback.format_exc())
            return '0'
        return update_type

    except Exception as e:
        core.updatelog('Error {0} occured while updating settings'.format(str(e)))
        logging.error(traceback.format_exc())
        return '0'
        

# ==========================================
# FROM: core/core.py
# ==========================================

"""
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
"""


## all the paths
path = os.path.dirname(os.path.abspath(__file__)).replace('/core','').replace(r'\core','')
lab_path = helper.fixpath(path + '/lab')
reports_path = helper.fixpath(path + '/reports')

# Version
with open(os.path.join(path, 'current_version'), encoding='utf-8') as vf:
    version = vf.read()

# All the variables
quiet = False
log = ""
raw_log = "\n\n\n"
report = {} #'{"name":"","version":"","author":"","permissions":[{"name":"","description":"","warning":""}],"urls":"","files":{"html":"","js":"","css":"","static":"","other":""},"content-scripts":[],"background-scripts":[],"pageaction-popup":[],"browseraction-popup":[]}'
reportids = {}
virustotal_api = ''
ignore_css = True
github_repo = 'https://github.com/Tuhinshubhra/ExtAnalysis'
github_zip = 'https://github.com/Tuhinshubhra/ExtAnalysis/archive/master.zip'
version_url = 'https://raw.githubusercontent.com/Tuhinshubhra/ExtAnalysis/master/current_version'

# settings for intel extraction! DO NOT EDIT HERE! use the settings.json instead
extract_comments = True
extract_btc_addresses = True
extract_base64_strings = True
extract_email_addresses = True
extract_ipv4_addresses = True
extract_ipv6_addresses = True

report_index = os.path.join(path, 'reports.json')
settings_file = helper.fixpath(path + '/settings.json')
log_file = helper.fixpath(path + '/extanalysis.log')


def print_logo():
    logo = '''
     _____     _   _____         _         _
    |   __|_ _| |_|  _  |___ ___| |_ _ ___|_|___
    |   __|_'_|  _|     |   | .'| | | |_ -| |_ -|
    |_____|_,_|_| |__|__|_|_|__,|_|_  |___|_|___|
    => Browser Extension Analysis |___| Framework
    => Version {0} By r3dhax0r

    '''.format(version)
    print(logo)

def updatelog(clog, type='info'):
    '''
    Logger
    TODO: it was already too late before i thought of type hence this shitty hack
    will fix it later
    '''
    global raw_log, log, quiet
    clog = str(clog)
    if any (val in clog.lower() for val in ['success', 'done', 'finished', "complete", 'found']):
        raw_log += '[SUC - {0}]  {1} \n'.format(time.strftime('%d-%b-%y %H:%M:%S', time.gmtime()), clog)
        if not quiet:
            msg = '[+] ' + clog
            print(msg)
    elif any (val in clog.lower() for val in ['error', 'wrong', 'not', "n't"]):
        raw_log += '[ERR - {0}]  {1} \n'.format(time.strftime('%d-%b-%y %H:%M:%S', time.gmtime()), clog)
        if not quiet:
            msg = '[!] ' + clog
            print(msg)
    else:
        raw_log += '[INF - {0}]  {1} \n'.format(time.strftime('%d-%b-%y %H:%M:%S', time.gmtime()), clog)
        if not quiet:
            msg = '[i] ' + clog
            print(msg)

    log += '<br>[' + time.strftime("%H:%M:%S", time.gmtime()) + '] ' + clog

def clearlog():
    global log
    log = ""

def initreport(manifestjson, ext_dir, ext_type='local'):
    global report, reportids, path, report_index
    try:
        ridfile = report_index
        ridcnt = open(ridfile, 'r', encoding='utf-8')
        ridcnt = ridcnt.read()
        reportids = json.loads(ridcnt)
        ext_manifest = os.path.join(ext_dir, 'manifest.json')
        try:
            report['name'] = manifestjson['name']
            # check if name is defined in locale
            if '__MSG_' in manifestjson['name']:
                updatelog('Getting extension name from _locales')
                #locale_dir = helper.fixpath(ext_dir + '/_locales/')
                ext_name = GetNameFromManifest(ext_manifest)
                if ext_name != False and ext_name != "" and ext_name != None:
                    report['name'] = ext_name
            report['crx'] = ""
            report['extracted'] = ''
            report['type'] = ext_type
            report['manifest'] = manifestjson
            report['version'] = manifestjson['version']
            report['permissions'] = []
            report['urls'] = []
            report['emails'] = []
            report['bitcoin_addresses'] = []
            report['ipv4_addresses'] = []
            report['ipv6_addresses'] = []
            report['base64_strings'] = []
            report['comments'] = []
            report['domains'] = []
            report['files'] = {'html':[], 'json':[], 'js':[], 'css':[], 'static':[], 'other':[]}
            try:
                # non Required values
                report['author'] = manifestjson['author']
            except:
                report['author'] = 'unknown'
                updatelog('No author name found')
            try:
                report['description'] = manifestjson['description']
                if '__MSG_' in report['description']:
                    updatelog('Getting Extension Description from locale')
                    app_desc = GetDescriptionFromManifest(ext_manifest)
                    if app_desc != False and app_desc != None and app_desc != "":
                        report['description'] = app_desc
                    else:
                        updatelog('Could not get extension description from locale')
            except:
                report['description'] = 'unknown'
                updatelog('No author name found')
            return True
        except Exception as e:
            updatelog('Error while parsing manifest.json, Error: ' + str(e))
            logging.error(traceback.format_exc())
            #print(manifestjson)
            return False
    except Exception as e:
        logging.error(traceback.format_exc())
        updatelog('Something went wrong while getting report ids. Error: ' + str(e))
        return False

def insertpermission(permarray):
    if all(val in permarray for val in ['name', 'description', 'warning', 'badge', 'risk']):
        global report
        report['permissions'].append(permarray)
    else:
        updatelog('Skipped adding permission "MISSING KEY". Perm: ' + str(permarray))

def extract_urls(file_path):
    updatelog('Extracting URLs From: ' + file_path)
    urls = []
    try:
        cnt = open(helper.fixpath(file_path), 'r', encoding='utf8')
        contents = cnt.read()
        curls = re.findall(r'(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?', contents)
        for url in curls:
            urls.append(url[0]+'://'+url[1]+url[2])
            updatelog('Found url: ' + url[0]+'://'+url[1]+url[2])
        urls = list(set(urls))
        return(urls)
    except Exception as e:
        updatelog('error: Something went wrong while reading file')
        updatelog('ERROR: ' + str(e))
        logging.error(traceback.format_exc())
        return []


def GetNameFromManifest(manifest_file):
    # Get's the name of an extension from manifest file
    if os.path.isfile(manifest_file):
        # Path is valid and it's a manifest file
        extension_path = helper.fixpath(manifest_file.replace('manifest.json', ''))
        manifest_content = open(manifest_file, 'r', encoding='utf-8')
        manifest_content = manifest_content.read()

        try:
            # load the json data
            manifest_json = json.loads(manifest_content)

            try:
                manifest_name = manifest_json['name']
                if '__MSG_' in manifest_name:
                    # This is the whole reason i created this function...
                    updatelog('Getting manifest name from locale file: ' + extension_path)
                    manifest_message = re.findall('__MSG_(.*?)__', manifest_name)[0]
                    locale_dir = helper.fixpath(extension_path + '/_locales/')
                    if os.path.isdir(locale_dir):
                        # locale directory exists let' s grab our thing
                        try:
                            # get the default locale from manifest
                            default_locale = manifest_json['default_locale']
                            en_locale_file = helper.fixpath(locale_dir + '/' + default_locale + '/messages.json')
                            updatelog('Default Locale: ' + default_locale)
                        except Exception as e:
                            # use hardcoded en
                            en_locale_file = helper.fixpath(locale_dir + '/en/messages.json')
                        if os.path.isfile(en_locale_file):
                            # en locale file found let's grab the name
                            en_locale_content = open(en_locale_file, 'r', encoding='utf-8')
                            try:
                                en_locale_content = json.loads(en_locale_content.read())
                                string_content = str(en_locale_content)
                                ext_name = ''
                                if manifest_message in string_content:
                                    ext_name = en_locale_content[manifest_message]['message']
                                    updatelog('Extension name grabbed from en locale file.. Name: ' + ext_name)
                                    return ext_name
                                else:
                                    updatelog('Could not find name')
                                    return False

                            except Exception as e:
                                updatelog('Something went wrong while reading or parsing en locale file...')
                                logging.error(traceback.format_exc())
                                return False
                        else:
                            # en locale not found let's just get the first one we find and be done with it
                            ldirs = os.listdir(locale_dir)
                            for dir in ldirs:
                                if os.path.isfile(helper.fixpath(locale_dir + '/' + dir + '/messages.json')):
                                    locale_content = open(helper.fixpath(locale_dir + '/' + dir + '/messages.json'), 'r', encoding='utf-8')
                                    try:
                                        en_locale_content = json.loads(locale_content.read())
                                        if manifest_message in locale_content:
                                            ext_name = en_locale_content[manifest_message]['message']
                                            updatelog('Extension name grabbed from en locale file.. Name: ' + ext_name)
                                            return ext_name
                                        else:
                                            updatelog('Could not find name')
                                            return False

                                    except Exception as e:
                                        updatelog('Something went wrong while reading or parsing en locale file...')
                                        logging.error(traceback.format_exc())
                                        return False
                    else:
                        # _locale dir doesn't exist let's just go...
                        updatelog('_locale directory doesn\'t exist.. dir: ' + locale_dir)
                        return False
                else:
                    return manifest_name
            except Exception as e:
                updatelog('No name in on manifest.json ... maybe an invalid extension?')
                logging.error(traceback.format_exc())
                return False
        except Exception as e:
            updatelog('Something went wrong while loading manifest json [GetNameFromManifest]')
            updatelog('Error: ' + str(e))
            logging.error(traceback.format_exc())
            return False

def GetDescriptionFromManifest(manifest_file):
    # Get's the desc of an extension from manifest file
    if os.path.isfile(manifest_file):
        # Path is valid and it's a manifest file
        extension_path = helper.fixpath(manifest_file.replace('manifest.json', ''))
        manifest_content = open(manifest_file, 'r', encoding="utf8")
        manifest_content = manifest_content.read()

        try:
            # load the json data
            manifest_json = json.loads(manifest_content)

            try:
                manifest_desc = manifest_json['description']
                if '__MSG_' in manifest_desc:
                    # This is the whole reason i created this function...
                    updatelog('Getting manifest description from locale file: ' + extension_path)
                    manifest_message = re.findall('__MSG_(.*?)__', manifest_desc)[0]
                    locale_dir = helper.fixpath(extension_path + '/_locales/')
                    if os.path.isdir(locale_dir):
                        # locale directory exists let' s grab our thing
                        try:
                            # get the default locale from manifest
                            default_locale = manifest_json['default_locale']
                            en_locale_file = helper.fixpath(locale_dir + '/' + default_locale + '/messages.json')
                            updatelog('Default Locale: ' + default_locale)
                        except Exception as e:
                            # use hardcoded en
                            en_locale_file = helper.fixpath(locale_dir + '/en/messages.json')
                        if os.path.isfile(en_locale_file):
                            # en locale file found let's grab the desc
                            en_locale_content = open(en_locale_file, 'r', encoding="utf8")
                            try:
                                en_locale_content = json.loads(en_locale_content.read())
                                string_content = str(en_locale_content)
                                ext_desc = ''
                                if manifest_message in string_content:
                                    ext_desc = en_locale_content[manifest_message]['message']
                                    updatelog('Extension description grabbed from default locale file.. description: ' + ext_desc)
                                    return ext_desc
                                else:
                                    updatelog('Could not find description')
                                    return False

                            except Exception as e:
                                updatelog('Something went wrong while reading or parsing default locale file...')
                                logging.error(traceback.format_exc())
                                return False
                        else:
                            # en locale not found let's just get the first one we find and be done with it
                            ldirs = os.listdir(locale_dir)
                            for dir in ldirs:
                                if os.path.isfile(helper.fixpath(locale_dir + '/' + dir + '/messages.json')):
                                    locale_content = open(helper.fixpath(locale_dir + '/' + dir + '/messages.json'), 'r', encoding="utf8")
                                    try:
                                        en_locale_content = json.loads(locale_content.read())
                                        if manifest_message in locale_content:
                                            ext_desc = en_locale_content[manifest_message]['message']
                                            updatelog('Extension description grabbed from ' + dir + ' locale file.. description: ' + ext_desc)
                                            return ext_desc
                                        else:
                                            updatelog('Could not find description')
                                            return False

                                    except Exception as e:
                                        updatelog('Something went wrong while reading or parsing en locale file...')
                                        logging.error(traceback.format_exc())
                                        return False
                    else:
                        # _locale dir doesn't exist let's just go...
                        updatelog('_locale directory doesn\'t exist.. dir: ' + locale_dir)
                        return False
                else:
                    return manifest_desc
            except Exception as e:
                updatelog('No description in on manifest.json ... maybe an invalid extension?')
                logging.error(traceback.format_exc())
                return False
        except Exception as e:
            updatelog('Something went wrong while loading manifest json [GetDescriptionFromManifest]')
            updatelog('Error: ' + str(e))
            logging.error(traceback.format_exc())
            return False

def get_result_info(analysis_id):
    '''
    GET INFO ABOUT A SPECIFIC ANALYSIS INFO
    RESPONSE = [TRUE/FALSE, JSON_LOADED_RESULT/ERROR_MSG]
    '''
    global reportids, report_index, reports_path
    if reportids == {}:
        # index not loaded.. let's load it up
        indexs = open(report_index, 'r', encoding='utf-8')
        indexs = json.loads(indexs.read())
        reportids = indexs

    reports = reportids['reports']
    if analysis_id in str(reports):
        for report in reports:
            if report['id'] == analysis_id:
                report['report_directory'] = helper.fixpath(report['report_directory'].replace('<reports_path>', reports_path).replace('\\', '/'))
                return [True, report]
        return [False, 'Analysis ID mismatch: {0}'.format(analysis_id)]
    else:
        return [False, 'Analysis ID {0} not found in result index!'.format(analysis_id) ]


def clear_lab():
    '''
    Deletes all the contents of lab
    Response = [True/False, Success_msg/err_msg]
    '''
    global lab_path
    if os.path.isdir(lab_path):
        updatelog('Lab directory found... deleting it!')
        try:
            shutil.rmtree(lab_path)
            updatelog('lab directory deleted successfully! Creating new directory...')
            try:
                os.mkdir(lab_path)
                updatelog('New lab directory created!')
                return [True, 'Lab successfully cleared!']
            except Exception as e:
                err_msg = 'Error: {0} encountered while creating empty lab directory!'.format(str(e))
                updatelog(err_msg)
                logging.error(traceback.format_exc())
                return[False, err_msg]
        except Exception as e:
            err_msg = 'Error {0} encountered while deleting lab directory'.format(str(e))
            updatelog(err_msg)
            logging.error(traceback.format_exc())
            return[False, err_msg]
    else:
        updatelog('No lab directory found! Creating a new directory')
        try:
            os.mkdir(lab_path)
            return [True, 'Empty lab directory created successfully!']
        except Exception as e:
            err_msg = 'Error: {0} encountered while creating empty lab directory!'.format(str(e))
            updatelog(err_msg)
            logging.error(traceback.format_exc())
            return[False, err_msg]

def handle_exit():
    '''
    Save logs and exit
    '''
    global raw_log, log_file
    try:
        with open(log_file, 'a', encoding='utf-8') as lf:
            lf.write(raw_log)
    except:
        pass
    os._exit(0)

def signal_handler(sig, frame):
    # Handle Ctrl+c
    print('\n[i] Shutting down...')
    handle_exit()

signal.signal(signal.SIGINT, signal_handler)


# ==========================================
# FROM: core/downloader.py
# ==========================================

"""
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
"""







class ExtensionDownloader:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
        }
        self.lab_path = core.lab_path
        # Use more recent Chrome version as in the JS implementation
        self.chrome_version = "121.0.0.0"
        self.nacl_arch = "x86-64"

    def _download_file(self, url: str, save_path: Path) -> bool:
        """Enhanced download method with additional error handling and retries."""
        try:
            request = urllib.request.Request(url, headers=self.headers)

            # Use certifi CA bundle to fix SSL certificate verification on Windows/Linux
            ssl_context = ssl.create_default_context(cafile=certifi.where())
            response = urllib.request.urlopen(request, context=ssl_context)
            while response.geturl() != url:
                url = response.geturl()
                request = urllib.request.Request(url, headers=self.headers)
                response = urllib.request.urlopen(request, context=ssl_context)

            save_path.write_bytes(response.read())
            core.updatelog(f"Extension downloaded successfully: {save_path}")
            return True

        except urllib.error.HTTPError as e:
            core.updatelog(f"HTTP Error: {e.code} - {e.reason}")
            return False
        except urllib.error.URLError as e:
            core.updatelog(f"URL Error: {str(e.reason)}")
            return False
        except Exception as ex:
            core.updatelog(f"Download failed: {str(ex)}")
            return False

    def _download_extension(self, url: str, save_name: str, extension_type: str) -> Optional[str]:
        """Handles the downloading of both Chrome and Firefox extensions."""
        save_path = Path(self.lab_path) / f"{save_name}.{extension_type}"
        core.updatelog(f"Download URL: {url}")
        if self._download_file(url, save_path):
            return save_name
        return None

    def _extract_edge_id(self, url: str) -> Optional[str]:
        """Extract Edge extension ID from URL."""
        parsed_url = urlparse(url)

        # Try getting ID from path
        if '/detail/' in parsed_url.path:
            path_parts = [p for p in parsed_url.path.split('/') if p]
            if len(path_parts) >= 3:
                return path_parts[-1].split('?')[0]

        # Try getting ID from query parameters
        if parsed_url.query:
            query_params = dict(parse_qsl(parsed_url.query))
            if 'x' in query_params and 'id%3D' in query_params['x']:
                return query_params['x'].split('id%3D')[1].split('%')[0]

        return None

    def _extract_chrome_id(self, url: str) -> Optional[str]:
        """Extract Chrome extension ID from URL."""
        from urllib.parse import urlparse
        # Handle both old and new Chrome Web Store URLs
        if 'chrome.google.com/webstore' in url or 'chromewebstore.google.com/detail' in url:
            # Drop query parameters and split by '/'
            path = urlparse(url).path
            return path.rstrip('/').split('/')[-1]
        # If the input is already an ID, return it directly
        elif len(url.split('?')[0].strip()) == 32:  
            return url.split('?')[0].strip()
        return None

    def download_chrome(self, ext_id: str, name: Optional[str] = None) -> Optional[str]:
        """Download Chrome extension using the updated URL format.

        Args:
            ext_id: The Chrome extension ID or URL
            name: Optional name for the saved file

        Returns:
            The name of the saved file if successful, None otherwise
        """
        # Extract extension ID if a URL is provided
        actual_id = self._extract_chrome_id(ext_id)
        if not actual_id:
            core.updatelog('Invalid Chrome extension ID or URL')
            return None

        save_name = name if name else actual_id

        dl_url = (
            "https://clients2.google.com/service/update2/crx?"
            "response=redirect&"
            f"prodversion={self.chrome_version}&"
            f"x=id%3D{actual_id}%26installsource%3Dondemand%26uc&"
            f"nacl_arch={self.nacl_arch}&"
            "acceptformat=crx2,crx3"
        )

        return self._download_extension(dl_url, save_name, 'crx')

    def download_firefox(self, url: str) -> Optional[str]:
        """Download Firefox extension."""
        if 'addons.mozilla.org' not in url:
            core.updatelog('Invalid Firefox addon URL')
            return None
        try:
            request = urllib.request.Request(url, headers=self.headers)
            # Use certifi CA bundle to fix SSL certificate verification on Windows/Linux
            ssl_context = ssl.create_default_context(cafile=certifi.where())
            with urllib.request.urlopen(request, context=ssl_context) as response:
                source_code = response.read().decode('utf-8')

            xpi_matches = re.findall(
                r'<a class="Button Button--action AMInstallButton-button Button--puffy" href="(.*?).xpi?',
                source_code
            )

            if not xpi_matches:
                core.updatelog('Could not find XPI download link')
                return None

            xpi_file = f"{xpi_matches[0]}.xpi"
            name = xpi_file.split('/')[-1]

            core.updatelog(f"Found XPI file: {xpi_file}")
            return self._download_extension(xpi_file, name, 'xpi')

        except Exception as ex:
            core.updatelog(f"Error processing Firefox addon: {str(ex)}")
            return None

    def download_edge(self, url: str) -> Optional[str]:
        """Download Microsoft Edge extension."""
        if 'microsoftedge.microsoft.com' not in url:
            core.updatelog('Invalid Edge addon URL')
            return None

        try:
            ext_id = self._extract_edge_id(url)
            if not ext_id:
                core.updatelog('Could not extract Edge extension ID')
                return None
            dl_url = (
                "https://edge.microsoft.com/extensionwebstorebase/v1/crx?"
                f"response=redirect&x=id%3D{ext_id}%26installsource%3Dondemand%26uc"
            )

            core.updatelog(f"Download URL: {dl_url}")
            return ext_id if self._download_extension(dl_url, ext_id, "crx") else None

        except Exception as e:
            core.updatelog(f'Error downloading Edge extension: {str(e)}')
            return None



# ==========================================
# FROM: core/scans.py
# ==========================================

"""
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
"""



def geoip(ip):
    '''
    Geo-IP Lookup via ipapi.co
    needed parameter = ip = the ip address
    response = [True/False, JSON_RESULT/ERROR_MSG]
    '''
    core.updatelog('Initiating Geo-IP Lookup for address: ' + ip)
    try:
        lookup_url = 'https://ipapi.co/{0}/json'.format(ip)
        lookup = requests.get(lookup_url)
        lookup = lookup.json()
        try:
            if lookup['error']:
                core.updatelog('Geo-IP Lookup failed: ' + lookup['reason'])
                return [False, lookup['reason']]
        except:
            core.updatelog('Geo-IP Lookup successful')
            return [True, lookup]
    except Exception as e:
        logging.error(traceback.format_exc())
        core.updatelog('Geo-IP Lookup failed: ' + str(e))
        return [False, str(e)]
    

def http_headers(url):
    '''
    HTTP Headers lookup
    needed parameter = url = the url to get the http headers of
    response = [True/False, HEADERS_LIST/ERROR_MSG]
    '''
    core.updatelog('Getting HTTP Headers of: ' + url)
    try:
        req = requests.get(url)
        headers = req.headers
        core.updatelog('HTTP Headers successfully acquired!')
        return [True, headers]
    except Exception as e:
        core.updatelog('Error while getting HTTP Headers of {0}! Error: {1}'.format(url, str(e)))
        logging.error(traceback.format_exc())
        return [False, str(e)]

def source_code(url):
    '''
    GET Source Code
    needed parameter = url = the url to get the source code of
    response = [True/False, SOURCE_CODE/ERROR_MSG]
    '''
    core.updatelog('Getting Source code of: ' + url)
    try:
        req = requests.get(url)
        headers = req.text
        core.updatelog('Source code successfully acquired!')
        return [True, headers]
    except Exception as e:
        core.updatelog('Error while getting Source code of {0}! Error: {1}'.format(url, str(e)))
        logging.error(traceback.format_exc())
        return [False, str(e)]

# ==========================================
# FROM: core/intel.py
# ==========================================

"""
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
"""


def extract(contents, relpath):
    '''
    EXTRACTS THE FOLLOWING:
        -> URL
        -> EMAIL
        -> BTC ADDRESS
        -> IPV4, IPV6 ADDRESSES
        -> BASE64 ENCODED STRINGS

    CONTENTS = FILE CONTENT
    RELPATH = RELATIVE PATH (FOR JSON ENTRY IN RESULT)
    '''

    found_urls = [] # URLS -> (http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?
    found_mail = [] # emails -> ([a-zA-Z0-9\.\-_]+(?:@| ?\[(?:at)\] ?)[a-zA-Z0-9\.\-]+(?:\.| ?\[(?:dot)\] ?)[a-zA-Z]+)
    found_btcs = [] # bitcoin address -> [^a-zA-Z0-9]([13][a-km-zA-HJ-NP-Z1-9]{26,33})[^a-zA-Z0-9]
    found_ipv4 = [] # IPv4 addr -> [^a-zA-Z0-9]([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})[^a-zA-Z0-9]
    found_ipv6 = [] # IPV6 -> (([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))(?=\s|$)
    found_b64s = [] # base64 -> (?:[A-Za-z0-9+/]{4}){2,}(?:[A-Za-z0-9+/]{2}[AEIMQUYcgkosw048]=|[A-Za-z0-9+/][AQgw]==)
    found_cmnt = [] # Comments -> ...

    # Check if the file is css and if ignore css is set to true
    if core.ignore_css and relpath.endswith('.css'):
        # return empty result
        core.updatelog('ignore css set to true... ignoring: ' + relpath)
        result = {
                "urls":found_urls, 
                "mails":found_mail, 
                "ipv4":found_ipv4, 
                "ipv6":found_ipv6, 
                "base64":found_b64s, 
                "btc":found_btcs,
                "comments":found_cmnt
            }
        return result
    
    '''
    EXTRACT URLS FROM JS, HTML, CSS AND JSON FILES
    ''' 
    curls = re.findall('(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?', contents)
    for url in curls:
        urlresult = {"file":relpath, "url":url[0]+'://'+url[1]+url[2]}
        if urlresult not in found_urls:
            found_urls.append(urlresult)

    
    '''
    EXTRACT EMAIL IDs FROM JS, HTML, JSON AND CSS FILES
    '''
    if core.extract_email_addresses:
        cmails = re.findall(r'([a-zA-Z0-9\.\-_]+(?:@| ?\[(?:at)\] ?)[a-zA-Z0-9\.\-]+(?:\.| ?\[(?:dot)\] ?)[a-zA-Z]+)', contents)
        for mail in cmails:
            mail = mail.replace('[at]', '@').replace('[dot]','.')
            core.updatelog('Found email address: ' + mail)
            mailarray = {"mail":mail, "file":relpath}
            if mailarray not in found_mail:
                found_mail.append(mailarray)


    '''
    EXTRACT BITCOIN ADDRESSES
    '''
    if core.extract_btc_addresses:
        btc_addresses = re.findall('[^a-zA-Z0-9]([13][a-km-zA-HJ-NP-Z1-9]{26,33})[^a-zA-Z0-9]', contents)
        for btc_address in btc_addresses:
            core.updatelog('Found BTC address: ' + btc_address)
            btcarr = {"address":btc_address, "file":relpath}
            if btcarr not in found_btcs:
                found_btcs.append(btcarr)


    '''
    EXTRACT IPV6 ADDRESSES
    '''
    if core.extract_ipv6_addresses:
        # Use simple pattern to prevent ReDoS, then validate via socket
        ipv6_candidates = re.findall(r'(?<![A-Za-z0-9:])[a-fA-F0-9:]+:[a-fA-F0-9:]+(?![A-Za-z0-9:])', contents)
        import socket
        for cand in ipv6_candidates:
            if cand.count(':') >= 2:
                try:
                    socket.inet_pton(socket.AF_INET6, cand)
                    core.updatelog('Found IP v6 Address: ' + cand)
                    v6arr = {"address":cand, "file":relpath}
                    if v6arr not in found_ipv6:
                        found_ipv6.append(v6arr)
                except Exception:
                    pass


    '''
    EXTRACT IPV4 ADDRESSES
    '''
    if core.extract_ipv4_addresses:
        ipv4s = re.findall(r'[^a-zA-Z0-9]([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})[^a-zA-Z0-9]', contents)
        for ipv4 in ipv4s:
            core.updatelog('Found IP v4 Address: ' + ipv4)
            iparr = {"address":ipv4, "file":relpath}
            if iparr not in found_ipv4:
                found_ipv4.append(iparr)


    '''
    EXTRACT BASE64 ENCODED STRINGS
    '''
    if core.extract_base64_strings:
        import base64 as _base64lib
        # Only match base64 strings that end with = or == padding (filters out plain English words)
        b64_candidates = re.findall(r'[A-Za-z0-9+/]{16,}={1,2}', contents)
        for cand in b64_candidates:
            try:
                _base64lib.b64decode(cand)
                core.updatelog('Found base64 encoded string: ' + cand[:50])
                stringarr = {"string": cand, "file": relpath}
                if stringarr not in found_b64s:
                    found_b64s.append(stringarr)
            except Exception:
                pass


    '''
    EXTRACT COMMENTS FROM JS AND HTML FILES
    '''
    if core.extract_comments:
        if relpath.endswith(('.html', '.js', '.htm', '.css')):
            # Limit block-comment match to 2000 chars to prevent slow scans on huge minified files
            c1 = re.findall(r'/\*.{0,2000}?\*/|//(.*?)\n', contents)
            c2 = re.findall(r'/\* *([^"\']{1,500}?) *\*/', contents)
            c3 = re.findall(r'<!-- *(.{1,500}?) *-->', contents)
            c1.extend(c2)
            c1.extend(c3)
            seen_comments = set()
            for comment in c1:
                if comment and comment.strip():
                    comment = helper.escape(comment)  # escape html
                    core.updatelog('Extracted comment: ' + comment[:30] + ' ...')
                    cmarray_key = comment + '|' + relpath
                    if cmarray_key not in seen_comments:
                        seen_comments.add(cmarray_key)
                        found_cmnt.append({"comment": comment, "file": relpath})
    
    result = {
                "urls":found_urls, 
                "mails":found_mail, 
                "ipv4":found_ipv4, 
                "ipv6":found_ipv6, 
                "base64":found_b64s, 
                "btc":found_btcs,
                "comments":found_cmnt
            }
    return result

# ==========================================
# FROM: core/ip2country.py
# ==========================================

"""
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
"""

def get_country(ip):
    '''
    Gets Country and country code from given IP.
    Parameters = ip = ip address for lookup
    Response = [True, {country_code}, {country_name}] or [False, {ERR_MSG}]
    Needs maxminddb for fast performance
    '''
    core.updatelog('Getting country from IP: ' + ip)
    try:
        # If maxminddb module is installed we don't have to query online services to get the country code hence saving a lot of time
        import maxminddb
        try:
            core.updatelog('Getting country from local DB')
            reader = maxminddb.open_database(helper.fixpath(core.path + '/db/geoip.mmdb'))
            ip_info = reader.get(ip)
            if ip_info is None or 'country' not in ip_info or ip_info['country'] is None:
                core.updatelog('No country data for IP (private/reserved): ' + ip)
                return [False, 'No country data available for this IP']
            iso_code = ip_info['country']['iso_code'].lower()
            country = ip_info['country']['names']['en']
            return [True, iso_code, country]
        except Exception as e:
            core.updatelog('Something went wrong while getting country from ip {0}! Error: {1}'.format(ip, str(e)))
            logging.error(traceback.format_exc())
            return [False, str(e)]
    except:
        core.updatelog('maxminddb module not installed! Using online service to get Country from IP')
        core.updatelog('To save time in future analysis; install maxminddb by: pip3 install maxminddb')
        gip = geoip(ip)
        if gip[0]:
           geoip = gip[1]
           return [True, geoip['country'].lower(), geoip['country_name']] 
        else:
            return [False, gip[1]]



# ==========================================
# FROM: core/virustotal.py
# ==========================================

"""
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
"""


pub_vt = []
## add extra virustotal apis if you have any! helps in faster scan. format: pub_vt = ['api1', 'api2']


virustotal_api = core.virustotal_api

def scan_url(url):
    # Scan the url
    global pub_vt, virustotal_api
    if virustotal_api == "":
        # get a random virustotal api
        virustotal_api = random.choice(pub_vt)
        core.updatelog('Using api: ' + virustotal_api)
    vturl = 'https://www.virustotal.com/vtapi/v2/url/scan'
    params = {'apikey': virustotal_api, 'url':url}
    response = requests.post(vturl, data=params)
    response = response.json()
    if response['response_code'] == 1:
        core.updatelog('URL queued for scan! getting report after 10 seconds...')
        time.sleep(10)
        newurl = 'https://www.virustotal.com/vtapi/v2/url/report'
        newparams = {'apikey': virustotal_api, 'resource':url}
        newresponse = requests.get(newurl, params=newparams)
        finalresp = newresponse.json()
        if finalresp['response_code'] == 1:
            print('{0}/{1} - {2}'.format(finalresp['positives'], finalresp['total'], finalresp['permalink']))
        else:
            return [False, 'Reached maximum rate limit for virustotal api! If you are using your own key, please wait a minute and try again']
    else:
        return [False, 'Reached maximum rate limit for virustotal api! If you are using your own key, please wait a minute and try again']


def scan_domain(domain):
    global pub_vt
    # get a random virustotal api
    tvirustotal_api = random.choice(pub_vt)
    core.updatelog('Using api: ' + tvirustotal_api)
    try:
        url = 'https://www.virustotal.com/vtapi/v2/domain/report'
        params = {'apikey':tvirustotal_api,'domain':domain}
        response = requests.get(url, params=params)
        response = response.json()
        if response['response_code'] == 1:
            return [True, response]
        else:
            return [False, 'Either rate limited or something else went wrong while getting domain report from virustotal']
    except Exception as e:
        logging.error(traceback.format_exc())
        return [False, str(e)]


def domain_batch_scan(domains):
    # used only when there is only one virustotal api and the pub_vt list is empty
    batch_result = {}
    total_domains = len(domains)

    if total_domains > 4:
        # virustotal has limitation of 4 scans per minute for an api so if the domain count is less then 4 we have nothing to wait
        gotta_wait = True
    else:
        gotta_wait = False

    if core.virustotal_api != "":
        # Do batch scan
        for index,domain in enumerate(domains):
            real_index = index + 1
            if gotta_wait and real_index%4 == 0:
                core.updatelog('Sleeping for 1 minute... virustotal api limit reached!')
                # Sleep for 60 seconds.. I really hate it but it seems there's no other way around other then you adding a bunch of diff apis to the above list
                time.sleep(60)
            core.updatelog('Getting virustotal report for: ' + domain)
            try:
                url = 'https://www.virustotal.com/vtapi/v2/domain/report'
                params = {'apikey':core.virustotal_api,'domain':domain}
                response = requests.get(url, params=params)
                response = response.json()
                if response['response_code'] == 1:
                    batch_result[domain] = [True, response]
                else:
                    batch_result[domain] = [False, {"error":"Either rate limited or something else went wrong while getting domain report from virustotal"}]
            except Exception as e:
                logging.error(traceback.format_exc())
                batch_result[domain] = [False, str(e)]
    else:
        for _domain in domains:
            core.updatelog('Skipping virustotal domain scan for {0}. Reason: No virustotal api added!'.format(_domain))
            batch_result[_domain] = [False, "No virustotal api found"]

    return batch_result


# ==========================================
# FROM: core/localextensions.py
# ==========================================

"""
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
"""


class GetLocalExtensions():
    def __init__(self):
        if sys.platform == 'win32':
            self.os = 'windows'
        elif sys.platform == 'darwin':
            self.os = 'osx'
        elif sys.platform == 'linux' or sys.platform == 'linux2':
            self.os = 'linux'
        else:
            self.os = 'unknown'
        
        self.user_directory = os.path.expanduser('~')
        core.updatelog('User Directory: ' + self.user_directory)
        self.chrome_extensions = []
        self.firefox_extensions = []
        self.brave_extensions = []
        self.vivaldi_extensions = []
    
    def extract_chromium_plugins(self, parent_dir):
        ret_list = []

        extension_dirs = os.listdir(parent_dir)
        for extension_dir in extension_dirs:
            extension_path = os.path.join(parent_dir, extension_dir)
            
            if not os.path.isdir(extension_path):
                core.updatelog("Invalid extension directory: " + extension_path)
                continue
            
            extension_vers = os.listdir(extension_path)
            
            for ver in extension_vers:
                manifest_file = helper.fixpath(extension_path + "/" + ver + "/manifest.json")
                if not os.path.isfile(manifest_file):
                    core.updatelog("Invalid extension directory: " + extension_path)
                    continue
                ext_name = core.GetNameFromManifest(manifest_file)
                if ext_name:
                    ext_version = ver.split('_')[0]
                    ext_name = ext_name + ' version ' + ext_version
                    # small hack to not let commas fuck around with the path
                    ext_name = ext_name.replace(",", "&#44;")
                    ret_list.append(ext_name + ',' + helper.fixpath(extension_path + "/" + ver))

        return ret_list

    def googlechrome(self):

        # TODO: add support for mac os

        chrome_directory = ""
        if self.os == 'windows':
            chrome_directory = helper.fixpath(self.user_directory + '\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Extensions')
        elif self.os == 'linux':
            chrome_directory = helper.fixpath(self.user_directory + '/.config/google-chrome/Default/Extensions')
        elif self.os == 'osx':
        	chrome_directory = helper.fixpath(self.user_directory + '/Library/Application Support/Google/Chrome/Profile 1/Extensions')
        
        if chrome_directory != "":
            if os.path.isdir(chrome_directory):
                core.updatelog('Found Google chrome extension directory: ' + chrome_directory)
                return self.extract_chromium_plugins(chrome_directory)
            else:
                core.updatelog('Could not find google chrome directory!')
                return False
        else:
            core.updatelog('Unsupported OS')

    def vivaldi_local_extensions_check(self):
        vivaldi_dir = ""
        if self.os == 'windows':
            vivaldi_dir = helper.fixpath(self.user_directory + '\\AppData\\Local\\Vivaldi\\User Data\\Default\\Extensions')
        
        if vivaldi_dir == "":
            core.updatelog('Unsupported OS')
            return

        if not os.path.isdir(vivaldi_dir):
            core.updatelog("Couldn't find Vivaldi Extension directory!")
            return

        # -- 
        core.updatelog('Found Vivaldi extension directory: ' + vivaldi_dir)
        return self.extract_chromium_plugins(vivaldi_dir)


    def braveLocalExtensionsCheck(self):
        brave_directory = ""
        
        if self.os == 'windows':
            brave_directory = helper.fixpath(self.user_directory + '\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Extensions')
        elif self.os == 'linux':
            brave_directory = helper.fixpath(self.user_directory + '/.config/BraveSoftware/Brave-Browser/Default/Extensions')
        
        if brave_directory != "":
            if os.path.isdir(brave_directory):
                core.updatelog('Found Brave extension directory: ' + brave_directory)
                return self.extract_chromium_plugins(brave_directory)
            else:
                core.updatelog('Could not find Brave extension directory!')
                return False
        else:
            core.updatelog('Unsupported OS')

    def firefox(self):
        # read the profiles.ini
        # check for previous list and create new if not found [list = extanalysis.json]
        # Get a list of all the xpi files
        # Unzip them
        # Get all their names from manifest.json
        # update the list
        firefox_directory = ""
        default_profile_path = ""
        
        if self.os == 'windows':
            firefox_directory = helper.fixpath(self.user_directory + '\\AppData\\Roaming\\Mozilla\\Firefox')
            
            if os.path.isdir(firefox_directory):
                # firfox installed
                firefox_profile = helper.fixpath(firefox_directory + '\\profiles.ini')
                if os.path.isfile(firefox_profile):
                    # found firefox profiles.ini
                    try:
                        firefox_config = configparser.SafeConfigParser()
                        with open(firefox_profile, 'rU') as ini_source:
                            firefox_config.readfp(ini_source)
                        default_profile_path = os.path.normpath(os.path.join(firefox_directory, firefox_config.get('Profile0', 'Path')))
                        core.updatelog('Found firefox profile path: ' + default_profile_path)
                    except Exception as e:
                        core.updatelog('Something went wrong while reading firefox profiles.ini')
                        logging.error(traceback.format_exc())
                        return False
                else:
                    core.updatelog('Could not find profiles.ini ExtAnalysis can\'t analyze local firefox extensions')
                    return False
            else:
                # Could not find firefox directory
                core.updatelog('Firefox installation could not be detected')
                return False
        elif self.os == 'linux':
            firefox_directory = helper.fixpath(self.user_directory + '/.mozilla/firefox/')
            if os.path.isdir(firefox_directory):
                # firfox installed
                firefox_profile = helper.fixpath(firefox_directory + '/profiles.ini')
                if os.path.isfile(firefox_profile):
                    # found firefox profiles.ini
                    try:
                        firefox_config = configparser.SafeConfigParser()
                        with open(firefox_profile, 'rU') as ini_source:
                            firefox_config.readfp(ini_source)
                        default_profile_path = os.path.normpath(os.path.join(firefox_directory, firefox_config.get('Profile0', 'Path')))
                        core.updatelog('Found firefox profile path: ' + default_profile_path)
                    except Exception as e:
                        core.updatelog('Something went wrong while reading firefox profiles.ini')
                        logging.error(traceback.format_exc())
                        return False
                else:
                    core.updatelog('Could not find profiles.ini ExtAnalysis can\'t analyze local firefox extensions')
                    return False
            else:
                # Could not find firefox directory
                core.updatelog('Firefox installation could not be detected')
                return False
        
        if default_profile_path != "":
            if os.path.isdir(default_profile_path):
                # profile path is valid
                firefox_extension_directory = os.path.join(default_profile_path, 'extensions')
                if os.path.join(firefox_extension_directory):
                    unfiltered_files = os.listdir(firefox_extension_directory)
                    xpi_files = []
                    for afile in unfiltered_files:
                        if afile.endswith('.xpi') and os.path.isfile(os.path.join(firefox_extension_directory, afile)):
                            xpi_files.append(afile)
                    core.updatelog('xpi list generated')
                else:
                    core.updatelog('extensions directory could not be found inside firefox default profile')
                    return False
            else:
                core.updatelog('Invalid firefox profile path... Can\'t get local firefox extensions')
                return False
        else:
            core.updatelog('Could not find default profile path for firefox')
            return False

        if xpi_files != []:
            exta_firefox_list = os.path.join(firefox_extension_directory, 'extanalysis.json')
            if os.path.isfile(exta_firefox_list):
                # found previous list
                core.updatelog('Found previous analysis log.. updating with current extensions')
                listed_extensions = []
                list_file = open(exta_firefox_list, 'r', encoding='utf-8')
                list_files = json.loads(list_file.read())
                for list_file in list_files['extensions']:
                    listed_extensions.append(list_file)
                for xpi_file in xpi_files:
                    if xpi_file not in listed_extensions:
                        core.updatelog('Inserting ' + xpi_file + ' into list')
                        self.createFirefoxListing(firefox_extension_directory, xpi_file)
                # return True
            else:
                core.updatelog('Creating ExtAnalysis list file')
                list_file = open(exta_firefox_list, 'w+', encoding='utf-8')
                list_file.write('{"extensions":{}}')
                list_file.close()
                core.updatelog('Updating list file with all xpi file infos')
                for xpi_file in xpi_files:
                    core.updatelog('Inserting ' + xpi_file + ' into list')
                    self.createFirefoxListing(firefox_extension_directory, xpi_file)
                # return True
        else:
            core.updatelog('No installed firefox extensions found!')
            return False
        
        # Read the final list and then create return list and return it
        firefox_extensions_list = []
        read_list = open(exta_firefox_list, 'r', encoding='utf-8')
        read_list = json.loads(read_list.read())
        if read_list['extensions'] != {}:
            # There are some extensions
            for fext in read_list['extensions']:
                prepare_to_insert = read_list['extensions'][fext]['name'] + ',' + read_list['extensions'][fext]['file']
                firefox_extensions_list.append(prepare_to_insert)
            return firefox_extensions_list
        else:
            core.updatelog('ExtAnalysis could not find any local firefox extensions')

    def createFirefoxListing(self, extension_directory, xpi_file):
        list_file = os.path.join(extension_directory, 'extanalysis.json')
        xpi_directory = os.path.join(extension_directory, xpi_file)
        if os.path.isfile(xpi_directory) and os.path.isfile(list_file):
            # extract the xpi file get name from manifest and delete the extract directory
            extract_directory = os.path.join(extension_directory, 'extanalysis_temp_directory_delete_if_not_done_automatically')
            try:
                core.updatelog('Trying to unzip xpi: ' + xpi_file)
                zip_contents = zipfile.ZipFile(xpi_directory, 'r')
                zip_contents.extractall(extract_directory)
                zip_contents.close()
                core.updatelog('Unzipped xpi successfully: ' + xpi_directory)
                xpi_manifest = os.path.join(extract_directory, 'manifest.json')
                if os.path.isfile(xpi_manifest):
                    ext_name = core.GetNameFromManifest(xpi_manifest)
                    if ext_name != False or ext_name != None:
                        # DO shits
                        core.updatelog(xpi_file + ' has the name: ' + ext_name + ' adding it to the list')
                        list_content = open(list_file, 'r', encoding='utf-8')
                        list_content = list_content.read()
                        list_content = json.loads(list_content)
                        list_content['extensions'][xpi_file] = ({"name":ext_name, "file":xpi_directory})
                        list_write = open(list_file, 'w+', encoding='utf-8')
                        list_write.write(json.dumps(list_content, indent=4, sort_keys=True))
                        list_write.close()
                        core.updatelog('List updated! Deleting temp extract directory')
                        shutil.rmtree(extract_directory)
                        core.updatelog('Removed temp extract directory')
                        return True
                    else:
                        core.updatelog('Could not file extension name hence it will not be added to the list')
                else:
                    core.updatelog('No manifest file found after extracting xpi! Deleting temp extract directory')
                    shutil.rmtree(extract_directory)
                    core.updatelog('Removed temp extract directory')
                    return False
            except Exception as e:
                core.updatelog('Error unzipping xpi file: ' + xpi_directory)
                logging.error(traceback.format_exc())
                return False

def analyzelocalfirefoxextension(path):
    if os.path.isfile(path) and path.endswith('.xpi'):
        # Extract the .xpi file to a temp directory in lab directory
        # Analyze the extracted directory
        # delete the temp directory
        extract_directory = helper.fixpath(core.lab_path + '/temp_extract_directory')

        try:
            core.updatelog('Unzipping ' + path + ' to: ' + extract_directory)
            zip_contents = zipfile.ZipFile(path, 'r')
            zip_contents.extractall(extract_directory)
            zip_contents.close()
            core.updatelog('Unzipping complete')
        except Exception as e:
            helper.fixpath('Something went wrong while unzipping ' + path + ' to ' + extract_directory)
            logging.error(traceback.format_exc())
            return False
        
        analysis_status = analysis.analyze(extract_directory, 'Local Firefox Extension')

        if 'error:' in analysis_status:
            core.updatelog('Something went wrong while analysis... deleting temporary extract directory')
        else:
            core.updatelog('Scanning complete... Deleting temporary extract directory')
        
        shutil.rmtree(extract_directory)
        core.updatelog('Successfully deleted: ' + extract_directory)
        return analysis_status

    else:
        core.updatelog('[analyzelocalfirefoxextension] Invalid local firefox extension path: ' + path)


# ==========================================
# FROM: core/result.py
# ==========================================

"""
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
"""


class createresult:

    def __init__(self, directory):
        self.current_file_number = 0
        self.current_directory_number = 0
        self.current_url_number = 0
        self.files = []
        self.dirs = []
        self.urls = []
        self.nodes = 'var nodes = new vis.DataSet(['
        self.edges = 'var edges = new vis.DataSet(['
        self.directory = directory
        self.extension_name = core.report['name']
        self.list_status = self.list(directory)

    def list(self, directory, parent=0):
        # This function is the one that helps create the graph for real
        # sub_directories list contains all the directories inside the current directory which we will use later
        # sub_directory = path,name
        sub_directories = []

        if self.current_directory_number == 0:
            # This means that this is the first time we're doing the directory listing so let's set directory 0 to the extension
            self.dirs.append({'id':'EXTAD0', 'name':self.extension_name, 'type':'extension', 'path':'/', 'parent':'none'})
            self.current_directory_number += 1

        if os.path.isdir(directory):
            # The given path is a directory and we will continue
            # core.updatelog('FUNCTION LIST IS EXECUTING ON: ' + directory)
            dirlist = os.listdir(directory)

            for folder in dirlist:
                # let's get the path...
                # print('Checking file: ' + folder)
                route = os.path.join(directory, folder)
                if os.path.isdir(route):
                    # Directory detected let's add it to the sub_directories list
                    sub_directories.append(route + ',' + str(self.current_directory_number))
                    self.dirs.append({'id':'EXTAD' + str(self.current_directory_number), 'name':folder, 'type':'directory', 'path':route, 'parent':'EXTAD' + str(parent)})
                    self.current_directory_number += 1
                else:
                    # this is a file let's classify it and add it to the list
                    if folder.endswith(('.html', '.htm')):
                        file_type = 'html'
                    elif folder.endswith('.js'):
                        file_type = 'js'
                    elif folder.endswith('.css'):
                        file_type = 'css'
                    elif folder.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.svg')):
                        file_type = 'static'
                    elif folder.endswith('.json'):
                        file_type = 'json'
                    else:
                        file_type = 'other'

                    self.files.append({'id':'EXTAF' + str(self.current_file_number), 'name':folder, 'path':route, 'type': file_type, 'parent':'EXTAD' + str(parent)})
                    self.current_file_number += 1
                # now that we are done with all the files let's go through the sub directories and work them out

            for sub_directory in sub_directories:
                # process all the sub directories
                # core.updatelog('Processing SUBDIRECTORY: ' + sub_directory)
                sub_directory = sub_directory.split(',')
                sub_parent = sub_directory[1]
                sub_directory = sub_directory[0]
                self.list(sub_directory, sub_parent)
        else:
            # Given path is not a directory hence no need for continuing
            return False

    def creategraphdata(self):
        if self.list_status != False:
            # Extract urls from all html, json, js files
            for file in self.files:
                if file['type'] == 'json' or file['type'] == 'html' or file['type'] == 'js':
                    file_path = file['path']
                    file_id = file['id']
                    file_urls = []
                    try:
                        core.updatelog('Trying to extract urls from: ' + file_path)
                        file_urls = core.extract_urls(file_path)
                        if file_urls != [] and file_urls != False:
                            for file_url in file_urls:
                                self.urls.append({'id':'EXTAU' + str(self.current_url_number), 'parent':file_id, 'type':'url', 'name':file_url})
                                self.current_url_number += 1
                    except Exception as e:
                        core.updatelog('Skipped getting URL from file: ' + file_path + ' Error: ' + str(e))
                        logging.error(traceback.format_exc())
            # TODO: Clean this mess and use format
            for file in self.files:
                # print('Doing File: ' + file + ' parent: ' + file['parent'])
                #prepare_node = '\n{ id: "{0}", label: "{1}", group: "{2}", cid: "{3}" },'.format(file['id'], file['name'], file['type'], file['parent'])
                prepare_node = '\n{id: "' + file['id'] + '", label: "' + file['name'] + '", group: "' + file['type'] + '", cid: "'+file['parent']+'"},'
                self.nodes += prepare_node
                #prepare_edge = '\n{ from: "{0}", to: "{1}", color:{color:\'#fff\', highlight:\'#89ff00\'} },'.format(file['parent'], file['id'])
                prepare_edge = '\n{from: "' + file['parent'] + '", to: "' + file['id'] + '", color:{color:\'#fff\', highlight:\'#89ff00\'}},'
                self.edges += prepare_edge

            for file in self.dirs:
                if file['parent'] == 'none' and file['id'] == 'EXTAD0':
                    # this is the parent directory i.e the extension
                    #prepare_node = '\n{ id: "{0}", label: "{1}", group: "{2}" },'.format(file['id'], file['name'], file['type'])
                    prepare_node = '\n{id: "' + file['id'] + '", label: "' + file['name'] + '", group: "' + file['type'] + '"},'
                    self.nodes += prepare_node
                else:
                    #prepare_node = '\n{ id: "{0}", label: "{1}", group: "{2}", cid: "{3}" },'.format(file['id'], file['name'], file['type'], file['parent'])
                    prepare_node = '\n{id: "' + file['id'] + '", label: "' + file['name'] + '", group: "' + file['type'] + '", cid: "'+file['parent']+'"},'
                    self.nodes += prepare_node
                    #prepare_edge = '\n{ from: "{0}", to: "{1}", color:{color:\'#fff\', highlight:\'#89ff00\'} },'.format(file['parent'], file['id'])
                    prepare_edge = '\n{from: "' + file['parent'] + '", to: "' + file['id'] + '", color:{color:\'#fff\', highlight:\'#89ff00\'}},'
                    self.edges += prepare_edge

            for url in self.urls:
                #prepare_node = '\n{ id: "{0}", label: "{1}", group: "{2}", cid: "{3}"},'.format(url['id'], url['name'], url['type'], url['parent'])
                prepare_node = '\n{id: "' + url['id'] + '", label: "' + url['name'] + '", group: "' + url['type'] + '", cid: "'+url['parent']+'"},'
                self.nodes += prepare_node
                #prepare_edge = '\n{ from: "{0}", to: "{1}", color:{color:\'#fff\', highlight:\'#89ff00\'} },'.format(url['parent'], url['id'])
                prepare_edge = '\n{from: "' + url['parent'] + '", to: "' + url['id'] + '", color:{color:\'#fff\', highlight:\'#89ff00\'}},'
                self.edges += prepare_edge

            self.nodes += '\n]);'
            self.edges += '\n]);'
            # print(self.nodes  + '\n\n\n\n\n\n\n' + self.edges)
            core.updatelog('Graph data creation complete!')
        else:
            core.updatelog('Graph data creation unsuccessful!')
            return False

    def copysource(self, result_directory):
        # copies all the json, html, css and js files and saves them to the result directory
        # create content for the source.json file
        source_json = {}

        # Copies all the json, css, js files to the result directory for future reference
        for file in self.files:
            if file['type'] == 'json' or file['type'] == 'html' or file['type'] == 'css' or file['type'] == 'js':
                file_path = file['path']
                new_path = helper.fixpath(result_directory + '/' + file['name'] + '.src')
                file_name = file['name']
                if os.path.isfile(file_path):
                    # Checks if file present
                    shutil.copyfile(file_path, new_path)
                    core.updatelog('Copied ' + file_path + ' to ' + new_path)
                    # append this to source_json dict
                    rel_path = os.path.relpath(file_path, self.directory)
                    file_size = str(os.path.getsize(file_path) >> 10) + ' KB'
                    if file['type'] == 'js':
                        # Retire js scan
                        core.updatelog('Running retirejs vulnerability scan on: ' + file_name)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as fc:
                                file_content = fc.read()
                                rjs_scan = retirejs.scan_file_content(file_content)
                                core.updatelog('Scan complete!')
                        except Exception as e:
                            core.updatelog('Error {0} while running retirejs scan on {1}'.format(str(e), file_name))
                            rjs_scan = []
                        source_json[file['id']] = ({'id':file['id'], 'file_name':file_name, 'location':new_path, 'relative_path':rel_path, 'file_size':file_size, 'retirejs_result':rjs_scan})
                    else:
                        source_json[file['id']] = ({'id':file['id'], 'file_name':file_name, 'location':new_path, 'relative_path':rel_path, 'file_size':file_size})

        # write all the changes to source.json
        source_file = helper.fixpath(result_directory + '/source.json')
        sf = open(source_file, 'w+', encoding='utf-8')
        sf.write(json.dumps(source_json, indent=4, sort_keys=True))
        sf.close()
        core.updatelog('Saved sources to: ' + source_file)
        return True

    def savereport(self):
        try:
            # Gen scan id
            report = core.report
            reportids = core.reportids

            curid = 'EXA' + time.strftime("%Y%j%H%M%S", time.gmtime())
            core.updatelog('Saving Analysis with ID: ' + curid)
            #saveas = curid + '.json'

            # create result directory
            result_directory = os.path.join(core.reports_path, curid)
            if not os.path.exists(result_directory):
                os.makedirs(result_directory)
                core.updatelog('Created Result directory: ' + result_directory)

            # create the basic report json file: extanalysis_report.json
            report_file = helper.fixpath(result_directory + '/extanalysis_report.json')
            f = open(report_file, 'w+', encoding='utf-8')
            reportfinal = json.dumps(report, sort_keys=True, indent=4)
            f.write(reportfinal)
            f.close()
            core.updatelog('Saved report file: ' + report_file)

            # get file list and create the graph
            graph_data_stat = self.creategraphdata()
            if graph_data_stat != False:
                graph_file = helper.fixpath(result_directory + '/graph.data')
                graph_file_create = open(graph_file, 'w+', encoding='utf-8')
                graph_file_create.write(self.nodes + '\n' + self.edges)
                core.updatelog('Saved graph data to: ' + graph_file)
            else:
                core.updatelog('Could not save graph data!')

            # save the source files
            # print(result_directory)
            self.copysource(result_directory)

            '''
            make an entry in the reports index file
            '''
            # use <reports_path> as a variable!
            relative_result_path = result_directory.replace(core.reports_path, '<reports_path>')
            reportindex = {"name":report['name'], "version":report['version'], "id": curid, "report_directory":relative_result_path, "time":time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())}
            reportids['reports'].append(reportindex)
            indexfile = core.report_index
            g = open(indexfile, 'w+', encoding='utf-8')
            indexfinal = json.dumps(reportids, sort_keys=True, indent=4)
            g.write(indexfinal)
            g.close()
            core.updatelog('Updated report index')

            # Clear global report value for new scan
            core.report = {}

            return(curid)
        except Exception as e:
            logging.error(traceback.format_exc())
            print('Something went wrong while saving result. Error: ' + str(e))

def clearAllResults():
    # Deletes all directories inside reports folder
    # create new reports.json file with the following content {"reports": []}
    core.updatelog('Clearing all results!')
    all_reports = core.reportids
    report_index = core.report_index
    if all_reports == {}:
        ri = open(report_index, 'r')
        ri = ri.read()
        all_reports = core.report_index = json.loads(ri)
    for report in all_reports['reports']:
        core.updatelog('Deleting analysis #{0} - {1}'.format(report['id'], report['name']))
        report_dir = report['report_directory'].replace('<reports_path>', core.reports_path)
        if os.path.isdir(report_dir):
            try:
                shutil.rmtree(report_dir)
                core.updatelog('Analysis #{0} deleted successfully!'.format(report['id']))
            except Exception as e:
                core.updatelog('Something went wrong while deleting Report directory {0}. Error: {1}'.format(report_dir, str(e)))
                logging.error(traceback.format_exc())
        else:
            core.updatelog('Report directory ({1}) of #{0} not found!'.format(report['id'], report_dir))
    core.updatelog('All individual result directories deleted! Updating report index...')
    try:
        i = open(report_index, 'w+', encoding='utf-8')
        js = {"reports": []}
        i.write(json.dumps(js, indent=4, sort_keys=True))
        i.close()
        core.reportids = js
        core.updatelog('Index file successfully created: ' + report_index)
        return True
    except Exception as e:
        core.updatelog('Something went wrong while updating {0}! Error: {1}'.format(report_index, str(e)))
        logging.error(traceback.format_exc())
        return False

def clearResult(result_id):
    # Delete report_directory
    # remove <result_id> entry from reports.json
    report_info = core.get_result_info(result_id)
    if not report_info[0]:
        core.updatelog('No result found for analysis ID: {0}'.format(result_id))
        return False
    analysis_dir = report_info[1]['report_directory']
    reportids = core.reportids
    report_index = core.report_index


    # Check if there is a directory with the analysis id
    if not os.path.isdir(analysis_dir):
        core.updatelog('Could not find any directory with the given analysis ID: ' + result_id)
    else:
        try:
            core.updatelog('Deleting analysis directory: ' + analysis_dir)
            shutil.rmtree(analysis_dir)
            core.updatelog('Successfully deleted analysis directory')
        except Exception as e:
            core.updatelog('Something went wrong while deleting analysis directory: ' + str(e))
            logging.error(traceback.format_exc())

    # Check if there is any analysis id in the index
    if result_id not in str(reportids):
        core.updatelog('No analysis with the id {0} in analysis index file'.format(result_id))
        #print(result_id)
        #print(str(reportids))
        return False
    else:
        reports = reportids['reports']
        for report in reports:
            if report['id'] == result_id:
                reports.remove(report)
        reportids['reports'] = reports
        core.reportids = reportids
        core.updatelog('Removed analysis {0} from index.. writing index to file'.format(result_id))
        r = open(report_index, 'w+', encoding='utf-8')
        r.write(json.dumps(reportids, indent=4, sort_keys=True))
        r.close()
        core.updatelog('Analysis index written to file: ' + report_index)
        return True


# ==========================================
# FROM: core/analyze.py
# ==========================================

"""
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
"""


def sort_files(extension_dir):
    try:
        extract_dir = helper.fixpath(core.lab_path + '/' + extension_dir)
        html_files = []
        js_files = []
        css_files = []
        static_files = []
        other_files = []  # File extensions that are not listed above
        for root, dirs, files in os.walk(extract_dir):
            for file in files:
                filepath = os.path.join(root, file)
                file = file.lower()
                if file.endswith('.html'):
                    core.updatelog('Discovered html file: ' + file)
                    html_files.append(filepath)
                elif file.endswith('.js'):
                    core.updatelog('Discovered js file: ' + file)
                    js_files.append(filepath)
                elif file.endswith('.css'):
                    core.updatelog('Discovered css file: ' + file)
                    css_files.append(filepath)
                elif file.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.svg')):
                    core.updatelog('Discovered static file: ' + file)
                    static_files.append(filepath)
                else:
                    other_files.append(filepath)
        core.updatelog('Sorted files: ' + extension_dir)
        # core.updatelog('HTML Files: {0}, JS Files: {1}, CSS Files: {2}, Static Files: {3}, Other Files: {4}'.format(str(count(html_files)), str(count(js_files)), str(count(css_files)), str(count(static_files)), str(count(other_files)))
        r = {'html_files': html_files, 'js_files': js_files, 'css_files': css_files,
             'static_files': static_files, 'other_files': other_files}
        return r
    except Exception as e:
        core.updatelog('Error while sorting files: ' + str(e))
        return False


def analyze(ext_name, ext_type='local'):
    # Handle the /detail/ format
    core.updatelog(ext_name)
    file_name = None
    if '?' in ext_name:
        # Split the path and get the last segment before any query parameters
        # This handles cases like /detail/histre/cmhjbooiibolkopmdohhnhlnkjikhkmn?hl=en-US
        file_name = ext_name.split('?')[0]

    # extension_extracted = False
    if ext_name.endswith('.crx') or ext_name.endswith('.xpi') or ext_name.endswith('.zip') or ext_name.endswith('.tar') or ext_name.endswith('.gzip'):
        '''
        EXTENSION NAME / PACKED PATH 
        UNZIP THE EXTENSION FOR FURTHER ANALYSIS
        '''

        if ext_name.endswith('.crx'):
            file_extension = '.crx'
            extract_method = 'zip'
        elif ext_name.endswith('.xpi'):
            file_extension = '.xpi'
            extract_method = 'zip'
        elif ext_name.endswith('.zip'):
            file_extension = '.zip'
            extract_method = 'zip'
        elif ext_name.endswith('.tar'):
            file_extension = '.tar'
            extract_method = 'tar'
        elif ext_name.endswith('.gzip'):
            file_extension = '.gzip'
            extract_method = 'tar'
        else:
            file_extension = ''
        ext_name = file_name + file_extension if file_name is not None else ext_name
        if os.path.isfile(ext_name):
            '''
            Full extension path sent, we unzip it to the lab directroy
            Used mostly to pass local firefox extensions
            '''
            ext_path = ext_name
            ext_name = os.path.basename(ext_name).split(file_extension)[0]
            extract_dir = helper.fixpath(core.lab_path + '/' + ext_name)
        else:
            '''
            Only the extension name is sent.. 
            In this case we assume that the extension is located inside the lab directory.
            Used while scanning an uploaded or downloaded extension
            '''
            ext_path = helper.fixpath(core.lab_path + '/' + ext_name)
            extract_dir = helper.fixpath(
                core.lab_path + '/' + ext_name.split(file_extension)[0])

        core.updatelog('Trying to unzip {0} to {1}'.format(
            ext_path, extract_dir))
        try:
            if os.path.exists(extract_dir):

                if os.path.exists(extract_dir + '_old'):
                    # there is already a _old directory we have to delete so that we can rename the last directory to this name
                    core.updatelog(
                        'Found previously created _old directory... deleting that')
                    try:
                        shutil.rmtree(extract_dir + '_old')
                    except Exception as e:
                        core.updatelog('Error while deleting: {0} . Error: {1}'.format(
                            extract_dir + '_old', str(e)))
                        logging.error(traceback.format_exc())
                        return ('error: Something went wrong while deleting old scan directory {0}'.format(extract_dir + '_old'))

                new_name = os.path.basename(extract_dir) + '_old'
                core.updatelog('Renaming old extract directory {0} as {1}'.format(
                    extract_dir, new_name))
                os.rename(extract_dir, extract_dir + '_old')
                core.updatelog('Old directory successfully renamed')

            if extract_method == 'zip':
                # zip, xpi, crx file extraction
                zip_contents = zipfile.ZipFile(ext_path, 'r')
                zip_contents.extractall(extract_dir)
                zip_contents.close()
                core.updatelog('Zip Extracted Successfully')
            elif extract_method == 'tar':
                # tar, gzip file extraction
                tar_contents = tarfile.open(ext_path)
                tar_contents.extractall(extract_dir)
                tar_contents.close()
                core.updatelog('Tar Extracted Successfully')

            # extension_extracted = True
        except Exception as e:
            logging.error(traceback.format_exc())
            core.updatelog(
                'Something went wrong while unzipping extension\nError: ' + str(e))
            return ('error: Something went wrong while unzipping extension. Check log for more information')

    elif os.path.isdir(ext_name):
        # if ext_name is a directory most likely it's a local extension
        ext_path = 'Local'
        extract_dir = ext_name
    else:
        return ('error: [analyze.py] Unsupported input!')

    core.updatelog('======== Analysis Begins ========')
    try:
        core.updatelog('Reading manifest.json')
        manifest_file = helper.fixpath(extract_dir + '/manifest.json')
        manifest_load = open(manifest_file, 'r', encoding='utf-8')
        manifest_content = manifest_load.read()
        manifest_content = json.loads(manifest_content)
        rinit = core.initreport(manifest_content, extract_dir, ext_type)
        if not rinit:
            return ('error: Something went wrong while parsing manifest.json... analysis stopped')
        core.report['crx'] = ext_path
        core.report['extracted'] = extract_dir

        #####################################################################
        ##### PERMISSION CHECKS AND OTHER STUFFS RELATED TO PERMISSIONS #####
        #####################################################################
        perm_file = helper.fixpath(core.path + '/db/permissions.json')
        perms = open(perm_file, 'r', encoding='utf-8')
        perms = perms.read()
        perms = json.loads(perms)
        try:
            for permission in manifest_content['permissions']:
                if permission != "":
                    permarray = {'name': permission}
                    core.updatelog('Discoverd Permission: ' +
                                   helper.escape(permission))
                    if permission in perms:
                        permarray['description'] = perms[permission]['description']
                        permarray['badge'] = perms[permission]['badge']
                        permarray['risk'] = perms[permission]['risk']
                        if perms[permission]['warning'] != 'none':
                            permarray['warning'] = perms[permission]['warning']
                            # core.updatelog('Warning: ' + perms[permission]['warning'])
                        else:
                            permarray['warning'] = 'na'
                    else:
                        permarray['description'] = 'na'
                        permarray['warning'] = 'na'
                        permarray['risk'] = 'none'
                        permarray['badge'] = '<i class="fas fa-question"></i>'
                    core.insertpermission(permarray)
        except Exception as e:
            core.updatelog('No permissions found')
            core.updatelog(str(e))

        #####################################################################
        #####     GET ALL FIELS AND STORE THEM FOR FURTHER ANALYSIS      ####
        #####################################################################
        html_files = []
        js_files = []
        json_files = []
        css_files = []
        static_files = []
        other_files = []  # File extensions that are not listed above

        for root, dirs, files in os.walk(extract_dir):
            for file in files:
                filepath = os.path.join(root, file)
                relpath = os.path.relpath(filepath, extract_dir)
                fname = file
                file = file.lower()
                if file.endswith(('.html', '.htm')):
                    html_files.append(filepath)
                    core.report['files']['html'].append({fname: relpath})
                elif file.endswith('.js'):
                    js_files.append(filepath)
                    core.report['files']['js'].append({fname: relpath})
                elif file.endswith('.json'):
                    json_files.append(filepath)
                    core.report['files']['json'].append({fname: relpath})
                elif file.endswith('.css'):
                    css_files.append(filepath)
                    core.report['files']['css'].append({fname: relpath})
                elif file.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.svg', '.gif')):
                    core.report['files']['static'].append({fname: relpath})
                    static_files.append(filepath)
                else:
                    core.report['files']['other'].append({fname: relpath})
                    other_files.append(filepath)

        ######################################################################
        ## EXTRACT INTELS FROM  FILES (url, email, ip address, btc address) ##
        ######################################################################

        urls = []
        domains = []
        for allfiles in (js_files, html_files, json_files, css_files):
            for file in allfiles:
                try:
                    cnt = open(file, 'r', encoding="utf8")
                    contents = cnt.read()
                    relpath = os.path.relpath(file, extract_dir)
                    core.updatelog('Extracting intels from: ' + file)
                    intels = intel.extract(contents, relpath)

                    # Parse the intels and add them to result
                    found_urls = intels['urls']
                    found_mail = intels['mails']
                    found_btcs = intels['btc']
                    found_ipv4 = intels['ipv4']
                    found_ipv6 = intels['ipv6']
                    found_b64s = intels['base64']
                    found_cmnt = intels['comments']

                    for u in found_urls:
                        urls.append(u)
                    for m in found_mail:
                        core.report['emails'].append(m)
                    for b in found_btcs:
                        core.report['bitcoin_addresses'].append(b)
                    for i in found_ipv4:
                        core.report['ipv4_addresses'].append(i)
                    for i in found_ipv6:
                        core.report['ipv6_addresses'].append(i)
                    for b in found_b64s:
                        core.report['base64_strings'].append(b)
                    for c in found_cmnt:
                        core.report['comments'].append(c)

                except Exception as e:
                    core.updatelog(
                        'Skipped reading file: {0} -- Error: {1}'.format(file, str(e)))
                    logging.error(traceback.format_exc())
        # urls = list(set(urls)) [NOTE TO SELF] we are tracking all urls in all files so set isn't used here

        ######################################################################
        ## APPEND URLS, DOMAINS TO REPORT AND DO VIRUSTOTAL SCAN ON DOMAINS ##
        ######################################################################

        for url in urls:
            core.updatelog('Found URL: ' + url['url'])
            domain = re.findall(
                r'^(?:https?:\/\/)?(?:[^@\/\\n]+@)?(?:www\.)?([^:\/?\\n]+)', url['url'])[0]
            url['domain'] = domain
            core.report['urls'].append(url)  # add url to the report file
            domains.append(domain)

        if virustotal.pub_vt == []:
            # No extra virustotal apis added hence the slow scan
            core.updatelog(
                'Starting virustotal analysis of domains. [SLOW MODE]')
            virustotal_scans = virustotal.domain_batch_scan(set(domains))

        for domain in set(domains):
            core.updatelog(
                'getting virustotal Scan results for domain: ' + domain)
            if virustotal.pub_vt != []:
                # the faster scan!
                virustotal_report = virustotal.scan_domain(domain)
                if not virustotal_report[0]:
                    core.updatelog(
                        'Error getting virustotal result... Error: ' + virustotal_report[1])
                    domain_vt = {
                        "error": "Either rate limited or something else went wrong while getting domain report from virustotal"}
                else:
                    core.updatelog('Virustotal result successfully acquired!')
                    domain_vt = virustotal_report[1]
            else:
                domain_vt = virustotal_scans[domain][1]
                core.updatelog('Virustotal result successfully acquired!')
            try:
                ip = socket.gethostbyname(domain)
            except:
                ip = 'unknown'
            if ip != 'unknown':
                ip_info = ip2country.get_country(ip)
                if ip_info[0]:
                    country = ip_info[2]
                    country_code = ip_info[1]
                else:
                    country = 'unknown'
                    country_code = 'unknown'
            else:
                country = 'unknown'
                country_code = 'unknown'

            domainarr = {"name": domain, "ip": ip, "country_code": country_code,
                         "country": country, "virustotal": domain_vt}
            core.report['domains'].append(domainarr)

        save_result = saveresult.createresult(extract_dir)
        cid = save_result.savereport()
        """
        if extension_extracted:
            # if the extension was extracted we delete the directory it was extracted to
            # don't want any local extensions to be deleted hence extension_extracted boolean
            core.updatelog('Deleting extraction directory: ' + extract_dir)
            try:
                shutil.rmtree(extract_dir)
                core.updatelog('Extraction directory successfully deleted')
            except Exception as e:
                core.updatelog('Something went wrong while deleting extraction directory: ' + str(e))
                logging.error(traceback.format_exc())
        """
        if cid != False and cid != None:
            return ('Extension analyzed and report saved under ID: ' + cid)
        else:
            return ('error:Something went wrong with the analysis!')
    except Exception as e:
        core.updatelog(
            'Something went wrong while reading source of manifest.json file')
        print(e)
        core.updatelog(logging.error(traceback.format_exc()))


"""
def handle_delete(func, path, exc_info):
    os.chmod(path, stat.S_IWRITE)
    os.unlink(path)
"""

# ==========================================
# FROM: core/updater.py
# ==========================================

"""
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
"""


def check():
    '''
    Check for update
    '''
    print('==== ExtAnalysis Update Check ====')
    core.updatelog('Current Version: ' + core.version)
    current_version = int(core.version.replace('.', ''))

    core.updatelog('Getting new version from github')
    v = scan.source_code(core.version_url)
    if v[0]:
        # Successfully acquired source code
        try:
            # validate version
            latest_version = int(v[1].replace('.', '').replace('\n', ''))
            core.updatelog('Latest version: ' + v[1])
            if latest_version > current_version:
                # Update available
                update_prompt = input('New Version available! Update Now? (y/n): ').lower()
                if update_prompt == 'y':
                    # update it
                    update()
                else:
                    core.updatelog('Update cancled! Make sure update the app later')
                    core.handle_exit()
            elif latest_version == current_version:
                print("you're already on the latest version!")
                core.handle_exit()
            else:
                print('The script was tampered with and i don\'t like it!')
                core.handle_exit()
        except Exception as e:
            core.updatelog('Invalid response from github')
            logging.error(traceback.format_exc())
            core.handle_exit()
    else:
        core.updatelog('Something went wrong while getting version from github')
        core.handle_exit()


def update():
    '''
    Updates ExtAnalysis
    1. Create the updater child script and save it to temp directory
    2. End self process and start the child script
    '''
    print("\n[i] Creating Updater file")

    child_script = open(helper.fixpath(core.path + '/db/updater.py'), 'r', encoding='utf-8')
    child_script = child_script.read()

    src = child_script.replace('<current_extanalysis_directory>', core.path.replace('\\', '\\\\'))
    src = src.replace('<github_zip_url>', core.github_zip)

    print('[i] Moving updater file to temp directory')
    temp_dir = tempfile.gettempdir()

    updater_script = helper.fixpath(temp_dir + '/update_extanalysis.py')
    f = open(updater_script, 'w+', encoding='utf-8')
    f.write(src)
    f.close()

    python_loc = sys.executable

    print('[i] Starting Updater script')

    if sys.platform == 'win32':
        os.chdir(temp_dir)
        command = [python_loc, 'update_extanalysis.py']
        subprocess.Popen(command, creationflags=subprocess.CREATE_NEW_CONSOLE, shell=False)
        print('[i] Killing self... Next time we meet I will be a better version of myself ;)')
        exit()
    else:
        os.chdir(temp_dir)
        command = ['x-terminal-emulator', '-e', python_loc, updater_script]
        subprocess.Popen(command, shell=False)
        print('[i] Killing self... Next time we meet I will be a better version of myself ;)')
        exit()


# ==========================================
# FROM: frontend/api.py
# ==========================================

"""
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
"""



def api_view(query, allargs):
    if query == 'dlanalysis':
        try:
            extension_id = allargs.get('extid')
            saveas = ""
            try:
                saveas = allargs.get('savedir')
                if saveas == "" or saveas == " ":
                    saveas = extension_id
            except Exception as e:
                print('Save name not specified')
            try:
                downloader = download_extension.ExtensionDownloader()
                download_log = downloader.download_chrome(extension_id, saveas)
                if download_log:
                    aok = analysis.analyze(
                        saveas + '.crx', 'Remote Google Chrome Extension')
                    return (aok)
                else:
                    return ('error: Something went wrong while downloading extension')
            except Exception as e:
                core.updatelog(
                    'Something went wrong while downloading extension: ' + str(e))
                return ('error: Something went wrong while downloading extension, check log for more information')

        except Exception as e:
            core.updatelog('Something went wrong: ' + str(e))
            return ('error: Something went wrong while downloading extension, check log for more information')

    elif query == 'firefoxaddon':
        try:
            addonurl = allargs.get('addonurl')
            try:
                downloader = download_extension.ExtensionDownloader()
                download_log = downloader.download_firefox(addonurl)
                if download_log:
                    aok = analysis.analyze(
                        download_log + '.xpi', 'Remote Firefox Addon')
                    return (aok)
                else:
                    return ('error: Something went wrong while downloading extension')
            except Exception as e:
                core.updatelog(
                    'Something went wrong while downloading extension: ' + str(e))
                return ('error: Something went wrong while downloading extension, check log for more information')
        except Exception as e:
            core.updatelog('Something went wrong: ' + str(e))
            return ('error: Something went wrong while downloading extension, check log for more information')

    elif query == 'edgeaddon':
        try:
            addonurl = allargs.get('addonurl')
            saveas = addonurl.split('/')[-1]
            try:
                downloader = download_extension.ExtensionDownloader()
                download_log = downloader.download_edge(addonurl)
                if download_log:
                    aok = analysis.analyze(
                        saveas + '.crx', 'Remote Edge Extension')
                    return (aok)
                else:
                    return ('error: Something went wrong while downloading extension')
            except Exception as e:
                core.updatelog(
                    'Something went wrong while downloading extension: ' + str(e))
                return ('error: Something went wrong while downloading extension, check log for more information')
        except Exception as e:
            core.updatelog('Something went wrong: ' + str(e))
            return ('error: Something went wrong while downloading extension, check log for more information')

    elif query == 'results':
        reportids = core.reportids
        if reportids == {}:
            # Result index not loaded so let's load it and show em results
            core.updatelog('Reading report index and loading json')
            ridfile = core.report_index
            ridcnt = open(ridfile, 'r', encoding='utf8')
            ridcnt = ridcnt.read()
            reportids = json.loads(ridcnt)

        rd = "<table class='result-table' id='result-table'><thead><tr><th>Name</th><th>Version</th><th>Date</th><th>Actions</th></tr></thead><tbody>"
        for areport in reportids['reports']:
            report_name = areport['name']
            report_id = areport['id']
            report_date = areport['time']
            report_version = areport['version']
            rd += '<tr><td>' + report_name + '</td><td>' + report_version + '</td><td>' + report_date + \
                '</td><td><button class="bttn-fill bttn-xs bttn-primary" onclick=viewResult(\'' + report_id + '\')><i class="fas fa-eye"></i> View</button> <button class="bttn-fill bttn-xs bttn-danger" onclick=deleteResult(\'' + \
                report_id + '\')><i class="fas fa-trash"></i> Delete</button></td></tr>'
        return (rd + '</tbody></table><br>')

    elif query == 'getlocalextensions':
        try:
            browser = allargs.get('browser')
            if browser == 'googlechrome':
                lexts = GetLocalExtensions()
                exts = ""
                exts = lexts.googlechrome()
                if exts != False and exts != [] and exts != None:
                    return_html = "<table class='result-table' id='result-table'><thead><tr><th>Extension Name</th><th>Action</th></tr></thead><tbody>"
                    for ext in exts:
                        ext_info = ext.split(',')
                        return_html += '<tr><td>' + ext_info[
                            0] + '</td><td><button class="bttn-fill bttn-xs bttn-success" onclick="analyzeLocalExtension(\'' + \
                            ext_info[1].replace('\\',
                                                '\\\\') + '\', \'googlechrome\')"><i class="fas fa-bolt"></i> Analyze</button></td></tr>'
                    return (return_html + '</tbody></table>')
                else:
                    return (
                        'error: Something went wrong while getting local Google Chrome extensions! Check log for more information')
            elif browser == 'firefox':
                lexts = GetLocalExtensions()
                exts = lexts.firefox()
                if exts != False and exts != [] and exts != None:
                    return_html = "<table class='result-table' id='result-table'><thead><tr><th>Extension Name</th><th>Action</th></tr></thead><tbody>"
                    for ext in exts:
                        ext_info = ext.split(',')
                        return_html += '<tr><td>' + ext_info[
                            0] + '</td><td><button class="bttn-fill bttn-xs bttn-success" onclick="analyzeLocalExtension(\'' + \
                            ext_info[1].replace('\\',
                                                '\\\\') + '\', \'firefox\')"><i class="fas fa-bolt"></i> Analyze</button></td></tr>'
                    return (return_html + '</tbody></table>')
                else:
                    return (
                        'error: Something went wrong while getting local firefox extensions! Check log for more information')
            elif browser == 'brave':
                lexts = GetLocalExtensions()
                exts = ""
                exts = lexts.braveLocalExtensionsCheck()
                if exts != False and exts != [] and exts != None:
                    return_html = "<table class='result-table' id='result-table'><thead><tr><th>Extension Name</th><th>Action</th></tr></thead><tbody>"
                    for ext in exts:
                        ext_info = ext.split(',')
                        return_html += '<tr><td>' + ext_info[
                            0] + '</td><td><button class="bttn-fill bttn-xs bttn-success" onclick="analyzeLocalExtension(\'' + \
                            ext_info[1].replace('\\',
                                                '\\\\') + '\', \'brave\')"><i class="fas fa-bolt"></i> Analyze</button></td></tr>'
                    return (return_html + '</tbody></table>')
                else:
                    return (
                        'error: Something went wrong while getting local Brave browser extensions! Check log for more information')

            elif browser == 'vivaldi':
                lexts = GetLocalExtensions()
                exts = ""
                exts = lexts.vivaldi_local_extensions_check()
                if exts and len(exts) > 0:
                    return_html = "<table class='result-table' id='result-table'><thead><tr><th>Extension Name</th><th>Action</th></tr></thead><tbody>"
                    for ext in exts:
                        ext_info = ext.split(',')
                        return_html += '<tr><td>' + ext_info[
                            0] + '</td><td><button class="bttn-fill bttn-xs bttn-success" onclick="analyzeLocalExtension(\'' + \
                            ext_info[1].replace('\\',
                                                '\\\\') + '\', \'vivaldi\')"><i class="fas fa-bolt"></i> Analyze</button></td></tr>'
                    return (return_html + '</tbody></table>')
                else:
                    return (
                        'error: Something went wrong while getting local Vivaldi browser extensions! Check log for more information')

            else:
                return ('error: Invalid Browser!')
        except Exception:
            logging.error(traceback.format_exc())
            return ('error: Incomplete Query')

    elif query == 'analyzelocalextension':
        try:
            browser = allargs.get('browser')
            path_to_local = allargs.get('path')
            path = helper.fixpath(path_to_local)

            if browser == 'firefox' and os.path.isfile(path):
                # valid firefox extension
                analysis_stat = analyzelocalfirefoxextension(path)
                return (analysis_stat)

            elif browser == 'googlechrome' and os.path.isdir(path):
                if os.path.isfile(os.path.join(path, 'manifest.json')):
                    analysis_stat = analysis.analyze(
                        path, 'Local Google Chrome Extension')
                    return (analysis_stat)
                else:
                    return ('error: Invalid Google Chrome Extension Directory')

            elif browser == 'brave' and os.path.isdir(path):
                if os.path.isfile(os.path.join(path, 'manifest.json')):
                    analysis_stat = analysis.analyze(
                        path, 'Local Brave browser Extension')
                    return (analysis_stat)
                else:
                    return ('error: Invalid Brave Extension Directory')

            elif browser == 'vivaldi' and os.path.isdir(path):
                if os.path.isfile(os.path.join(path, 'manifest.json')):
                    analysis_stat = analysis.analyze(
                        path, 'Local Vivaldi brwoser Extension')
                    return analysis_stat
                else:
                    return 'error: Invalid Vivaldi Extension Directory'

            else:
                return ('error: Malformed Query')
        except Exception:
            logging.error(traceback.format_exc())
            return ('error: Incomplete Query')

    elif query == 'deleteAll':
        '''
        DELETES ALL RESULTS
        RESPONSE = SUCCESS / ERROR
        '''
        delete_status = clearAllResults()
        if delete_status:
            return "success"
        else:
            return ('There were some errors while deleting all analysis reports... refer to log for more information')

    elif query == 'clearLab':
        '''
        Deletes all the contents of lab
        RESPONSE = SUCCESS / ERROR
        '''
        clear_lab = core.clear_lab()
        if clear_lab[0]:
            # Successful
            return (clear_lab[1])
        else:
            # Unsuccessful
            return ('error: ' + clear_lab[1])

    elif query == 'deleteResult':
        '''
        DELETES A SPECIFIC RESULT
        PARAMETER = resultID
        RESPONSE = SUCCESS_MSG / 'error: ERROR_MSG'
        '''
        try:
            result_id_to_delete = allargs.get('resultID')
            delete_status = clearResult(result_id_to_delete)
            if delete_status:
                return "success"
            else:
                return "Something went wrong while deleting result! Check log for more information"
        except Exception:
            return ('Invalid Query')

    elif query == 'vtDomainReport':
        try:
            domain = allargs.get('domain')
            analysis_id = allargs.get('analysis_id')
            ranalysis = core.get_result_info(analysis_id)
            if ranalysis[0]:
                # if ranalysis[0] is True then ranalysis[1] contains the details
                analysis_dir = ranalysis[1]['report_directory']
                analysis_report = os.path.join(
                    analysis_dir, 'extanalysis_report.json')
                if os.path.isfile(analysis_report):
                    report = open(analysis_report, 'r', encoding='utf-8')
                    domains = json.loads(report.read())['domains']
                    for adomain in domains:
                        if adomain['name'] == domain:
                            vtjson = json.dumps(
                                adomain['virustotal'], indent=4, sort_keys=False)
                            # return_html = '<div id="vt_info"></div><script>var wrapper1 = document.getElementById("vt_info");var data = '+vtjson+' try {var data = JSON.parse(dataStr);} catch (e) {} var tree = jsonTree.create(data, wrapper1);tree.expand(function(node) {   return node.childNodes.length < 2 || node.label === "phoneNumbers";});</script>'
                            return vtjson
                    return ('error: Domain info not found in analysis report!')
                else:
                    return ('error: Analysis report for #{0} not found'.format(analysis_id))
            else:
                # ranalysis[1] is the error msg when ranalysis[0] = False
                return ('error: ' + ranalysis[1])
        except:
            logging.error(traceback.format_exc())
            return ('error: Malformed api call')

    elif query == 'retirejsResult':
        '''
        GET RETIREJS SCAN RESULTS FOR FILE
        REQUIRED PARAMETER: file = FILE_ID
        '''
        try:
            file_id = allargs.get('file')
            analysis_id = allargs.get('analysis_id')
            ranalysis = core.get_result_info(analysis_id)
            if ranalysis[0]:
                # if ranalysis[0] is True then ranalysis[1] contains the details
                analysis_dir = ranalysis[1]['report_directory']
                source_json = os.path.join(analysis_dir, 'source.json')
                if os.path.isfile(source_json):
                    report = open(source_json, 'r', encoding='utf-8')
                    files = json.loads(report.read())
                    for _file in files:
                        if _file == file_id:
                            retirejs_result = files[_file]['retirejs_result']
                            if retirejs_result == []:
                                ret = 'none'
                            else:
                                ret = json.dumps(
                                    retirejs_result, indent=4, sort_keys=False)
                            return ret
                    return ('error: File ID not found in report!')
                else:
                    return ('error: Analysis report for #{0} not found'.format(analysis_id))
            else:
                # ranalysis[1] is the error msg when ranalysis[0] = False
                return ('error: ' + ranalysis[1])
        except:
            logging.error(traceback.format_exc())
            return ('error: Malformed api call')

    elif query == 'whois':
        '''
        GET WHOIS REPORT OF DOMAIN
        REQUIRES 'python-whois' module
        RESPONSE = HTML DIV WITH FORMATTED WHOIS INFO
        '''
        try:
            domain = allargs.get('domain')
            try:
                import whois
            except:
                return (
                    "error: python-whois module not installed! install it using `pip3 install python-whois` or `pip3 install -r requirements.txt`")
            whois_result = whois.whois(domain)
            whois_html = '<div class="whois-data" style="overflow-y: scroll; max-height:500px; text-align: left;">'
            for data in whois_result:
                proper_data = data.replace('_', ' ').capitalize()
                if isinstance(whois_result[data], list):
                    for subdata in whois_result[data]:
                        whois_html += '<b style="color:#89ff00;">{0} : </b>{1}<br>'.format(
                            proper_data, subdata)
                else:
                    whois_html += '<b style="color:#89ff00;">{0} : </b>{1}<br>'.format(
                        proper_data, whois_result[data])
            whois_html += '</div>'
            if whois_result:
                return ('<center><h4>Whois Results For {0}</h4></center><br>{1}'.format(domain, whois_html))
            else:
                return ("error: Something went wrong while checking whois information of: " + domain)
        except Exception:
            logging.error(traceback.format_exc())
            return ('error: Invalid Query')

    elif query == 'geoip':
        '''
        GEO-IP LOOKUP OF AN IP ADDRESS
        PARAMETERS -> IP = CONTAINS IP ADDRESS TO BE LOOKED UP
        RETURNS A HTML TO BE SHOWN
        '''
        try:
            ip_address = allargs.get('ip')
            geo_ip = scan.geoip(ip_address)
            if geo_ip[0]:
                gip = geo_ip[1]
                rethtml = '<div class="whois-data" style="overflow-y: scroll; max-height:500px; text-align: left;">'
                for g in gip:
                    name = str(g).replace('_', ' ').capitalize()
                    val = str(gip[g])
                    rethtml += '<b style="color:#89ff00;">{0} : </b>{1}<br>'.format(
                        name, val)
                rethtml += '</div>'
                return ('<center><h4>Geo-IP Lookup Results For {0}</h4></center><br>{1}'.format(ip_address, rethtml))

            else:
                # in case of geo_ip[0] being false element 1 has the error msg
                return ('error: ' + geo_ip[1])

        except Exception as e:
            logging.error(traceback.format_exc())
            return ('error: Invalid Query')

    elif query == 'HTTPHeaders':
        '''
        HTTP HEADERS OF AN URL
        PARAMETERS -> URL -> BASE64 ENCODED URL
        RETURNS HTML
        '''
        try:
            url = allargs.get('url')
            url = base64.b64decode(url).decode('ascii')
            headers_status = scan.http_headers(url)
            if headers_status[0]:
                rethtml = '<div class="whois-data" style="overflow-y: scroll; max-height:500px; text-align: left;">'
                headers = headers_status[1]
                for header in headers:
                    hval = headers[header]
                    rethtml += '<b style="color:#89ff00;">{0} : </b>{1}<br>'.format(
                        header, hval)
                rethtml += '</div>'
                return ('<center><h4>Showing HTTP Headers of: {0}</h4></center><br>{1}'.format(url, rethtml))
            else:
                return ('error: ' + headers_status[1])
        except Exception as e:
            logging.error(traceback.format_exc())
            return ('error: Invalid Query')

    elif query == 'SourceCode':
        '''
        GET SOURCE CODE OF AN URL
        PARAMETERS -> URL -> BASE64 ENCODED URL
        RETURNS HTML
        '''
        try:
            url = allargs.get('url')
            rurl = base64.b64decode(url).decode('ascii')
            headers_status = scan.source_code(rurl)
            if headers_status[0]:
                rethtml = '<textarea id="src_code" class="source_code" autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false">'
                headers = headers_status[1]
                rethtml += headers
                rethtml += '</textarea><br><br><center><a href="{0}" target="_blank" class="start_scan"><i class="fas fa-external-link-alt"></i> View Full Screen</a>'.format(
                    '/source-code/' + url)
                return ('<center><h4>Source Code of: {0}</h4></center><br>{1}'.format(rurl, rethtml))
            else:
                return ('error: ' + headers_status[1])
        except Exception as e:
            logging.error(traceback.format_exc())
            return ('error: Invalid Query')

    elif query == 'clearlogs':
        '''
        CLEARS LOG
        '''
        core.clearlog()
        return ('Logs cleared successfully!')

    elif query == 'changeReportsDir':
        '''
        CHANGES THE REPORT DIRECTORY
        RESPONSE = SUCCESS / 'error: ERROR_MSG'
        '''
        try:
            newpath = allargs.get('newpath')
            if os.path.isdir(newpath):
                # valid directory.. let's get the absolute path and set it
                absolute_path = os.path.abspath(newpath)
                change = changedir(absolute_path)
                if change[0]:
                    return (change[1])
                else:
                    return ('error: ' + change[1])
            else:
                return ('error: Invalid directory path!')
        except:
            logging.error(traceback.format_exc())
            return ('error: Invalid request for directory change!')

    elif query == 'changeVTapi':
        '''
        CHANGE VIRUSTOTAL API
        RESPONSE = SUCCESS_MSG / 'error: ERROR_MSG'
        '''
        try:
            new_api = allargs.get('api')
            change = change_vt_api(new_api)
            if change[0]:
                return (change[1])
            else:
                return ('error: ' + change[1])
        except:
            logging.error(traceback.format_exc())
            return ('error: Invalid request!')

    elif query == 'changelabDir':
        '''
        CHANGES THE LAB DIRECTORY
        RESPONSE = SUCCESS / 'error : ERROR_MSG'
        '''
        try:
            newpath = allargs.get('newpath')
            if os.path.isdir(newpath):
                # valid directory.. let's get the absolute path and set it
                absolute_path = os.path.abspath(newpath)
                change = changelabdir(absolute_path)
                if change[0]:
                    return (change[1])
                else:
                    return ('error: ' + change[1])
            else:
                return ('error: Invalid directory path!')
        except:
            logging.error(traceback.format_exc())
            return ('error: Invalid request for directory change!')

    elif query == 'updateIntelExtraction':
        '''
        UPDATES INTELS TO BE EXTRACTED
        RESPONSE = SUCCESS_MSG / 'error: ' + ERROR_MSG
        '''
        try:
            # Create the dict with all values and keys
            parameters = {}
            parameters["extract_comments"] = str(
                allargs.get('extract_comments'))
            parameters["extract_btc_addresses"] = str(
                allargs.get('extract_btc_addresses'))
            parameters["extract_base64_strings"] = str(
                allargs.get('extract_base64_strings'))
            parameters["extract_email_addresses"] = str(
                allargs.get('extract_email_addresses'))
            parameters["extract_ipv4_addresses"] = str(
                allargs.get('extract_ipv4_addresses'))
            parameters["extract_ipv6_addresses"] = str(
                allargs.get('extract_ipv6_addresses'))
            parameters["ignore_css"] = str(allargs.get('ignore_css'))

            status_code = update_settings_batch(parameters)
            # 0 = failed, 1 = success, 2 = some updated some not!
            if status_code == '0':
                return ('error: Settings could not be updated! Check log for more information')
            elif status_code == '1':
                return ('Settings updated successfully... Please restart ExtAnalysis for them to take effect!')
            elif status_code == '2':
                return (
                    'Some settings were updated and some were not... Please restart ExtAnalysis for them to take effect!')
            else:
                return (
                    'error: Invalid response from "update_settings_batch". please report it here: https://github.com/Tuhinshubhra/ExtAnalysis/issues/new')
        except:
            logging.error(traceback.format_exc())
            return ('error: Incomplete Request!')

    else:
        return ('error: Invalid Query!')


# ==========================================
# FROM: frontend/viewfile.py
# ==========================================

"""
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
"""


def viewfile_view(analysis_id, file_id):
    int(analysis_id.replace('EXA','')) # throws exception if improper id passed
    int(file_id.replace('EXTAF', ''))
    analysis_info = core.get_result_info(analysis_id)
        
    if not analysis_info[0]:
        # Could not get analysis_info
        error_txt = 'Something went wrong while getting analysis info!<br>Error: ' + analysis_info[1]
        return render_template('error.html', error_title = "Invalid Result ID", error_head = "Invalid Result ID: {0}".format(analysis_id) , error_txt=error_txt)
        
    analysis_path = analysis_info[1]['report_directory'].replace('<reports_path>', core.reports_path)
    sources_file = os.path.join(analysis_path, 'source.json')

    if os.path.isfile(sources_file):
        # valid source
        s = open(sources_file, 'r', encoding='utf-8')
        sources = json.loads(s.read())
        try:
            file_info = sources[file_id]
            file_name = file_info['file_name']
            file_location = file_info['location']
            file_type = file_name.split('.')[-1]
            if file_type.endswith(('html', 'htm')):
                file_icon = 'html1.png'
            elif file_type.endswith('js'):
                file_icon = 'js1.png'
            elif file_type.endswith('css'):
                file_icon = 'css1.png'
            elif file_type.endswith(('png', 'jpg', 'jpeg', 'bmp', 'tiff', 'svg')):
                file_icon = 'static1.png'
            elif file_type.endswith('json'):
                file_icon = 'json1.png'
            else:
                file_icon = 'other1.png'
            icon_url = url_for('static',filename='images/' + file_icon)
            file_icon = '<img src="' + icon_url + '">'
            file_type = ('javascript' if file_type == 'js' else file_type)
            try:
                fs = open(file_location, 'r', encoding='utf8')
                file_source = fs.read()
                file_size = str(os.path.getsize(file_location) >> 10) + ' KB'
                return render_template('source.html', file_name = file_name, file_source = file_source, file_id = file_id, file_location = file_location, file_type = file_type, file_size = file_size, file_icon = file_icon)
            except Exception as e:
                logging.error(traceback.format_exc())
                return render_template('error.html', error_title = "Error Accessing File", error_head = "Problem while reading file source!" , error_txt='Something went wrong while reading the file source... error: ' + str(e))

        except:
            return render_template('error.html', error_title = "Invalid File ID", error_head = "Invalid File ID" , error_txt='I could not find any file with the given file id... well either you tempered with the parameter or something went WRONG!')

    else:
        return render_template('error.html', error_title = "Invalid Analysis ID", error_head = "Invalid Analysis ID" , error_txt='There seems to be no result corresponding to the provided ID. Did you delete the result? or maybe you did some weird shit with the parameter?')


# ==========================================
# FROM: frontend/viewgraph.py
# ==========================================

"""
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
"""


def viewgraph_view(analysis_id):
    try:
        int(analysis_id.replace('EXA','')) # throws exception if improper id passed
        analysis_info = core.get_result_info(analysis_id)
        
        if not analysis_info[0]:
            # Could not get analysis_info
            error_txt = 'Something went wrong while getting analysis info!<br>Error: ' + analysis_info[1]
            return render_template('error.html', error_title = "Invalid Result ID", error_head = "Invalid Result ID: {0}".format(analysis_id) , error_txt=error_txt)
        
        analysis_path = analysis_info[1]['report_directory'].replace('<reports_path>', core.reports_path)
        
        graph_data = os.path.join(analysis_path, 'graph.data')
        if os.path.isfile(graph_data):
            graph_data = open(graph_data, 'r', encoding='utf-8')
            graph_data = graph_data.read()
            return render_template('graph.html', graph_data = graph_data)
        else:
            return render_template('error.html', error_title = "Missing Graph File", error_head = "Missing Graph File for Result ID: {0}".format(analysis_id) , error_txt='ExtAnalysis could not find "grpah.data" file in the analysis report directory! Please re-analyze the extension') 
    except:
        error_txt = 'There seems to be no result corresponding to the provided ID. Did you delete the result? or maybe you did some weird shit with the parameter?'
        return render_template('error.html', error_title = "Invalid Result ID", error_head = "Invalid Result ID: {0}".format(analysis_id) , error_txt=error_txt) 


# ==========================================
# FROM: frontend/viewresult.py
# ==========================================

"""
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
"""


def viewresult_view(analysis_id):
    # so the result ids are in this format : EXA<some digits> so we can try to replace 'EXTA' and convert the rest to int if it passes it's a valid type
    try:
        int(analysis_id.replace('EXA','')) # Check

        analysis_info = core.get_result_info(analysis_id)
        
        if not analysis_info[0]:
            # Could not get analysis_info
            error_txt = 'Something went wrong while getting analysis info!<br>Error: ' + analysis_info[1]
            return render_template('error.html', error_title = "Invalid Result ID", error_head = "Invalid Result ID: {0}".format(analysis_id) , error_txt=error_txt)
        else:
            result_directory = analysis_info[1]['report_directory'].replace('<reports_path>', core.reports_path)

            if os.path.isdir(result_directory):
                # result directory found let's check for all necessary files
                graph_file = os.path.join(result_directory, 'graph.data')
                report_json = os.path.join(result_directory, 'extanalysis_report.json')
                source_file = os.path.join(result_directory, 'source.json')


                if all([os.path.isfile(the_file) for the_file in [graph_file, report_json, source_file]]):
                    core.updatelog('Viewing Analysis {0}'.format(analysis_id))
                    graph_data = open(graph_file, 'r', encoding='utf-8')
                    graph_data = graph_data.read()
                    source_data = open(source_file, 'r', encoding='utf-8')
                    source_data = json.loads(source_data.read())
                    report_data = open(report_json, 'r', encoding='utf-8')
                    report_data = json.loads(report_data.read())

                    # prepare data to be sent to result page
                    basic_info_t = [report_data['name'], 
                                    report_data['version'], 
                                    report_data['author'], 
                                    report_data['description'],
                                    analysis_info[1]['time']
                                    ]
                    
                    # extension type
                    extension_type = report_data['type']
                    if 'firefox' in extension_type.lower():
                        extension_type = '<i class="fab fa-firefox"></i> ' + extension_type
                    elif 'chrome' in extension_type.lower():
                        extension_type = '<i class="fab fa-chrome"></i> ' + extension_type

                    # URL Table
                    if report_data['urls'] != []:
                        urls_table = '<table class="result-table" id="urls-table"><thead><tr><th>URL</th><th>Domain</th><th>File</th><th>Actions</th></tr></thead><tbody>'
                        extjs_table = '<table class="result-table" id="extjs-table"><thead><tr><th>URL</th><th>Domain</th><th>File</th><th>Actions</th></tr></thead><tbody>'
                        done_urls = []
                        done_ejss = []
                        urls_count = 0
                        extjs_count = 0
                        for aurl in report_data['urls']:
                            if aurl['url'].endswith('.js'):
                                if aurl['url'] not in done_ejss:
                                    done_ejss.append(aurl['url'])
                                    aurl_href = '<a href="{0}" class="ext_url" target="_blank"><i class="fas fa-external-link-alt" style="font-size:12px;"></i> {0}</a>'.format(aurl['url'])
                                    extjs_table += '<tr><td>' + aurl_href + '</td>'
                                    b64url = "'" + base64.b64encode(aurl['url'].encode('ascii', 'ignore')).decode('ascii') + "'"
                                    extjs_table += '<td>{0}</td><td>{1}</td>'.format(aurl['domain'], aurl['file'])
                                    extjs_table += '<td><button class="bttn-fill bttn-xs bttn-primary" onclick=whois(\'{1}\')><i class="fab fa-searchengin"></i> WHOIS</button> <button class="bttn-fill bttn-xs bttn-success" onclick="getSource({0})"><i class="fas fa-code"></i> Source</button> <button class="bttn-fill bttn-xs bttn-danger" onclick="getHTTPHeaders({0})"><i class="fas fa-stream"></i> HTTP Headers</button></td></tr>'.format(b64url, aurl['url'])
                                    extjs_count += 1
                            else:
                                if aurl['url'] not in done_urls:
                                    done_urls.append(aurl['url'])
                                    aurl_href = '<a href="{0}" class="ext_url" target="_blank"><i class="fas fa-external-link-alt" style="font-size:12px;"></i> {0}</a>'.format(aurl['url'])
                                    urls_table += '<tr><td>' + aurl_href + '</td>'
                                    urls_table += '<td>{0}</td><td>{1}</td>'.format(aurl['domain'], aurl['file'])
                                    b64url = "'" + base64.b64encode(aurl['url'].encode('ascii', 'ignore')).decode('ascii') + "'"
                                    urls_table += '<td><button class="bttn-fill bttn-xs bttn-primary" onclick=whois(\'{1}\')><i class="fab fa-searchengin"></i> WHOIS</button> <button class="bttn-fill bttn-xs bttn-success" onclick="getSource({0})"><i class="fas fa-code"></i> Source</button> <button class="bttn-fill bttn-xs bttn-danger" onclick="getHTTPHeaders({0})"><i class="fas fa-stream"></i> HTTP Headers</button></td></tr>'.format(b64url, aurl['url'])
                                    urls_count += 1

                        if done_urls != []:
                            urls_table += '</tbody></table>'
                        else:
                            urls_table = '<h3 class="nothing"> No URLs Found </h3>'

                        if done_ejss != []:
                            extjs_table += '</tbody></table>'
                        else:
                            extjs_table = '<h3 class="nothing"> No External JavaScript Found in any files! </h3>'
                    else:
                        urls_table = '<h3 class="nothing"> No URLs Found </h3>'
                        extjs_table = '<h3 class="nothing"> No External JavaScript Found in any files! </h3>'
                        extjs_count = 0
                        urls_count = 0

                    # Domains div
                    if report_data['domains'] != []:
                        domains_table = '<table class="result-table" id="domains-table"><thead><tr><th>Country</th><th>Domain</th><th>IP Address</th><th>Actions</th></tr></thead><tbody>'
                        for domain in report_data['domains']:
                            domain_flag = helper.fixpath(core.path + '/static/images/flags/' + domain['country_code'] + '.png')
                            if os.path.isfile(domain_flag):
                                flag_path = url_for('static',filename='images/flags/' + domain['country_code'] + '.png')
                            else:
                                flag_path = url_for('static',filename='images/flags/unknown.png')
                            country_html = '<img src="{0}" class="country_flag"> {1}'.format(flag_path, domain['country'])
                            domains_table += '<tr><td>{4}</td><td>{0}</td><td>{2}</td><!-- td>{1}</td --><td><button class="bttn-fill bttn-xs bttn-danger" onclick=whois("{0}")><i class="fab fa-searchengin"></i> WHOIS</button> <button class="bttn-fill bttn-xs bttn-primary" onclick="domainvt(\'{0}\', \'{3}\')"><i class="fas fa-hourglass-end"></i> VT Report</button> <button class="bttn-fill bttn-xs bttn-success" onclick=geoip("{2}")><i class="fas fa-globe-americas"></i> Geo-IP Lookup</button></td></tr>'.format(domain['name'], '0/66', domain['ip'], analysis_id, country_html)
                        domains_table += '</tbody></table>'
                    else:
                        domains_table = '<h3 class="nothing"> No Domains Extracted! </h3>'
                    unique_domains = len(report_data['domains'])

                        
                    # Permissions div containing all permissions accordions
                    permissions_div = ""
                    for perm in report_data['permissions']:
                        #perm_html = '<div class="perm"><div class="perm-name">{0}</div> <div class="perm-desc">{1}</div> <div class="perm-warn">{2}</div></div>'.format(perm['name'], perm['description'], (perm['warning'] if perm['warning'] != 'na' else ''))
                        perm_html = '<div class="accordion"><div class="accordion__item"><div class="accordion__question">{0} {1} <div class="risk-pill {4}">{4}</div></div><div class="accordion__answer">{2} <div class="warning"> {3} </div></div></div></div>'.format(perm['badge'], helper.escape(perm['name']), perm['description'], (perm['warning'] if perm['warning'] != 'na' else ''), perm['risk'])
                        permissions_div += perm_html
                    permissions_count = len(report_data['permissions'])



                    # table consisting of all the viewable source files
                    files_table = '<table class="result-table" id="files-table"><thead><tr><th>File Name</th><th>Path</th><th>Size</th><th>Actions</th></tr></thead><tbody>'
                    for file_info in source_data:
                        file_name = source_data[file_info]['file_name']
                        rel_path = source_data[file_info]['relative_path']
                        file_id = source_data[file_info]['id']
                        file_size = source_data[file_info]['file_size']
                        file_action = '<button class="bttn-fill bttn-xs bttn-primary" onclick="viewfile(\'' + analysis_id + '\', \'' + file_id + '\')"><i class="fas fa-code"></i> View Source</button>'
                        if file_name.endswith('.js'):
                            # Add button for viewing retirejs vulnerability scan results
                            # okay it's annoying to show button on every js file let's just show where there is vuln.
                            if source_data[file_id]['retirejs_result'] != []:
                                file_action += ' <button class="bttn-fill bttn-xs bttn-danger" onclick="retirejsResult({0}, {1}, {2})"><i class="fas fa-spider"></i> Vulnerabilities</button>'.format("'"+file_id+"'", "'"+analysis_id+"'", "'"+file_name+"'")
                        file_type = helper.fixpath(core.path + '/static/images/' + file_name.split('.')[-1] + '1.png')
                        if os.path.isfile(file_type):
                            file_type = file_name.split('.')[-1] + '1.png'
                        else:
                            file_type = 'other1.png'
                        file_type = url_for('static',filename='images/' + file_type)
                        file_type = '<img src="{0}" class="ft_icon">'.format(file_type)
                        file_html = "<tr><td>{2} {0}</td><td>{1}</td><td>{4}</td><td>{3}</td></tr>".format(file_name, rel_path, file_type, file_action, file_size)
                        files_table += file_html
                    files_table += '</tbody></table>'


                    # table consisting of ipv6 and ipv4 addresses
                    if report_data['ipv4_addresses'] == [] and report_data['ipv6_addresses'] == []:
                        ips_table = '<h3 class="nothing">No IPv4 or IPv6 addresses found!</h3>'
                    else:
                        ips_table = '<table class="result-table" id="ips_table"><thead><tr><th>IP Address</th><th>Type</th><th>File</th></tr></thead><tbody>'
                        for ip in report_data['ipv4_addresses']:
                            ips_table += '<tr><td>{0}</td><td>{1}</td><td>{2}</td></tr>'.format(ip['address'], 'IPv4', ip['file'])
                        for ip in report_data['ipv6_addresses']:
                            ips_table += '<tr><td>{0}</td><td>{1}</td><td>{2}</td></tr>'.format(ip['address'], 'IPv6', ip['file'])
                        ips_table += '</tbody></table>'


                    # table consisting of emails
                    if report_data['emails'] != []:
                        mails_table = '<table class="result-table" id="mails_table"><thead><tr><th>Email Address</th><th>File</th></tr></thead><tbody>'
                        for mail in report_data['emails']:
                            mails_table += '<tr><td>{0}</td><td>{1}</td></tr>'.format(mail['mail'], mail['file'])
                        mails_table += '</tbody></table>'
                    else:
                        mails_table = '<h3 class="nothing">No email addresses found in any of the files!</h3>'

                    # table containing btc addresses
                    if report_data['bitcoin_addresses'] != []:
                        btc_table = '<table class="result-table" id="btc_table"><thead><tr><th>BTC Address</th><th>File</th></tr></thead><tbody>'
                        for mail in report_data['bitcoin_addresses']:
                            btc_table += '<tr><td>{0}</td><td>{1}</td></tr>'.format(mail['address'], mail['file'])
                        btc_table += '</tbody></table>'
                    else:
                        btc_table = '<h3 class="nothing">No Bitcoin Address found!</h3>'

                    # table containing comments
                    if report_data['comments'] != []:
                        comments_table = '<table class="result-table" id="comments_table"><thead><tr><th>Comment</th><th>File</th></tr></thead><tbody>'
                        for comment in report_data['comments']:
                            comments_table += '<tr><td>{0}</td><td>{1}</td></tr>'.format(helper.escape(comment['comment']), comment['file'])
                        comments_table += '</tbody></table>'
                    else:
                        comments_table = '<h3 class="nothing">No comments found in any js/html/css files!</h3>'


                    # table containing base64 encoded strings
                    if report_data['base64_strings'] != []:
                        base64_table = '<table class="result-table" id="base64_table"><thead><tr><th>Base64 Encoded String</th><th>File</th></tr></thead><tbody>'
                        for b64 in report_data['base64_strings']:
                            base64_table += '<tr><td>{0}</td><td>{1}</td></tr>'.format(b64['string'], b64['file'])
                        base64_table += '</tbody></table>'
                    else:
                        base64_table = '<h3 class="nothing">No base64 encoded string found in any js/html/css files!</h3>'

                    manifest_content = json.dumps(report_data['manifest'])

                    '''
                    Files count
                    '''
                    js_files_count = len(report_data['files']['js'])
                    css_files_count = len(report_data['files']['css'])
                    html_files_count = len(report_data['files']['html'])
                    json_files_count = len(report_data['files']['json'])
                    other_files_count = len(report_data['files']['other'])
                    static_files_count = len(report_data['files']['static'])

                    return render_template("report.html",
                                            extension_type = extension_type, 
                                            graph_data = graph_data, 
                                            basic_info = basic_info_t, 
                                            urls_table = urls_table, 
                                            permissions_div = permissions_div, 
                                            analysis_id=analysis_id, 
                                            files_table=files_table, 
                                            manifest_content=manifest_content,
                                            domains_table = domains_table,
                                            base64_table = base64_table,
                                            comments_table = comments_table,
                                            ips_table = ips_table,
                                            btc_table = btc_table,
                                            mails_table = mails_table,
                                            extjs_table = extjs_table,
                                            urls_count = urls_count,
                                            extjs_count = extjs_count,
                                            permissions_count = permissions_count,
                                            unique_domains = unique_domains,
                                            js_files_count = js_files_count,
                                            css_files_count = css_files_count,
                                            html_files_count = html_files_count,
                                            json_files_count = json_files_count,
                                            other_files_count = other_files_count,
                                            static_files_count = static_files_count
                                        )
                
                
                else:
                    error_txt = 'All the result files are not found.. Try scanning the extension again! and don\'t mess with the result files this time'
                    return render_template('error.html', error_title = "Malformed Result", error_head = "Incomplete Result", error_txt=error_txt)
           
           
            else:
                error_txt = 'The result directory corresponding to result id {0} could not be found... hence ExtAnalysis has nothing to show'.format(analysis_id)
                return render_template('error.html', error_title = "Result Directory Not Found", error_head = "Result Directory Not Foundt", error_txt=error_txt)
    
    except:
        logging.error(traceback.format_exc())
        return render_template('error.html', error_title = "Invalid Result ID", error_head = "Invalid Result ID" , error_txt='There seems to be no result corresponding to the provided ID. Did you delete the result? or maybe you did some weird shit with the parameter?')

# ==========================================
# FROM: frontend/viewsource.py
# ==========================================

"""
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
"""


def viewsource_view(url):
    try:
        decoded_url = base64.b64decode(url).decode('ascii')
        scstat = scan.source_code(decoded_url)
        if scstat[0]:
            # Successful 
            source_code = scstat[1]
            icon_url = url_for('static',filename='images/url1.png')
            url_icon = '<img src="' + icon_url + '">'
            return render_template('sourcecode.html', 
                                    source_code = source_code,
                                    url_icon = url_icon,
                                    target_url = decoded_url
                                )
        else:
            return render_template('error.html', error_title = "Error Encountered!", error_head = "Error getting source code!" , error_txt='Something went wrong while getting source code of the given url!<br>Error: ' + scstat[1])

    except:
        logging.error(traceback.format_exc())
        return render_template('error.html', error_title = "Error Encountered!", error_head = "Invalid URL Parameter" , error_txt='Something went wrong while decoding url!')



# ==========================================
# FROM: extanalysis.py
# ==========================================

#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
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
"""


# Default values for host and port (Gunicorn-friendly)
host = os.environ.get('HOST', '127.0.0.1')
port = int(os.environ.get('PORT', 13337))

# In cloud environments, we must bind to all interfaces
if 'PORT' in os.environ:
    host = '0.0.0.0'

allowed_extension = set(['crx', 'zip', 'xpi', 'tar', 'gzip'])
werkzeug_log = logging.getLogger('werkzeug')
werkzeug_log.setLevel(logging.ERROR)

def run_cli():
    global host, port
    parser = argparse.ArgumentParser(prog='extanalysis.py', add_help=False)
    parser.add_argument('-h', '--host', help='Host to run ExtAnalysis on. Default host is 127.0.0.1')
    parser.add_argument('-p', '--port', help='Port to run ExtAnalysis on. Default port is 13337')
    parser.add_argument('-v', '--version', action='store_true', help='Shows version and quits')
    parser.add_argument('-u', '--update', action='store_true', help='Checks for update')
    parser.add_argument('-q', '--quiet', action='store_true', help='Quiet mode shows only errors on cli!')
    parser.add_argument('-n', '--nobrowser', action='store_true', help='Skips launching a web browser')
    parser.add_argument('--help', action='store_true', help='Shows this help menu and exits')
    args = parser.parse_args()

    # Set host and port from CLI if provided
    if args.host is not None:
        host = args.host
    if args.port is not None:
        port = int(args.port)
        
    # enable Quiet mode
    if args.quiet:
        core.quiet = True

    # help
    if args.help:
        parser.print_help()
        parser.exit()

    # version
    if args.version:
        print('ExtAnalysis Version: ' + core.version)
        exit()

    if args.update:
        check()

    core.print_logo()
    settings.init_settings()
    main_url = 'http://{0}:{1}'.format(host, port)
    # Skip browser launch in production/cloud environments
    if args.nobrowser is not True and 'PORT' not in os.environ:
        webbrowser.open(main_url)
    print('\n[~] Starting ION SecOps Extension Analyzer at: {0} \n\n'.format(main_url))
    app.run(host=host, port=port, debug=False)


# core.updatelog('Initiating settings...')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extension


csrf = CSRFProtect()
app = Flask('ION SecOps Extension Analyzer')
app.config['UPLOAD_FOLDER'] = core.lab_path
app.secret_key = str(os.urandom(24))
csrf.init_app(app)


@app.errorhandler(404)
def page_not_found(e):
    error_txt = 'The page you are trying to browse does not exist... Please click on the logo to go back to homepage.'
    return render_template('error.html', error_title="Error 404 - Page Not Found!",
                           error_head="The page you are looking for is kinda imaginary!", error_txt=error_txt), 404


@app.errorhandler(500)
def internal_error(e):
    error_txt = 'Welp! There\'s no good way of telling this but something has gone terribly wrong with the program!'
    return render_template('error.html', error_title="Error 500 - Internal Server Error!",
                           error_head="Something seriously went wrong... ", error_txt=error_txt), 500


@app.route("/")
def home():
    core.updatelog('Accessed Main page')
    sett = open(core.settings_file, 'r', encoding='utf-8')
    settings_json = sett.read()
    return render_template("index.html",
                           report_dir=core.reports_path,
                           lab_dir=core.lab_path,
                           virustotal_api=core.virustotal_api,
                           settings_json=settings_json
                           )


@app.route('/upload/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return ('error: No File uploaded')
        file = request.files['file']
        if file.filename == '':
            return ('error: Empty File!')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            core.updatelog('File Uploaded.. Filename: ' + filename)
            # saveas = filename.split('.')[0]
            anls = analysis.analyze(filename)
            return (anls)
        else:
            return (
                'error: Invalid file format! only .crx files allowed. If you\'re trying to upload zip file rename it to crx instead')


@app.route("/api/", methods=["POST"])
def api():
    if request.method == 'POST':
        # query = request.args.get('query')
        query = request.form['query']
        return api_view(query, request.args)


@app.route("/log/")
def updatelogs():
    return (core.log)


@app.route('/view-graph/<analysis_id>')
def large_graph(analysis_id):
    return viewgraph_view(analysis_id)


@app.route('/view-source/<analysis_id>/<file_id>')
def view_source(analysis_id, file_id):
    return viewfile_view(analysis_id, file_id)


@app.route('/source-code/<url>')
def route_source_code(url):
    return viewsource_view(url)


@app.route('/analysis/<analysis_id>')
def show_analysis(analysis_id):
    return viewresult_view(analysis_id)


if __name__ == "__main__":
    run_cli()
