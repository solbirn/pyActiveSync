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

"""[MS-ASCMD] Generic/various class namespace objects"""

class FolderHierarchy:
    class FolderCreate:
        class Type:
            Generic =   1
            Mail =      12
            Calendar =  13
            Contacts =  14
            Tasks =     15
            Journal =   16
            Notes =     17

class ResolveRecipients:
    class CertificateRetrieval:
        DoNotRetrieve = 0
        RetrieveFull =  1
        RetrieveMini =  2
    class Type:
        Contacts =  1
        GAL =       2