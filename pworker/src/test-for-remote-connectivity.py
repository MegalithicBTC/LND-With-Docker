import lightning_pb2 as ln, lightning_pb2_grpc as lnrpc
import grpc
import os
import codecs
import json
import pika
import time
import subprocess
import random

print('in test for remote connectivits')

def metadata_callback(context, callback):
    # for more info see grpc docs
    callback([('macaroon', macaroon)], None)

os.environ["GRPC_SSL_CIPHER_SUITES"] = 'HIGH+ECDSA'

cert = open(os.path.expanduser('/workspace/bound_lnd_folder/lnd-data/tls.cert'), 'rb').read()
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

CLEARNET_ADDRESS = "0322d0e43b3d92d30ed187f4e101a9a9605c3ee5fc9721e6dac3ce3d7732fbb13e@146.190.43.195:9735"
TOR_ADDRESS = "0322d0e43b3d92d30ed187f4e101a9a9605c3ee5fc9721e6dac3ce3d7732fbb13e@m563h7c5fdzq63d4znhkl2pbhskbf4meeybjgxmp7mkkp5j7osadgwad.onion:9735"
TOR_HOST = "m563h7c5fdzq63d4znhkl2pbhskbf4meeybjgxmp7mkkp5j7osadgwad.onion:9735"
PUB_KEY = "0322d0e43b3d92d30ed187f4e101a9a9605c3ee5fc9721e6dac3ce3d7732fbb13e"
CLEARNET_HOST = "164.92.106.32:9735"
def disconnect():
    try: 
        request = ln.DisconnectPeerRequest(
        pub_key=PUB_KEY,
        ) 
        print('disconnected')
        response = stub.DisconnectPeer(request)
        print(response)
    except: 
        print('disconnect failed')

def measure_connection_times(rabbit_channel):
    disconnect()
    print('sleep after disconnect')
    time.sleep(2)
    print('testing clearnet')
    print('clearnet addredss', CLEARNET_ADDRESS)
    #peer_params = {}
    # peer_params['addr'] = ,
    # peer_params['perm'] = False
    # peer_params['timeout'] = 60
    is_in_error = False
    error_message =""
    connection_time = None
    start_time = time.time()
    try: 
        request = ln.ConnectPeerRequest(
                addr=ln.LightningAddress(pubkey=PUB_KEY, host=CLEARNET_HOST),
                perm=False,
                timeout=30)
        print("here is the connect requst", request)
        response = stub.ConnectPeer(request)
        print('connected clearnet')
        print(response)
        elapsed_time = time.time() - start_time
        print("connected in:", elapsed_time)
        connection_time = elapsed_time
    except Exception as e:
        print('----exception---')
        print(e)
        error = str(e)  # Convert the exception to a string
        if not "already connected" in error:
            is_in_error = True
            error_message = error
    hash = {}
    hash['is_in_error'] = is_in_error
    hash['connection_time'] = connection_time
    hash['error_message'] = error_message
    print(hash)
    rabbit_channel.basic_publish(
            exchange="",
            routing_key='ln-connectivity-status',
            body=json.dumps(hash),
            properties=pika.BasicProperties(
                content_type="application/json", delivery_mode=1)
            )
    time.sleep(2)


    # disconnect()
    
    # print('testing tor')
    # request = ln.ConnectPeerRequest(
    # addr=ln.LightningAddress(pubkey=PUB_KEY, host=TOR_HOST),
    # perm=False,
    # timeout=60,
    # )
    # response = stub.ConnectPeer(request)
    # print('connected tor')
    # print(response)

rabbit_url = os.getenv("RABBITMQ_URL", "unk-url")
params = pika.URLParameters(rabbit_url + "?heartbeat=500")
connection = pika.BlockingConnection(params)  # Connect to CloudAMQP
channel = connection.channel()
channel.basic_qos(prefetch_count=1)
heartbeat = 30

print('sleep before test for remote connection')
time.sleep(10)
while True:
    measure_connection_times(channel)
    time.sleep(heartbeat)


    

