#!/usr/bin/env python
#
# Take the given iPhone backup and parcel it out into different directories
#
# $Id: sortiPhoneBackup.py 3969 2012-12-28 08:11:29Z mshafae $
#

# location of iPhone backups:
# Mac ~/Library/Application Support/MobileSync/Backup/
# Windows XP: \Documents and Settings\(username)\Application Data\Apple Computer\MobileSync\Backup\
# Windows Vista and Windows 7: \Users\(username)\AppData\Roaming\Apple Computer\MobileSync\Backup\

"""
The sqlite db with the madrid_chat table is the SMS database
The sqlite db with the voicemail table is the voicemail database

Unique types identified by looking at '~/Library/Application Support/MobileSync/Backup/*' 
"""

import os
import os.path
import sys
import shutil
import glob

# external dependency
import magic

def buildTable(targetDir):
  iOSBackupFiles = {}
  m = magic.Magic(mime = True)
  files = glob.glob(targetDir + '/*')
  print('Inspecting {} files. This may take a while.'.format(len(files)))
  count = 0
  for f in files:
    magicName = m.from_file(f)
    try:
      iOSBackupFiles[magicName].append(f)
    except KeyError:
      iOSBackupFiles[magicName] = []
      iOSBackupFiles[magicName].append(f)
    count += 1
    if count % 500 == 0:
      print('{} files remaining'.format(len(files) - count))
  return iOSBackupFiles

def slashToUnderscore(s):
  return s.replace('/', '_')

def makeDirectories(dirNames, targetDir):
  for d in dirNames:
    os.makedirs(targetDir + '/' + d)

def fileExtensionLookUp(key):
  if key == 'application/xml':
    ext = '.xml'
  elif key == 'application/zip':
    ext = '.zip'
  elif key == 'audio/mp4':
    ext = '.mp4'
  elif key == 'image/gif':
    ext = '.gif'
  elif key == 'image/jpeg':
    ext = '.jpg'
  elif key == 'image/png':
    ext = '.png'
  elif key == 'image/tiff':
    ext = '.tiff'
  elif key == 'text/html':
    ext = '.html'
  elif key == 'text/plain':
    ext = '.txt'
  elif key == 'video/3gpp':
    ext = '.3gpp'
  elif key == 'text/x-vcard':
    ext = '.vcard'
  elif key == 'audio/mpeg':
    ext = '.mpeg'
  elif key == 'text/x-asm':
    ext = '.asm'
  elif key == 'video/quicktime':
    ext = '.mov'
  elif key == 'application/octet-stream':
    ext = 'special'
  else:
    ext = ''
  return ext

def specialExtensionLookup(s):
  if s == 'Adaptive Multi-Rate Codec (GSM telephony)':
    ext = '.amr'
  elif s == 'Apple binary property list':
    ext = '.plist'
  elif s.startswith('SQLite 3.x database'):
    ext = '.sqlite3'
  elif s == 'CoreAudio Format audio file version 1':
    ext = '.caf'
  elif s == 'DOS executable (device driver)':
    ext = '.exe'
  elif s == 'exported SGML document text':
    ext = '.sgml'
  elif s.startswith('XWD X Window Dump image data'):
    ext = '.xwd'
  else:
    ext = '.data'
  return ext
  
def copyDataToDirectories(iOSDict, targetDir):
  for k in iOSDict.keys( ):
    dest = targetDir + '/' + slashToUnderscore(k) + '/'
    fileExtension = fileExtensionLookUp(k)
    if fileExtension == 'special':
      for i in iOSDict[k]:
        name = os.path.basename(i)
        ext = specialExtensionLookup(magic.from_file(i))
        dirExt = ext[1:]
        if not os.path.exists(dest + dirExt):
          os.makedirs(dest + dirExt)
        shutil.copy2(i, dest + dirExt + '/' + name + ext)
    else:
      for i in iOSDict[k]:
        name = os.path.basename(i)
        print('copying {} to {}'.format(i, dest + i + fileExtension))
        shutil.copy2(i, dest + name + fileExtension)
        
def main( ):
  """
  sys.argv[1] is the source directory
      ~/Library/Application\ Support/MobileSync/Backup/
  sys.argv[2] is the target directory 
      ~/Documents/phone-4gs
  """
  
  if not os.path.exists(sys.argv[2]):
    os.makedirs(sys.argv[2])
  else:
    print('Directory exists ({}); exiting.'.format(sys.argv[2]))
    sys.exit(1)
  print('Reading entire backup...')
  typesAndFilesDict = buildTable(sys.argv[1])
  types = typesAndFilesDict.keys()
  dirNames = map(slashToUnderscore, types)
  print('Preparing destination directories.')
  makeDirectories(dirNames, sys.argv[2])
  print('Copying data...')
  copyDataToDirectories(typesAndFilesDict, sys.argv[2])


if __name__ == '__main__':
  main( )
