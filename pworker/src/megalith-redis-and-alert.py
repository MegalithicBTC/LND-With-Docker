import redis
import time
import json
import sentry_sdk

sentry_sdk.init(
    dsn="https://40425deb8455f665b472e012d073c7f1@o127869.ingest.sentry.io/4506388932067328",
    traces_sample_rate=0.0,
)
from pushover import send_pushover_notification

redis_connection = redis.from_url("redis://redis:6379/0")

heartbeat = 10
print('sleep to allow first message to get to redis')
time.sleep(heartbeat * 2)
while True:
    megalith_status = redis_connection.get("megalith-status")
    should_alarm = False
    alarm_message = ''
    if megalith_status:
        #print(megalith_status)
        megalith_dict = json.loads(megalith_status)
        how_long_has_passed  = int(time.time()) - megalith_dict['timestamp']
        how_long_has_passed_since_chain_sync  = int(time.time()) - megalith_dict['last_confirmed_synced_to_chain']
        print('how long has passed since message from megalith', how_long_has_passed)
        print('how long has passed since synced to chain', how_long_has_passed_since_chain_sync)
        if how_long_has_passed > 60:
            should_alarm = True
            alarm_message = 'Megalith has not sent a status message in {} seconds'.format(how_long_has_passed)
        if how_long_has_passed_since_chain_sync > 120:
            should_alarm = True
            alarm_message = 'Megalith has not synced to chain in {} seconds'.format(how_long_has_passed_since_chain_sync)
        if megalith_dict['num_towers'] < 1:
            should_alarm = True
            alarm_message = 'Megalith has no towers'
        # if megalith_dict['synced_to_chain'] != True:
        #     should_alarm = True
        #     alarm_message = 'Megalith is not synced to the chain'
        if megalith_dict['synced_to_graph'] != True:
            should_alarm = True
            alarm_message = 'Megalith is not synced to the graph'
        print('here is the zpool status')
        print(megalith_dict['zpool_status'])
        if 'degraded' in megalith_dict['zpool_status'].lower():
            should_alarm = True
            alarm_message = 'Megalith zpool is degraded'
    else:
        should_alarm = True
        alarm_message = 'Megalith has not sent a status message yet'
    if should_alarm:
        print('ALARM!!!!!!')
        print(alarm_message)
        send_pushover_notification(alarm_message)
        time.sleep(30)
    else:
        print( 'all ok in check megalith redis')

    time.sleep(10)