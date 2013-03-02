# Changelog for Hayaku

## 1.3.3 <sup>2013.03.02</sup>

- **New setting:** `hayaku_CSS_syntax_quote_symbol` for used quote symbol ([#71][])

- **New setting:** `hayaku_CSS_syntax_url_quotes` for wrapping clipboarded links in urls with quotes ([#208][])

- Added support for `user-select` property ([#207][])

- Fixing values in abbreviations for `opacity` property ([#209][])

- Don't add units if the value could be unitless (like `line-height`), also `hayaku_CSS_units_for_unitless_numbers` setting for this ([#153][])

[#71]: https://github.com/hayaku/hayaku/issues/71
[#207]: https://github.com/hayaku/hayaku/issues/207
[#208]: https://github.com/hayaku/hayaku/issues/208
[#209]: https://github.com/hayaku/hayaku/issues/209
[#153]: https://github.com/hayaku/hayaku/issues/153

## 1.3.2 <sup>2013.02.27</sup>

- Fix the importing method for ST3 again, now should work from the `.sublime-package`.

## 1.3.1 <sup>2013.02.08</sup>

- Fix the importing method, now the plugin would work from PC in ST3 ([#205][])

[#205]: https://github.com/hayaku/hayaku/issues/205

## 1.3.0 <sup>2013.02.07</sup>

- **Support for [Sublime Text 3](http://www.sublimetext.com/3) ([#201][])**

- Fixed inline comment setting for OS X and Linux ([#200][], thanks to @freshmango)

- Disable inline commenting in functions and quotes ([#203][])

[#200]: https://github.com/hayaku/hayaku/issues/200
[#201]: https://github.com/hayaku/hayaku/issues/201
[#203]: https://github.com/hayaku/hayaku/issues/203

## 1.2.1 <sup>2012.12.23</sup>

- Hotfixing automatic new line after expand's bug ([#190][])

[#190]: https://github.com/hayaku/hayaku/issues/190

## 1.2.0 <sup>2012.12.23</sup>

- **New feature:** [basic clipboard defaults](https://github.com/hayaku/hayaku/#clipboard-defaults) (for colors and urls) ([#180][])
- **New setting:** optional [automatic new line after expand](https://github.com/hayaku/hayaku/#automatic-new-line-after-expand) (not by default) ([#123][])
- Better handling of multiple carets in snippets ([#188][])
- Fixed an issue with color postexpands and their default values ([#189][])
- Restructured the repo, so it would be better updatable and maintainable.

[#123]: https://github.com/hayaku/hayaku/issues/123
[#180]: https://github.com/hayaku/hayaku/issues/180
[#188]: https://github.com/hayaku/hayaku/issues/188
[#189]: https://github.com/hayaku/hayaku/issues/189

## 1.1.1 <sup>2012.12.16</sup>

- Fixed bug with more than 99 completion parts in a snippet (`display: inline` affected) ([#182][])
- Fixed bug with wrong position of color postexpand in prefixed clusters ([#183][])
- Better handling for values that can be parts of other values in postexpands ([#184][])
- Overall refactoring of the postexpands, not completed, but already fixed some minor issues and the code is almost ready for moving the postexpands to the dictionaries.

[#182]: https://github.com/hayaku/hayaku/issues/182
[#183]: https://github.com/hayaku/hayaku/issues/183
[#184]: https://github.com/hayaku/hayaku/issues/184

## 1.1.0 <sup>2012.12.10</sup>

- **Changed default setting**: now when you use the block expand it expands to the more common code style.
- **New feature:** added [importance to the postexpand](https://github.com/hayaku/hayaku/#postexpand-for-importance) ([#156][])
- **New setting:** disabling the [inline comment](https://github.com/hayaku/hayaku/#inline-comments) shortcut for CSS ([#169][])
- **New setting:** [handling the case of expanded colors](https://github.com/hayaku/hayaku/#colors-case) ([#177][])
- **New setting:** [handling the length of expanded colors](https://github.com/hayaku/hayaku/#shorthand-colors) ([#50][])
- Moved the default syntax settings to code, so no restart needed for them to apply ([#160][])
- Don't indent prefixed properties when using Stylus or Sass ([#176][])

[#169]: https://github.com/hayaku/hayaku/issues/169
[#156]: https://github.com/hayaku/hayaku/issues/156
[#160]: https://github.com/hayaku/hayaku/issues/160
[#176]: https://github.com/hayaku/hayaku/issues/176
[#177]: https://github.com/hayaku/hayaku/issues/177
[#50]:  https://github.com/hayaku/hayaku/issues/50

## 1.0.4 <sup>2012.11.29</sup>

- Fixed jumping to newline with proper indentation by tab/enter in  non-CSS syntaxes ([#166][])
- Fixed the occasional removing of the content right to the point where the tab/enter happened ([#168][])
- Allowing expand to work on a line with other properties (“single line” code style) ([#170][])
- Some minor refactoring.

[#166]: https://github.com/hayaku/hayaku/issues/166
[#168]: https://github.com/hayaku/hayaku/issues/168
[#170]: https://github.com/hayaku/hayaku/issues/170

## 1.0.3 <sup>2012.11.27</sup>

- **New feature:** Added a way to write [color abbreviations for rgba](https://github.com/hayaku/hayaku/#rgba-values), like `cF.5` to `color: rgba(255,255,255,.5)` etc. ([#66][])
- Removed colons from default Stylus syntax ([#161][])
- Fixed possible leaks of default values ([#164][])

[#66]:  https://github.com/hayaku/hayaku/issues/66
[#161]: https://github.com/hayaku/hayaku/issues/161
[#164]: https://github.com/hayaku/hayaku/issues/164

## 1.0.2 <sup>2012.11.26</sup>

- Tab didn't work at the empty line after the last statement in Stylus/Sass ([#146][])
- Enhanced the behaviour of the `enter`/`tab` at the end of the prefixed cluster ([#52][])
- Fixed strange bugs in expands, when the `<dimension>` token could show up ([#155][])
- Upgraded expand code block action (you can press `enter` inside the brackets — in this position: `{|}` — to create a block), so it is not hardcoded now ([#159][])
- Added an option to disable postexpand ([#152][])

[#146]: https://github.com/hayaku/hayaku/issues/146
[#52]:  https://github.com/hayaku/hayaku/issues/52
[#155]: https://github.com/hayaku/hayaku/issues/155
[#159]: https://github.com/hayaku/hayaku/issues/159
[#152]: https://github.com/hayaku/hayaku/issues/152

## 1.0.1 <sup>2012.11.23</sup>

- Updated installation instructions ([#147][])

[#147]: https://github.com/hayaku/hayaku/issues/147

## 1.0.0 <sup>2012.11.22</sup>

- Initial public alpha