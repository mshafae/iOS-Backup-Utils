# iOS Backup Utils
Author: Michael Shafae
URL: <http://michael.shafae.com/>
Date: 12/28/2012
Release: 0.1

# Summary

This repository includes two programs which sort through a backup of an iOS host. The backups are assumed to be those made by iTunes.

Each program was tested with Python v.2.7.

# Dependencies

* Python Magic v.0.4.3 <http://pypi.python.org/pypi/python-magic/>

# sortiPhoneBackup.py

Usage: sortiPhoneBackup.py <iOS Backup> <dest. dir.>

Ex.: sortiPhoneBackup.py ~/Library/ApplicationsortiPhoneBackup.py ~/Library/Application\ Support/MobileSync/Backup/8360021332ed2d7109617aa376c569ffa1b8668d ~/Documents/iPhone4-2012-01-10-backup

All the files in the source backup directory are sorted by their MIME types into individual directories. The files are renamed with the appropriate extension to facilitate inspecting each file.

# extractiPhoneVoiceMails.py

Usage: extractiPhoneVoiceMails.py <iOS Backup> <dest. dir.>

Ex.: ~/Library/ApplicationsortiPhoneBackup.py ~/Library/Application\ Support/MobileSync/Backup/8360021332ed2d7109617aa376c569ffa1b8668d ~/Documents/voicemails

An iOS backup is searched for the voicemail.db and voicemail files. The voicemail files will be copied to the destination directory in it's own directory constructed from today's date (i.e. 2012-01-10). A manifest is generated from the voicemail.db and outputed as tab delimitted test in the destination directory. Voicemails are not renamed from the mangled names since a mapping was not found from the voicemail.db entries to the appropriate voicemail audio files.

Voicemail files are left in the default "Adaptive Multi-Rate Codec (GSM telephony)" file format. (They can be trivially converted using ffmpeg.)

