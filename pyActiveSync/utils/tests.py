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


from utils.as_code_pages import as_code_pages
from utils.wbxml import wbxml_parser
from utils.wapxml import *
import pprint, traceback, sys
from client.as_connect import as_connect

#create wbxml_parser test
parser = wbxml_parser(as_code_pages.build_as_code_pages())

#wbxml_parser encode codepage test
print parser.encode_xmlns_as_codepage("folderhierarchy")

#code page __iter__ test
for tag in parser.code_pages[0]:
    print tag

#wbxml encode test
import binascii
print binascii.hexlify(parser.encode())

#wapxml creation/__repr__ test
xmldoc = wapxmltree()
xmlrootnode = wapxmlnode("FolderSync")
xmldoc.set_root(xmlrootnode, "folderhierarchy")
xmlsynckeynode = wapxmlnode("SyncKey", xmlrootnode, "0")
#xmlsyncchangenode = wapxmlnode("Changes",xmlrootnode, "10")
print xmldoc

#wbxml encode/decode test
print ""
try:
    print parser.decode(parser.encode(xmldoc))
except Exception, e:
    #print "wbxml: ", binascii.hexlify(parser.wbxml)
    #print "wbmxl index: ", parser.pointer
    #for i in parser.wbxml:
    #    print binascii.hexlify(bytes(i))
    type_, value_, traceback_ = sys.exc_info()
    print "wbxml encode/decode test: ", e, "\r\n", ''.join(traceback.format_tb(traceback_))