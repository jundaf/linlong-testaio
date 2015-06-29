# testaio - Load tests against ZeroMQ and Boost.Asio

rrserver and myclient.py is for testing REQ-REP pattern.

pbserver and wuclient.py is for testing PUB-SUB pattern.

## Usage: SERVER MESAGE_SIZE

SERVER is rrserver or pbserser.

MESAGE_SIZE is 1 for 1k, 8 for 8k and so on.

## Usage: CLIENT SERVER_NAME DATA_SIZE PROCESSES THREADS

CLIENT is mtclient.py or wuclient.py.

SERVER_NAME is the IP address of the server which is default to 'localhost'.

DATA_SIZE is the size of data to be received from server per connection.
It is optional and default to 100 (100M).

PROCESSES is the number of processes which is optional and default to 10.

THREADS is the number of threads per process which is optional and default to 10.
