## MOZI SNET Service

The purpose of this service is to enable SingularityNet users to run [MOSES](https://github.com/opencog/moses) analysis on their datasets

## Getting Started

### Prerequisites

 * [Python 3.6.5](https://www.python.org/downloads/release/python-365/)

### Installing

* Clone the git repo

```bash
    $ git clone https://github.com/Habush/mozi_service.git

    $ cd mozi_snet_service
```

* Install library dependencies

```bash
    $ pip install -r requirements.txt
```


### Configuration

* The following configuration can be overriden by changing their values in `mozi_service/config.py`

* SERVER_PORT: the port on which the example service will listen for incoming JSON-RPC calls over http

* DEBUG_MODE: whether the server should run in debug mode or not

### Running

#### Standalone

* Invoke the service directly

```bash
    $ python mozi_service
```


### Testing

* Run the *client.py* against a running mozi service

```bash
    $ python ./scripts/client.py
```

* After sending the JSONRPC request the server will respond with a url address on which you can poll the current status of the task