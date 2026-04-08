import sys
import pyjson5 as json
import os


# Uses CONFIG_DIR if it exists, otherwise falls back to "/etc"
_etc_path = os.getenv("CONFIG_DIR", "/etc/ticketweb/apps/reporting")






def _get_config_data_all():
    ldap_file = os.path.join(_etc_path,"app-server-config.json5")

    f = open(ldap_file,"r")
    ldap_data = json.load(f)
    f.close()
    return ldap_data


config_data = _get_config_data_all()