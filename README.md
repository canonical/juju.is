# juju.is

[![CircleCI build status](https://circleci.com/gh/canonical-web-and-design/juju.is.svg?style=shield)](https://circleci.com/gh/canonical-web-and-design/juju.is)
[![Code coverage](https://codecov.io/gh/canonical-web-and-design/juju.is/branch/master/graph/badge.svg)](https://codecov.io/gh/canonical-web-and-design/juju.is)

This is the repo for the [Juju website](https://juju.is).

## Usage

Install [the `dotrun` snap](https://github.com/canonical-web-and-design/dotrun/#installation), then run:

```bash
dotrun
```

And click on the server link that appears in the server logs.

### Run locally with search functionality

If you wish to run the site locally with search enabled, you'll need to pass a key. This key can be obtained [from the Google Cloud Platform console](https://console.cloud.google.com/apis/credentials?project=ubuntu-search-1530889417216&pli=1), or by contacting #webteam on IRC if you don't have access.

```bash
dotrun --env SEARCH_API_KEY={your_key_here}
```

# Deploy
You can find the deployment config in the deploy folder.
