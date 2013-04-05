import sys
import os
import subprocess
import sublime
import sublime_plugin

import re
import json
import tempfile

import urllib.request
import urllib.response
import urllib.error

from . import desktop

# Check if this is Sublime Text 2
#
ST2 = sys.version_info < (3, 3)

# Location of Strapdown.js files with themes
#
STRAPDOWN_LIB_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'strapdown'))

def getTempFilename(view):
  return os.path.join(tempfile.gettempdir(), '%s.html' % view.id())

class StrapdownMarkdownPreviewCommand(sublime_plugin.TextCommand):
  def run(self, edit, target = 'browser'):

    global settings
    settings = sublime.load_settings("Strapdown Markdown Preview.sublime-settings")

    contents = self.view.substr(sublime.Region(0, self.view.size()))
    encoding = self.view.encoding()

    if encoding == 'Undefined':
        encoding = 'utf-8'
    elif encoding == 'Western (Windows 1252)':
        encoding = 'windows-1252'

    # Read header with meta attributes
    #
    title, theme = self.getMeta(contents)

    if target != 'sublime':
      contents = self.fixLocalImages(contents)

    # Construct the content
    #
    html = u'<!DOCTYPE html>\n'
    html += '<html>\n'
    html += '<head>\n'
    html += '<meta charset="%s">\n' % encoding
    html += '<title>%s</title>\n' % title
    html += '</head>\n'
    html += '<xmp theme="%s" style="display:none;">\n' % theme
    html += contents
    html += '\n</xmp>\n'

    config_local = settings.get('strapdown', 'default')
    if config_local and config_local == 'local':
      html += '<script src="%s"></script>\n' % urllib.request.pathname2url(os.path.join(STRAPDOWN_LIB_DIR, "strapdown.js"))
    else:
      html += '<script src="http://strapdownjs.com/v/0.2/strapdown.js"></script>\n'

    html += '</html>'

    # Update output HTML file. It is executed both for disk and also for
    # browser targets
    #
    if target in ['disk', 'browser']:

      tmp_fullpath = getTempFilename(self.view)
      tmp_html = open(tmp_fullpath, 'wt', encoding=encoding)
      tmp_html.write(html)
      tmp_html.close()

      if target == 'browser':
        config_browser = settings.get('browser', 'default')

        if config_browser and config_browser != 'default':
          cmd = '%s "%s"' % (config_browser, tmp_fullpath)

          # In OS X is specific
          if sys.platform == 'darwin':
            cmd = "open -a %s" % cmd

          try:
            subprocess.Popen([config_browser, tmp_fullpath])
          except FileNotFoundError:
            sublime.error_message('System cannot find the command specified "%s". Please check plugin settings.' % config_browser)
          except:
            sublime.error_message('For an unknown reason the system failed to execute "%s". Please check plugin settings.' % config_browser)
          else:
            sublime.status_message('Preview successfully launched with command: "%s"' % config_browser)

        else:

          # Preview with default browser
          desktop.open(tmp_fullpath)
          sublime.status_message('Preview launched in default browser')

    elif target == 'sublime':
      new_view = self.view.window().new_file()
      new_edit = new_view.begin_edit()
      new_view.insert(new_edit, 0, html)
      new_view.end_edit(new_edit)
      sublime.status_message('Strapdown.js Preview launched in Sublime Text')

  def getMeta(self, string):

    filename = self.view.file_name()

    if filename:
      title, extension = os.path.splitext(os.path.basename(filename))
    else:
      title = 'Untitled document'

    result = { "title": title, "theme" : settings.get('theme', 'united') }

    match = re.search(re.compile(r'<!--.*title:\s*([^\n]*)\s*\n.*-->', re.IGNORECASE | re.DOTALL), string)
    if match:
      result["title"] = match.group(1)

    match = re.search(re.compile(r'<!--.*theme:\s*([^\n]*)\s*\n.*-->', re.IGNORECASE | re.DOTALL), string)
    if match:
      result["theme"] = match.group(1)

    return result["title"], result["theme"]

  # Fix relative paths
  #
  def fixLocalImages(self, string):

    def imgfix(match):
      tag, src = match.groups()
      filename = self.view.file_name()

      if filename:
        if not src.startswith(('file://', 'https://', 'http://', '/')):
          # abs_path = u'file://%s/%s' % (os.path.dirname(filename), src)
          abs_path = u'%s/%s' % (os.path.dirname(filename), src)
          abs_path = urllib.request.pathname2url(abs_path)
          tag = tag.replace(src, abs_path)

      return tag

    rexp = re.compile(r'(\!\[[^\]]*\]\((.*)\))')
    string = rexp.sub(imgfix, string)
    return string
