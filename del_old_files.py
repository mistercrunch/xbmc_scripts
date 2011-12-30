#!/usr/bin/python
import os, time, shutil

from datetime import datetime, timedelta

file_dir = "/home/mistercrunch/Videos/TV/"
conf_file = "del_old_files.conf"
nb_removed = 0
size_cleared_bytes = 0

for line in open(conf_file):
	if len(line.split(',')) > 1:
		folder,retention_days = line.replace('\n','').split(',')
		for file in os.listdir(file_dir + folder):
			file_full_path = os.path.join(file_dir, folder, file)
			time_diff = datetime.now() - datetime.fromtimestamp(os.path.getmtime(file_full_path))
			#if(type(retention_days) in (int,)):	
			if(int(time_diff.days) > int(retention_days)):
					#print "rm " + file_full_path
					nb_removed+=1
					size_cleared_bytes += os.path.getsize(file_full_path)
					if(os.path.isdir(file_full_path)):
						shutil.rmtree(file_full_path)
					else:
						os.remove(file_full_path)

print str(nb_removed) + ' files were removed'
print str(size_cleared_bytes / (1024*1024)) + ' MBs were cleared'


