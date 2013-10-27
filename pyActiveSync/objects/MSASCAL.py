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

"""[MS-ASCAL] Calendar objects"""

from MSASEMAIL import airsyncbase_Body

@staticmethod
def parse_calendar(data):
    calendar_dict = {}
    calendar_base = data.get_children()
    calendar_dict.update({"server_id" : calendar_base[0].text})
    calendar_elements = calendar_base[1].get_children()
    for element in calendar_elements:
        if element.tag == "calendar:AllDayEvent":
            calendar_dict.update({ "calendar_AllDayEvent" : element.text })
        elif element.tag == "calendar:AppointmentReplyTime":
            calendar_dict.update({ "calendar_AppointmentReplyTime" : element.text })
        elif element.tag == "calendar:Attendee":
            calendar_dict.update({ "calendar_Attendee" : element.text })
        elif element.tag == "calendar:Attendees":
            calendar_dict.update({ "calendar_Attendees" : element.text })
        elif element.tag == "calendar:AttendeeStatus":
            calendar_dict.update({ "calendar_AttendeeStatus" : element.text })
        elif element.tag == "calendar:AttendeeType":
            calendar_dict.update({ "calendar_AttendeeType" : element.text })
        elif element.tag == "airsyncbase:Body":
            body = airsyncbase_Body()
            body.parse(element)
            calendar_dict.update({ "airsyncbase_Body" : body })
        elif element.tag == "calendar:BusyStatus":
            calendar_dict.update({ "calendar_BusyStatus" : element.text })
        elif element.tag == "calendar:CalendarType":
            calendar_dict.update({ "calendar_CalendarType" : element.text })
        elif element.tag == "calendar:Categories":
            calendar_dict.update({ "calendar_Categories" : element.text })
        elif element.tag == "calendar:Category":
            calendar_dict.update({ "calendar_Category" : element.text })
        elif element.tag == "calendar:DayOfMonth":
            calendar_dict.update({ "calendar_DayOfMonth" : element.text })
        elif element.tag == "calendar:DayOfWeek":
            calendar_dict.update({ "calendar_DayOfWeek" : element.text })
        elif element.tag == "calendar:Deleted":
            calendar_dict.update({ "calendar_Deleted" : element.text })
        elif element.tag == "calendar:DisallowNewTimeProposal":
            calendar_dict.update({ "calendar_DisallowNewTimeProposal" : element.text })
        elif element.tag == "calendar:DtStamp":
            calendar_dict.update({ "calendar_DtStamp" : element.text })
        elif element.tag == "calendar:Email":
            calendar_dict.update({ "calendar_Email" : element.text })
        elif element.tag == "calendar:EndTime":
            calendar_dict.update({ "calendar_EndTime" : element.text })
        elif element.tag == "calendar:Exception":
            calendar_dict.update({ "calendar_Exception" : element.text })
        elif element.tag == "calendar:Exceptions":
            calendar_dict.update({ "calendar_Exceptions" : element.text })
        elif element.tag == "calendar:ExceptionStartTime":
            calendar_dict.update({ "calendar_ExceptionStartTime" : element.text })
        elif element.tag == "calendar:FirstDayOfWeek":
            calendar_dict.update({ "calendar_FirstDayOfWeek" : element.text })
        elif element.tag == "calendar:Interval":
            calendar_dict.update({ "calendar_Interval" : element.text })
        elif element.tag == "calendar:IsLeapMonth":
            calendar_dict.update({ "calendar_IsLeapMonth" : element.text })
        elif element.tag == "calendar:Location":
            calendar_dict.update({ "calendar_Location" : element.text })
        elif element.tag == "calendar:MeetingStatus":
            calendar_dict.update({ "calendar_MeetingStatus" : element.text })
        elif element.tag == "calendar:MonthOfYear":
            calendar_dict.update({ "calendar_MonthOfYear" : element.text })
        elif element.tag == "calendar:Name":
            calendar_dict.update({ "calendar_Name" : element.text })
        elif element.tag == "airsyncbase:NativeBodyType":
            calendar_dict.update({ "airsyncbase_NativeBodyType" : element.text })
        elif element.tag == "calendar:Occurrences":
            calendar_dict.update({ "calendar_Occurrences" : element.text })
        elif element.tag == "calendar:OnlineMeetingConfLink":
            calendar_dict.update({ "calendar_OnlineMeetingConfLink" : element.text })
        elif element.tag == "calendar:OnlineMeetingExternalLink":
            calendar_dict.update({ "calendar_OnlineMeetingExternalLink" : element.text })
        elif element.tag == "calendar:OrganizerEmail":
            calendar_dict.update({ "calendar_OrganizerEmail" : element.text })
        elif element.tag == "calendar:OrganizerName":
            calendar_dict.update({ "calendar_OrganizerName" : element.text })
        elif element.tag == "calendar:Recurrence":
            calendar_dict.update({ "calendar_Recurrence" : element.text })
        elif element.tag == "calendar:Reminder":
            calendar_dict.update({ "calendar_Reminder" : element.text })
        elif element.tag == "calendar:ResponseRequested":
            calendar_dict.update({ "calendar_ResponseRequested" : element.text })
        elif element.tag == "calendar:ResponseType":
            calendar_dict.update({ "calendar_ResponseType" : element.text })
        elif element.tag == "calendar:Sensitivity":
            calendar_dict.update({ "calendar_Sensitivity" : element.text })
        elif element.tag == "calendar:StartTime":
            calendar_dict.update({ "calendar_StartTime" : element.text })
        elif element.tag == "calendar:Subject":
            calendar_dict.update({ "calendar_Subject" : element.text })
        elif element.tag == "calendar:Timezone":
            calendar_dict.update({ "calendar_Timezone" : element.text })
        elif element.tag == "calendar:Type":
            calendar_dict.update({ "calendar_Type" : element.text })
        elif element.tag == "calendar:UID":
            calendar_dict.update({ "calendar_UID" : element.text })
        elif element.tag == "calendar:Until":
            calendar_dict.update({ "calendar_Until" : element.text })
        elif element.tag == "calendar:WeekOfMonth":
            calendar_dict.update({ "calendar_WeekOfMonth" : element.text })
    return calendar_dict