#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import codecs
import glob

try:
  import simplejson as json
except ImportError:
  import json

dir_path = sys.argv[1]
save_path = sys.argv[1] + "/opelog.out"

files = glob.glob(dir_path + "/*")

if len(files) == 0:
  print(dir_path)
  print("File to be converted in the directory does not exist.")
  sys.exit(1)

def merge_tasks(orig_data, merge_data):
  for task in merge_data.keys():
    if task in orig_data:
      host_data = merge_data[task]
      for host, data in host_data.items():
        orig_data[task][host] = host_data[host]
    else:
      orig_data[task] = merge_data[task]

def write_data(host, data, fd):
  fd.write("[%s]\n" % host)

  if "cmd" in data:
    fd.write("# %s\n" % data['cmd'])
  else:
    return

  for e in ['stdout', 'stderr']:
    if e + "_lines" in data:
      fd.write("%s:\n" % e)
      for line in data[e + '_lines']:
        fd.write("  %s\n" % line)

  for e in ['rc', 'start', 'end', 'delta']:
    if e in data:
      fd.write("%6s: %s\n" % (e, data[e]))

  fd.write("\n")

def convert_humanlog(json_data, fd):
  for task, host_dict in sorted(json_data.items()):
    fd.write("### %s ###\n" % str(task))

    for host, data in sorted(host_dict.items()):
      if "results" in data:
        for v in data['results']:
          write_data(host, v, fd)
        continue

      write_data(host, data, fd)

with open(files[0], "r") as fd:
  try:
    save_data = json.load(fd)
  except:
    save_data = dict()

for f in files[1:]:
  with open(f, "r") as fd:
    try:
      merge_json = json.load(fd)
    except:
      merge_json = dict()
    merge_tasks(save_data, merge_json)

with codecs.open(save_path, "w", "utf-8") as fd:
  convert_humanlog(save_data, fd)
#print(json.dumps(save_data, indent=2))

