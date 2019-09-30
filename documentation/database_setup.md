### Installation of PostgreSQL database server (from Docker image)
#### 1. Prerequisites:
    - Operating System: Ubuntu
    - Python3
#### 2. Install Docker and Docker Compose
```bash
sudo apt install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo apt-key fingerprint 0EBFCD88
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
```
At this point an error could appear as follows:
```bash
 File "/usr/bin/add-apt-repository", line 11, in <module>
    from softwareproperties.SoftwareProperties import
SoftwareProperties, shortcut_handler
  File
"/usr/lib/python3/dist-packages/softwareproperties/SoftwareProperties.py",
line 28, in <module>
    import apt_pkg
ModuleNotFoundError: No module named 'apt_pkg'
```
This is a problem of conflicting Python versions. This can be fixed as follows:
```bash
cd /usr/lib/python3/dist-packages
la -la
```
In this directory, search for "apt_pkg.cpython-XX-x86_64-linux-gnu.so" where XX is the old python version, e.g. 36. Assuming old python version is 3.6 and the newest on system is 3.7, run the following command:
```bash
sudo ln -s apt_pkg.cpython-{36m,37m}-x86_64-linux-gnu.so
```
Finally, run `sudo apt-get install python3-apt --reinstall`.

Now we can continue with the installation of Docker:
```bash
sudo apt update
sudo apt install docker-ce
```
Next, install latest release of Docker Compose (1.25.0 as of time of writing) using following commands:
```bash
curl -L https://github.com/docker/compose/releases/download/1.25.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```
#### 3. Install PostgreSQL and PgAdmin from Docker images
The [docker-compose.yml](../code/thu/docker-compose.yml) file will be used to launch 2 inter-dependent containers for PostgreSQL server and PgAdmin server. Certain configurations for the server are contained in this file.
```bash
cd ../code/thu/
sudo docker-compose -d up
```
The PgAdmin server can now be accessed at https://pg.dev.iota.pw.
Login credentials are stored in [docker-compose.yml](../code/thu/docker-compose.yml):
- Email address: arpb@iota.dev
- Password: iota999

The PostgreSQL server can be managed by PgAdmin or by a CLI tool called **psql**, which is available inside the PostgreSQL container. To enter the container, look for its ID with the command
```bash
sudo docker ps
```
Go inside the container and run psql to connect to the database server using matching database name and username:
```bash
sudo docker exec -it <container-ID-here> bash 
psql -U arp_b -d arp_b
```
Using PgAdmin or psql to adjust the timezone and create 2 tables "HARDWARE" and "SENSOR_DATA" using following queries:
```sql
ALTER DATABASE arp_b SET timezone TO 'Europe/Berlin';

CREATE TABLE public."HARDWARE_STATUS"
(
    "hardwareID" integer NOT NULL,
    "address_index" integer NOT NULL,
    "session_address" text NOT NULL,
    "latitude" real NOT NULL,
    "longitude" real NOT NULL,
    PRIMARY KEY ("hardwareID")
);

CREATE TABLE public."SENSOR_DATA"
(
    "hardwareID" integer NOT NULL,
    "address" text,
    "latitude" real NOT NULL,
    "longitude" real NOT NULL,
    "temperature" real NOT NULL,
    "humidity" real NOT NULL,
    "timestamp" timestamp with time zone NOT NULL
);
```

The graphical view of the Tables (Schemas) is as follows:

<img src = "../media/db_new.png" width="720px">

#### 4. Install psycopg2 
**Psycopg2** package is required for the communication between any Python application, e.g. the [Python API server](API_python.md) and the PostgreSQL database server. Try `pip install psycopg2`. If not successful, try following steps:
```bash
sudo apt-get install libpq-dev
git clone https://github.com/psycopg/psycopg2
cd psycopg2
python setup.py build
sudo python setup.py install
```
