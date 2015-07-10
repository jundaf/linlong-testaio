//
// echo_client.cpp
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//
// Copyright (c) 2003-2015 Christopher M. Kohlhoff (chris at kohlhoff dot com)
// Copyright (c) 2015 Junda Feng (jundaf@139.com)
//
// Distributed under the Boost Software License, Version 1.0. (See accompanying
// file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
//

#include <cstdlib>
#include <cstring>
#include <iostream>
#include <vector>
#include <boost/asio.hpp>
#include <boost/bind.hpp>
#include <boost/chrono.hpp>

using boost::asio::ip::tcp;
using namespace boost::chrono;

enum { data_required = 1024 * 1024 * 100 };

class client_session
{
public:
    client_session(boost::asio::io_service& io_service,
            const char *host, const char *port)
        : socket_(io_service),
          total_transferred_(0),
          request_("hello")
    {
        tcp::resolver resolver(io_service);
        tcp::resolver::query query(tcp::v4(), host, port);
        tcp::resolver::iterator iterator = resolver.resolve(query);

        boost::asio::async_connect(socket_, iterator,
            boost::bind(&client_session::handle_connect, this,
                        boost::asio::placeholders::error,
                        boost::asio::placeholders::iterator));
    }

private:
    void handle_read(const boost::system::error_code& error,
                     size_t bytes_transferred)
    {
        if (!error)
        {
            total_transferred_ += bytes_transferred;
            if (total_transferred_ >= data_required)
            {
                // std::cout << total_transferred_ << std::endl;
                return;
            }
            send_request();
        }
        else
        {
            std::cerr << error.value() << std::endl;
            std::cerr << error.category().name() << std::endl;
        }
    }

    void handle_write(const boost::system::error_code& error)
    {
        if (!error)
        {
            socket_.async_read_some(
                boost::asio::buffer(data_, max_length),
                boost::bind(&client_session::handle_read, this,
                            boost::asio::placeholders::error,
                            boost::asio::placeholders::bytes_transferred));
        }
    }

    void handle_connect(const boost::system::error_code& error,
                        tcp::resolver::iterator iterator)
    {
        if (!error)
        {
            send_request();
        }
    }

    void send_request()
    {
        boost::asio::async_write(socket_,
            boost::asio::buffer(request_),
            boost::bind(&client_session::handle_write, this,
                        boost::asio::placeholders::error));
    }

    tcp::socket socket_;
    enum { max_length = 1024 };
    char data_[max_length];
    size_t total_transferred_;
    std::string request_;
};


int main(int argc, char* argv[])
{
    try
    {
        if (argc != 3)
        {
            std::cerr << "Usage: echo_client <host> <port>\n";
            return 1;
        }

        boost::asio::io_service io_service;

        // client_session cs1(io_service, argv[1], argv[2]);
        // client_session cs2(io_service, argv[1], argv[2]);

        std::vector<client_session*> vc;
        for (int i=0; i < 100; ++i)
            vc.push_back(new client_session(io_service, argv[1], argv[2]));

        system_clock::time_point start = system_clock::now();

        io_service.run();

        std::cout << duration_cast<milliseconds>(system_clock::now() - start) << std::endl;
    }
    catch (std::exception& e)
    {
        std::cerr << "Exception: " << e.what() << "\n";
    }

    return 0;
}
