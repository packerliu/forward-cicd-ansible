#!/usr/bin/env python

import json

# Open the paths.json that contains the Path API json output
try:
  f = open("paths.json", "r")
  if f.mode == 'r':
      file_str = f.read()
except:
  print("An exception occurred while opening the API json file")

# convert the file from string to Python object format
paths_json = json.loads(file_str)

# Extract the first path and the related outcomes
best_path = paths_json['info']['paths'][0]
path_security_outcome   = best_path['securityOutcome']
path_forwarding_outcome = best_path['forwardingOutcome']

# Take action based on the forwarding and security outcomes
if path_forwarding_outcome == "DENIED":
    print("The is no valid routing path between source and destination")
    print("Please contact your network administrator")

elif path_forwarding_outcome == "DELIVERED" and path_security_outcome == "DELIVERED":
    print("The security policy is already configured. No changes needed")

elif path_forwarding_outcome == "DELIVERED" and path_security_outcome == "DENIED":
    print("The forwarding is OK but the security rules need to be changed ")
    print("on these devices: ")
    for hop in best_path['hops']:
        for behavior in hop['behaviors']:
            if behavior == "ACL_DENY":
                print(hop['deviceName'])
                
else:
    print("something went wrong!!")
    print("Path Security Outcome: "   + path_security_outcome)
    print("Path Forwarding Outcome: " + path_forwarding_outcome)
