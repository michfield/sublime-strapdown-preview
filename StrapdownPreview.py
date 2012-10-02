import sublime, sublime_plugin
import desktop
import tempfile
import os
import sys
import re

settings = sublime.load_settings('StrapdownPreview.sublime-settings')

def getTempFilename(view):
  return os.path.join(tempfile.gettempdir(), '%s.html' % view.id())

class StrapdownPreviewListener(sublime_plugin.EventListener):
  """ update the output html when file has already been saved once """

  def on_post_save(self, view):
    if view.file_name().endswith(('.md', '.markdown', '.mdown')):
      temp_file = getTempFilename(view)

      if os.path.isfile(temp_file):
        # reexec markdown conversion
        print 'started again but on disk'
        view.run_command('strapdown_preview', {'target': 'disk'})
        sublime.status_message('Strapdown.js preview file updated')

class StrapdownPreviewCommand(sublime_plugin.TextCommand):
  def run(self, edit, target = 'browser'):

    contents = self.view.substr(sublime.Region(0, self.view.size()))
    encoding = self.view.encoding()

    if encoding == 'Undefined':
        encoding = 'utf-8'
    elif encoding == 'Western (Windows 1252)':
        encoding = 'windows-1252'

    # read header content
    title, theme = self.getMeta(contents)

    # check if LiveReload ST2 extension installed
    livereload_installed = ('LiveReload' in os.listdir(sublime.packages_path()))

    # construct the content
    html = u'<!DOCTYPE html>\n'
    html += '<html>\n'
    html += '<head>\n'
    html += '<meta charset="%s">\n' % encoding
    html += '<title>%s</title>\n' % title
    html += '</head>\n'
    html += '<xmp theme="%s" style="display:none;">\n' % theme
    html += contents
    html += '\n</xmp>\n'
    html += '<script src="http://strapdownjs.com/v/0.1/strapdown.js"></script>\n'

    if livereload_installed:
      html += '<script>document.write(\'<script src="http://\' + (location.host || \'localhost\').split(\':\')[0] + \':35729/livereload.js?snipver=1"></\' + \'script>\')</script>\n'

    html += '</html>'

    if target in ['disk', 'browser']:
      # update output html file (executed both for disk and browser targets)

      tmp_fullpath = getTempFilename(self.view)
      tmp_html = open(tmp_fullpath, 'w')
      tmp_html.write(html.encode(encoding))
      tmp_html.close()

      if target == 'browser':
        config_browser = settings.get('browser', 'default')

        if config_browser and config_browser != 'default':
          cmd = '"%s" %s' % (config_browser, tmp_fullpath)
    
          if sys.platform == 'darwin':
            # Mac OSX
            cmd = "open -a %s" % cmd
            print "Strapdown.js Preview: executing", cmd
            result = os.system(cmd)

            if result != 0:
              sublime.error_message('cannot execute "%s" Please check your Markdown Preview settings' % config_browser)
            else:
              sublime.status_message('Strapdown.js preview launched in %s' % config_browser)

        else:
          # open default browser
          desktop.open(tmp_fullpath)
          sublime.status_message('Strapdown.js preview launched in default HTML viewer')

    elif target == 'sublime':
      new_view = self.view.window().new_file()
      new_edit = new_view.begin_edit()
      new_view.insert(new_edit, 0, html)
      new_view.end_edit(new_edit)
      sublime.status_message('Strapdown.js preview launched in sublime')

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

