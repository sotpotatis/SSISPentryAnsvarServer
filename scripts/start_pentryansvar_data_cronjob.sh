#Installs a crontab for starting the pentryansvar data downloader every day at 01:00
echo "Installing pentryansvar data crontab..."
cd /SSISPentryAnsvarServer || exit 1
cp cronjobs/cronjobs /etc/cron.d/pentryansvar.cron
chmod 0644 /etc/cron.d/pentryansvar.cron
touch /var/log/cron.log #Create cron log

echo "Starting cronjob..."
cron -f