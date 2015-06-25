ZRR = zmq-reqrep
ZPB = zmq-pubsub
INC = zmq-helper

all: rrserver

rrserver:
	$(CC) -g -o $(ZRR)/rrserver -I$(INC) $(ZRR)/mtserver.c -lzmq -lpthread

clean:
	$(RM) $(ZRR)/rrserver
