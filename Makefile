ZRR = zmq-reqrep
ZPB = zmq-pubsub
INC = zmq-helper

all: rrserver pbserver

rrserver:
	$(CC) -g -o $(ZRR)/rrserver -I$(INC) $(ZRR)/mtserver.c -lzmq -lpthread

pbserver:
	$(CC) -g -o $(ZPB)/pbserver -I$(INC) $(ZPB)/wuserver.c -lzmq

clean:
	$(RM) $(ZRR)/rrserver
	$(RM) $(ZPB)/pbserver
