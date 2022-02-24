# SSISPentryAnsvarServer

A simple server for handling and providing who is responsible for the pentries ("pentryansvar") 
in my school (Stockholm Science and Innovation School). (Code comments are in Swedish).
The server is built using [Python](https://python.org/) and [FastAPI](https://fastapi.tiangolo.com/)

### Installation

**Basic installation:**
* `git clone https://github.com/sotpotatis/SSISPentryAnsvarServer.git /srv/SSISPentryAnsvarServer` or `gh repo clone sotpotatis/SSISPentryAnsvarServer`:  **Note the directory part, it is important if you don't want to edit the services!**
* `pip install -r "requirements.json"`
* You might (read: should) also want to change the user agent in the `data_downloader.py` file to include your contact details.

**Scheduling server start and data retrieval:**
* cd `/srv/SSISPentryAnsvarServer`/`[cloned directory]`
* `chmod +x start_pentryansvar_server.sh`
* `mv services/pentryansvar_data_downloader.service /etc/systemd/system/pentryansvar_data_downloader.service`
* `mv services/pentryansvar_data_downloader.timer /etc/systemd/system/pentryansvar_data_downloader.timer`
* `mv services/pentryansvar_data_server.service /etc/systemd/system/pentryansvar_data_server.service`
* `systemctl status ssis_pentryansvar:`

**Dealing with various firewall problems:**
(Note: These are just example commands that I found worked.
They might not work for you.)

* `sudo ufw allow 80`/`sudo ufw allow http`
* `sudo iptables -I INPUT -p tcp -s 0.0.0.0/0 --dport 80 -j ACCEPT` (thanks, [Stack Overflow]())

### How to use

##### Note: Hosted version
A hosted version which is maintained by me is available at `https://pentryansvar.albins.website/`. New data should be updated every day at 01:00AM.

**Quick usage guide:**

* Visit `/api/pentryansvar` to get data for current week
* Add a parameter `?week_number` to the `/api/pentryansvar` to get data for a specific week
  (example `http://<Server URL>/api/pentryansvar/?week_number=8`)

**Example API response:**
```json
[{
"pentry_name": "Pentry 2",
"pentry_number": "2",
"responsible_class": "Te20A",
"responsible_persons": ["Person 1", "Person 2", "Person 3", "Person 4", "Person 5"]
},
{
"pentry_name": "Pentry 1",
"pentry_number": "1",
"responsible_class": "Te20B",
"responsible_persons": ["Person 6", "Person 7", "Person 8", "Person 9", "Person 10"]
}]
```

**Documentation:**

Documentation is available at `/docs` and `/redoc` on the server.
A spec is available at `/openapi.json` on the server.
