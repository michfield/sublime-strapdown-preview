import sys
import os
import re

import urllib.request

import html
import webbrowser

import sublime
import sublime_plugin

from threading import Timer

# Check if this is Sublime Text 2
#
ST2 = sys.version_info < (3, 3)

# Location of Strapdown.js files with themes
#
STRAPDOWN_LIB_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'strapdown'))

def getTempFilename(view):
  file = os.path.join(sublime.packages_path(), 'strapdown-preview-%s.html' % view.id())

  # Remove the temporary file after 15 seconds.
  Timer(15, lambda: os.remove(file)).start()

  return file

class StrapdownMarkdownPreviewCommand(sublime_plugin.TextCommand):
  def run(self, edit, target = 'browser'):
    self.settings = sublime.load_settings("Strapdown Markdown Preview.sublime-settings")

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
    output_html = u'<!DOCTYPE html><html><head><meta charset="%s"><title>%s</title></head>\n' % (encoding, title)
    output_html += '<xmp theme="%s" style="display:none;">\n\n' % theme
    output_html += contents
    output_html += '\n</xmp>'

    config_local = self.settings.get('strapdown', 'remote')
    if config_local and config_local == 'local':
      output_html += '<script src="%s"></script>' % urllib.request.pathname2url(os.path.join(STRAPDOWN_LIB_DIR, "strapdown.js"))
    else:
      output_html += '<script src="' + html.escape(self.settings.get('remote', 'http://strapdownjs.com/v/0.2/strapdown.js')) + '"></script>'

    output_html += '</html>'

    # Update output HTML file. It is executed both for disk and also for
    # browser targets
    #
    if target in ['disk', 'browser']:

      if not self.view.file_name():
        target = "browser"

      if target == "disk":
        target_file = os.path.splitext(self.view.file_name())[0] + ".html"

      elif target == "browser":
        target_file = getTempFilename(self.view)

      with open(target_file, 'wt', encoding=encoding) as f:
        f.write(output_html)

      browser = self.settings.get('browser')
      controller = webbrowser.get(browser)
      controller.open(target_file)
      sublime.status_message('Preview launched in default browser')

    elif target == 'sublime':
      new_view = self.view.window().new_file()
      new_view.set_name(title + ".html")
      new_view.insert(edit, 0, output_html)
      sublime.status_message('Preview launched in Sublime Text')

  def getMeta(self, string):
    filename = self.view.file_name()

    if filename:
      title, extension = os.path.splitext(os.path.basename(filename))
    else:
      title = self.view.name() or 'Untitled document'

    result = {"title": title, "theme" : self.settings.get('theme', 'united') }

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
