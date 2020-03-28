ST3 » Strapdown.js Markdown Preview
===================================

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

`target` argument can be:

* `browser`: Creates a HTML file in the OS temporary folder and opens it with the configured browser.
* `disk`: Creates a HTML file within the folder of the original markdown file and
  opens it with the configured browser.
* `sublime`: Opens a new view in Sublime Text and puts the HTML content in it.

### Metadata


You can specify additional attributes on top of your text file / active
window. These details can change theme and the title of rendered file.
Just add a comment near the start, like this:

```
<!--
  Title: Strapdown.js Markdown Preview plugin for Sublime Text
  Theme: cerulean
-->
```

The idea is very similar to [YAML Front Matter][yamlfront] or
[MultiMarkdown metadata header block][mmeta], but it's more in line with
Strapdown.js idea. Thus using HTML comment markers as metadata markers.

Metadata can be anywhere in document. If some attribute is specified
multiple times, the last value will be used. For now, the only usable
attributes are `title` and `theme`.

[yamlfront]: https://github.com/mojombo/jekyll/wiki/YAML-Front-Matter
[mmeta]: https://github.com/fletcher/MultiMarkdown/wiki/MultiMarkdown-Syntax-Guide#metadata

## Licence

The code is available at
[GitHub](https://github.com/michfield/StrapdownPreview) under MIT
licence.


