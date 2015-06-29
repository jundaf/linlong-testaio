ZRR = zmq-reqrep
ZPB = zmq-pubsub
INC = zmq-helper
LINK = ln -fs

all: rrserver psserver

rrserver:
	$(CC) -g -o $(ZRR)/rrserver -I$(INC) $(ZRR)/mtserver.c -lzmq -lpthread
	$(LINK) ../$(ZRR)/rrserver bin/rrserver

psserver:
	$(CC) -g -o $(ZPB)/psserver -I$(INC) $(ZPB)/wuserver.c -lzmq
	$(LINK) ../$(ZPB)/psserver bin/psserver

clean:
	$(RM) $(ZRR)/rrserver
	$(RM) $(ZPB)/psserver
