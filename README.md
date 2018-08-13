## Destiny-Ghost
![ghost](ghost.png)

Pulls data out of your Follett Destiny/Asset Manager and changes values on the machine to match.

## Note
You may use the package releases which includes pytds already (in egg form).

If you want to help develop, install pytds:

`easy_install --upgrade python-tds`

## Usage
```
usage: ghost.py [-h] [--computername] [--assettag] [--lockmessage] [--debug]
                [--config CONFIG]

Set's Computer info based on Follet Asset Manager info. You must have the
devices serial number entered inside of Asset Manager. It can set computer
name, the lock message to a custom message with additional info, and the
barcode into computer info 1.

optional arguments:
  -h, --help       show this help message and exit
  --computername   Sets Computer Name based on DistrictID
  --assettag       Sets Computer Info Field 1 as the barcode
  --lockmessage    Sets Lock Message to include info based on other arguments.
                   If no other arguments are specified, it will set whatever
                   is in config.json's lockmessage
  --debug          Turns Debug Logging On.
  --config CONFIG  Specify path to config.json
```
Requires a file called `config.json` to be either in the same directory as Ghost,
which is `/Library/Application Support/com.github.wardsparadox.destiny-ghost`.

See `config_example.json`.

## Deployment
#### Recommended:
Use Outset to Launch with Arguments *(outset script now included in destiny-ghost-pkg subdir)*

Copy the config_example.json located in repo

_Image Credit: [3d-bear](http://3d-bear.tumblr.com/post/152604050800/ghost-shell-3d-sprite-destiny-my-boyfriend)_
