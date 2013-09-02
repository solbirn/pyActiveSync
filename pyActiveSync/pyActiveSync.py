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

#create wbxml_parser test
parser = wbxml_parser(as_code_pages.build_as_code_pages())

#create activesync connector - Note: no provisioning support yet
as_conn = as_connect("activesync.myserver.com")
as_conn.set_credential("place user here", "place password here")
as_conn.options()

#FolderSync
foldersync_xmldoc_req = wapxmltree()
xmlrootnode = wapxmlnode("FolderSync")
foldersync_xmldoc_req.set_root(xmlrootnode, "folderhierarchy")
xmlsynckeynode = wapxmlnode("SyncKey", xmlrootnode, "0")
print "Request:"
print foldersync_xmldoc_req

res = as_conn.post("FolderSync", parser.encode(foldersync_xmldoc_req))
foldersync_xmldoc_res = parser.decode(res)
print "\r\nResponse:"
print foldersync_xmldoc_res

foldersync_status = None
foldersync_synckey = None
foldersync_changes = None

for node in foldersync_xmldoc_res.get_root():
    if node.tag is "Status":
        foldersync_status = node
        if foldersync_status.text is not "1":
            raise Exception("AS FolderSync Exception")
    elif node.tag is "SyncKey":
        foldersync_synckey = node
    elif node.tag is "Changes":
        foldersync_changes = node

#Sync
as_sync_xmldoc_req = wapxmltree()
xml_as_sync_rootnode = wapxmlnode("Sync")
as_sync_xmldoc_req.set_root(xml_as_sync_rootnode, "airsync")

xml_as_collections_node = wapxmlnode("Collections", xml_as_sync_rootnode)

xml_as_Collection_1_node = wapxmlnode("Collection", xml_as_collections_node)  #http://msdn.microsoft.com/en-us/library/gg650891(v=exchg.80).aspx
xml_as_SyncKey_node = wapxmlnode("SyncKey", xml_as_Collection_1_node, "0")    #http://msdn.microsoft.com/en-us/library/gg663426(v=exchg.80).aspx
#xml_as_Supported_node = wapxmlnode("Supported", xml_as_Collection_1_node, "") #http://msdn.microsoft.com/en-us/library/gg650908(v=exchg.80).aspx
xml_as_CollectionId_node = wapxmlnode("CollectionId", xml_as_Collection_1_node, "5") #http://msdn.microsoft.com/en-us/library/gg650886(v=exchg.80).aspx
#xml_as_DeleteAsMoves_node = wapxmlnode("DeleteAsMoves", xml_as_Collection_1_node, "1") #DEFAULT is "True" #OPT #http://msdn.microsoft.com/en-us/library/gg675480(v=exchg.80).aspx
#xml_as_GetChanges_node = wapxmlnode("GetChanges", xml_as_Collection_1_node, "0") #MUST be False or absent when SyncKey is 0. #OPT http://msdn.microsoft.com/en-us/library/gg675447(v=exchg.80).aspx
xml_as_WindowSize_node = wapxmlnode("WindowSize", xml_as_Collection_1_node, "512") #OPT Specify how many change you want at a time, up to 512. #http://msdn.microsoft.com/en-us/library/gg650865(v=exchg.80).aspx

#xml_as_Options_node = wapxmlnode("Options", xml_as_Collection_1_node)


#xml_as_ConverationMode_node = wapxmlnode("ConversationMode", xml_as_Collection_1_node, "0") #OPT #will implement later #http://msdn.microsoft.com/en-us/library/gg672034(v=exchg.80).aspx

#xml_as_Commands_collection_node = wapxmlnode("Commands", xml_as_Collection_1_node)
#xml_as_Commands_Add_node = wapxmlnode("Add", xml_as_Commands_collection_node) #http://msdn.microsoft.com/en-us/library/gg675487(v=exchg.80).aspx
#xml_as_Commands_Delete_node = wapxmlnode("Delete", xml_as_Commands_collection_node) #http://msdn.microsoft.com/en-us/library/gg663450(v=exchg.80).aspx
#xml_as_Commands_Change_node = wapxmlnode("Change", xml_as_Commands_collection_node) #http://msdn.microsoft.com/en-us/library/gg675544(v=exchg.80).aspx
#xml_as_Commands_Fetch_node = wapxmlnode("Fetch", xml_as_Commands_collection_node) #http://msdn.microsoft.com/en-us/library/gg675490(v=exchg.80).aspx

#xml_as_collections_node = wapxmlnode("Collections", xml_as_sync_rootnode)

print "\r\nRequest:"
print as_sync_xmldoc_req

res = as_conn.post("Sync", parser.encode(as_sync_xmldoc_req))
as_sync_xmldoc_res = parser.decode(res)
print "\r\nResponse:"
print as_sync_xmldoc_res

xml_as_SyncKey_node.text = as_sync_xmldoc_res.get_root().get_children()[0].get_children()[0].get_children()[0].text

print "\r\nRequest:"
print as_sync_xmldoc_req

res = as_conn.post("Sync", parser.encode(as_sync_xmldoc_req))
as_sync_xmldoc_res = parser.decode(res)
print "\r\nResponse:"
print as_sync_xmldoc_res


#GetItemsEstimate
getitemestimate_xmldoc_req = wapxmltree()
xmlrootgetitemestimatenode = wapxmlnode("GetItemEstimate")
getitemestimate_xmldoc_req.set_root(xmlrootgetitemestimatenode, "getitemestimate")

xmlcollectionsnode = wapxmlnode("Collections", xmlrootgetitemestimatenode)

xml_Collection_1_node = wapxmlnode("Collection", xmlcollectionsnode)
xml_gie_airsyncSyncKey_node = wapxmlnode("airsync:SyncKey", xml_Collection_1_node, "0")
xml_gie_CollectionId_node = wapxmlnode("CollectionId", xml_Collection_1_node, "5")#?
#xml_gie_ConverationMode_node = wapxmlnode("airsync:ConversationMode", xml_Collection_1_node, "0")#?
xml_gie_airsyncOptions_node = wapxmlnode("airsync:Options", xml_Collection_1_node)
xml_gie_airsyncClass_node = wapxmlnode("airsync:Class", xml_gie_airsyncOptions_node, "Email") #STR #http://msdn.microsoft.com/en-us/library/gg675489(v=exchg.80).aspx
#xml_gie_airsyncFilterType_node = wapxmlnode("airsync:FilterType", xml_gie_airsyncOptions_node, "0")   #INT #http://msdn.microsoft.com/en-us/library/gg663562(v=exchg.80).aspx
#xml_gie_airsyncMaxItems_node = wapxmlnode("airsync:MaxItems", xml_gie_airsyncMaxItems_node, 0) #OPTIONAL  #INT   #http://msdn.microsoft.com/en-us/library/gg675531(v=exchg.80).aspx

print "\r\nRequest:"
print getitemestimate_xmldoc_req

res = as_conn.post("GetItemEstimate", parser.encode(getitemestimate_xmldoc_req))
getitemestimate_xmldoc_res = parser.decode(res)
print "\r\nResponse:"
print getitemestimate_xmldoc_res #responds that needs airsync:Sync first



a = raw_input()