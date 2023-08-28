***flacpack*** is a simple tool packing cuesheet and cover front image
inside the FLAC file.

***flacpack*** works fine on current Debian sid and requires following
packages:

* python3-mutagen;
* python3-chardet.

***flacpack*** can pack cuesheet inside the FLAC file:

```
flacpack sample.flac
```

Packing cover front image is optional, only JPEG image:

```
flacpack -p folder.jpg sample.flac
```

***flacpack*** can extract cuesheet from FLAC as well if there is one in
metadata and there is only FLAC file inside the parent directory:

```
flacpack sample.flac
```

More information is available on my [web-site](https://codej.ru/iMOCFZNc) or
in terminal with the key --help.

```
flacpack --help
```

***flacpack*** is free, you can use it in accordance with GNU GPLv3. Be aware,
some [donation](https://yoomoney.ru/to/410015590807463) would be excellent.
