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

from MSASEMAIL import *

email1 = Email()
print email1

meeting_request1 = email_MeetingRequest()
print meeting_request1

meeting_recurrence1 = email_Recurrence()
print meeting_recurrence1

from MSASAIRS import airsyncbase_Type, airsyncbase_Body, airsyncbase_Attachment

body1 = airsyncbase_Body(airsyncbase_Type.HTML)
print body1

attachment1 = airsyncbase_Attachment(None, None, None)
print attachment1