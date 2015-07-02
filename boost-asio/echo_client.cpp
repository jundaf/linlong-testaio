//
// blocking_tcp_echo_client.cpp
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//
// Copyright (c) 2003-2015 Christopher M. Kohlhoff (chris at kohlhoff dot com)
//
// Distributed under the Boost Software License, Version 1.0. (See accompanying
// file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
//

#include <cstdlib>
#include <cstring>
#include <iostream>
#include <boost/asio.hpp>
#include <boost/bind.hpp>

using boost::asio::ip::tcp;

enum { max_length = 1024 };

class session
{
public:
    session(boost::asio::io_service& io_service,
            const char *host, const char *port)
        : socket_(io_service), total_transferred(0)
  {
      data_[0] = 'a';
      data_[1] = '\0';
      connect(io_service, host, port);
  }

  void start()
  {
      boost::asio::async_write(socket_,
        boost::asio::buffer(data_, 1),
        boost::bind(&session::handle_write, this,
                    boost::asio::placeholders::error));
  }

    size_t transferred()
        {
            return total_transferred;
        }

private:
  void handle_read(const boost::system::error_code& error,
      size_t bytes_transferred)
  {
    if (!error)
    {
        total_transferred += bytes_transferred;
        if (total_transferred >= max_length) {
            std::cout << total_transferred << std::endl;
            delete this;
            return;
        }
      boost::asio::async_write(socket_,
          boost::asio::buffer(data_, 1),
          boost::bind(&session::handle_write, this,
            boost::asio::placeholders::error));
    }
    else
    {
      delete this;
    }
  }

  void handle_write(const boost::system::error_code& error)
  {
    if (!error)
    {
      socket_.async_read_some(boost::asio::buffer(data_, max_length),
          boost::bind(&session::handle_read, this,
            boost::asio::placeholders::error,
            boost::asio::placeholders::bytes_transferred));
    }
    else
    {
      delete this;
    }
  }

    void connect(boost::asio::io_service& io_service,
                 const char *host, const char *port)
        {
            tcp::resolver resolver(io_service);
            tcp::resolver::query query(tcp::v4(), host, port);
            tcp::resolver::iterator iterator = resolver.resolve(query);

            boost::asio::connect(socket_, iterator);
        }

  tcp::socket socket_;
  enum { max_length = 1024 };
  char data_[max_length];
    size_t total_transferred;
};


int main(int argc, char* argv[])
{
  try
  {
    if (argc != 3)
    {
      std::cerr << "Usage: blocking_tcp_echo_client <host> <port>\n";
      return 1;
    }

    boost::asio::io_service io_service;

    session *ps = new session(io_service, argv[1], argv[2]);
    ps->start();

    io_service.run();

    // tcp::resolver resolver(io_service);
    // tcp::resolver::query query(tcp::v4(), argv[1], argv[2]);
    // tcp::resolver::iterator iterator = resolver.resolve(query);

    // tcp::socket s(io_service);
    // boost::asio::connect(s, iterator);

    // using namespace std; // For strlen.
    // std::cout << "Enter message: ";
    // char request[max_length];
    // std::cin.getline(request, max_length);
    // size_t request_length = strlen(request);
    // boost::asio::write(s, boost::asio::buffer(request, request_length));

    // char reply[max_length];
    // size_t reply_length = boost::asio::read(s,
    //     boost::asio::buffer(reply, request_length));
    // std::cout << "Reply is: ";
    // std::cout.write(reply, reply_length);
    // std::cout << "\n";
  }
  catch (std::exception& e)
  {
    std::cerr << "Exception: " << e.what() << "\n";
  }

  return 0;
}
