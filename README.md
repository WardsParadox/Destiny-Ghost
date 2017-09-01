## Destiny-Ghost
![ghost](ghost.png)

Pulls data out of your Follett Destiny/Asset Manager and changes values on the machine to match.

## Note
Use the binary releases. It includes pytds already. If you want to help develop,
install pytds:

`pip install --user pytds`

## Usage
```
usage: ghost.py [-h] [--computername] [--assettag] [--lockmessage] [--debug]

Set's Computer info based on Follet Asset Manager info. You must have the
devices serial number entered inside of Asset Manager. It can set computer
name, the lock message to a custom message with additional info, and the
barcode into computer info 1.

optional arguments:
  -h, --help      show this help message and exit
  --computername  Sets Computer Name based on DistrictID
  --assettag      Sets Computer Info Field 1 as the barcode
  --lockmessage   Sets Lock Message to include info based on other arguments.
  --debug         Turns Debug Logging On.
```
Requires a file called `config.json` to be in the same directory as ghost. See `config_example.json`.

## Deployment
#### Recommended:
Use Outset to Launch with Arguments

_Image Credit: [3d-bear](http://3d-bear.tumblr.com/post/152604050800/ghost-shell-3d-sprite-destiny-my-boyfriend)_
