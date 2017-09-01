#!/usr/bin/python
'''
Pull data from  Follett Destiny (Specifically Asset Manager) and change your computer name to match
'''
# Standard Imports
import json
import argparse
import subprocess
import logging
import os.path
import sys
# Custom Imports
import pytds
from Foundation import CFPreferencesSynchronize, \
                       CFPreferencesSetValue, \
                       kCFPreferencesAnyUser, \
                       kCFPreferencesAnyHost
# Set up argparse
parser = argparse.ArgumentParser(
    description="Set's Computer info based on Follet Asset Manager info. You must have the devices serial number entered inside of Asset Manager. It can set computer name, the lock message to a custom message with additional info, and the barcode into computer info 1.")
parser.add_argument("--computername",
                    help="Sets Computer Name based on DistrictID",
                    action="store_true")
parser.add_argument("--assettag",
                    help="Sets Computer Info Field 1 as the barcode",
                    action="store_true")
parser.add_argument("--lockmessage",
                    help="Sets Lock Message to include info based on other arguments. If no other arguments are specified, it will set whatever is in config.json's lockmessage",
                    action="store_true")
parser.add_argument("--debug",
                    help="Turns Debug Logging On.",
                    action="store_true")
args = parser.parse_args()
level = logging.INFO
if args.debug:
    level = logging.DEBUG
logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %I:%M:%S %p',
                    level=level,
                    filename=os.path.join('/Library/Logs/destiny-ghost.log'))
stdout_logging = logging.StreamHandler()
stdout_logging.setFormatter(logging.Formatter())
logging.getLogger().addHandler(stdout_logging)
try:
    with open("config.json") as config_file:
        settings = json.load(config_file)
except IOError:
    logging.error("No config.json file found! Please create one!")
    sys.exit(2)

def serialnumber():
    '''
    Shamelessly stolen from Frogor magic
    https://gist.github.com/pudquick/c7dd1262bd81a32663f0
    '''
    import objc
    from Foundation import NSBundle

    IOKit_bundle = NSBundle.bundleWithIdentifier_('com.apple.framework.IOKit')

    functions = [("IOServiceGetMatchingService", b"II@"),
                 ("IOServiceMatching", b"@*"),
                 ("IORegistryEntryCreateCFProperty", b"@I@@I"),
                ]
    # pylint: disable=E0602
    objc.loadBundleFunctions(IOKit_bundle, globals(), functions)
    logging.debug("Got Machine Serial Number")
    return IORegistryEntryCreateCFProperty(
        IOServiceGetMatchingService(0,
                                    IOServiceMatching("IOPlatformExpertDevice")),
        "IOPlatformSerialNumber",
        None, 0)
    # pylint: enable=E0602

def get_device_data(serial, host, user, password, db):
    '''
    Retrieves Device's barcode and district id
    '''
    barcode_cmd = \
    """
    SELECT CopyBarcode, DistrictID
    FROM CircCatAdmin.CopyAssetView
    WHERE SerialNumber = '{0}'
    """.format(serial)
    db_host = host
    db_user = user
    db_password = password
    db_name = db
    try:
        with pytds.connect(db_host, database=db_name, user=db_user,
                           password=db_password, as_dict=True) as conn:
            logging.debug("Server Connection Success")
            with conn.cursor() as cur:
                cur.execute(barcode_cmd)
                logging.debug("Lookup Command Executed")
                devicedata = (cur.fetchone())
                logging.debug("Date retrieved, closing connection")
    except pytds.tds.LoginError:
        logging.error("Unable to connect to server! Connection may have timed out!")
        sys.exit(2)
    cur.close()
    conn.close()
    return devicedata

def set_machine_name(newname):
    '''
    Set's machine ComputerName,HostName, and LocalHostName to value in field
    '''
    command = {}
    command[0] = ['/usr/sbin/scutil', '--set', 'ComputerName', str(newname)]
    command[1] = ['/usr/sbin/scutil', '--set', 'HostName', str(newname)]
    command[2] = ['/usr/sbin/scutil', '--set', 'LocalHostName', \
                  str(newname.replace(' ', '-'))]
    for x in command:
        subprocess.call(command[x])
        logging.debug("Setting %s", command[x][2])
    logging.info("Set Device Names")
    return

def set_ARD_Field(field):
    '''
    Set's Apple Remote Desktop Fields
    '''
    CFPreferencesSetValue("Text1", field,
                          "/Library/Preferences/com.apple.RemoteDesktop",
                          kCFPreferencesAnyUser, kCFPreferencesAnyHost)
    CFPreferencesSynchronize("/Library/Preferences/com.apple.RemoteDesktop",
                             kCFPreferencesAnyUser, kCFPreferencesAnyHost)
    logging.info("Set ComputerInfo1 Field")
    return

def process_lockmessage(assettag="", districtid=""):
    try:
        message = str(settings["lockmessage"])
    except KeyError:
        message = ""
    if args.assettag:
        message += "Asset Tag: {0}\n".format(assettag)
    if args.computername:
        message += "District ID: {0}".format(districtid)
    return message

def set_lockmessage(lockmessage):
    CFPreferencesSetValue('LoginwindowText', lockmessage,
                          "/Library/Preferences/com.apple.loginwindow",
                          kCFPreferencesAnyUser, kCFPreferencesAnyHost)
    CFPreferencesSynchronize("/Library/Preferences/com.apple.loginwindow",
                             kCFPreferencesAnyUser, kCFPreferencesAnyHost)
    logging.info("Set LoginwindowText")
    return

def main():
    '''
    Do all the main things
    '''
    if not any(vars(args).values()):
        logging.error("No arguments specified! One or more is required")
        parser.error("No arguments specified! One or more is required")
        sys.exit(1)
    else:
        server_settings = settings["server_info"]
        data = get_device_data(serialnumber(),
                               server_settings["server"],
                               server_settings["user"],
                               server_settings["password"],
                               server_settings["database"])
        logging.info("Got device data from server!\n%s", data)
        barcode = data["CopyBarcode"]
        name = data["DistrictID"]
        if barcode == "" or barcode is None:
            logging.error("Barcode not found in Asset Manager or this serial has no barcode!\
             Ensure you have these fields filled out for this serial before running again.")
        if name == "" or name is None:
            logging.error("DistrictID not found in Asset Manager or this serial has no DistrictID!\
             Ensure you have these fields filled out for this serial before running again.")
        if args.computername:
            set_machine_name(name)
        if args.assettag:
            set_ARD_Field(barcode)
        if args.lockmessage:
            newlockmessage = process_lockmessage(barcode, name)
            set_lockmessage(newlockmessage)

        logging.info("All selections are complete, exiting")
        sys.exit(0)
if __name__ == '__main__':
    main()
