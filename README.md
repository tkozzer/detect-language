# Detect Language
This is a simple widget that will check whether your current keyboard language input is "U.S." or "Pinyin" (or Mandarin Chinese). I created this widget to help me know which keyboard language is current while I do Duolingo exercises. 

## Project Description

I am currently learning Mandarin Chinese on Duolingo and I needed a way to see which keyboard language input is current. For those that are unfamiliar [Duolingo](https://www.duolingo.com) is a popular language learning application that has both a mobile app and web app. I mostly use the web app because I like to practice typing [pinyin](https://en.wikipedia.org/wiki/Pinyin). As you do the excersises, it switches back and forth between typing english and pinyin. For mac users, there is a very easy keyboard shortcut to switch back and forth which is **ctrl - spacebar**. This works really well, but one issue I was having I would forget which keyboard is current. Now on a mac you can see which language is current if you look in the top right corner of the title bar, but it was a bit annoying having to look up every time. I wanted to have a small widget that could be right next to the input box.

**Currently the only two languages supported are Chinese and English.**

## Prerequistes 

- python 3.9 or higher
- tkinter
- macOS 12.1 or higher*

**note: it most likely works on various versions of python and macOS, but this is what I have used to build and test the code*

## Installation
    git clone https://github.com/tkozzer/detect-language.git
    cd detect-language
    python main.py

## To Do List

- [ ] Add an exit button
- [ ] Add more languages
- [ ] Be able to customize attributes
