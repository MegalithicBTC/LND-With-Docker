docker compose -f ./pworker/dpworker.yml down upmonitor
./pworker/write_zpool_status.sh & docker compose -f ./pworker/dren.yml up upmonitor