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
from client.ResolveRecipients import ResolveRecipients
from client.FolderCreate import FolderCreate
from client.FolderUpdate import FolderUpdate
from client.FolderDelete import FolderDelete
from client.Ping import Ping
from client.MoveItems import MoveItems

from proto_creds import * #create a file proto_creds.py with vars: as_server, as_user, as_pass

storage.create_db_if_none()

#create wbxml_parser test
parser = wbxml_parser(as_code_pages.build_as_code_pages())

#create activesync connector - Note: no provisioning support yet, so attm you must disable require provision on server to use
as_conn = as_connect(as_server) #e.g. "as.myserver.com"
as_conn.set_credential(as_user, as_pass)
as_conn.options()

def as_request(cmd, wapxml_req):
    print "%s Request:" % cmd
    print wapxml_req
    res = as_conn.post(cmd, parser.encode(wapxml_req))
    wapxml_res = parser.decode(res)
    print "\r\n%s Response:" % cmd
    print wapxml_res
    return wapxml_res

conn, curs = storage.get_conn_curs()

##MoveItems
#moveitems_xmldoc_req = MoveItems.build([("5:24","5","10")])
#moveitems_xmldoc_res = as_request("MoveItems", moveitems_xmldoc_req)
#moveitems_res = MoveItems.parse(moveitems_xmldoc_res)
#for moveitem_res in moveitems_res:
#    if moveitem_res[1] == "3":
#        storage.update_email({"server_id": moveitem_res[0] ,"ServerId": moveitem_res[2]}, curs)
#        conn.commit()

#Ping
from objects.MSASCMD import Ping as PingObjs
ping_xmldoc_req = Ping.build("60", [("5", "Email"),("10","Email")])
ping_xmldoc_res = as_request("Ping", ping_xmldoc_req)
print Ping.parse(ping_xmldoc_res)

#FolderOps vars
from objects.MSASCMD import FolderHierarchy

#FolderSync
foldersync_xmldoc_req = FolderSync.build()
foldersync_xmldoc_res = as_request("FolderSync", foldersync_xmldoc_req)
folderhierarchy_changes = FolderSync.parse(foldersync_xmldoc_res)
if len(folderhierarchy_changes) > 0:
    storage.update_folderhierarchy(folderhierarchy_changes)

#FolderCreate
parent_folder = storage.get_folderhierarchy_folder_by_name("Inbox", curs)
new_folder = FolderHierarchy.Folder(parent_folder[0], "TestFolder1", str(FolderHierarchy.FolderCreate.Type.Mail))
foldercreate_xmldoc_req = FolderCreate.build(new_folder.ParentId, new_folder.DisplayName, new_folder.Type)
foldercreate_xmldoc_res = as_request("FolderCreate", foldercreate_xmldoc_req)
foldercreate_res_parsed = FolderCreate.parse(foldercreate_xmldoc_res)
print foldercreate_res_parsed
if foldercreate_res_parsed[0] == "1":
    new_folder.ServerId = foldercreate_res_parsed[2]
    storage.insert_folderhierarchy_change(new_folder, curs)
    storage.update_synckey(foldercreate_res_parsed[1], "0", curs)
    conn.commit()

#FolderUpdate
old_folder_name = "TestFolder1"
new_folder_name = "TestFolder2"
#new_parent_id = parent_folder = storage.get_folderhierarchy_folder_by_name("Inbox", curs)
folder_row = storage.get_folderhierarchy_folder_by_name(old_folder_name, curs)
update_folder = FolderHierarchy.Folder(folder_row[1], new_folder_name, folder_row[3], folder_row[0])
folderupdate_xmldoc_req = FolderUpdate.build(update_folder.ServerId, update_folder.ParentId, update_folder.DisplayName)
folderupdate_xmldoc_res = as_request("FolderUpdate", folderupdate_xmldoc_req)
folderupdate_res_parsed = FolderUpdate.parse(folderupdate_xmldoc_res)
print folderupdate_res_parsed
if folderupdate_res_parsed[0] == "1":
    new_folder.DisplayName = new_folder_name
    storage.update_folderhierarchy_change(new_folder, curs)
    storage.update_synckey(folderupdate_res_parsed[1], "0", curs)
    conn.commit()

#FolderDelete
folder_name = "TestFolder2"
folder_row = storage.get_folderhierarchy_folder_by_name(folder_name, curs)
delete_folder = FolderHierarchy.Folder()
delete_folder.ServerId = folder_row[0]
folderdelete_xmldoc_req = FolderDelete.build(delete_folder.ServerId)
folderdelete_xmldoc_res = as_request("FolderDelete", folderdelete_xmldoc_req)
folderdelete_res_parsed = FolderDelete.parse(folderdelete_xmldoc_res)
print folderdelete_res_parsed
if folderdelete_res_parsed[0] == "1":
    storage.delete_folderhierarchy_change(delete_folder, curs)
    storage.update_synckey(folderdelete_res_parsed[1], "0", curs)
    conn.commit()

#Folder Ops cleanup
if storage.close_conn_curs(conn):
        del conn, curs

#ResolveRecipients
resolverecipients_xmldoc_req = ResolveRecipients.build("zebra")
resolverecipients_xmldoc_res = as_request("ResolveRecipients", resolverecipients_xmldoc_req)

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
    getitemestimate_xmldoc_res = as_request("GetItemEstimate", getitemestimate_xmldoc_req)

    getitemestimate_res = GetItemEstimate.parse(getitemestimate_xmldoc_res)
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
collections_to_sync = ["5","10"]
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

#a = raw_input()
