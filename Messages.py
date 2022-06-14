import sqlite3
def attachfrommid(mid):
    dbfile = 'sms.db'
    con = sqlite3.connect(dbfile)
    cur = con.cursor()
    files = []
    filename = []
    for row in cur.execute("SELECT * FROM message_attachment_join WHERE message_id = ?",(str(mid),)):
        files.append(row[1])
    for filez in files:
        for row2 in cur.execute("SELECT * FROM attachment WHERE ROWID =?",(str(filez),)):
            filename.append(str(row2[4]))
    relnames = []
    for name in filename:
        relnames.append(name[2:])
    con.close()
    dbfile = 'Manifest.db'
    filenam=[]
    con = sqlite3.connect(dbfile)
    cur = con.cursor()
    for name in relnames:
        for row3 in cur.execute("SELECT fileID FROM Files WHERE relativePath = ?",(str(name),)):
            filenam.append(str(row3[0]))
    return filenam

def parse_smsdb4(): #outputs to a directory with all files attached
    '''
    TODO: Add support for image files and whatnot, output to PDF
    '''
    import shutil
    import glob
    from datetime import datetime
    import os, os.path
    dbfile = 'sms.db'
    con = sqlite3.connect(dbfile)
    cur = con.cursor()
    clA = []
    unix = datetime(1970, 1, 1)  # UTC
    cocoa = datetime(2001, 1, 1)  # UTC
    delta = cocoa - unix  # timedelta instance
    for row in cur.execute("SELECT ROWID,chat_identifier FROM chat"):
        clA.append(row)
    counter = 0
    for chat in clA:
        allchat = []
        for row2 in cur.execute("SELECT message.*, handle.id as sender_name FROM chat_message_join INNER JOIN message ON message.rowid = chat_message_join.message_id INNER JOIN handle ON handle.rowid = message.handle_id WHERE chat_message_join.chat_id ="+str(chat[0])): #TODO: Understand this better.
            allchat.append(row2)
        os.makedirs(os.path.dirname("./chatoutput/"+str(chat[1])+"/"), exist_ok=True)
        with open("./chatoutput/"+str(chat[1])+"/"+str(chat[1])+".txt", "a+", encoding="utf-8") as file: #MUST be set to "a" or the file might overwrite itself if theres a mixed imessage/sms convo...
            for msg in allchat:

                    if "￼" in str(msg[2]):
                        if msg[21] == 1:
                            objlist = []
                            for obj in attachfrommid(msg[0]):
                                path = "C:\\Users\\Daniel\\Apple\\MobileSync\\Backup\\00008101-0009704A2281001E"
                                f1le = glob.glob(path + "/**/"+str(obj), recursive=True)[0]
                                shutil.copy(f1le, "./chatoutput/"+str(chat[1])+"/")
                                objlist.append(str(obj))
                            file.write("OUTBOUND ---> ["+','.join(objlist)+'], (MID:'+str(msg[0])+'), {MDATEHR:'+str(datetime.fromtimestamp(int(msg[15])/1000000000) + delta)+'}\n') #Fix so it shows who its from, the time, etc...

                        else:
                            objlist = []
                            for obj in attachfrommid(msg[0]):
                                path = "C:\\Users\\Daniel\\Apple\\MobileSync\\Backup\\00008101-0009704A2281001E"
                                f1le = glob.glob(path + "/**/"+str(obj), recursive=True)[0]
                                objlist.append(str(obj))
                                shutil.copy(f1le, "./chatoutput/"+str(chat[1])+"/")
                            file.write("INBOUND <--- ["+','.join(objlist)+'], (MID:'+str(msg[0])+'), {MDATEHR:'+str(datetime.fromtimestamp(int(msg[15])/1000000000) + delta)+'}\n') #Fix so it shows who its from, the time, etc...
                    else:
                        if msg[21] == 1:
                            file.write("OUTBOUND ---> ["+str(msg[2])+'], (MID:'+str(msg[0])+'), {MDATEHR:'+str(datetime.fromtimestamp(int(msg[15])/1000000000) + delta)+'}\n') #Fix so it shows who its from, the time, etc...
                        else:
                            file.write("INBOUND <--- ["+str(msg[2])+'], (MID:'+str(msg[0])+'), {MDATEHR:'+str(datetime.fromtimestamp(int(msg[15])/1000000000) + delta)+'}\n') #Fix so it shows who its from, the time, etc...
