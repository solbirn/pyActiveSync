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
from client.storage import storage

class GetItemEstimate:
    class getitemestimate_response:
        def __init__(self):
            self.Status = None
            self.CollectionId = None
            self.Estimate = None

    @staticmethod
    def build(collection_ids):
        getitemestimate_xmldoc_req = wapxmltree()
        xmlrootgetitemestimatenode = wapxmlnode("GetItemEstimate")
        getitemestimate_xmldoc_req.set_root(xmlrootgetitemestimatenode, "getitemestimate")

        xmlcollectionsnode = wapxmlnode("Collections", xmlrootgetitemestimatenode)

        for collection_id in collection_ids:
            xml_Collection_node = wapxmlnode("Collection", xmlcollectionsnode)
            xml_gie_airsyncSyncKey_node = wapxmlnode("airsync:SyncKey", xml_Collection_node, storage.get_synckey(collection_id))
            xml_gie_CollectionId_node = wapxmlnode("CollectionId", xml_Collection_node, collection_id)#?
            #xml_gie_ConverationMode_node = wapxmlnode("airsync:ConversationMode", xml_Collection_node, "0")#?
            xml_gie_airsyncOptions_node = wapxmlnode("airsync:Options", xml_Collection_node)
            xml_gie_airsyncClass_node = wapxmlnode("airsync:Class", xml_gie_airsyncOptions_node, "Email") #STR #http://msdn.microsoft.com/en-us/library/gg675489(v=exchg.80).aspx
            #xml_gie_airsyncFilterType_node = wapxmlnode("airsync:FilterType", xml_gie_airsyncOptions_node, "0")   #INT #http://msdn.microsoft.com/en-us/library/gg663562(v=exchg.80).aspx
            #xml_gie_airsyncMaxItems_node = wapxmlnode("airsync:MaxItems", xml_gie_airsyncMaxItems_node, 0) #OPTIONAL  #INT   #http://msdn.microsoft.com/en-us/library/gg675531(v=exchg.80).aspx
        return getitemestimate_xmldoc_req
        
    @staticmethod
    def parse(inwapxml=None):
        wapxml = inwapxml

        namespace = "getitemestimate"
        root_tag = "GetItemEstimate"

        root_element = wapxml.get_root()
        if root_element.get_xmlns() != namespace:
            raise AttributeError("Xmlns '%s' submitted to '%s' parser. Should be '%s'." % (root_element.get_xmlns(), root_tag, namespace))
        if root_element.tag != root_tag:
            raise AttributeError("Root tag '%s' submitted to '%s' parser. Should be '%s'." % (root_element.tag, root_tag, root_tag))

        getitemestimate_getitemestimate_children = root_element.get_children()

        #getitemestimate_responses = getitemestimate_getitemestimate_children.get_children()

        responses = []

        for getitemestimate_response_child in getitemestimate_getitemestimate_children:
            response = GetItemEstimate.getitemestimate_response()
            for element in getitemestimate_response_child:
                if element.tag is "Status":
                    response.Status = element.text
                elif element.tag == "Collection":
                    getitemestimate_collection_children = element.get_children()
                    collection_id = 0
                    estimate = 0
                    for collection_child in getitemestimate_collection_children:
                        if collection_child.tag == "CollectionId":
                            response.CollectionId = collection_child.text
                        elif collection_child.tag == "Estimate":
                            response.Estimate = collection_child.text
            responses.append(response)
        return responses




