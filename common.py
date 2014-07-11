#!/usr/bin/env python
# encoding: utf-8

# Copyright (c) 2013 liudanking

import urllib2
import json
import traceback

def func():
    dic = {'username': u'中文liudanking',
           'password': 'psw'}
    print str(dic)
    print 'len:', len(str(dic))

    str_json = json.dumps(dic)
    print 'json string:' + str_json
    print 'len:', len(str_json)

    str_back = json.loads(str_json)
    print str(str_back)
    str_json = json.dumps(str_back)
    print 'json string:' + str_json
    print 'len:', len(str_json)


def response_json_error(msg, errno=2000):
    res = {'rest':errno, 'msg':msg}
    return json.dumps(res)


def call_http_api(url, params, method='post'):
    timeout = 30
    # for test
    print 'request url:', url  # url = 'http://api.fenhetech.com/api.php?p=chat.auth.getToken&username=u&password=p'
    try:
        if method == 'post':
            f = urllib2.urlopen(url, params, timeout)
        else:  # get method
            for k, v in params.items():
                url += '&'+str(k)+'='+str(v)
            print url
            f = urllib2.urlopen(url)
    except urllib2.URLError as msg:
        print 'urlopen fail, error msg: ', msg
        return response_json_error(msg)
    except:  # traceback.print_exc()
        return response_json_error('server error')
    else:
        res_code = f.getcode()
        if (res_code != 200):
            print f.read()
            return response_json_error('server error')
        return f.read()

# to get access token
if __name__ == '__main__':
    print call_http_api('http://api.fenhetech.com/api.php?p=chat.auth.getToken&username=u&password=p', {'params':123},'get')
