#!/usr/bin/env python
# Hagan Franks <hagan.franks@gmail.com>
# Version 0.0.1
# 
# TO USE: 
#  $> sudo apt-get install libacl1-dev 
#  $> pip install pylibacl

import os
import pwd
import grp
import errno
import pprint
import posix1e
from posix1e import *


pp = pprint.PrettyPrinter(indent=4)

##### MAGIC THAT IMPORTS OUR .env CONFIGURATION #######
# Import our pylib_bcf script (loading the .env)
# Needs to find the pylib_bcf module relative to this file
if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
else:
    raise Exception("Cannot load pylib_bcf modules")

from pylib_bcf.load_env_vars import *

expected_vars = [
    'CELERYD_UNIX_USER', 'CELERYD_UNIX_GROUP', 'PROJECT_FILE_OWNER', 'PROJECT_FILE_GROUP', 'PROJECT_WEBSERVER_OWNER',
    'PROJECT_WEBSERVER_GROUP', 'MEDIA_ROOT', 'PROTECTED_ROOT',
]
for v in expected_vars:
    if v not in globals():
        raise Exception("Is {} set in the .env file?".format(v))
del expected_vars
#######################################################

celeryd_unix_user_id = pwd.getpwnam(CELERYD_UNIX_USER).pw_uid
celeryd_unix_group_id = grp.getgrnam(CELERYD_UNIX_GROUP).gr_gid
project_unix_user_id = pwd.getpwnam(PROJECT_FILE_OWNER).pw_uid
project_unix_group_id = grp.getgrnam(PROJECT_FILE_GROUP).gr_gid
project_webserver_owner_id = pwd.getpwnam(PROJECT_WEBSERVER_OWNER).pw_uid
project_webserver_group_id = grp.getgrnam(PROJECT_WEBSERVER_GROUP).gr_gid


def return_list_of_subfolders(root_dir):
    list_of_folders = []
    for root, sub_folders, files in os.walk(root_dir):
        # print("subfolder: {}".format(sub_folders))
        for folder in sub_folders:
            list_of_folders.append(os.path.join(root, folder))
    return list_of_folders


def set_directory_acl_permissions(dir_path):
    """
    Setup the directory permissions with acl permissions like so:
    owner: PROJECT_FILE_OWNER
    group: PROJECT_FILE_GROUP
    user::rwx
    user::rwx
    group:CELERYD_UNIX_USER:r-x
    mask::rwx
    other::r-x
    """
    if(os.path.exists(dir_path) and os.path.isdir(dir_path)):
        os.chown(dir_path, project_unix_user_id, project_unix_group_id)

        acl = posix1e.ACL()

        # Set User object rwx
        e_user_obj = acl.append()
        e_user_obj.tag_type = posix1e.ACL_USER_OBJ
        # e.qualifier = project_unix_user_id
        e_user_obj.permset.add(posix1e.ACL_READ)
        e_user_obj.permset.add(posix1e.ACL_WRITE)
        e_user_obj.permset.add(posix1e.ACL_EXECUTE)

        # Set Group object r-x
        e_group_obj = acl.append()
        e_group_obj.tag_type = posix1e.ACL_GROUP_OBJ
        e_group_obj.permset.add(posix1e.ACL_READ)
        e_group_obj.permset.add(posix1e.ACL_EXECUTE)

        # Set other object r-x
        e_other_obj = acl.append()
        e_other_obj.tag_type = posix1e.ACL_OTHER
        e_other_obj.permset.add(posix1e.ACL_READ)
        e_other_obj.permset.add(posix1e.ACL_EXECUTE)

        # Set mask
        e_mask_obj = acl.append()
        e_mask_obj.tag_type = posix1e.ACL_MASK
        e_mask_obj.permset.add(posix1e.ACL_READ)
        e_mask_obj.permset.add(posix1e.ACL_WRITE)
        e_mask_obj.permset.add(posix1e.ACL_EXECUTE)

        # Set CELERYD_UNIX_USER:user:rwx
        e_celeryd_user_obj = acl.append()
        e_celeryd_user_obj.tag_type = posix1e.ACL_USER
        e_celeryd_user_obj.qualifier = celeryd_unix_user_id
        e_celeryd_user_obj.permset.add(posix1e.ACL_READ)
        e_celeryd_user_obj.permset.add(posix1e.ACL_WRITE)
        e_celeryd_user_obj.permset.add(posix1e.ACL_EXECUTE)

        # Set CELERYD_UNIX_GROUP:group:rwx
        e_celeryd_group_obj = acl.append()
        e_celeryd_group_obj.tag_type = posix1e.ACL_GROUP
        e_celeryd_group_obj.qualifier = celeryd_unix_group_id
        e_celeryd_group_obj.permset.add(posix1e.ACL_READ)
        e_celeryd_group_obj.permset.add(posix1e.ACL_WRITE)
        e_celeryd_group_obj.permset.add(posix1e.ACL_EXECUTE)

        # Set the PROJECT_WEBSERVER_USER:user:rwx
        e_webserver_user_obj = acl.append()
        e_webserver_user_obj.tag_type = posix1e.ACL_USER
        e_webserver_user_obj.qualifier = project_webserver_owner_id
        e_webserver_user_obj.permset.add(posix1e.ACL_READ)
        e_webserver_user_obj.permset.add(posix1e.ACL_WRITE)
        e_webserver_user_obj.permset.add(posix1e.ACL_EXECUTE)

        # Set the PROJECT_FILE_GROUP:group:rwx
        e_webserver_group_obj = acl.append()
        e_webserver_group_obj.tag_type = posix1e.ACL_GROUP
        e_webserver_group_obj.qualifier = project_webserver_group_id
        e_webserver_group_obj.permset.add(posix1e.ACL_READ)
        e_webserver_group_obj.permset.add(posix1e.ACL_WRITE)
        e_webserver_group_obj.permset.add(posix1e.ACL_EXECUTE)

        acl.applyto(dir_path)
        acl.applyto(dir_path, posix1e.ACL_TYPE_DEFAULT)

        print("fixed: {}".format(dir_path))
    else:
        raise Exception("ERROR: missing directory: {}".format(dir_path))

print("Setup Folders with ACL permissions.")

set_directory_acl_permissions(MEDIA_ROOT)
fix_folders = return_list_of_subfolders(MEDIA_ROOT)
for folder in fix_folders:
    set_directory_acl_permissions(folder)
