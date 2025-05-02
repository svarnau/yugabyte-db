# Library for test reporting to YB Report Portal server.

import json
import os
import requests

# API & Token should be set via jenkins jobs,
# but launch is only set if CSI reporting is enabled.
# If launch is set, we can assume the other two are as well.
def csi_env():
  return {
    'launch': os.getenv('YB_CSI_LAUNCH', None),
    'api': os.getenv('CSI_API', ''),
    'headers': {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + os.getenv('CSI_TOKEN', '')
    }
  }

# Convert floating-point seconds epoch time to integer milliseconds
def mst(time_sec):
  return round(time_sec * 1000)

def create_suite(name, parent, time_sec):
  csi = csi_env()
  # If we have a launch, it is still possible creation of parent failed.
  if not csi['launch'] or not parent:
    return None

  req_data = {
    'name': name,
    'launchUuid': csi['launch'],
    'type': 'suite',
    'uniqueId': name,
    'startTime': mst(time_sec)
  }
  response = request.post(csi['url'] + '/item/' + parent,
                          headers=csi['headers'],
                          data=req_data)
  if response.status_code == 201:
    return reponse.json()['id']
  else:
    print(f"Error: Creation of {name} failed: {response.text}"
    return None


def create_test(tname, coderef, lang, parent, attempt, time_sec):
  csi = csi_env()
  if not csi['launch'] or not parent:
    return None

  req_data = {
    'name': tname,
    'launchUuid': csi['launch'],
    'type': 'test',
    'uniqueId': tname,
    'codeRef': coderef,
    'retry': (attempt > 1),  # These might run out of order, if all attmpts are pre-planned
    'startTime': mst(time_sec),
    'attributes': {
      'class': cname,
      'test': tname,
      'lang': lang
    }
  }
  response = request.post(csi['url'] + '/item/' + parent,
                          headers=csi['headers'],
                          data=req_data)
  if response.status_code == 201:
    return reponse.json()['id']
  else:
    print(f"Error: Creation of {name} failed: {response.text}"
    return None

# finish test or suite
def close_item(item, result):
  csi = csi_env()
  if not csi['launch'] or not item:
    return None
 # TODO

def upload_log():
  csi = csi_env()
  if not csi['launch']:
    return None
 # TODO
