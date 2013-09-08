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
    class parser:
        def __init__(self, inwapxml=None):
            self.wapxml = inwapxml
        def parse_message(self, message):
            from objects.MSASEMAIL import Email
            new_message = Email()
            new_message.parse(message)
            return new_message
        def parse(self, inwapxml=None):
            if inwapxml:
                self.wapxml = inwapxml
#            try:
            root_element = self.wapxml.get_root()
            if root_element.get_xmlns() is not "airsync":
                raise AttributeError("Xmlns '%s' submitted to 'Sync' parser. Should be 'airsync'." % root_element.get_xmlns())
            if root_element.tag is not "Sync":
                raise AttributeError("Root tag '%s' submitted to 'Sync' parser. Should be 'Sync'." % root_element.tag)

            airsyncbase_sync_children = root_element.get_children()
            if len(airsyncbase_sync_children) >  1:
                raise AttributeError("Sync response does not conform to any known Sync responses.")
            if airsyncbase_sync_children[0].tag != "Collections":
                raise AttributeError("Sync response does not conform to any known Sync responses.")

            self.response = []            

            airsyncbase_sync_collections_children = airsyncbase_sync_children[0].get_children()
            airsyncbase_sync_collections_children_count = len(airsyncbase_sync_collections_children)
            collections_counter = 0
            while collections_counter < airsyncbase_sync_collections_children_count:

                if airsyncbase_sync_collections_children[collections_counter].tag != "Collection":
                    raise AttributeError("Sync response does not conform to any known Sync responses.")

                airsyncbase_sync_collection_children = airsyncbase_sync_collections_children[0].get_children()
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
                            return new_collection
                    elif airsyncbase_sync_collection_children[collection_counter].tag == "MoreAvailable":
                        new_collection.MoreAvailable = airsyncbase_sync_collection_children[collection_counter].text
                    elif airsyncbase_sync_collection_children[collection_counter].tag == "Commands":
                        airsyncbase_sync_commands_children = airsyncbase_sync_collection_children[collection_counter].get_children()
                        airsyncbase_sync_commands_children_count = len(airsyncbase_sync_commands_children)
                        commands_counter = 0
                        while commands_counter < airsyncbase_sync_commands_children_count:
                            if airsyncbase_sync_commands_children[commands_counter].tag == "Add":
                                add_message = self.parse_message(airsyncbase_sync_commands_children[commands_counter])
                                new_collection.Commands.append(("Add", add_message))
                            elif airsyncbase_sync_commands_children[commands_counter].tag == "Delete":
                                continue
                            elif airsyncbase_sync_commands_children[commands_counter].tag == "Change":
                                continue
                            elif airsyncbase_sync_commands_children[commands_counter].tag == "SoftDelete":
                                continue
                            commands_counter+=1
                    elif airsyncbase_sync_collection_children[collection_counter].tag == "Responses":
                        print airsyncbase_sync_collection_children[collection_counter]
                    collection_counter+=1
                self.response.append(new_collection)
                collections_counter+=1
            return self.response