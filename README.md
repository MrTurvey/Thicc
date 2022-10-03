# Thicc - Your Non-Proxy-Aware Thick App Testing Friend
## What is this project? 

Thicc is a useful Windows tool to aid non-proxy-aware thick application assessments. 
It will find the applications external IP addresses and then use them to generate BurpSuite settings to avoid a lot of messing around.

This project is maintained by [TurvSec](https://twitter.com/TurvSec)

[![Follow on Twitter](https://img.shields.io/twitter/follow/TurvSec.svg?logo=twitter)](https://twitter.com/TurvSec)

## Why have you made this? 

Because testing Non-Proxy-Aware Thick applications on Windows is painful.

Have you tried setting your system proxy to BurpSuite? It's a mess of certificate errors for websites and applications.

Instead, why not use this tool to generate the Burp Suite settings you need to ensure none of that happens.

## How does it look? 

Not great, but it does the job.

<img src="https://github.com/MrTurvey/Thicc/blob/main/Screenshot.png">

- - -

## Installation
Simple, git clone Thicc, install the dependencies and you're away
```
git clone https://github.com/MrTurvey/Thicc.git
cd Thicc
pip3 install -r requirements.txt
python thicc.py
```

## Usage
Find the thick application external IPs by finding it's process name + magic.
```
python thicc.py -a <application process to match>
python thicc.py -a Spotify
python thicc.py -a Spot
```
Enable the system proxy
```
python thicc.py -Pe <BurpIP:Port>
python thicc.py -Pe 127.0.0.1:8080
```
Disable the system proxy
```
python thicc.py -Pd
```