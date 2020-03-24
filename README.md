# Slack Dump

[![Latest Version](https://img.shields.io/pypi/v/slackdump.svg)](https://pypi.python.org/pypi/slackdump)

Dump slack data via chrome browser, and do analytics on it

* [scraper.py](slackdump/scraper.py) scrapes a slack channel
* [chrome.py](slackdump/chrome.py) starts a temporary chrome process on osx


## Install

```bash
$ pip install slackdump
```

## Usage

```bash
$ slackdump --ROOTURL=https://somewhere.slack.com/messages/66666666 > output.json
```

