#!/usr/bin/env python3
"""
    The program tests the operation of time servers.
    Server addresses are declared in the ntp_domains variable.
    Libraries are required for work: ntplib, dnspython.

        pip3 install ntplib dnspython

    Program version 1.00
"""

import ntplib
from time import ctime
import dns.resolver
import socket
import re


"""
    List of NTP server to test
"""
ntp_domains = [
    '0.pool.ntp.org',
    '1.pool.ntp.org',
    '2.pool.ntp.org',
    '3.pool.ntp.org',
    'info.cyf-kr.edu.pl',
    'ntp.certum.pl',
    'ucirtr.agh.edu.pl',
    'ntp.icm.edu.pl',
    'vega.cbk.poznan.pl',
    'tempus1.gum.gov.pl',
    'tempus2.gum.gov.pl',
    'ntp.itl.waw.pl',
    'ntp.elproma.com.pl',
    'ntp.nask.pl'
    ]


def tabg_head():
    print('|' + 27*'=' + '|' + 17*'=' + '|' + 26*'=' + '|' + 9*'=' + '|' + 23*'=' + '|' + 25*'=' + '|')
    print('| Adres' + 21*' ' + '| Adres IP' + 8*' ' + '| Czas' + 21*' ' + '| Stratum | Opóźnienie' + 12*' '
          + '| Czas wzgl. lokalnego' + 4*' ' + '|')
    print('|' + 27*'=' + '|' + 17*'=' + '|' + 26*'=' + '|' + 9*'=' + '|' + 23*'=' + '|' + 25*'=' + '|')


def tabg_row_ok(address, tx_time, stratum, delay, offset, n_a):
    n = "| %-25s | %-15s | %-24s | %-7s | %-21s | %-23s |" % (n_a, address, tx_time, "   "+str(stratum), delay, offset)
    print(n)


def tabg_row_er(address, n_a, e):
    b = "| %-25s | %-15s | %24s | %7s | %-47s |" % (n_a, address, "ERROR", "", e)
    print(b)


def tabg_end():
    print('|' + 27*'=' + '|' + 17*'=' + '|' + 26*'=' + '|' + 9*'=' + '|' + 23*'=' + '|' + 25*'=' + '|')
    print("")


def tabs_head():
    print('|' + 27*'=' + '|' + 7*'=' + '|')
    print('| Adres' + 21*' ' + '| Error |')
    print('|' + 27*'=' + '|' + 7*'=' + '|')


def tabs_row(key, value):
    if value == 0:
        l_s = '| %-25s | %5s |' % (key, value)
    else:
        l_s = '| %-25s | %-5s |' % (key, value)
    print(l_s)


def tabs_end():
    print('|' + 27*'=' + '|' + 7*'=' + '|')


def is_ip(address):
    pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
    if re.match(pattern, address):
        return True
    else:
        return False


def resolve_ntp_domains(domains):
    addresses = []
    naddresses = []
    f_addresses = {}

    for domain in domains:
        f_addresses[domain] = 0
        if is_ip(domain):
            addresses.append(domain)
            naddresses.append(domain)
        else:
            try:
                answers = dns.resolver.resolve(domain, 'A')
                for rdata in answers:
                    addresses.append(rdata.address)
                    naddresses.append(domain)
            except Exception as e:
                print(f"Nie udało się rozwiązać {domain}: {e}")
    return addresses, naddresses, f_addresses


def check_ntp_servers(addresses, naddresses, faddress):

    tabg_head()

    i = 0
    for address in addresses:
        n_a = naddresses[i]

        try:
            ntp_client = ntplib.NTPClient()
            response = ntp_client.request(address, version=3)
            i = i + 1

            tabg_row_ok(address, ctime(response.tx_time), response.stratum, response.delay, response.offset, n_a)
        except (ntplib.NTPException, socket.gaierror) as e:
            tabg_row_er(address, n_a, e)

            f_a = faddress[n_a]
            f_a = f_a + 1
            faddress[n_a] = f_a

    tabg_end()
    tabs_head()

    for key, value in faddresses.items():
        tabs_row(key, value)

    tabs_end()


ntp_addresses, ntp_naddresses, faddresses = resolve_ntp_domains(ntp_domains)
check_ntp_servers(ntp_addresses, ntp_naddresses, faddresses)
