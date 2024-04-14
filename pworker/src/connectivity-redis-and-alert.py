import redis
import time
import json

from pushover import send_pushover_notification
import sentry_sdk

sentry_sdk.init(
    dsn="https://40425deb8455f665b472e012d073c7f1@o127869.ingest.sentry.io/4506388932067328",
    traces_sample_rate=0.0,
)
redis_connection = redis.from_url("redis://redis:6379/0")

heartbeat = 30
print('sleep to allow first message to get to redis')
time.sleep(heartbeat * 2)
while True:
    connectivity_status = redis_connection.get("connectivity-status")
    should_alarm = False
    alarm_message = ''
    if connectivity_status:
        print(connectivity_status)
        connectivity_dict = json.loads(connectivity_status)
        how_long_has_passed  = int(time.time()) - connectivity_dict['timestamp']
        print(how_long_has_passed)
        if how_long_has_passed > 60:
            should_alarm = True
            alarm_message = 'Connectivity has not sent a status message in {} seconds'.format(how_long_has_passed)
        if connectivity_dict['is_in_error'] == True:
            should_alarm = True
            alarm_message = 'Connectivity status is not ok'
        if not connectivity_dict['connection_time'] or connectivity_dict['connection_time'] > 5:
            should_alarm = True
            alarm_message = 'connectivity connection time is too high'
    else:
        should_alarm = True
        alarm_message = "connectivity status is not in redis"
    if should_alarm:
        print('ALARM!!!!!!')
        print(alarm_message)
        send_pushover_notification(alarm_message)
        time.sleep(30)
    else:
        print( 'all ok in check connectivity redis')

    time.sleep(heartbeat)