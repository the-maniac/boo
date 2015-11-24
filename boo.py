import os
import sys
import shlex
from subprocess import call

SEPARATOR = '======================================================================='

if 1 < len(sys.argv):
    original_path = sys.argv[1].replace(' ', '\ ')
else:
    original_path = raw_input('Path to iso file: ')

head, tail = os.path.split(original_path)

target_path = original_path + '.img'

final_path = target_path + '.dmg'

print SEPARATOR

print 'Creating image file ==> ' + final_path

call('hdiutil convert -format UDRW -o %s  %s' % (target_path, original_path), shell=True)

print SEPARATOR

print 'LIST OF ALL DISKS'

print SEPARATOR

call('diskutil list', shell=True)

print SEPARATOR

disk_number = raw_input('Enter disk number: ')
disk_name = '/dev/disk%s' % disk_number
rdisk_name = '/dev/rdisk%s' % disk_number

call('diskutil list ' + disk_name, shell=True)

print SEPARATOR

yes_no = raw_input('Are you sure that you want process this disk, all data will be erased y/n: ')

if not yes_no.lower().startswith('y'):
    exit(1)

call('diskutil unmountDisk %s' % disk_name, shell=True)
call(shlex.split("sudo dd if=%s of=%s bs=1m" % (final_path, rdisk_name)))
call('diskutil eject %s' % disk_name, shell=True)
