This repository accompanies the tutorial at the [Megalithic Lightning Docs](https://docs.megalithic.me).

Following this tutorial will help you run LND, Tor, and Bitcoin Core, and then additionally (if you want), helps you set up a Watchtower, a Clearnet IP, and various scripts you can constantly run to ensure your node is always online and reachable.

You can clone this repository and use it, but we recommend instead that you follow the full tutorial, which presents each Docker container in order and helps you configure each Docker process.

Each of the scripts in the root directory launches something useful.

Currently to run everything, you need four (4) different machines, typically two (2) local computers with at least 1 TB of storage, which will be running LND and an LND Watchtower, and then (2) two more machines, typically two different VPS instances. 

You might only want to run the one (1) MAIN LND NODE MACHINE...  that's why we recommend you do the [full tutorial](https://docs.megalithic.me/category/should-i-run-a-lightning-node), as that will help you decide if you need to add the other machines, too.

Here's a rundown on the scripts, in the rough order you might want to run them.


### MAIN LND NODE MACHINE (REQUIRED)

`start-tor.sh`: [Tor](https://docs.megalithic.me/set-up-a-lightning-node/setup-tor-with-docker) 

`start-bitcoin.sh`: [Bitcoin Core](https://docs.megalithic.me/set-up-a-lightning-node/setup-tor-with-docker) ([configuration](https://docs.megalithic.me/set-up-a-lightning-node/setup-bitcoin-core-with-docker#make-the-bitcoind-configuration-file))

`start-lnd.sh`: [LND](https://docs.megalithic.me/set-up-a-lightning-node/setup-lnd-with-docker) ([configuration](https://docs.megalithic.me/set-up-a-lightning-node/setup-lnd-with-docker#make-the-lndconf-file))

`exec-lncli`: [Executes CLI in running LND container](https://docs.megalithic.me/set-up-a-lightning-node/setup-lnd-with-docker#lets-meet-our-script-which-provides-cli-access-in-the-running-lnd-container)


 (OPTIONAL SCRIPTS TO RUN ON THIS MACHINE)

`start-watch-backups.sh`: [Python script for automatic SCB uploads to S3](https://docs.megalithic.me/set-up-a-lightning-node/disaster-recovery) ([configuration](https://docs.megalithic.me/set-up-a-lightning-node/disaster-recovery#save-information-about-your-aws-account-in-the-private-directory))

`start-send-node-status.sh`: [Constantly send node status messages to a RabbitMQ Queue](https://docs.megalithic.me/the-gentlemans-guide-to-routing-nodes/alarms_rabbitmq_redis) (configuration requires these directions)

### WATCHTOWER MACHINE (OPTIONAL)

`start-tor.sh`: [Tor](https://docs.megalithic.me/set-up-a-lightning-node/setup-tor-with-docker) 

`start-bitcoin.sh`: [Bitcoin Core](https://docs.megalithic.me/set-up-a-lightning-node/setup-tor-with-docker) ([configuration](https://docs.megalithic.me/set-up-a-lightning-node/setup-bitcoin-core-with-docker#make-the-bitcoind-configuration-file))
`start-watchtower.sh`: [LND Watchtower](https://docs.megalithic.me/set-up-a-lightning-node/connect-to-a-watchtower#set-up-a-watchtower-the-hard-way) (configuration requires these directions)

`start-remote-connectivity.sh`: [Constantly test LND for external connectivity](https://docs.megalithic.me/the-gentlemans-guide-to-routing-nodes/alarms_rabbitmq_redis) (configuration requires these directions)


### MACHINE WITH STATIC IP, TO RUN WIREGUARD VPN  (OPTIONAL)
`start-wireguard-on-vps.sh`: [Wireguard VPN](https://docs.megalithic.me/the-gentlemans-guide-to-routing-nodes/gentlemans-networking-stack) (configuration requires these directions)

### QUEUE LISTENER MACHINE  (OPTIONAL)

`start-queue-listeners.sh`: [Listen to RabbitMQ queue and trigger alarms when necessary](https://docs.megalithic.me/the-gentlemans-guide-to-routing-nodes/alarms_rabbitmq_redis) (configuration requires these directions)

---









This repository uses bits of other repositories, including:

[tor-socks-proxy](https://github.com/PeterDaveHello/tor-socks-proxy/)

[docker-bitcoind](https://github.com/kylemanna/docker-bitcoind)

[lndg](https://github.com/cryptosharks131/lndg)

[lnd](https://github.com/lightningnetwork/lnd)

[Dual-LND-Wireguard-VPS](https://github.com/TrezorHannes/Dual-LND-Wireguard-VPS)

[wg-easy](https://github.com/wg-easy/wg-easy)