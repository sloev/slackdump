# Slack Dump

<a href="https://www.buymeacoffee.com/sloev" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-pink.png" alt="Buy Me A Coffee" height="51px" width="217px"></a>

[![Latest Version](https://img.shields.io/pypi/v/slackdump.svg)](https://pypi.python.org/pypi/slackdump)

Dump slack data via chrome browser, and do analytics on it

* [scraper.py](slackdump/scraper.py) scrapes a slack channel
* [chrome.py](slackdump/chrome.py) starts a temporary chrome process on osx


## Install

```bash
$ pip install slackdump
```

## Usage

Before running the `slackdump` command you need to

* be logged into slack in chrome
* close chrome completely

**for osx**

```bash
$ slackdump --ROOTURL=https://somewhere.slack.com/messages/66666666 > output.json
```

