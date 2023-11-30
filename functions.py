from dateutil.parser import parse
from arrow import Arrow
from db import *
from yapi import *


'''
def update_if_changed(customer_id) - апдейтит записи в events если 
  есть изменения. Если update был, то возращает True, иначе - False

'''

# ldrslvhwyabcvjio


def update_if_changed(customer_id: int, email: str, username: str, password: str):
  delete_timeout_events()

  ya_events = get_event_yandex_info(email, username, password)
  db_events = get_events(customer_id)

  if len(ya_events) < len(db_events):
    for db_event in db_events:
      is_in = False
      for ya_event in ya_events:
        if ya_event['uid'] == db_event['event_id']:
          is_in = True
          if ya_event['last_modified'] != db_event['event_last_modified']:
            update_event(
              ya_event['uid'], 
              ya_event['event'],
              ya_event['start'],
              ya_event['end'],
              ya_event['last_modified']
            )
          break
      if not is_in:
        delete_event(db_event['event_id'])
    return True

  if len(ya_events) > len(db_events):
    for ya_event in ya_events:
      is_in = False
      for db_event in db_events:
        if ya_event['uid'] == db_event['event_id']:
          is_in = True
          if ya_event['last_modified'] != db_event['event_last_modified']:
            update_event(
              ya_event['uid'], 
              ya_event['event'],
              ya_event['start'],
              ya_event['end'],
              ya_event['last_modified']
            )
          break
      if not is_in:
        add_info('event', EVENT_COLS, [
          ya_event['uid'],
          customer_id,
          ya_event['event'],
          ya_event['start'],
          ya_event['end'],
          ya_event['last_modified']
        ])
    return True


  flag = False

  for ya_event in ya_events:
    for db_event in db_events:
      if ya_event['uid'] == db_event['event_id']:
        if ya_event['last_modified'] != db_event['event_last_modified']:
          update_event(
              ya_event['uid'], 
              ya_event['event'],
              ya_event['start'],
              ya_event['end'],
              ya_event['last_modified']
            )
          flag = True
        break

  return flag


# print(update_if_changed(1, email, username, password))