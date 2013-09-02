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

"""[MS-ASEMAIL] Email class namespace objects"""

from MSASAIRS import Type as airsync_Type, Body as airsync_Body, Attachment, Method as airsync_Method


class Importance:
    Low =    0
    Normal = 1
    High =   2

class MessageClass:                     #http://msdn.microsoft.com/en-us/library/ee200767(v=exchg.80).aspx
    IPM_Note =                          "IPM.Note"                         #Normal e-mail message.
    IPM_Note_SMIME =                    "IPM.Note.SMIME"                   #The message is encrypted and can also be signed.
    IPM_Note_SMIME_MultipartSigned =    "IPM.Note.SMIME.MultipartSigned"   #The message is clear signed.
    IPM_Note_Receipt_SMIME =            "IPM.Note.Receipt.SMIME"           #The message is a secure read receipt.
    IPM_InfoPathForm =                  "IPM.InfoPathForm"                 #An InfoPath form.
    IPM_Schedule_Meeting =              "IPM.Schedule.Meeting"             #Meeting request.
    IPM_Notification_Meeting =          "IPM.Notification.Meeting"         #Meeting notification.
    IPM_Post =                          "IPM.Post"                         #Post.
    IPM_Octel_Voice =                   "IPM.Octel.Voice"                  #Octel voice message.
    IPM_Voicenotes =                    "IPM.Voicenotes"                   #Electronic voice notes.
    IPM_Sharing =                       "IPM.Sharing"                      #Shared message.

    REPORT_IPM_NOTE_NDR =                           "REPORT.IPM.NOTE.NDR"                       #Non-delivery report for a standard message.
    REPORT_IPM_NOTE_DR =                            "REPORT.IPM.NOTE.DR"                        #Delivery receipt for a standard message.
    REPORT_IPM_NOTE_DELAYED =                       "REPORT.IPM.NOTE.DELAYED"                   #Delivery receipt for a delayed message.
    REPORT_IPM_NOTE_IPNRN =                         "REPORT.IPM.NOTE.IPNRN"                     #Read receipt for a standard message.
    REPORT_IPM_NOTE_IPNNRN =                        "REPORT.IPM.NOTE.IPNNRN"                    #Non-read receipt for a standard message.
    REPORT_IPM_SCHEDULE_MEETING_REQUEST_NDR =       "REPORT.IPM.SCHEDULE.MEETING.REQUEST.NDR"   #Non-delivery report for a meeting request.
    REPORT_IPM_SCHEDULE_MEETING_RESP_POS_NDR =      "REPORT.IPM.SCHEDULE.MEETING.RESP.NDR"      #Non-delivery report for a positive meeting response (accept).
    REPORT_IPM_SCHEDULE_MEETING_RESP_TENT_NDR =     "REPORT.IPM.SCHEDULE.MEETING.TENT.NDR"      #Non-delivery report for a Tentative meeting response.
    REPORT_IPM_SCHEDULE_MEETING_CANCELED_NDR =      "REPORT.IPM.SCHEDULE.MEETING.CANCELED.NDR"  #Non-delivery report for a cancelled meeting notification.
    REPORT_IPM_NOTE_SMIME_NDR =                     "REPORT.IPM.NOTE.SMIME.NDR"                 #Non-delivery report for a Secure MIME (S/MIME) encrypted and opaque-signed message.
    REPORT_IPM_NOTE_SMIME_DR =                      "REPORT.IPM.NOTE.SMIME.DR"                  #Delivery receipt for an S/MIME encrypted and opaque-signed message.
    REPORT_IPM_NOTE_SMIME_MULTIPARTSIGNED_NDR =     "REPORT.IPM.NOTE.SMIME.MULTIPARTSIGNED.NDR" #Non-delivery report for an S/MIME clear-signed message.
    REPORT_IPM_NOTE_SMIME_MULTIPARTSIGNED_DR =      "REPORT.IPM.NOTE.SMIME.MULTIPARTSIGNED.DR"  #Delivery receipt for an S/MIME clear-signed message.

class InstanceType:
    Single =              0
    Recurring_Master =    1
    Recurring_Instance =  2
    Recurring_Exception = 3


class Type: #Recurrence type            #http://msdn.microsoft.com/en-us/library/ee203639(v=exchg.80).aspx
    Daily =                             0
    Weekly =                            1
    Monthly_Nth_day =                   2
    Monthly =                           3
    Yearly_Nth_day_Nth_month =          4
    Yearly_Nth_day_of_week_Nth_month =  5

class email2_CalendarType:                 #http://msdn.microsoft.com/en-us/library/ee625428(v=exchg.80).aspx
    Default =                       0
    Gregorian =                     1
    Gregorian_US =                  2
    Japan =                         3 
    Tiawan =                        4
    Korea =                         5
    Hijri =                         6
    Thai =                          7
    Hebrew =                        8
    GregorianMeFrench =             9
    Gregorian_Arabic =              10
    Gregorian_translated_English =  11
    Gregorian_translated_French =   12
    Japanese_Lunar =                13
    Chinese_Lunar =                 14
    Korean_Lunar =                  15

class DayOfWeek:
    Sunday =    1
    Monday =    2
    Tuesday =   4
    Wednesday = 8
    Thursday =  16
    Friday =    32
    Saturday =  64

class email2_FirstDayOfWeek:
    Sunday =    0
    Monday =    1
    Tuesday =   2
    Wednesday = 2
    Thursday =  4
    Friday =    4
    Saturday =  6

class Sensitivity:
    Normal =        0
    Personal =      1
    Private =       2 
    Confidential =  3

class BusyStatus:
    Free =          0
    Tentative =     1
    Busy =          2
    OutOfOffice =   3

class email2_MeetingMessageType:    #http://msdn.microsoft.com/en-us/library/ff631404(v=exchg.80).aspx
    Silent =            0           #A silent update was performed, or the message type is unspecified.
    Initial =           1           #Initial meeting request.
    Full =              2           #Full update.
    Informational =     3           #Informational update.
    Outdated =          4           #Outdated. A newer meeting request or meeting update was received after this message.
    Delegators_Copy =   5           #Identifies the delegator's copy of the meeting request.
    Delegated =         6           #Identifies that the meeting request has been delegated and the meeting request MUST NOT be responded to.

class Recurrence(object):                                       #http://msdn.microsoft.com/en-us/library/ee160268(v=exchg.80).aspx
    def __init__(self):
        self.Type = Type.Daily                                  #Required. Byte. See "MSASEMAIL.Type" for enum.
        self.Interval = 1                                       #Required. Integer. An Interval element value of 1 indicates that the meeting occurs every week, month, or year, depending upon the value of "self".Type. An Interval value of 2 indicates that the meeting occurs every other week, month, or year.
        self.Until = None                                       #Optional. dateTime. End of recurrence.
        self.Occurances = None                                  #Optional. Integer. Number of occurrences before the series of recurring meetings ends.
        self.WeekOfMonth = None                                 #Optional. Integer. The week of the month in which the meeting recurs. Required when the Type is set to a value of 6.
        self.DayOfMonth = None                                  #Optional. Integer. The day of the month on which the meeting recurs. Required when the Type is set to a value of 2 or 5.
        self.DayOfWeek = None                                   #Optional. Integer. See "MSASEMAIL.DayOfWeek" emun for values. The day of the week on which this meeting recurs. Can be anded together for multiple days of week. Required when the Type is set to a value of 1 or 6
        self.MonthOfYear = None                                 #Optional. Integer. The month of the year in which the meeting recurs. Required when the Type is set to a value of 6.
        self.email2_CalendarType = email2_CalendarType.Default  #Required. Byte. See "MSASEMAIL.email2_CalendarType" for enum.
        self.email2_IsLeapMonth = 0                             #Optional. Byte. Does the recurrence takes place in the leap month of the given year?
        self.email2_FirstDayOfWeek = email2_FirstDayOfWeek.Sunday #Optional. Byte. See "MSASEMAIL.email2_FirstDayOfWeek" for enum. What is considered the first day  of the week for this recurrence?

class MeetingRequest(object):                   #http://msdn.microsoft.com/en-us/library/ee157541(v=exchg.80).aspx
    def __init__(self):
        self.AllDayEvent = False                #Optional. Byte. Is meeting all day? 0 or 1.
        self.StartTime = None                   #Optional. dateTime.
        self.DtStamp = None                     #Required. dateTime. Time that the MeetingRequest item was created.
        self.EndTime = None                     #Optional. dateTime.
        self.InstanceType = InstanceType.Single #Optional. Byte. See "MSASEMAIL.InstanceTypes" enum.
        self.Location = ""                      #Optional. String. Location of meeting.
        self.Organizer = ""                     #Optional. Email address as String. Email address of  meeting organizer.
        self.RecurrenceId = None                #Optional. dateTime of specific instance of recurring meeting.
        self.Reminder = 0                       #Optional. Interger?. Time in seconds before meeting that reminder will be triggered.
        self.ResponseRequested = 1              #Optional. Byte. Has the organizer requested a response of this MeetingRequest? 0 or 1.
        self.Recurrences = []                   #Optional. List of "MSASEMAIL.Recurrence". If specified, at least one recurrence in list is required.
        self.Sensitivity = Sensitivity.Normal   #Optional. Integer. See "MSASEMAIL.Sensitivity" for enum. How sensitive is the meeting? Default is Normal.
        self.BusyStatus = BusyStatus.Tentative  #Optional. Integer. See "MSASEMAIL.BusyStatus" for enum. Default is Tentantive.
        self.TimeZone = ""                      #Required. String formated as per http://msdn.microsoft.com/en-us/library/ee204550(v=exchg.80).aspx.
        self.GlobalObjId = self.set_GlobalObjId()                   #Required. Generated by self.generate_GlobalObjId()
        self.DisallowNewTimeProposal = 0                            #Optional. Byte. 0 = new time proposals allowed, >0 = new time proposals not allowed. Default is 0.
        self.MeetingMessageType = email2_MeetingMessageType.Silent  #Optional. Byte. See "MSASEMAIL.email2_MeetingMessageType" for enum. Default is Silent.
    def set_GlobalObjId(self):
        #TODO
        return
    def set_TimeZone(self, intimezone=None):
        from MSASDTYPE import TimeZone
        if intimezone:
            self.TimeZone = TimeZone.get_timezone_bytes(intimezone)
        else:
            self.TimeZone = TimeZone.get_local_timezone_bytes()

class Email(object):
    """description of class"""
    def __init__(self):
        self.To = []                #String. List of string seperated by commas.
        self.Cc = []                #String. List of string seperated by commas.
        self.From = ""              #String
        self.Subject = ""           #String
        self.ReplyTo = ""           #String. Specifies the e-mail address to which replies will be addressed by default.
        self.DateReceived = None    #dataTime. 
        self.DisplayTo = []         #String. List of display names of recipient seperated by semi-colons.
        self.ThreadTopic = ""       #String
        self.Importance = 1         #Byte. See "MSASEMAIL.Importance"
        self.Read = 0               #Boolean. Whether or not email has been read.
        self.airsync_Attachments = [] #"MSASAIRS.Attachments". List of "MSASAIRS.Attachment"s.
        self.airsync_Body = None    #"MSASAIRS.Body". Email message body.
        self.MessageClass = MessageClass.IPM_Note #String. See "MSASEMAIL.MessageClass" enum.