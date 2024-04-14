import lightning_pb2 as ln
import lightning_pb2_grpc as lnrpc
import grpc
import wtclient_pb2 as wtclientrpc
import wtclient_pb2_grpc as wtclientstub
import os
import codecs
import json
import pika
import time
import subprocess
import random

print('in up monitor')

def metadata_callback(context, callback):
    # for more info see grpc docs
    callback([('macaroon', macaroon)], None)

os.environ["GRPC_SSL_CIPHER_SUITES"] = 'HIGH+ECDSA'

cert = open(os.path.expanduser('/workspace/lightning/lnd/lnd-data/tls.cert'), 'rb').read()
# print(cert)
# creds = grpc.ssl_channel_credentials(cert)
# channel = grpc.secure_channel('127.0.0.1:10009', creds)
# stub = lnrpc.LightningStub(channel)
# print(stub)
with open(os.path.expanduser('/workspace/bound_lnd_folder/lnd-data/data/chain/bitcoin/mainnet/admin.macaroon'), 'rb') as f:
    macaroon_bytes = f.read()
    macaroon = codecs.encode(macaroon_bytes, 'hex')

# build ssl credentials using the cert the same as before
cert_creds = grpc.ssl_channel_credentials(cert)

# now build meta data credentials
auth_creds = grpc.metadata_call_credentials(metadata_callback)

# combine the cert credentials and the macaroon auth credentials
# such that every call is properly encrypted and authenticated
combined_creds = grpc.composite_channel_credentials(cert_creds, auth_creds)

# finally pass in the combined credentials when creating a channel
channel = grpc.secure_channel('localhost:10009', combined_creds)    
stub = lnrpc.LightningStub(channel)

wtclientstub = wtclientstub.WatchtowerClientStub(channel)



def report_current_status(rabbit_channel):
    response = stub.GetInfo(ln.GetInfoRequest())
    # print(response)
    hash = {}
    hash['synced_to_chain'] = response.synced_to_chain
    hash['synced_to_graph'] = response.synced_to_graph
    request = wtclientrpc.ListTowersRequest(
    include_sessions=True,
    exclude_exhausted_sessions=True,
    )
    response = wtclientstub.ListTowers(request)
    hash['num_towers'] = len(response.towers)
    file_path = '/workspace/lightning/zpool_status/pool_status.txt'
    with open(file_path, 'r') as file:
        # Read and print the file's content
        zpool_status_string = file.read()
    hash['zpool_status'] = zpool_status_string

    rabbit_channel.basic_publish(
            exchange="",
            routing_key='ln-megalith-status',
            body=json.dumps(hash),
            properties=pika.BasicProperties(
                content_type="application/json", delivery_mode=1)
            ),
    if random.random() <= 0.05:
        print('megalith status sent')
    

rabbit_url = os.getenv("RABBITMQ_URL", "unk-url")
params = pika.URLParameters(rabbit_url + "?heartbeat=500")
connection = pika.BlockingConnection(params)  # Connect to CloudAMQP
channel = connection.channel()
channel.basic_qos(prefetch_count=1)

heartbeat = 10
while True:
    report_current_status(channel)
    time.sleep(heartbeat)