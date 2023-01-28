# Example - Bash

*NOTE: I did not test this script completely*

```bash
#!/usr/bin/env bash

TGT_IP=$1
TGT_SSH_PORT=$2
TGT_SSH_USER=$3

# parameter/argument validation:
#   one may want to use 'getopts' to parse parameters: https://www.computerhope.com/unix/bash/getopts.htm
#   custom validation should be added here to make sure wrong parameters won't break the whole processing

# constants
CNF_SRC='./files'
CNF_TMP='/tmp/1234/'
PATH_WEB='/var/www/app1'
UPDATE_SVC='app1-update'
DB='app1'

set -euo pipefail  # see: https://gist.github.com/mohanpedala/1e2ff5661761d3abd0385e8223e16425
# add -x for debugging

function MSG () {
  msg="$1"
  time=$(date +"%Y-%m-%d %T")
  echo ''
  echo "$time | $msg"
}

# changing working directory so relative source-paths are correct
cd "$(dirname "$0")"

# shortcut for executing a command on the target system; will ask for sudo privileges every time
SSH="ssh $TGT_SSH_USER@$TGT_IP -p $TGT_SSH_PORT -t"
# shortcut for copying files to the target system
SCP_ARG="-P $TGT_SSH_PORT $TGT_SSH_USER@$TGT_IP:/$CNF_TMP"

function COPY () {
  file="$1"
  target="$2"
  mode="$3"
  owner="$4"
  scp -r "$file" $SCP_ARG
  # copy tmp to target-dir, change file privileges
  $SSH "sudo mv $CNF_TMP/$file $target && sudo chmod $mode $target && sudo chown $owner $target"
}

MSG '### PREREQUISITES ###'

MSG 'Creating local tmp directory'
mkdir -p "$CNF_TMP"

MSG 'Creating remote tmp directory'
$SSH "mkdir -p $CNF_TMP"

MSG '### INSTALLING ###'
MSG 'Installing packages'
$SSH 'sudo apt install mariadb-client mariadb-server apache2 wget'

MSG 'Enabling services'
$SSH 'sudo systemctl enable apache2.service mariadb.service'
MSG 'Starting services'
$SSH 'sudo systemctl start apache2.service mariadb.service'

MSG '### CONFIGURING ###'

MSG 'Configuring MariaDB'
cp "$CNF_SRC/mariadb.cnf" "$CNF_TMP/mariadb.cnf"
# INSERT HERE: making changes to the TMP config file using 'sed'
COPY "$CNF_TMP/mariadb.cnf" '/etc/mariadb/mariadb.cnf' '640' 'root:mysql'
MSG 'Reloading MariaDB'
$SSH 'sudo systemctl reload mariadb.service'

MSG 'Checking if Database is initialized'
tables=$(mysql -s -e "SELECT count(*) FROM information_schema.TABLES WHERE (TABLE_SCHEMA = '$DB');" | tail -n 1)
if [[ "$tables" == "0" ]]
then
  MSG 'Importing Database'
  COPY "$CNF_SRC/db.sql" '/tmp/db.sql' '640' 'root:root'
  $SSH 'sudo mysql < /tmp/db.sql'
fi

MSG 'Creating MariaDB Users'
$SSH "sudo mysql -e \"CREATE USER 'user1'@'localhost' IDENTIFIED BY 'pwd1'; CREATE USER 'user2'@'localhost' IDENTIFIED BY 'pwd2'; GRANT ALL PRIVILEGES ON $DB.* TO 'user1'@'localhost';  GRANT SELECT ON $DB.* TO 'user2'@'localhost'; FLUSH PRIVILEGES;\""

MSG 'Removing Apache2 default sites'
$SSH 'sudo rm /etc/apache2/sites-enabled/000-default.conf /etc/apache2/sites-enabled/default-ssl.conf'

MSG 'Copying web application data'
# NOTE: files might be set to mode 644
$SSH "sudo mkdir -p $PATH_WEB"
COPY "$CNF_SRC/app1/" "$PATH_WEB/" '755' 'root:www-data'
$SSH "sudo chown -R root:www-data $PATH_WEB/ && sudo chmod -R 755 $PATH_WEB/"

MSG 'Configuring Apache2'
cp "$CNF_SRC/apache_site.conf" "$CNF_TMP/apache_site.conf"
# INSERT HERE: making changes to the TMP config file using 'sed'
COPY "$CNF_TMP/apache_site.conf" '/etc/apache2/sites-enabled/site.conf' '640' 'root:www-data'
$SSH 'sudo a2enmod ssl headers rewrite http2'
MSG 'Reloading Apache'
$SSH 'sudo systemctl reload apache2.service'

MSG 'Adding systemd timer to update some data'
COPY "$CNF_SRC/systemd.service" "/etc/systemd/system/$UPDATE_SVC.service" '755' 'root:root'
COPY "$CNF_SRC/systemd.timer" "/etc/systemd/system/$UPDATE_SVC.timer" '755' 'root:root'
$SSH "sudo systemctl enable $UPDATE_SVC.timer && sudo systemctl start UPDATE_SVC.timer"

MSG '### CLEANUP ###'

MSG 'Removing local tmp directory'
rm -rf "$CNF_TMP"

MSG 'Removing remote tmp directory'
$SSH "rm -rf $CNF_TMP"
```
