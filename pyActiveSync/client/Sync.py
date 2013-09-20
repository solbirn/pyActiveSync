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

from utils.wapxml import wapxmltree, wapxmlnode

from objects.MSASEMAIL import Email, parse_email_to_dict

class Sync:
    """'Sync' command builders and parsers"""
    class sync_response_collection:
        def __init__(self):
            self.SyncKey = 0
            self.CollectionId = None
            self.Status = 0
            self.MoreAvailable = None
            self.Commands = []
            self.Responses = None

    @staticmethod
    def build(synckeys, collection_ids):
        as_sync_xmldoc_req = wapxmltree()
        xml_as_sync_rootnode = wapxmlnode("Sync")
        as_sync_xmldoc_req.set_root(xml_as_sync_rootnode, "airsync")

        xml_as_collections_node = wapxmlnode("Collections", xml_as_sync_rootnode)

        for collection_id in collection_ids:
            xml_as_Collection_node = wapxmlnode("Collection", xml_as_collections_node)  #http://msdn.microsoft.com/en-us/library/gg650891(v=exchg.80).aspx
            try:
                xml_as_SyncKey_node = wapxmlnode("SyncKey", xml_as_Collection_node, synckeys[collection_id])    #http://msdn.microsoft.com/en-us/library/gg663426(v=exchg.80).aspx
            except KeyError:
                xml_as_SyncKey_node = wapxmlnode("SyncKey", xml_as_Collection_node, "0") 
            #xml_as_Supported_node = wapxmlnode("Supported", xml_as_Collection_1_node, "") #http://msdn.microsoft.com/en-us/library/gg650908(v=exchg.80).aspx
            xml_as_CollectionId_node = wapxmlnode("CollectionId", xml_as_Collection_node, collection_id) #http://msdn.microsoft.com/en-us/library/gg650886(v=exchg.80).aspx
            #xml_as_DeleteAsMoves_node = wapxmlnode("DeleteAsMoves", xml_as_Collection_1_node, "1") #Default is "True" #OPT #http://msdn.microsoft.com/en-us/library/gg675480(v=exchg.80).aspx
            #xml_as_GetChanges_node = wapxmlnode("GetChanges", xml_as_Collection_1_node, "0") #MUST be False or absent when SyncKey is 0. #OPT http://msdn.microsoft.com/en-us/library/gg675447(v=exchg.80).aspx
            xml_as_WindowSize_node = wapxmlnode("WindowSize", xml_as_Collection_node, "512") #OPT Specify how many change you want at a time, up to 512. #http://msdn.microsoft.com/en-us/library/gg650865(v=exchg.80).aspx

            xml_as_Options_node = wapxmlnode("Options", xml_as_Collection_node)
            xml_as_Options_BodyPreference_node = wapxmlnode("airsyncbase:BodyPreference", xml_as_Options_node)
            xml_as_Options_BodyPreference_Type_node = wapxmlnode("airsyncbase:Type", xml_as_Options_BodyPreference_node)
            xml_as_Options_BodyPreference_Type_node.text = "1"
            xml_as_Options_BodyPreference_TruncationSize_node = wapxmlnode("airsyncbase:TruncationSize", xml_as_Options_BodyPreference_node)
            xml_as_Options_BodyPreference_TruncationSize_node.text = "10000000"

            #xml_as_ConverationMode_node = wapxmlnode("ConversationMode", xml_as_Collection_1_node, "0") #OPT #will implement later #http://msdn.microsoft.com/en-us/library/gg672034(v=exchg.80).aspx

            #xml_as_Commands_collection_node = wapxmlnode("Commands", xml_as_Collection_1_node)
            #xml_as_Commands_Add_node = wapxmlnode("Add", xml_as_Commands_collection_node) #http://msdn.microsoft.com/en-us/library/gg675487(v=exchg.80).aspx
            #xml_as_Commands_Delete_node = wapxmlnode("Delete", xml_as_Commands_collection_node) #http://msdn.microsoft.com/en-us/library/gg663450(v=exchg.80).aspx
            #xml_as_Commands_Change_node = wapxmlnode("Change", xml_as_Commands_collection_node) #http://msdn.microsoft.com/en-us/library/gg675544(v=exchg.80).aspx
            #xml_as_Commands_Fetch_node = wapxmlnode("Fetch", xml_as_Commands_collection_node) #http://msdn.microsoft.com/en-us/library/gg675490(v=exchg.80).aspx

            #xml_as_collections_node = wapxmlnode("Collections", xml_as_sync_rootnode)

        return as_sync_xmldoc_req

    @staticmethod
    def parse_message(message):   
        new_message = Email()
        new_message.parse(message)
        return new_message

    @staticmethod
    def parse_update(message):
        return parse_email_to_dict(message)

    @staticmethod
    def parse(wapxml):

        namespace = "airsync"
        root_tag = "Sync"

        root_element = wapxml.get_root()
        if root_element.get_xmlns() != namespace:
            raise AttributeError("Xmlns '%s' submitted to '%s' parser. Should be '%s'." % (root_element.get_xmlns(), root_tag, namespace))
        if root_element.tag != root_tag:
            raise AttributeError("Root tag '%s' submitted to '%s' parser. Should be '%s'." % (root_element.tag, root_tag, root_tag))

        airsyncbase_sync_children = root_element.get_children()
        if len(airsyncbase_sync_children) >  1:
            raise AttributeError("%s response does not conform to any known %s responses." % (root_tag, root_tag))
        if airsyncbase_sync_children[0].tag == "Status":
            if airsyncbase_sync_children[0].text == "4":
                print "Sync Status: 4, Protocol Error."
        if airsyncbase_sync_children[0].tag != "Collections":
            raise AttributeError("%s response does not conform to any known %s responses." % (root_tag, root_tag))

        response = []            

        airsyncbase_sync_collections_children = airsyncbase_sync_children[0].get_children()
        airsyncbase_sync_collections_children_count = len(airsyncbase_sync_collections_children)
        collections_counter = 0
        while collections_counter < airsyncbase_sync_collections_children_count:

            if airsyncbase_sync_collections_children[collections_counter].tag != "Collection":
                raise AttributeError("Sync response does not conform to any known Sync responses.")

            airsyncbase_sync_collection_children = airsyncbase_sync_collections_children[collections_counter].get_children()
            airsyncbase_sync_collection_children_count = len(airsyncbase_sync_collection_children)
            collection_counter = 0
            new_collection = Sync.sync_response_collection()
            while collection_counter < airsyncbase_sync_collection_children_count:
                if airsyncbase_sync_collection_children[collection_counter].tag == "SyncKey":
                    new_collection.SyncKey = airsyncbase_sync_collection_children[collection_counter].text
                elif airsyncbase_sync_collection_children[collection_counter].tag == "CollectionId":
                    new_collection.CollectionId = airsyncbase_sync_collection_children[collection_counter].text
                elif airsyncbase_sync_collection_children[collection_counter].tag == "Status":
                    new_collection.Status = airsyncbase_sync_collection_children[collection_counter].text
                    if new_collection.Status != "1":
                        response.append(new_collection)
                elif airsyncbase_sync_collection_children[collection_counter].tag == "MoreAvailable":
                    new_collection.MoreAvailable = airsyncbase_sync_collection_children[collection_counter].text
                elif airsyncbase_sync_collection_children[collection_counter].tag == "Commands":
                    airsyncbase_sync_commands_children = airsyncbase_sync_collection_children[collection_counter].get_children()
                    airsyncbase_sync_commands_children_count = len(airsyncbase_sync_commands_children)
                    commands_counter = 0
                    while commands_counter < airsyncbase_sync_commands_children_count:
                        if airsyncbase_sync_commands_children[commands_counter].tag == "Add":
                            add_message = Sync.parse_message(airsyncbase_sync_commands_children[commands_counter])
                            new_collection.Commands.append(("Add", add_message))
                        elif airsyncbase_sync_commands_children[commands_counter].tag == "Delete":
                            new_collection.Commands.append(("Delete", airsyncbase_sync_commands_children[commands_counter].get_children()[0].text))
                        elif airsyncbase_sync_commands_children[commands_counter].tag == "Change":
                            update_message = Sync.parse_update(airsyncbase_sync_commands_children[commands_counter])
                            new_collection.Commands.append(("Change", update_message))
                        elif airsyncbase_sync_commands_children[commands_counter].tag == "SoftDelete":
                            new_collection.Commands.append(("SoftDelete", airsyncbase_sync_commands_children[commands_counter].get_children()[0].text))
                        commands_counter+=1
                elif airsyncbase_sync_collection_children[collection_counter].tag == "Responses":
                    print airsyncbase_sync_collection_children[collection_counter]
                collection_counter+=1
            response.append(new_collection)
            collections_counter+=1
        return response
