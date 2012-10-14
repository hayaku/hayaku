# Hayaku

Hayaku is a bundle of useful scripts aiming for rapid front-end web development.

The main aim is to create the fastest way to write and maintain CSS code in an editor.

## Table of Contents

1. [Install Hayaku for Sublime Text](#install-hayaku-for-sublime-text)
2. [Features](#features)



## Install Hayaku for [Sublime Text](http://www.sublimetext.com/2)

To install hayaku write this in your Sublime Packages directory:

``` sh
git clone git://github.com/hayaku/hayaku.git
```

Or wait untill we'll submit hayaku to Sublime Package Control (when it'd be ready for it)



## Features

### Smart CSS Abbreviations

Hayaku is not your average snippet engine. Most of the CSS snippets to date are static — you need to remember all the abbreviations if you want to use them.

Hayaku offers a better and faster way: you don't need to remember anything, you can just try to write the shortest abbreviation for a thing you want to write in CSS — and Hayaku would try to guess it when you press `tab`.

There are a lot of things Hayaku can do in abbeviations, here are some of them:

#### Fuzzy CSS property abbreviations

This is the first basic thing: Hayaku don't have any premade snippets for CSS, it have a dictionary with a lot of CSS properties, so when you write some abrakadabra, it tries to parse it and guess what you meant. For most properties those abbreviations could be rather short, but you're not sticked to them: you can write as much letters for a property as you wish.

So, writing `w`, `wi` or `wid` would give you `width`. And don't forget about the fuzzy part: `wdt` and `wdth` would work too.

Sometimes you would guess that some abbreviations must become other things, but in most cases all the variants have some logic beyound. `b` could be expanded to `background` or `border`, but expanded to `bottom` instead — it's becouse all the “sides” values are abbreviated to just one letter: **l**eft,  **r**eft,  **t**op, so  **b**ottom goes by this path.

However, if you feel that some abbreviation just need to be not that is expands to, feel free to [fill up an issue](https://github.com/hayaku/hayaku/issues/new).

#### Smart CSS string values abbreviations

Here comes the second basic thing of Hayaku, the awesome one. You can expand abbreviations for the property+value parts, but you don't need to use any delimiters in those abbreviations! That's right — you can just write something like `por` and get `position:relative`!

This works also fuzzy, so to get `position:relative` you could use any number of letters: `pore`, `posrel`, `pstnrltv` etc. Also, if you want, you can still use a delimiter — just add a colon between the property and value and get the same result. So, if you want to stick to Zen style, use it — `pos:r` would work as intended. And `p:r` would work too — while `pr` would expand to `padding-right`, adding delimiter could help by removing ambiguity — padding can't have any values containing `r`, so hayaku falls to `position`.

#### Numeric values abbreviations



- - -

And this is just the start, there would be a lot of other nice features, so still tuned and follow the [official bundle's twitter](http://twitter.com/#!/hayakubundle)!

