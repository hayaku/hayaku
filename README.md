# Hayaku Bundle for Sublime Text 2

This is the bundle that contains all the features the Hayaku offers for [Sublime Text 2](http://www.sublimetext.com/2) editor.

## Installation

To install, go to the `Packages` folder and then:

    git clone git://github.com/hayaku/Hayaku-for-Sublime-Text-2.git
    
Then, init submodules:

    git submodule init
    git submodule update

Otherwise, if you have the latest git (1.6.5 and later), use the recursive clone instead:

    git clone git://github.com/hayaku/Hayaku-for-Sublime-Text-2.git --recursive

### Developing

If you want to push the changed submodule, change it's remote to the appropriate `read+write` one:

    git remote set-url origin git@github.com:hayaku/hayaku.git

### No git

Otherwise, if you don't have git, you can download the latest version using github and extact it to the `Packages` folder, plus, as GitHub don't currently give a way to download all submodules in one zip, download the [Core](https://github.com/hayaku/Hayaku-Core) and place it in `core` directory.

## Using

Right now you can do the following things:

- expand the CSS abbreviation by pressing `tab`;
- write inline comment in CSS writing `//`;
- open the CSS block by pressing the `CMD+Enter` after the desired selector.

All those features are in pre-alpha state now, there is almost no preferences you can use and there are a lot of bugs, so use the plugin with care and, please, file up any issues you find at the [Github Issues](https://github.com/hayaku/Hayaku-Core/issues/) of the core project.

## Expanding the CSS abbreviations

You can expand any of the CSS abbreviations just by casually pressing the `tab` key.

We'd disabled the default autocomplete in CSS for Sublime Text in the `CSS.sublime-settings`, 'cause it's useless in CSS and the Hayaku is so much better at guessing what you need!

For example, try the following abbreviations:

- `poa`
- `fstn`
- `bra`
- `w10`
- `cF`
- `m-.5`

And this is just the start, there would be a lot of other nice features, so still tuned and follow the [official bundle's twitter](http://twitter.com/#!/hayakubundle)!
