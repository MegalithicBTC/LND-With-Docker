This repository accompanies the tutorial at the [Megalithic Lightning Docs](https://docs.megalithic.me).

You can clone this repository and use it, but we recommend instead that you follow the full tutorial.

Each of the scripts in the root directory launches something useful.

Here's a rundown on the scripts, in the rough order you might want to run them: 


### MAIN LND NODE MACHINE

`start-tor.sh`: [Tor](https://docs.megalithic.me/set-up-a-lightning-node/setup-tor-with-docker) 

`start-bitcoin.sh`: [Bitcoin Core](https://docs.megalithic.me/set-up-a-lightning-node/setup-tor-with-docker) ([configuration](https://docs.megalithic.me/set-up-a-lightning-node/setup-bitcoin-core-with-docker#make-the-bitcoind-configuration-file))

`start-lnd.sh`: [LND](https://docs.megalithic.me/set-up-a-lightning-node/setup-lnd-with-docker) ([configuration](https://docs.megalithic.me/set-up-a-lightning-node/setup-lnd-with-docker#make-the-lndconf-file))

`start-watch-backups.sh`: [Python script for automatic SCB uploads to S3](https://docs.megalithic.me/set-up-a-lightning-node/disaster-recovery) ([configuration](https://docs.megalithic.me/set-up-a-lightning-node/disaster-recovery#save-information-about-your-aws-account-in-the-private-directory))







This repository uses bits of other repositories, including:

[tor-socks-proxy](https://github.com/PeterDaveHello/tor-socks-proxy/)

[docker-bitcoind](https://github.com/kylemanna/docker-bitcoind)

[lndg](https://github.com/cryptosharks131/lndg)

[lnd](https://github.com/lightningnetwork/lnd)

[Dual-LND-Wireguard-VPS](https://github.com/TrezorHannes/Dual-LND-Wireguard-VPS)

[wg-easy](https://github.com/wg-easy/wg-easy)