//  Multithreaded REQ-REP server

#include "zhelpers.h"
#include <pthread.h>
#include <unistd.h>

#define DATA_UNIT_SIZE 1024

static char *buffer = NULL;

static void *
worker_routine (void *context) {
    //  Socket to talk to dispatcher
    void *receiver = zmq_socket (context, ZMQ_REP);
    zmq_connect (receiver, "inproc://workers");

    while (1) {
        char *string = s_recv (receiver);
        // printf ("Received request: [%s]\n", string);
        free (string);
        //  Send reply back to client
        s_send (receiver, buffer);
    }
    zmq_close (receiver);
    return NULL;
}

int main (int argc, char **argv)
{
    size_t bufsize = DATA_UNIT_SIZE;
    int multiple = 1;

    if (argc >= 2) {
        multiple = atoi(argv[1]);
        bufsize *= multiple;
    }

    buffer = (char *) malloc(bufsize + 1);
    memset(buffer, 0, bufsize + 1);

    int i = 0;
    for (; i < bufsize; i++)
        buffer[i] = 'z';

    printf("Set buffer size to %ld\n", bufsize);
    // printf("%ld %s\n", strlen(buffer), buffer);

    void *context = zmq_ctx_new ();

    //  Socket to talk to clients
    void *clients = zmq_socket (context, ZMQ_ROUTER);
    zmq_bind (clients, "tcp://*:5555");

    //  Socket to talk to workers
    void *workers = zmq_socket (context, ZMQ_DEALER);
    zmq_bind (workers, "inproc://workers");

    //  Launch pool of worker threads
    int thread_nbr;
    for (thread_nbr = 0; thread_nbr < 5; thread_nbr++) {
        pthread_t worker;
        pthread_create (&worker, NULL, worker_routine, context);
    }
    //  Connect work threads to client threads via a queue proxy
    zmq_proxy (clients, workers, NULL);

    //  We never get here, but clean up anyhow
    zmq_close (clients);
    zmq_close (workers);
    zmq_ctx_destroy (context);
    return 0;
}
