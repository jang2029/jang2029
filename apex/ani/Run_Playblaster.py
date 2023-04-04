import sys

ver = sys.version
if (ver.split('.')[0]) == '3':
    exec(open(r'Q:\pipeline_script\script\playBlaster.py', 'r', encoding = 'UTF8' ).read())

if (ver.split('.')[0]) == '2':
    execfile(r'Q:\pipeline_script\script\playBlaster.py')