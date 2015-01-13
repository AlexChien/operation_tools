#!/usr/bin/env python
# coding=utf8

# This is a script which connects to a delegate periodically to check if the pay balance is at a,
# threshold set in the config.json file. If it is, it sends the balance_threshold amount to the payto account
# specified.
# if each delegate has seperate payto account, delete can be set as 'delegate_name|pay_to_different_account' and payto_account will serve as default payto account, pay_to_different_account will override default payto_account for this particular delegate

import requests
import sys
import os
import json
import getpass
import time
import datetime
from pprint import pprint

BTS_PRECISION = 100000
# loop interval in seconds to check balance
# set to 1 hour
CHECK_INTERVAL = 60 * 60

config_data = open('config.json')
config = json.load(config_data)
config_data.close()

auth = (config["bts_rpc"]["username"], config["bts_rpc"]["password"])
url = config["bts_rpc"]["url"]

WALLET_NAME = config["wallet_name"]

DELEGATE_NAMES = config["delegate_name"]
DEFAULT_PAYTO = config["payto_account"]
THRESH = config["balance_threshold"]

def parse_date(date):
  return datetime.datetime.strptime(date, "%Y%m%dT%H%M%S")

def call(method, params=[]):
  headers = {'content-type': 'application/json'}
  request = {
          "method": method,
          "params": params,
          "jsonrpc": "2.0",
          "id": 1
          }

  while True:
    try:
      response = requests.post(url, data=json.dumps(request), headers=headers, auth=auth)
      result = json.loads(vars(response)["_content"])
      #print "Method:", method
      #print "Result:", result
      return result
    except:
      print "Warnning: rpc call error, retry 5 seconds later"
      time.sleep(5)
      continue
    break
  return None

while True:
  try:
    os.system("clear")
    print("\nRunning Balance Keeper: %s" % time.strftime("%Y%m%dT%H%M%S", time.localtime(time.time())))

    for DELEGATE_NAME_SETTING in DELEGATE_NAMES:
      # use individual delegate|payto setting, otherwise, use default payto
      data = DELEGATE_NAME_SETTING.split('|')
      DELEGATE_NAME = data[0]
      if len(data) > 1:
        PAYTO = data[1]
      else:
        PAYTO = DEFAULT_PAYTO

      response = call("wallet_get_account", [DELEGATE_NAME] )
      if "error" in response:
        print("FATAL: Failed to get info:")
        print(result["error"])
        exit(1)
      response = response["result"]

      balance = response["delegate_info"]["pay_balance"] / BTS_PRECISION

      print ("%s: %s BTS" % (DELEGATE_NAME, balance))

      if balance > THRESH:
         print(">> wallet_delegate_withdraw_pay %s, %s, %s" % (DELEGATE_NAME, PAYTO, THRESH))
         response = call("wallet_delegate_withdraw_pay", [DELEGATE_NAME, PAYTO, THRESH])

    time.sleep(CHECK_INTERVAL)
  except:
    time.sleep(CHECK_INTERVAL)
