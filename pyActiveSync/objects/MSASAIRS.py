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

"""[MS-ASAIRS] AirSyncBase namespace objects"""

class airsyncbase_Type:             #http://msdn.microsoft.com/en-us/library/hh475675(v=exchg.80).aspx
    Plaintext = 1
    HTML =      2
    RTF =       3
    MIME =      4

class airsyncbase_NativeBodyType:   #http://msdn.microsoft.com/en-us/library/ee218276(v=exchg.80).aspx
    Plaintext = 1
    HTML =      2
    RTF =       3

class airsyncbase_Method:   #http://msdn.microsoft.com/en-us/library/ee160322(v=exchg.80).aspx
    Normal_attachment = 1   #Regular attachment
    Reserved1 =         2
    Reserved2 =         3
    Reserved3 =         4
    Embedded_message =  5   #Email with .eml extension
    Attach_OLE =        6   #OLE such as inline image

class airsyncbase_BodyPart_status:
    Success =   1
    Too_long =  176

class airsyncbase_Body(object):
    def __init__(self, type, estimated_data_size=None, truncated=None, data=None, part=None, preview=None):
        self.airsyncbase_Type = type                                #Required. Integer. Max 1. See "MSASAIRS.Type" enum. 
        self.airsyncbase_EstimatedDataSize = estimated_data_size    #Optional. Integer. Max 1. Estimated data size before content filtering rules. http://msdn.microsoft.com/en-us/library/hh475714(v=exchg.80).aspx
        self.airsyncbase_Truncated = truncated                      #Optional. Boolean. Max 1. Specifies whether body is truncated as per airsync:BodyPreference element. http://msdn.microsoft.com/en-us/library/ee219390(v=exchg.80).aspx
        self.airsyncbase_Data = data                                #Optional. String (formated as per Type; RTF is base64 string). http://msdn.microsoft.com/en-us/library/ee202985(v=exchg.80).aspx
        self.airsyncbase_Part = part                                #Optional. Integer. See "MSASCMD.Part". Only present in multipart "MSASCMD.ItemsOperations" response. http://msdn.microsoft.com/en-us/library/hh369854(v=exchg.80).aspx
        self.airsyncbase_Preview = preview                          #Optional. String (unicode). Plaintext preview message. http://msdn.microsoft.com/en-us/library/ff849891(v=exchg.80).aspx

class airsyncbase_BodyPart(object):
    def __init__(self):
        self.airsyncbase_BodyPart_status = airsyncbase_BodyPart_status.Too_long #Required. Byte. See airsyncbase_BodyPart_status enum.
        self.airsyncbase_Type = airsyncbase_Type.HTML               #Required. Integer. Max 1. See "MSASAIRS.Type" enum. 
        self.airsyncbase_EstimatedDataSize = estimated_data_size    #Optional. Integer. Max 1. Estimated data size before content filtering rules. http://msdn.microsoft.com/en-us/library/hh475714(v=exchg.80).aspx
        self.airsyncbase_Truncated = truncated                      #Optional. Boolean. Max 1. Specifies whether body is truncated as per airsync:BodyPreference element. http://msdn.microsoft.com/en-us/library/ee219390(v=exchg.80).aspx
        self.airsyncbase_Data = data                                #Optional. String (formated as per Type; RTF is base64 string). http://msdn.microsoft.com/en-us/library/ee202985(v=exchg.80).aspx
        self.airsyncbase_Part = part                                #Optional. Integer. See "MSASCMD.Part". Only present in multipart "MSASCMD.ItemsOperations" response. http://msdn.microsoft.com/en-us/library/hh369854(v=exchg.80).aspx
        self.airsyncbase_Preview = preview                          #Optional. String (unicode). Plaintext preview message. http://msdn.microsoft.com/en-us/library/ff849891(v=exchg.80).aspx
        return

class airsyncbase_Attachment(object): #Repsonse-only object.
    def __init__(self, file_reference, method, estimated_data_size, display_name=None, content_id=None, content_location = None, is_inline = None, email2_UmAttDuration=None, email2_UmAttOrder=None):
        self.airsyncbase_DisplayName = display_name                 #Optional. String. http://msdn.microsoft.com/en-us/library/ee160854(v=exchg.80).aspx
        self.airsyncbase_FileReference = file_reference             #Required. String. Location of attachment on server. http://msdn.microsoft.com/en-us/library/ff850023(v=exchg.80).aspx
        self.airsyncbase_Method = method                            #Required. Byte. See "MSASAIRS.Method". Type of attachment. http://msdn.microsoft.com/en-us/library/ee160322(v=exchg.80).aspx
        self.airsyncbase_EstimatedDataSize = estimated_data_size    #Required. Integer. Max 1. Estimated data size before content filtering rules. http://msdn.microsoft.com/en-us/library/hh475714(v=exchg.80).aspx
        self.airsyncbase_ContentId = content_id                     #Optional. String. Max 1. Unique object id of attachment - informational only.
        self.airsyncbase_ContentLocation = content_location         #Optional. String. Max 1. Contains the relative URI for an attachment, and is used to match a reference to an inline attachment in an HTML message to the attachment in the attachments table. http://msdn.microsoft.com/en-us/library/ee204563(v=exchg.80).aspx
        self.airsyncbase_IsInline = is_inline                       #Optional. Boolean. Max 1. Specifies whether the attachment is embedded in the message. http://msdn.microsoft.com/en-us/library/ee237093(v=exchg.80).aspx
        self.email2_UmAttDuration = email2_UmAttDuration            #Optional. Integer. Duration of the most recent electronic voice mail attachment in seconds. Only used in "IPM.Note.Microsoft.Voicemail", "IPM.Note.RPMSG.Microsoft.Voicemail", or "IPM.Note.Microsoft.Missed.Voice".
        self.email2_UmAttOrder = email2_UmAttOrder                  #Optional. Integer. Order of electronic voice mail attachments. Only used in "IPM.Note.Microsoft.Voicemail", "IPM.Note.RPMSG.Microsoft.Voicemail", or "IPM.Note.Microsoft.Missed.Voice".


    
