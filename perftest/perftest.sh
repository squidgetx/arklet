docker exec -it arklet_minter python ./manage.py --ark-count $1 --naan 1234 &&
./fetch_random_arks.sh > arks.csv && 
python performance_test.py arks.csv