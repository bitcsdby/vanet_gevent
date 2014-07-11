#!/usr/bin/env python
# encoding: utf-8

# networking config

ConfigServer = {'tcp_host': '0.0.0.0',
                'tcp_port': 6000,
                'udp_host': '0.0.0.0',
                'udp_port': 9001,
                #'db_host':'vanet.fenhetech.com',
                'db_host': 'www.ecloudan.com',  # 'db_host':'localhost',
                'db_user': 'root',
                'db_psw': ''}


#ConfigAPI = {'base_url':'http://vanet.fenhetech.com/api.php?p='}
ConfigAPI = {'base_url': 'http://www.ecloudan.com/api.php?p='}
#ConfigAPI = {'base_url':'http://localhost/vanet/vanet/api.php?p='}
if __name__ == '__main__':
    print ConfigServer
    print ConfigServer['tcp_host']