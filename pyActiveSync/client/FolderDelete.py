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

class FolderDelete:
    """http://msdn.microsoft.com/en-us/library/gg650949(v=exchg.80).aspx"""

    @staticmethod
    def build(server_id):
        folderdelete_xmldoc_req = wapxmltree()
        xmlrootnode = wapxmlnode("FolderDelete")
        folderdelete_xmldoc_req.set_root(xmlrootnode, "folderhierarchy")
        xmlsynckeynode = wapxmlnode("SyncKey", xmlrootnode, storage.get_synckey("0"))
        xmlserveridnode = wapxmlnode("ServerId", xmlrootnode, server_id)
        return folderdelete_xmldoc_req

    @staticmethod
    def parse(inwbxml):
        wapxml = inwapxml

        namespace = "folderhierarchy"
        root_tag = "FolderDelete"

        root_element = wapxml.get_root()
        if root_element.get_xmlns() != namespace:
            raise AttributeError("Xmlns '%s' submitted to '%s' parser. Should be '%s'." % (root_element.get_xmlns(), root_tag, namespace))
        if root_element.tag != root_tag:
            raise AttributeError("Root tag '%s' submitted to '%s' parser. Should be '%s'." % (root_element.tag, root_tag, root_tag))

        folderhierarchy_folderdelete_children = root_element.get_children()

        folderhierarchy_folderdelete_status = None
        folderhierarchy_folderdelete_synckey = None
        folderhierarchy_folderdelete_serverid = None

        for element in folderhierarchy_folderdelete_children:
            if element.tag is "Status":
                folderhierarchy_folderdelete_status = element.text
                if folderhierarchy_folderdelete_status != "1":
                     print "FolderDelete Exception: %s" % folderhierarchy_folderdelete_status
            elif element.tag == "SyncKey":
                folderhierarchy_folderdelete_synckey = element.text
        return (folderhierarchy_folderdelete_status, folderhierarchy_folderdelete_synckey)