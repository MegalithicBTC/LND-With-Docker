docker compose -f ./pworker/dren.yml down

./pworker/write_zpool_status.sh & docker compose -f ./pworker/dren.yml up