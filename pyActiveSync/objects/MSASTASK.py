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

"""[MS-ASTASK] Task objects"""

from MSASEMAIL import airsyncbase_Body

@staticmethod
def parse_task(data):
    task_dict = {}
    task_base = data.get_children()
    task_dict.update({"server_id" : task_base[0].text})
    task_elements = task_base[1].get_children()
    for element in task_elements:
        if element.tag == "airsyncbase:Body":
            body = airsyncbase_Body()
            body.parse(element)
            task_dict.update({ "airsyncbase_Body" : body })
        elif element.tag == "tasks:CalendarType":
            task_dict.update({ "tasks_CalendarType" : element.text })
        elif element.tag == "tasks:Categories":
                    note_dict.update({ "tasks_Categories" : []})
                    categories_elements = element.get_children()
                    for category in categories_elements:
                        note_dict["tasks_Categories"].append(category.text)
        elif element.tag == "tasks:Complete":
            task_dict.update({ "tasks_Complete" : element.text })
        elif element.tag == "tasks:DateCompleted":
            task_dict.update({ "tasks_DateCompleted" : element.text })
        elif element.tag == "tasks:DayOfMonth":
            task_dict.update({ "tasks_DayOfMonth" : element.text })
        elif element.tag == "tasks:DayOfWeek":
            task_dict.update({ "tasks_DayOfWeek" : element.text })
        elif element.tag == "tasks:DeadOccur":
            task_dict.update({ "tasks_DeadOccur" : element.text })
        elif element.tag == "tasks:DueDate":
            task_dict.update({ "tasks_DueDate" : element.text })
        elif element.tag == "tasks:FirstDayOfWeek":
            task_dict.update({ "tasks_FirstDayOfWeek" : element.text })
        elif element.tag == "tasks:Importance":
            task_dict.update({ "tasks_Importance" : element.text })
        elif element.tag == "tasks:Interval":
            task_dict.update({ "tasks_Interval" : element.text })
        elif element.tag == "tasks:IsLeapMonth":
            task_dict.update({ "tasks_IsLeapMonth" : element.text })
        elif element.tag == "tasks:MonthOfYear":
            task_dict.update({ "tasks_MonthOfYear" : element.text })
        elif element.tag == "tasks:Occurrences":
            task_dict.update({ "tasks_Occurrences" : element.text })
        elif element.tag == "tasks:OrdinalDate":
            task_dict.update({ "tasks_OrdinalDate" : element.text })
        elif element.tag == "tasks:Recurrence":
            task_dict.update({ "tasks_Recurrence" : element.text })
        elif element.tag == "tasks:Regenerate":
            task_dict.update({ "tasks_Regenerate" : element.text })
        elif element.tag == "tasks:ReminderSet":
            task_dict.update({ "tasks_ReminderSet" : element.text })
        elif element.tag == "tasks:ReminderTime":
            task_dict.update({ "tasks_ReminderTime" : element.text })
        elif element.tag == "tasks:Sensitivity":
            task_dict.update({ "tasks_Sensitivity" : element.text })
        elif element.tag == "tasks:Start":
            task_dict.update({ "tasks_Start" : element.text })
        elif element.tag == "tasks:StartDate":
            task_dict.update({ "tasks_StartDate" : element.text })
        elif element.tag == "tasks:Subject":
            task_dict.update({ "tasks_Subject" : element.text })
        elif element.tag == "tasks:SubOrdinalDate":
            task_dict.update({ "tasks_SubOrdinalDate" : element.text })
        elif element.tag == "tasks:Type":
            task_dict.update({ "tasks_Type" : element.text })
        elif element.tag == "tasks:Until":
            task_dict.update({ "tasks_Until" : element.text })
        elif element.tag == "tasks:UtcDueDate":
            task_dict.update({ "tasks_UtcDueDate" : element.text })
        elif element.tag == "tasks:UtcStartDate":
            task_dict.update({ "tasks_UtcStartDate" : element.text })
        elif element.tag == "tasks:WeekOfMonth":
            task_dict.update({ "tasks_WeekOfMonth" : element.text })
    return task_dict