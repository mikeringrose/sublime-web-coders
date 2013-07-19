import sublime, sublime_plugin
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
