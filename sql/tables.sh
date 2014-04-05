mysql --defaults-file=~/.my.halfak.cnf -h db1047.eqiad.wmnet halfak -e "SHOW CREATE TABLE nov13_creation";
mysql --defaults-file=~/.my.halfak.cnf -h db1047.eqiad.wmnet halfak -e "SELECT * FROM nov13_creation" > ../datasets/nov13_creation.tsv;

mysql --defaults-file=~/.my.halfak.cnf -h db1047.eqiad.wmnet halfak -e "SHOW CREATE TABLE nov13_user_stats";
mysql --defaults-file=~/.my.halfak.cnf -h db1047.eqiad.wmnet halfak -e "SELECT * FROM nov13_user_stats" > ../datasets/nov13_user_stats.tsv;

mysql --defaults-file=~/.my.halfak.cnf -h db1047.eqiad.wmnet halfak -e "SHOW CREATE TABLE nov13_page_origin";
mysql --defaults-file=~/.my.halfak.cnf -h db1047.eqiad.wmnet halfak -e "SELECT * FROM nov13_page_origin" > ../datasets/nov13_page_origin.tsv;


