pip install -r requirements.txt --break-system-packages
sudo apt install postgresql -y
createdb Postgresql -U jawa
psql -U jawa -d Postgresql -a -f database_rh.psql