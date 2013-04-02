Strapdown.js Markdown Preview in Sublime Text
=============================================

Sublime Text 3 plug-in that allows you preview your markdown files in
your browser, using beautiful [Strapdown.js](http://strapdownjs.com/).

Strapdown.js is mixing some Javascript with
[Bootstrap](http://twitter.github.com/bootstrap/) (Twitter's HTML5 & CSS
framework) to show you beautiful presentation of your Markdown files.

The good thing about Strapdown.js is that resulting HTML, besides
looking very good and being themeable, also **contains unmodified**
Markdown content that can be easily edited anywhere and extracted back,
if you need it again.

## Installation

 - recommended is to use use [Sublime Package
   Manager](http://wbond.net/sublime_packages/package_control#Features)
 - press `Ctrl+Shift+P` then `Package Control: Install Package`
 - look for `Strapdown.js Markdown Preview` and install it.

## Usage

 - use `Ctrl+Shift+P` then `Strapdown.js Markdown Preview` to launch a
   preview
 - or bind some key in your user key binding, using a line like this
   one:
   `{ "keys": ["ctrl+alt+m"], "command": "strapdown_markdown_preview", "args": {"target": "browser"} },`
 
### Custom attributes

You can specify additional details on top of your text file / active
window. These details can change theme and the title of rendered file.
Just add a comment near the start, like this:

```
<!--
  title: This file's title
  theme: cerulean
-->
```

## Licence

The code is available at
[GitHub](https://github.com/michfield/StrapdownPreview) under MIT
licence.
