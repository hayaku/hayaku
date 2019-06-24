# Hayaku <sup>[1.5.4](https://github.com/hayaku/hayaku/blob/master/CHANGELOG.md)</sup> [![Build Status][build]][build-link]
[build]: https://travis-ci.org/hayaku/hayaku.png?branch=master
[build-link]: https://travis-ci.org/hayaku/hayaku

Hayaku is a bundle of useful scripts aiming for rapid front-end web development.

The main aim of Hayaku is to create the fastest way to write and maintain CSS code in an editor.

# Table of Contents

1. [Install Hayaku for Sublime Text](#install-hayaku-for-sublime-text)

2. [Features](#features)
    - [Smart CSS Abbreviations](#smart-css-abbreviations)
        - [Fuzzy CSS property abbreviations](#fuzzy-css-property-abbreviations)
        - [Smart CSS values abbreviations](#smart-css-values-abbreviations)
        - [Numeric values in abbreviations](#numeric-values-in-abbreviations)
        - [Color values in abbreviations](#color-values-in-abbreviations) with [RGBA values](#rgba-values)
        - [Importance modifier](#importance-modifier)
        - [Default values](#Default-values)
        - [Clipboard defaults](#clipoard-defaults)
    - [Postexpands](#postexpands)
        - [Simple property postexpands](#simple-property-postexpands)
        - [Postexpands for units](#postexpands-for-units)
        - [Postexpands for colors](#postexpands-for-colors)
        - [Postexpand for importance](#postexpand-for-importance)
    - [Creating new CSS rule blocks](#creating-new-css-rule-blocks)
    - [Inline comments](#inline-comments)
    <br/><br/>
    - [Value cycling <sup>new!</sup>](#value-cycling)
        - [Supported value types](#supported-value-types)
        - [Basics](#basics)
        - [Key bindings](#key-bindings)

3. [Settings and Preferences](#settings-and-preferences)
    - [User dictionaries <sup>new!</sup>](#user-dictionaries)
        - [Syntax of user dictionaries](#syntax-of-user-dictionaries)
        - [User dictionary overrides](#user-dictionary-overrides)
    - [User aliases <sup>new!</sup>](#user-aliases)
    - [Using both dictionary and alias <sup>new!</sup>](#using-both-dictionary-and-alias)
    - [Extra scopes for dictionaries and aliases](#extra-scopes-for-dictionaries-and-aliases)
    - [Autoguessing the code style](#autoguessing-the-code-style)
    - [Single code style](#single-code-style)
    - [Automatic new line after expand](#automatic-new-line-after-expand)
    - [Quotes and URLs](#quotes-and-urls)
    - [Units for unitless values](#units-for-unitless-values)
    - [Prefixes options](#prefixes-options)
        - [The aligning for the prefixes](#the-aligning-for-the-prefixes)
        - [Using only specific prefixes](#using-only-specific-prefixes)
    - [Options for colors](#options-for-colors)
        - [Colors' case](#colors-case)
        - [Shorthand colors](#shorthand-colors)
    <br/><br/>

4. [Using Hayaku with CSS Preprocessors](#using-hayaku-with-css-preprocessors)

5. [License and copyrights](#license-and-copyrights)


# Install Hayaku for [Sublime Text](http://www.sublimetext.com/2)

Right now Hayaku is available only for Sublime Text (even for third version!), but when it would be complete, we would port it to some other editors.

#### Using [Package Control](http://wbond.net/sublime_packages/package_control):

1. Run `Package Control: Install Package` command
2. Search for `Hayaku - tools for writing CSS faster` (`Hayaku` should be enough) and wait for it to be installed
3. Restart Sublime Text (required to make default settings for different syntaxes to work)

#### Or manually, using git:

Clone repository into Packages directory (can be found using `Preferences: Browse Packages` command in Sublime Text)
``` sh
git clone git://github.com/hayaku/hayaku.git
```

And then restart Sublime Text.

## Note on autocomplete

**Important:** Hayaku disables the autocomplete for CSS by default. This was made to remove the ambiguosity and confusion that could happen when you'll see one result in autocomplete and would get something different on pressing `tab`.

You can restore the autocomplete by redefining the `auto_complete_selector` setting in your `User/Preferences.sublime-settings` to either the default value:

``` js
{
    "auto_complete_selector": "source - comment, meta.tag - punctuation.definition.tag.begin"
}
```

Or to anything other you'd like.

However, for CSS scopes this would only enable the autocompletes by `enter`, the `tab` autocomplete would still run the Hayaku when possible.

# Features

## Smart CSS Abbreviations

Hayaku is not your average snippet engine. Most of the CSS snippets to date are static — you need to remember all the abbreviations if you want to use them.

Hayaku offers a better and faster way: you don't need to remember anything, you can just try to write the shortest abbreviation for a thing you want to write in CSS — and Hayaku would try to guess it when you press `tab`.

There are a lot of things Hayaku can do in abbeviations, here are some of them:

### Fuzzy CSS property abbreviations

This is the first basic thing: Hayaku don't have any premade snippets for CSS, it have a dictionary with a lot of CSS properties, so when you write some abrakadabra, it tries to parse it and guess what you meant. For most properties those abbreviations could be rather short, but you're not sticked to them: you can write as much letters for a property as you wish.

So, writing `w`, `wi` or `wid` would give you `width`. And don't forget about the fuzzy part: `wdt` and `wdth` would work too.

Sometimes you would guess that some abbreviations must become other things, but in most cases all the variants have some logic beyound. `b` could be expanded to `background` or `border`, but expanded to `bottom` instead — it's becouse all the “sides” values are abbreviated to just one letter: **l**eft,  **r**ight,  **t**op, so  **b**ottom goes by this path.

However, if you feel that some abbreviation just need to be not that is expands to, feel free to [fill up an issue](https://github.com/hayaku/hayaku/issues/new).

### Smart CSS values abbreviations

Here comes the second basic thing of Hayaku, the awesome one. You can expand abbreviations for the property+value parts, but you don't need to use any delimiters in those abbreviations! That's right — you can just write something like `por` and get `position: relative`!

This works also fuzzy, so to get `position: relative` you could use any number of letters: `pore`, `posrel`, `pstnrltv` etc. Also, if you want, you can still use a delimiter — just add a colon between the property and value and get the same result. So, if you want to stick to Zen style, use it — `pos:r` would work as intended. And `p:r` would work too — while `pr` would expand to `padding-right`, adding delimiter could help by removing ambiguity — padding can't have any values containing `r`, so hayaku falls to `position`.

### Numeric values in abbreviations

Hayaku understands a lot of ways of writing numeric abbreviations.

- You can just write a number after abbreviation to treat it as a value: `w10` would expand to `width: 10px` (see? automatic pixels!).

- Negative numbers supported too: `ml-10` would expand to `margin-left: -10px`.

- If you'd write a dot somewhere in abbreviation, Hayaku would guess what you need `em`s, so `w10.5` would expand to `width: 10.5em`.

- There are some abbreviations for some units, like `percents` for `%`, or `.` for em, so `100p` would expand to `100%` and `10.` to `10em`.

- All other units are supported, `h2pt` would expand to `height:2pt` and so on. Fuzzy guess is there too: if you'd want `vh` you could write just `w10h` and get `width: 10vh`.

### Color values in abbreviations

Actually, you can not only expand strings and numbers, you can expand even colors using abbreviations! You can use different ways to achieve that (as anything in Hayaku), so just look at those examples:

- `c0` → `color: #000`
- `cF` → `color: #FFF` (use uppercase to tell Hayaku it's a color)
- `cFA` → `color: #FAFAFA`
- `c#fa` → `color: #FAFAFA` (no need in uppercase if you use `#`)

And, of course, this works everywhere you would expect colors to work, so `brc0` would expand to `border-right-color: #000;`

#### RGBA values

There is also a way to expand `rgba` values for colors — you can either use rgba's alpha after the dot, either use hexadecimal alpha after the full color, if you'd like. This would look like this:

- `c0.5` → `color: rgba(0,0,0,.5)`
- `cF.2` → `color: rgba(255,255,255,.2)`
- `cABCD` → `color: rgba(170,187,204,0.87)`
- `cABC80` → `color: rgba(170,187,204,0.5)`

You can also write just the dot and get the placeholder on the `alpha` part of the `rgba`:

- `cF00.` → `color: rgba(255,0,0,.[5])`

### Importance modifier

A nice little feature: add `!` after abbreviation and get ` !important` at the end. Not that importance is something you would want to use everyday, but still.

`dn!` would give you `display:none !important;`, yeah.

### Automatic vendor prefixes

If you need some vendor prefixes, Hayaku could provide them!

`bra1.5` would expand to this:

``` css
-webkit-border-radius: 1.5em;
        border-radius: 1.5em;
```

Right now there are no prefixes for values (like gradients etc.) but someday they'd be there.

### Default values

If you'd write something that is only a property (as Hayaku would guess), Hayaku would insert a snippet with some default value already selected for you, so you could start writing your own value to replace it or to press `tab` again to keep it and move forward. So, writing `w` would actually expand to `width: [100%]` (braces mean that this value is selected by default).

### Clipboard defaults

Aside from the normal defaults, Hayaku would try to use your clipboard for getting the value from it as the default value.

Right now it's available for colors and images urls:

- If you'd have color in hexadecimal, rgb(a) or hsl(a) in your clipboard, Hayaku would use it as a default shown value. That would work even is the value is hashless, so if you've copied `808080` from anywhere, then on expanding `c` you would get `color: #[808080]`.

- If you'd have an image url in your clipboard (even relative, Hayaku would look at extension), you'd have it added as default values along inside an `url()`. Also, see [quotes and URLs](#quotes-and-urls) settings on how to adjust the quoting of the inserted url if you want.

#### Configure clipboard defaults

Hayaku offers a setting to set up the behavior of the Clipboard defaults: `hayaku_CSS_clipboard_defaults`. It is an array of the value types that Hayaku could accept as the defaults. So, to disable all the clipboard defaults you could use this setting:

``` js
{
    "hayaku_CSS_clipboard_defaults": [""]
}
```

## Postexpands

“Postexpands” is a nice Hayaku's feature, that allows you to expand only the property at first and then use instant autocomplete for the values of numbers.

That must be said is that postexpand is a bit different from the usual abbreviation expands — it don't have any fuzzy search inside, so only the first letters matter. However, as you'd use it you would see that it is still a powerfull feature.

### Simple property postexpands

The simplest postexpand feature is autocomplete for the string values of different properties.

If you'd expand some property like `po` to `position: |;`, then you could start writing any of it's values and get they expanded right after the cursor. So, writing `a` would give you `position: a|bsolute;`.

### Postexpands for units

Another postexpand feature would allow you to firstly expand the property that can have numeric values, like `width` and then write only the digits and let Hayaku place the corresponding units automatically.

So, when you expand, for example, `w` to `width: |;`, you'd get different options:

- write any iteger like `10` and you'd get `width: 10|px;`
- write any float like `1.5` and you'd get `width: 1.5|em;`
- write an integer and them `e`, so you'd get `width: 10e|m;`
- if the value have any string values, you can also use them: writing `a` would give you `width: a|uto;`

Negative numbers could still be used and if you'd like any other unit, you could just write it down, the autocompleted units won't bother you.

### Postexpands for colors

As you can use shortcuts to colors in abbreviations, you could also write the color values after expanding only the property. The basics are the same: `color: |;` + `F` would give you `color: #F|FF;`, and so on. You can use or don't use the hash symbol.

Another somewhat obscure (but helpful) feature is postexpand for `rgba` colors. This is triggered by writing the comma after decimal value. There is also a shortcut to the alpha value.

- `color: 255,|` would transform to `color: rgba(255,|255,255,1);`
- `color: 255,.|` would transform to `color: rgba(255,255,255,.|5);`

There are a lot of things we could improve there, so stay tuned.

### Postexpand for importance

If you'd like to make some value important, you could just write the first symbols of `!important` keyword and Hayaku would autocomplete it for you.

### Disabling postexpands

If you'd wish to disable postexpands at all for some reason, you could use this setting for this: `"hayaku_CSS_disable_postexpand": true`

## Creating new CSS rule blocks

In Hayaku there is a simple but powerful feature: when you wrote a selector, you could just press `CMD+Enter` to get a block for writing CSS here.

## Inline comments

Another little helper: write `//` in CSS to have it expanded to `/* | */` (where the pipe is a caret placement).

If you'd wish to disable inline comments, you could use this setting: `"hayaku_CSS_disable_inline_comment": true`

*This feature is in development, we plan on adding a lot of things to make commenting fun.*

## Value cycling

Another big feature Hayaku provides — a powerful implementation of cycling values. You can use it to increment or decrement any numeric values (both in CSS and anywhere else) and to cycle through all the possible values for any given CSS property.

### Supported value types

- **CSS values** — both numeric, like `10px`, and string values, like in `position: fixed` are supported.
- **Dates in ISO format**.
- **Versions by semver**.
- **Just any numbers** — even inside word-like strings like `$foo4`.

### Basics

Unlike other similar implementations, Hayaku's cycling is much more powerful and polished:

- When nothing is selected, Hayaku finds the closest to the caret value in the line and cycles through it.

- When only part of a number is selected, Hayaku understands the context and cycles the selected digit, but handling the whole number, so you could easily increment/decrement numbers by 100, 1000 or 0.001 etc.

- Hayaku tries its best to save the position of the cursor or selection, by adjusting it after the replacement. This way you would always be at the same place as before no matter what.

- Hayaku perfectly handles multiple carets, cycling through each of them.

- Hayaku handles multiple lines selected, cycling through the first value in each line.

- Hayaku can cycle through values of CSS properties, like between `static`, `relative` and `absolute` for `position`.

- It can use all the Hayaku powers beneath! It already can use Hayaku's dictionary for cycling through CSS property values and treat properly properties that can't be negative, and there are a lot of things to appear in the next releases of Hayaku.

We are trying to make this feature as polished as we can, so feel free to report on any, even most minor bugs in cycling and propose improvements!

### Key bindings

The default command comes in three variants:

- `alt+↑` and `alt+↓` would call the default action — incrementing or decrementing numeric value by one, cycling CSS properties etc.
- `alt+ctrl+↑` and `alt+ctrl+↓` (`win` key instead of `ctrl` for windows) would call “lowered” action, it would do the same thing for everything except numeric values — it would increment or decrement them by `0.1`.
- `alt+shift+↑` and `alt+shift+↓` on the other hand would increment or decrement numeric values by `10`, doing all the same default stuff for other kinds of values.

If you'd like to use all your own keybindings or Hayaku's keybindings are come in conflict with other installed packages, you can disable the default keybindings using this setting in `User/Preferences.sublime-settings`:

``` js
"hayaku_use_default_cycling_keymaps": false
```

Otherwise, if you'd like a more precise control over any action, you can redefine a key binding for this action in your `User/*.sublime-keymap` like this:

``` js
{
    "keys": ["alt+up"],
    "command": "hayaku_cycling_through_values",
    "args": {"modifier": 1}
},
```

The `modifier` is both the direction (for the cycling) and the amount (for numeric), so to cycle backwards CSS values and to reduce the numbers by `3`, you can say there `"args": {"modifier": -3}.`

# Settings and Preferences

Hayaku have **a lot** of different configurable options, both for your code style and for different features you'd wish to use.

## User dictionaries

Hayaku don't have a preset list of snippets. It have a dictionary with properties, their values and other information Hayaku uses to make writing CSS a spectacular experience.

If you don't see a property you use, or a value for some property, or you'd like to change the defaults for anything, you could extend and override the built-in dictionary with anything you'd like.

That's where the three specific settings are coming into play from the box: `hayaku_user_dict`, `hayaku_syntax_dict` and `hayaku_project_dict`.

Those settings work in the same way, applying the provided dictionaries in the given order after the built-in one.

Why is there three settings — to let you make overrides in ST-way. Sublime Text have different scopes for preferences: User's, Syntax Specific and Project, when you declare any settings in the Preferences, all those settings are merged together. Although, each one specific setting is completely overriden by the setting with the same name in the next scope, so there is no simple way to merge things using one name. That's why Hayaku provides you with three settings: you can use `hayaku_user_dict` in your `User/Preferences.sublime-settings`, then add some other things using `hayaku_syntax_dict` in your Syntax Specific settings, like in `user/Stylus.sublime-settings`, and, finally, make overrides for your specific project in your `*.sublime-project` files.

The syntax of all three settings is the same, although don't forget, that for `.sublime-project` you need to place the settings into the `"settings": {}` key.

### Syntax of user dictionaries

Hayaku uses `json` for defining dictionaries, you can see the [build-in one](https://github.com/hayaku/hayaku/blob/master/dictionaries/hayaku_CSS_dictionary.json) as an example.

The dictionary is an array, consisting of property objects having this structure:

``` js
{
    "name": "position",
    "values": [ "static", "relative", "absolute", "fixed" ]
}
```

Where the `name` is the property's name and the `values` is the array of possible values.

This is the simplest example, however there could be more complex entries like this one:

``` js
{
    "name": "width, height, min-width, min-height",
    "values": [ "auto", "<dimension>" ],
    "default": "100%",
    "always_positive": true
}
```

There are four things to mention:

1. You can specify more than one property in `name`, just divide them by comma and optional spaces.

2. There are some special entities that can go into values, like `<dimension>`, this means that if there is a “property” entry with this name, it would be expanded to it. Think of it as of links.

3. There is a possible `default` key that contains the value that would be inserted in the result if there were no values given.

4. There is a `always_positive` key that tells Hayaku that this property accepts only positive numbers, so the Cycling feature won't reduce it below zero.

There are other possible values, you can read the build-in dictionary and see which ones (in future we would explain all of them in the docs, of course).

### User dictionary overrides

Except for the things mentioned above, there are some things you can use that are absent in the built-in dictinary.

The first one is an ability to remove values from the dictionary, just use `remove_values` key with the array of the values you'd like to remove from the given property.

For example, this User dictionary would remove `static` from `position`:

``` js
{
    "hayaku_user_dict": [
        {
            "name": "position",
            "remove_values": ["static"]
        }
    ]
}
```

The second thing is that you can control where the new values would go. By default they would be placed before all the built-in ones, but if you'll need to change this, you could define where all the non-defined values of built-in dictionary should go. This is done using `"..."` token in `values` array. An example:

``` js
{
    "hayaku_user_dict": [
        {
            "name": "position",
            "values": ["static", "..." ,"sticky"]
        }
    ]
}
```

Such dictionary would make the `static` value to go first, then all other built-in values would be placed and the `sticky` value would be the last one.

## User aliases

In some cases you would want some abbreviation to point to a different property, for example you would want `z` to point at `z-index` and not to `zoom`. For this purpose there are settings similar to the dictionary ones: `hayaku_user_aliases`, `hayaku_syntax_aliases` and `hayaku_project_aliases`:

``` js
{
    "hayaku_user_aliases": {
        "z": "z-index"
    }
}
```

would do the work for you.

You can alias both only properties (and it would work for complex abbreviations, so `z9` would be `z-index: 9` with an above abbreviation), and for property-value parts, so you can create an abbreviation like this:

``` js
{
    "hayaku_user_aliases": {
        "fv": "font: 11px/1.5 Verdana, sans-serif"
    }
}
```

And then tabbing after `fv` would give you the desired output.

However, you can also use a user dictionary for this:

``` js
{
    "hayaku_user_dict": {
        "CSS": [
            {
                "name": "font",
                "values": [
                    "11px/1.5 Verdana, sans-serif"
                ]
            }
        ]
    }
}
```

And then you could write `fver`, `fonve`, `f:v` or any other abbreviations that Hayaku would expand to the desired output.

## Using both dictionary and alias

The difference between creating an alias and defining a new value in a User Dict is that alias works like a static snippet (with an addition to possible values), but a new value in a Dict would be treated along other values and properties, Hayaku would still use its alrorithm and would select `font-variant` for `fv` instead of the `font: 11px/1.5 Verdana, sans-serif`.

However, one of the nice things in aliases is that they're aliases not to some static strings, but to Hayaku abbreviations. This way you can add this to your User settings:

``` js
{
    "hayaku_user_aliases": {
        "fv": "font:verdana"
    },
    "hayaku_user_dict": {
        "CSS": [
            {
                "name": "font",
                "values": [
                    "11px/1.5 Verdana, sans-serif"
                ]
            }
        ]
    }
}
```

And then you would have both abbreviations like `fove` to work, and `fv` would be aliased to the abbreviation that also would work like intended! This is also means reuse, so if you'd like to change that one value, you'll need to change it only in one place.

## Extra scopes for dictionaries and aliases

In a case you would need more than three scopes, you can add more using a `hayaku_extra_scopes` option that accepts an array of extra scopes.

For example, `"hayaku_extra_scopes": ['ololo'],` would allow you to define extra `hayaku_ololo_dict` and `hayaku_ololo_aliases` which would be merged after the `user`, `syntax` and `project` in the given order.

## Autoguessing the code style

The easiest way to set the basic settings for your codestyle, is to use `hayaku_CSS_syntax_autoguess` option:

``` js
{
    "hayaku_CSS_syntax_autoguess": [
        "    selector {              ",
        "        property: value;    ",
        "        }                   "
    ]
}
```

There you can use any whitespaces between the predefined keywords and they would be used by Hayaku. A few notes regarding this setting:

- You should use the newline symbol `\n` or multiple array items, because JSON don't support multiline well.
- For your convenience you can use any leading of trailing spaces. Trailing spaces would be stripped at all, leading spaces would be stripped as if there weren't spaces at the start of the selector.

Maybe someday there'd be a _real_ autoguessing, that would read your open stylesheet and find what better suits it, but not today.

## Single code style

If you don't want to use autoguessing, then you could define single options one by one. This would also be helpful if you'd want to redefine only some of the code styling settings in other project or syntax.

Here is a JSON with all the available single code styling options:

``` js
{
    "hayaku_CSS_whitespace_after_colon":        " ",
    "hayaku_CSS_whitespace_block_start_before": " ",
    "hayaku_CSS_whitespace_block_start_after":  "\n\t",
    "hayaku_CSS_whitespace_block_end_before":   "\n\t",
    "hayaku_CSS_whitespace_block_end_after":    ""
}
```

The names speak for themselves there.

The important thing is that the single code style settings always override the autoguessed one.

## Automatic new line after expand

That's somewhat experimental feature, that is disabled by default. To enable it use this setting:

``` js
{
    "hayaku_CSS_newline_after_expand": true
}
```

With this setting you could save a bit more time, cause Hayaku would add a new line after you expand your abbreviations. The only downside is that you'll need to delete a line when you finish with the selector or when you're inserting something between existing lines.

## Quotes and URLs

By default Hayaku uses double quotes for different CSS stuff (like `content: ""`). You can change this by setting this:

``` js
{
    "hayaku_CSS_syntax_quote_symbol": "'"
}
```

Also, by default the image urls wouldn't have quotes in CSS-like syntaxes and would have them in Sass or Stylus, you can override this automatic behaviour by setting `hayaku_CSS_syntax_url_quotes` setting to `true` or `false`.

## Units for unitless values

By default Hayaku won't add `em` or `px` after values for properties like `line-height`. If you're not using unit less values for those properties, you could enable them like this:

``` js
{
    "hayaku_CSS_units_for_unitless_numbers": true
}
```

## Prefixes options

If you don't want to use any prefixes at all (as if you're using some mixins for it in Stylus, or use prefix-free), you can disable them with that option:

``` js
{
    "hayaku_CSS_prefixes_disable": true
}
```

### The aligning for the prefixes

By default Hayaku aligns expanded prefixed properties in this nice way:

``` css
.foo {
    -webkit-transform: rotate(45deg);
       -moz-transform: rotate(45deg);
        -ms-transform: rotate(45deg);
         -o-transform: rotate(45deg);
            transform: rotate(45deg);
    }
```

This way it's easier to spot changes to a single prefixed property and to use multiline edit on them.

However, if you'd want to expand such properties left aligned, set

``` js
{
    "hayaku_CSS_prefixes_align": false
}
```

### Using only specific prefixes

This is not something that you would use often, but if you'd need, you could use only prefixes for browsers you want. There are two settings for this:

``` js
{
    "hayaku_CSS_prefixes_only": ["webkit","moz","o"],
    "hayaku_CSS_prefixes_no_unprefixed": true
}
```

- `hayaku_CSS_prefixes_only` is an array of the prefixes you'd want to use **only**. In the upper example I excuded `ms` prefix, so if you'd use meta to emulate all IE versions to IE7 for example, then you could remove `ms` prefix, so your CSS would be a bit cleaner.
- when `hayaku_CSS_prefixes_no_unprefixed` is set to `True`, such prefixed clusters won't contain the official unprefixed variant.

Right now there is no easy way to adjust prefixes per property, but it would be there in a near feature, so stay tuned!

## Options for colors

Note that those settings would work for every pre-set and expanded colors, like the default color values, but they won't work for postexpands due to their mechanics.

### Colors' case

You can tell Hayaku if you prefer `lowercase` or `uppercase` for color values, so it would change the case while expanding abbreviations like `c#f`, `cF` etc.

The default value is `uppercase`, so `c#f` would become `color: #FFF`. If you'd like to change that to `lowercase`, you can set it this way:

``` js
{
    "hayaku_CSS_colors_case": "lowercase"
}
```

And if you'd like it to leave the color as is, you could use value `initial`.

### Shorthand colors

By default Hayaku shortens the colous, so if there could be `#FFFFFF` expanded, Hayaku would make it `#FFF`.

However, if you wish, you can redefine this behavior using this setting:

``` js
{
    "hayaku_CSS_colors_length": "long"
}
```

That would make `cF` to be expanded into `color: #FFFFFF`.


# Using Hayaku with CSS Preprocessors

“Hey! I don't need to write CSS faster — I use Preprocessors!” you could say. But, well, you would still need to write all those extra symbols, so abbreviations would fit preprocessors well. And as Hayaku is highly customizable, you could use it with any preprocessor: Sass, Less, Stylus etc.

Right now only basic things are available, but in the future you could expand different mixins and functions too, so just wait for it.

- - -

And this is just the start, there would be a lot of other nice features, so still tuned and follow the [official bundle's twitter](http://twitter.com/#!/hayakubundle)!

# Acknowledgments

The initial idea of Hayaku for CSS came from the merged ideas of [Vadim Makeev](https://twitter.com/pepelsbey) ([Zen CSS](http://pepelsbey.net/2008/10/zen-css/)) and [Vitaly Harisov](https://twitter.com/harisov) ([CSS Snippets](http://vitaly.harisov.name/article/css-fast-typing.html)). Big thanks to them!

# License and copyrights

This software is released under the terms of the [MIT license](https://github.com/hayaku/hayaku/blob/master/LICENSE).
