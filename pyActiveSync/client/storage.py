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

import sqlite3

class storage:
    @staticmethod
    def create_db(path=None):
        if path:
            if path != "pyas.asdb":
                if not path[-1] == "\\":
                    path = path + "\\pyas.asdb"
        else:
            path="pyas.asdb"
        conn = sqlite3.connect(path)
        curs = conn.cursor()
        curs.execute("""CREATE TABLE FolderHierarchy (ServerId text, ParentId text, DisplayName text, Type text)""")
        curs.execute("""CREATE TABLE SyncKeys (SyncKey text, CollectionId text)""")
        curs.execute("""CREATE TABLE KeyValue (Key text, Value blob)""")

        curs.execute("""CREATE TABLE MSASEMAIL (ServerId text, 
                                                email_To text, 
                                                email_Cc text,
                                                email_From text,
                                                email_Subject text,
                                                email_ReplyTo text,
                                                email_DateReceived text,
                                                email_DisplayTo text,
                                                email_ThreadTopic text,
                                                email_Importance text,
                                                email_Read text,
                                                airsyncbase_Attachments text,
                                                airsyncbase_Body text,
                                                email_MessageClass text,
                                                email_InternetCPID text,
                                                email_Flag text,
                                                airsyncbase_NativeBodyType text,
                                                email_ContentClass text,
                                                email2_UmCallerId text,
                                                email2_UmUserNotes text,
                                                email2_ConversationId text,
                                                email2_ConversationIndex text,
                                                email2_LastVerbExecuted text,
                                                email2_LastVerbExecutedTime text,
                                                email2_ReceivedAsBcc text,
                                                email2_Sender text,
                                                email_Categories text,
                                                airsyncbase_BodyPart text,
                                                email2_AccountId text,
                                                rm_RightsManagementLicense text)""")
        conn.commit()
        conn.close()

    @staticmethod
    def insert_folderhierarchy_change(folder, curs):
        sql = "INSERT INTO FolderHierarchy VALUES ('%s', '%s', '%s', '%s')""" % (folder.ServerId, folder.ParentId, folder.DisplayName, folder.Type)
        curs.execute(sql)

    @staticmethod
    def update_folderhierarchy_change(folder, curs):
        sql = "UPDATE FolderHierarchy SET ParentId='%s', DisplayName='%s', Type='%s' WHERE ServerId == '%s'""" % (folder.ParentId, folder.DisplayName, folder.Type, folder.ServerId)
        curs.execute(sql)

    @staticmethod
    def delete_folderhierarchy_change(folder, curs):
        #Command only sent we permement delete is requested. Otherwise it would be 'Update' to ParentId='3' (Deleted Items).
        #sql = "UPDATE FolderHierarchy SET ParentId='4' WHERE ServerId == '%s'""" % (folder.ServerId)
        sql = "DELETE FROM MSASEMAIL WHERE ServerId like '%s:%%'" % (folder.ServerId)
        curs.execute(sql)
        sql = "DELETE FROM FolderHierarchy WHERE ServerId == '%s'" % (folder.ServerId)
        curs.execute(sql)

    @staticmethod
    def update_folderhierarchy(changes, path="pyas.asdb"):
        conn = sqlite3.connect(path)
        curs = conn.cursor()
        for change in changes:
            if change[0] == "Update":
                storage.update_folderhierarchy_change(change[1], curs)
            elif change[0] == "Delete":
                storage.delete_folderhierarchy_change(change[1], curs)
            elif change[0] == "Add":
                storage.insert_folderhierarchy_change(change[1], curs)
        conn.commit()
        conn.close()

    @staticmethod
    def insert_email(email, curs):
        sql = """INSERT INTO MSASEMAIL VALUES ('%s', '%s', '%s', '%s', '%s', 
                                                '%s', '%s', %s, '%s', '%s', 
                                                '%s', '%s', '%s', '%s', '%s', 
                                                '%s', '%s', '%s', '%s', '%s', 
                                                '%s', '%s', '%s', '%s', '%s', 
                                                '%s', '%s', %s, '%s', '%s')"""  % (
                                                           email.server_id, email.email_To, repr(email.email_Cc), email.email_From, email.email_Subject,
                                                           email.email_ReplyTo, email.email_DateReceived, repr(email.email_DisplayTo), email.email_ThreadTopic, email.email_Importance,
                                                           email.email_Read, repr(email.airsyncbase_Attachments), repr(email.airsyncbase_Body), email.email_MessageClass, email.email_InternetCPID,
                                                           repr(email.email_Flag), email.airsyncbase_NativeBodyType, email.email_ContentClass, email.email2_UmCalledId, email.email2_UmUserNotes,
                                                           email.email2_ConversationId, email.email2_ConversationIndex, email.email2_LastVerbExecuted, email.email2_LastVerbExecutedTime, email.email2_ReceivedAsBcc,
                                                           email.email2_Sender, repr(email.email_Categories), repr(email.airsyncbase_BodyPart), email.email2_AccountId, repr(email.rm_RightsManagementLicense))
        curs.execute(sql)

    @staticmethod
    def update_emails(collections, path="pyas.asdb"):
        conn = sqlite3.connect(path)
        curs = conn.cursor()
        for collection in collections:
            if collection.SyncKey > 1:
                storage.update_synckey(collection.SyncKey, collection.CollectionId, curs)
                conn.commit()
            else:
                conn.close()
                raise AttributeError("SyncKey incorrect")

            for command in collection.Commands:
                if command[0] == "Add":
                    storage.insert_email(command[1], curs)
                elif command[0] == "Delete":
                    continue
                elif command[0] == "Change":
                    continue
                elif command[0] == "SoftDelete":
                    continue
        conn.commit()
        conn.close()

    @staticmethod
    def update_synckey(synckey, collectionid, curs=None):
        cleanup = False
        if not curs:
            cleanup = True
            conn = sqlite3.connect("pyas.asdb")
            curs = conn.cursor()
        curs.execute("SELECT SyncKey FROM SyncKeys WHERE CollectionId = %s" % collectionid)
        prev_synckey = curs.fetchone()
        if not prev_synckey:
            curs.execute("INSERT INTO SyncKeys VALUES ('%s', '%s')" % (synckey, collectionid))
        else:
            curs.execute("UPDATE SyncKeys SET SyncKey='%s' WHERE CollectionId='%s'" % (synckey, collectionid)) 
        if cleanup:
            conn.commit()
            conn.close()

    @staticmethod
    def get_synckey(collectionid, path="pyas.asdb"):
        conn = sqlite3.connect(path)
        curs = conn.cursor()
        curs.execute("SELECT SyncKey FROM SyncKeys WHERE CollectionId = %s" % collectionid)
        try:
            synckey = curs.fetchone()[0]
        except TypeError:
            synckey = "0"
        conn.close()
        return synckey

    @staticmethod
    def create_db_if_none(path="pyas.asdb"):
        import os
        if not os.path.isfile(path):
            storage.create_db(path)