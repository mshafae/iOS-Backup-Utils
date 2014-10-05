#!/usr/bin/env python
#
# Copyright (c) 2012 Michael Shafae.
# All rights reserved.
#
# Back up iPhone voicemails from src dir to target dir
#
# $Id: extractiPhoneVoiceMails.py 3968 2012-12-28 08:06:19Z mshafae $
#

# location of iPhone backups:
# Mac ~/Library/Application Support/MobileSync/Backup/
# Windows XP: \Documents and Settings\(username)\Application Data\Apple Computer\MobileSync\Backup\
# Windows Vista and Windows 7: \Users\(username)\AppData\Roaming\Apple Computer\MobileSync\Backup\

import glob
import os
import os.path
import sys
import shutil
import time
import sqlite3

# external dependency
import magic


def allAMRAndSQLiteFiles(targetDir):
  amrFiles = []
  sqliteFiles = []
  files = glob.glob(targetDir + '/*')
  print('Inspecting {} files. This may take a while.'.format(len(files)))
  count = 0
  for f in files:
    if magic.from_file(f) == 'Adaptive Multi-Rate Codec (GSM telephony)':
      amrFiles.append(f)
    elif magic.from_file(f).startswith('SQLite 3.x database'):
      sqliteFiles.append(f)
    count += 1
    if count % 500 == 0:
      print('{} files remaining'.format(len(files) - count))
  return (amrFiles, sqliteFiles)

def copyAndRenameVoicemails(files, targetDir):
  for vm in files:
    theVM = os.path.basename(vm)
    targetFileName = targetDir + '/' + theVM + '.amr'
    print('copying {} to {}'.format(vm, targetFileName))
    shutil.copy2(vm, targetFileName)

def targetCTimeDateString(target):
  t = time.localtime(os.path.getctime(target))
  return time.strftime('%Y-%m-%d', t)

def findVoicemailDB(sqliteFiles):
  """
  SELECT name FROM sqlite_master WHERE type='table' AND name='voicemail';
  """
  print('Searching for voicemail metadata database.')
  rv = None
  for f in sqliteFiles:
    connection = sqlite3.connect(f)
    c = connection.cursor( )
    s = c.execute("select name from sqlite_master where type='table' and name='voicemail'").fetchone( )
    connection.close( )
    if s != None:
      rv = f
      break
  return rv

def outputVoicemailManifest(db, target):
  connection = sqlite3.connect(db)
  c = connection.cursor( )
  fh = open(target + '/voicemail_manifest.txt', 'w')
  fh.write('Date (YYYY-MM-DD-HH:MM)\tSender\t\tDuration (Sec.)\n')
  for row in c.execute("select date, sender, duration from voicemail order by date ASC"):
    date = time.strftime('%Y-%m-%d-%H:%M', time.localtime(row[0]))
    fh.write('{}\t{}\t{}\n'.format(date, row[1], row[2]))
  connection.close( )

def copyAndRenameVoicemailDB(db, target):
  targetFileName = target + '/voicemail.db'
  print('copying {} to {}'.format(db, targetFileName))
  shutil.copy2(db, targetFileName)
  
def main( ):
  """
  sys.argv[1] is the source directory
      ~/Library/Application\ Support/MobileSync/Backup/
  sys.argv[2] is the target directory 
      ~/Documents/phone-4gs
  """
  ctime = targetCTimeDateString(sys.argv[1])
  target = sys.argv[2] + '/' + ctime
  if not os.path.exists(target):
    os.makedirs(target)
    print('makedir')
  else:
    print('Directory exists ({}); exiting.'.format(target))
    sys.exit(1)
  print('Searching for voicemail data.')
  amrFiles, sqliteFiles = allAMRAndSQLiteFiles(sys.argv[1])
  print('Found a total of {} voicemails'.format(len(amrFiles)))
  print('Looking for the voicemail metadata database')
  voicemailDB = findVoicemailDB(sqliteFiles)
  print voicemailDB
  copyAndRenameVoicemails(amrFiles, target)
  copyAndRenameVoicemailDB(voicemailDB, target)
  outputVoicemailManifest(voicemailDB, target)

if __name__ == '__main__':
  main( )
