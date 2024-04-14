docker compose -f ./pworker/dpworker.yml down send-node-status-to-queue
./pworker/write_zpool_status.sh & docker compose -f ./pworker/dpworker.yml up send-node-status-to-queue