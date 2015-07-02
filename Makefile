ZRR = zmq-reqrep
ZPB = zmq-pubsub
INC = zmq-helper

ASIO = boost-asio
LINK = ln -fs

all: echo_server echo_client rrserver psserver

echo_server: $(ASIO)/echo_server.cpp
	$(CXX) -g -o bin/echo_server $(ASIO)/echo_server.cpp -lboost_system

echo_client: $(ASIO)/echo_client.cpp
	$(CXX) -g -o bin/echo_client $(ASIO)/echo_client.cpp -lboost_system -lpthread

rrserver: $(ZRR)/mtserver.c
	$(CC) -g -o bin/rrserver -I$(INC) $(ZRR)/mtserver.c -lzmq -lpthread

psserver: $(ZPB)/wuserver.c
	$(CC) -g -o bin/psserver -I$(INC) $(ZPB)/wuserver.c -lzmq

clean:
	$(RM) bin/echo*
	$(RM) bin/*server
