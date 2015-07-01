//  PUB-SUB server
//  Binds PUB socket to tcp://*:5556

#include "zhelpers.h"

#define DATA_UNIT_SIZE 1024

int main (int argc, char **argv)
{
    size_t bufsize = DATA_UNIT_SIZE;
    int multiple = 1;

    if (argc >= 2) {
        multiple = atoi(argv[1]);
        bufsize *= multiple;
    }

    char *buffer = (char *) malloc(bufsize + 1);
    memset(buffer, 0, bufsize + 1);

    int i = 0;
    for (; i < bufsize; i++)
        buffer[i] = 'z';

    printf("Set buffer size to %ld\n", bufsize);
    // printf("%ld %s\n", strlen(buffer), buffer);

    //  Prepare our context and publisher
    void *context = zmq_ctx_new ();
    zmq_ctx_set(context, ZMQ_IO_THREADS, 5);

    void *publisher = zmq_socket (context, ZMQ_PUB);

    int hwm = 100;
    zmq_setsockopt(publisher, ZMQ_SNDHWM, &hwm, sizeof(int));

    int rc = zmq_bind (publisher, "tcp://*:5556");
    assert (rc == 0);

    while (1) {
        //  Send message to all subscribers
        s_send (publisher, buffer);
    }
    zmq_close (publisher);
    zmq_ctx_destroy (context);
    return 0;
}
