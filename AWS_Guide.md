# AWS Guide

## Basics

[basile-rommes.com](http://basile-rommes.com)

https://aws.amazon.com/

Top right: Sign in to the console

After sign in, make sure to select on the top right

Stockholm (EU-North)

which will lead you to:

https://eu-north-1.console.aws.amazon.com/

EC2

This should show you the amount of running instances: e.g. Instances (1)



Select instance and click “connect” on the top right



Important:

```bash
sudo su # change to root

frontend = digital-resume-template-streamlit-Basile on Github (use git pull to update?)
```

Important files:

```bash
~/frontend/Dockerfile
```

\# This is only the (conda?) python environment for the frontend app, all the files that make the app run are alredy in frontend

```bash
~/frontend/digital-resume-template-streamlit-Basile 
```

##  Load balancer:

```bash
vim reverseproxy/nginx.conf
```

nginx is the software used to configure a load balancer for your webserver

![poxy_webserver.png](./md_images/poxy_webserver.png)

## Check if reverseproxy 

```bash
systemctl status
```

Important processes:

​      │ ├─reverseproxy.service

​      │ │ └─630767 sudo docker run -p 80:80 reverseproxy

…

​      │ ├─docker-3050bf8a265c42649bb6cb7f97b4a06f80a1644f502cc0f0eb86653bfb63e36e.scope

​      │ │ ├─630853 "nginx: master process /usr/sbin/nginx -g daemon off;"

​      │ │ └─630876 "nginx: worker process"

​      │ ├─docker-c25dc9a5db54f35f564c5e63afc3c7e5f4e99d03ee9aa94a7309e6e63eeffd54.scope

​      │ │ └─630502 /usr/local/bin/python3.12 /usr/local/bin/streamlit run --server.port=80 --server.address=0.0.0.0 app.py

Or check them individually:

```bash
systemctl status reverseproxy

systemctl status frontend # always shows (code=exited, status=203/EXEC) for some reason
```

## Guide: setting up an additional page on [basile-rommes.com](http://basile-rommes.com), without putting the code into digital-resume/app.py

```bash
git clone https://github.com/your-git-account/you-git-url.git project_name
```

$(~/ubuntu/reverseproxy) OR ubuntu@ip-172-31-37-139:~/basile-rommes/nginx$
```bash
vim nginx.conf or sudo nano default.conf 
```

-> add upstream project_name {…}

-> add location /project_name {…}

$(~/ubuntu/reverseproxy) OR ubuntu@ip-172-31-37-139:~/basile-rommes/nginx$

```bash
docker build -t reverseproxy . --no-cache OR docker build -t nginx . --no-cache
```

\# stop old running docker processes:

```bash
docker ps
```

root@ip-172-31-37-139:/home/ubuntu/reverseproxy# docker ps

CONTAINER ID  IMAGE     COMMAND         CREATED   STATUS   PORTS                  NAMES

3050bf8a265c  b3880ad7dba6  "/docker-entrypoint.…"  6 days ago  Up 6 days  0.0.0.0:80->80/tcp, :::80->80/tcp    ecstatic_chatelet

c25dc9a5db54  frontend    "streamlit run --ser…"  6 days ago  Up 6 days  0.0.0.0:3000->80/tcp, :::3000->80/tcp  tender_grothendieck



\# stops all running docker processes

```bash
docker stop $(docker ps -q)
```

```bash
docker ps
```

We can see that reverseproxy is immediatly restarted because of daemon

```bash
systemctl status reverseproxy
```

```bash
cd ../NEAR_data_request

vim Dockerfile # add correct port, e.g. 3001

docker build -t project_name . --no-cache
```

\# threw error for me becuase I was out of space

29.27 ERROR: Could not install packages due to an OSError: [Errno 28] No space left on device: '/usr/local/lib/python3.12/site-packages/pandas/core/internals'



\# to clean:

```bash
docker system df

docker system prune -af
```


\# to increase EC2 storage volume:

https://stackoverflow.com/questions/66773832/increase-ec2-disk-storage-without-losing-any-data

-> backup EC2 instance via GUI

-> increase volume via GUI

\# ssh into your instance 

```bash
df -h -> will tell you the volume size
```

```bash
lsblk -> display information about the block devices attached to your instance

sudo growpart /dev/nvme0n1 1 # resize the first partition on the device nvme0n1.

df -h -> to verify the size again (no change should be noticable)
```

\# Use df -T / | awk 'NR==2 {print $2}' to get the file system type. Then use resize2fs for ext4 and xfs_growfs for xfs.

```bash
sudo resize2fs /dev/nvme0n1p1 # extends the filesystem to fill the newly expanded partition space

df -h -> to verify the size again (change should be noticable)
```


\# Finally we can build the docker image as now there should be enough space:

```bash
docker build -t near_data_request . --no-cache # -t gives a nametag, which is referenced in the docker run command! Base of the docker image is the Dockerfile, so make sure you are in the correct folder!
```


\# source: https://medium.com/@sstarr1879/how-to-build-and-deploy-multiple-streamlit-apps-on-aws-ec2-with-nginx-1424fef8737f

Test Everything Locally First! Run the following commands to run the containers you just built and make sure everything launches correctly.

```bash
docker network create streamlit-network
```

```bash
docker run --name frontend --network my-network -p 3000:80 frontend

docker run -d --name near-data-request --network my-network -p 3001:3001 near-data-request
```

```bash
docker run -d --name sarahs_app --network streamlit-network -p 8501:8501 sarahs_app # -d : run container in background and print container id

docker run -d --name justins_app --network streamlit-network -p 8502:8502 justins_app

docker run -d --name nginx --network streamlit-network -p 80:80 nginx_proxy

```



## When one of the apps is not running

```bash
docker ps -a # see all containrrs

docker -ps # see running containers
```

 then:

```bash
docker start nginx
```
doesn’t work (no error but it doesn’t start back up if you check with docker ps)



Find the container ID or name

```bash
docker ps | grep nginx
```


Stop the container then remove the stopped container using its ID or name and flag -f 
```bash
docker rm -f <container_id_or_name>
```

```bash
docker run -dit --name nginx --network basile-rommes-network -p 80:80 nginx_proxy
# (instead of: docker run -d -p 80:80 nginx/dockerfile)
# docker build -t nginx/dockerfile nginx/
```


# Situation: I changed only digital-resume/app.py. Here is how I implement the changes on the server

```bash

sudo su

mv digital-resume digital-resume-old

git clone https://github.com/romba050/digital-resume-template-streamlit-Basile digital-resume
```
```bash
# or rename it after cloning it with:
mv digital-resume-template-streamlit-Basile digital-resume # keep this name because it is used in a lot of documentation ,docker.sh, etc,...
```

```bash
cp digital-resume-old/Dockerfile digital-resume/

(rm -rf digital-resume-old # maybe wait until you are sure you don't need it anymore!)
```

```bash
docker stop digital-resume
docker rm digital-resume
```

```bash
# docker build -t digital-resume .
```

```bash
# docker run -d --name digital-resume digital-resume
```


```bash
docker build --progress=plain -t digital-resume ./digital-resume

docker run -dit --name digital-resume --network basile-rommes-network -p 8501:8501 digital-resume

docker run -dit --name nginx --network basile-rommes-network -p 80:80 nginx_proxy
```



```bash
docker ps

docker run -dit --name digital-resume --network basile-rommes-network -p 8501:8501 digital-resume # fails because there is already a docker by that name

docker rm -f digital-resume # from now on website is no longer online?

docker run -dit --name digital-resume --network basile-rommes-network -p 8501:8501 digital-resume
```


FAIL - got Bad gateway on website for a short while, then it restarted nginx and displayed the old website somehow, even though I deleted the old docker and the files it should have used?

Maybe I deleted the container but not the image? 

YOU FORGOT TO COPY NEW DOCKERFILE!

```bash
cp digital-resume-old/Dockerfile digital-resume
```
