import sublime, sublime_plugin
import re, os, mimetypes
from base64 import b64encode
from urllib.request import urlopen
from urllib.parse import quote_plus, unquote_plus

class TextTransformer(sublime_plugin.TextCommand):
  def transform(self, edit, transformation):
    sels = self.view.sel()
    for sel in sels:
      txt = self.view.substr(sel)
      if txt:
        val = transformation(txt)
        sel = sublime.Region(sel.begin(), sel.end())
        self.view.replace(edit, sel, val)

class EncoderCommand(TextTransformer):
  def run(self, edit):
    self.transform(edit, quote_plus)

class DecoderCommand(TextTransformer):
  def run(self, edit):
    self.transform(edit, unquote_plus)

class BaseSixFourCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    sels = self.view.sel()
    curr_dir = os.path.dirname(self.view.file_name())

    for sel in sels:
      path = self.view.substr(sel)
      if path:
        resource = find_resource(path, curr_dir)
        if resource:
          sel = sublime.Region(sel.begin(), sel.end())
          self.view.replace(edit, sel, build_data_uri(resource))  
      else:
        print("no such file")

def build_data_uri(resource):
  encoded = b64encode(resource[1])
  return "data:" + resource[0] + ";base64," + encoded.decode('UTF-8')

def find_resource(filename, start_path):
  if filename[0] == '/':
    return read_file(start_path + '/..' + filename)
  elif re.match('^https?\://', filename):
    return read_url(filename)
  else:
    return read_file(start_path + '/' + filename)

def read_file(filename):
  retval = None
  if os.path.exists(filename):
    retval = (mimetypes.guess_type(filename)[0], open(filename, 'rb').read())
  return retval

def read_url(url):
  resp = urlopen(url)
  return (resp.getheader('Content-Type'), resp.read())
