# Changelog for Hayaku

## 1.0.4 (2012.11.29)

- Fixed jumping to newline with proper indentation by tab/enter in  non-CSS syntaxes ([#166][])
- Fixed the occasional removing of the content right to the point where the tab/enter happened ([#168][])
- Allowing expand to work on a line with other properties (“single line” code style) ([#170][])
- Some minor refactoring.

[#166]: https://github.com/hayaku/hayaku/issues/166
[#168]: https://github.com/hayaku/hayaku/issues/168
[#170]: https://github.com/hayaku/hayaku/issues/170

## 1.0.3 (2012.11.27)

- **New feature:** Added a way to write color abbreviations as rgba, like `cF.5` to `color: rgba(255,255,255,.5)` etc. ([#66][])
- Removed colons from default Stylus syntax ([#161][])
- Fixed possible leaks of default values ([#164][])

[#66]:  https://github.com/hayaku/hayaku/issues/66
[#161]: https://github.com/hayaku/hayaku/issues/161
[#164]: https://github.com/hayaku/hayaku/issues/164

## 1.0.2 (2012.11.26)

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

## 1.0.1 (2012.11.23)

- Updated installation instructions ([#147][])

[#147]: https://github.com/hayaku/hayaku/issues/147

## 1.0.0 (2012.11.22)

- Initial public alpha