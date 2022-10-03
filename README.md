# Thicc - Your Non-Proxy-Aware Thick App Testing Friend
## What is this project? 

Thicc is a useful Windows tool to aid non-proxy-aware thick application assessments. 
It will find the applications external IP addresses and then use them to generate BurpSuite settings to avoid a lot of messing around.
This project is maintained by [TurvSec](https://twitter.com/TurvSec)

[![Follow on Twitter](https://img.shields.io/twitter/follow/TurvSec.svg?logo=twitter)](https://twitter.com/TurvSec)

## Why have you made this? 

Because when testing Thick applications on Windows that are not proxy aware, it's painful. Typically you will have to use an outdated proxy injection tool or proxy your whole Windows system and it's not ideal. Using this tool, you still do proxy your whole Windows system. But the specific external IPs for the thick application are found and then regex is created. This regex is then used within BurpSuite to ensure it isn't actually your whole system that get's intercepted by Burp Suite.

## How does it look? 

<img src="https://github.com/MrTurvey/Thicc/blob/main/Screenshot.png">

- - -

## Installation

```
git clone https://github.com/MrTurvey/Thicc.git
cd Thicc
pip3 install -r requirements.txt
python thicc.py
```

## Usage
```
Find the thick application external IPs by finding it's process name + magic.
python thicc.py -a <application process to match>
python thicc.py -a Spotify
python thicc.py -a Spot
```
```
Enable the system proxy
python thicc.py -Pe <BurpIP:Port>
python thicc.py -Pe 127.0.0.1:8080
```
```
Disable the system proxy
python thicc.py -Pd
```