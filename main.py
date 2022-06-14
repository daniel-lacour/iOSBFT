"""
TODO:
    [] Streamline process from backup folder to end result
    [] Clean code
    [] Add contact recognition
"""
from Messages import parse_smsdb4
def main(backuppath):
    manifestDB = backuppath+"/Manifest.db"
    smsDB = backuppath+"3d/3d0d7e5fb2ce288813306e4d4636395e047a3d28" #TODO: Make this based on the manifest.db entry
parse_smsdb4()
