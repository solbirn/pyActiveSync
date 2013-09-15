########################################################################
#  Copyright (C) 2013 Sol Birnbaum
# 
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
# 
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
# 
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA  02110-1301, USA.
########################################################################

# Code Playground

from utils.as_code_pages import as_code_pages
from utils.wbxml import wbxml_parser
from utils.wapxml import wapxmltree, wapxmlnode
from client.as_connect import as_connect
from client.storage import storage

from client.FolderSync import FolderSync
from client.Sync import Sync
from client.GetItemEstimate import GetItemEstimate

from proto_creds import * #create a file proto_creds.py with vars: as_server, as_user, as_pass

storage.create_db_if_none()

#create wbxml_parser test
parser = wbxml_parser(as_code_pages.build_as_code_pages())

#create activesync connector - Note: no provisioning support yet, so attm you must disable require provision on server to use
as_conn = as_connect(as_server) #e.g. "as.myserver.com"
as_conn.set_credential(as_user, as_pass)
as_conn.options()

#FolderSync
foldersync_xmldoc_req = FolderSync.build()
print "Request:"
print foldersync_xmldoc_req

res = as_conn.post("FolderSync", parser.encode(foldersync_xmldoc_req))
foldersync_xmldoc_res = parser.decode(res)
print "\r\nResponse:"
print foldersync_xmldoc_res

foldersync_parser = FolderSync.parser()
folderhierarchy_changes = foldersync_parser.parse(foldersync_xmldoc_res)
if len(folderhierarchy_changes) > 0:
    storage.update_folderhierarchy(folderhierarchy_changes)

#Sync function
def do_sync(collection_ids):
    as_sync_xmldoc_req = Sync.build(collection_ids)
    print "\r\nRequest:"
    print as_sync_xmldoc_req

    res = as_conn.post("Sync", parser.encode(as_sync_xmldoc_req))
    print "\r\nResponse:"

    if res == '':
        print "Nothing to Sync!"
    else:
        as_sync_xmldoc_res = parser.decode(res)
        print as_sync_xmldoc_res

        sync_parser = Sync.parser()
        sync_res = sync_parser.parse(as_sync_xmldoc_res)
        storage.update_emails(sync_res)

#GetItemsEstimate
def do_getitemestimates(collection_ids):
    getitemestimate_xmldoc_req = GetItemEstimate.build(collection_ids)
    print "\r\nRequest:"
    print getitemestimate_xmldoc_req

    res = as_conn.post("GetItemEstimate", parser.encode(getitemestimate_xmldoc_req))
    getitemestimate_xmldoc_res = parser.decode(res)
    print "\r\nResponse:"
    print getitemestimate_xmldoc_res

    getitemestimate_parser = GetItemEstimate.parser()
    getitemestimate_res = getitemestimate_parser.parse(getitemestimate_xmldoc_res)
    return getitemestimate_res

def getitemestimate_check_prime_collections(getitemestimate_responses):
    has_synckey = []
    needs_synckey = []
    for response in getitemestimate_responses:
        if response.Status == "1":
            has_synckey.append(response.CollectionId)
        if response.Status == "2":
            print "GetItemEstimate Status: Unknown CollectionId (%s) specified. Removing." % response.CollectionId
        if response.Status == "3":
            print "GetItemEstimate Status: Sync needs to be primed."
            needs_synckey.append(response.CollectionId)
            has_synckey.append(response.CollectionId) #technically *will* have synckey after do_sync() need end of function
    if len(needs_synckey) > 0:
        do_sync(needs_synckey)
    return has_synckey, needs_synckey

#GetItemsEstimate and Sync process test
collections_to_sync = ["5","3"]
getitemestimate_responses = do_getitemestimates(collections_to_sync)

has_synckey, just_got_synckey = getitemestimate_check_prime_collections(getitemestimate_responses)

if (len(has_synckey) < collections_to_sync) or (len(just_got_synckey) > 0): #grab new estimates, since they changed
    getitemestimate_responses = do_getitemestimates(has_synckey)

collections_to_sync = [] 

for response in getitemestimate_responses:
    if response.Status == "1":
        if int(response.Estimate) > 0:
            collections_to_sync.append(response.CollectionId)
    else:
        print "GetItemEstimate Status (error): %s, CollectionId: %s." % (response.Status, response.CollectionId)

if len(collections_to_sync) > 0:
    do_sync(collections_to_sync)

a = raw_input()
