sublime-web-coders
==================

A set of encoders that I find handy for web development. Currently just three: 

* url encoding - encodes the selected string, shortcut is ctrl+shift+x
* url decoding - decodes the selected string, shortcut is cmd+shift+x
* base64 data uri encoding - looks for the given file and base64 encodes it into a data URI scheme, shortcut is ctrl+b

For base64 data uri encoding, the rules for locating the file are:
* if the file starts with '/', will look for the file in the directory of the currently opened file
* if the file starts with 'http://' or 'https://', will attempt to download the file
* all else fails, look relative to the current directory
