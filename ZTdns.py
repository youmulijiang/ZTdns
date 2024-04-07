import threading
import dns.query
import dns.resolver
import dns.zone
from lib.colorprint import cprint,Color
from concurrent.futures import ThreadPoolExecutor
import argparse
import time
import os

Lock = threading.Lock()
xfr_dns_domain_list = []

logo = """ 
  ____..--',---------.  ______     ,---.   .--.   .-'''-.  
 |        |\          \|    _ `''. |    \  |  |  / _     \ 
 |   .-'  ' `--.  ,---'| _ | ) _  \|  ,  \ |  | (`' )/`--' 
 |.-'.'   /    |   \   |( ''_'  ) ||  |\_ \|  |(_ o _).    
    /   _/     :_ _:   | . (_) `. ||  _( )_\  | (_,_). '.  
  .'._( )_     (_I_)   |(_    ._) '| (_ o _)  |.---.  \  : 
.'  (_'o._)   (_(=)_)  |  (_.\.' / |  (_,_)\  |\    `-'  | 
|    (_,_)|    (_I_)   |       .'  |  |    |  | \       /  
|_________|    '---'   '-----'`    '--'    '--'  `-...-'                                                             
"""

def check_domain_dns_z_t(domain):
    with Lock:
        zone = dns.zone.Zone(domain)
        resolver = dns.resolver.Resolver()
        resolver.nameservers = ['8.8.8.8','114.114.114.114']

        ns_dns_name = resolver.resolve(domain,'NS')
        for dns_name_server in ns_dns_name:
            dns_name_server = str(dns_name_server)[:-1]
            try:
                dns.query.inbound_xfr(dns_name_server,zone)
                cprint(f"域名为{domain},dns服务器为{dns_name_server}存在域传输漏洞",style=Color.RED)
                warning_str = f"域名为{domain},dns服务器为{dns_name_server}存在域传输漏洞"
                xfr_dns_domain_list.append(warning_str)

            except Exception as e:
                # print(e)
                cprint(f"域名为{domain},dns服务器为{dns_name_server}不存在域传输漏洞\n",style=Color.GREEN)


def check_domain_list_dns_z_t(file_path):
    with open(file_path,encoding='utf-8') as file:
        domain_list = [domain.strip() for domain in file]

    with ThreadPoolExecutor(max_workers=100) as pool:
        pool.map(check_domain_dns_z_t,domain_list)

def save_result(save_file_path):
    count = 0
    with open(save_file_path,"w+") as file:
        for warning_str in xfr_dns_domain_list:
            file.write(warning_str)
        for i in file:
            count = count + 1
        cprint(f"共发现{count}条dns域传输漏洞")

def save_result(save_file_path):
    count = 0
    with open(save_file_path,"w+") as file:
        for warning_str in xfr_dns_domain_list:
            file.write(warning_str)
        for i in file:
            count = count + 1
        if count > 1:
            cprint(f"共发现{count}条dns域传输漏洞!!!",style=Color.RED)

if __name__ == '__main__':
    parse = argparse.ArgumentParser()
    mu_group = parse.add_mutually_exclusive_group()
    mu_group.add_argument("-d",metavar="domain",help="指定探测域名")
    mu_group.add_argument("-f",metavar="domain_file",help="指定domain列表文件")
    parse.add_argument("-o",metavar="save_path",help="写入文件的路径")
    args = parse.parse_args()
    start_time = time.time()
    cprint(f"{logo}",style=Color.PURPLE)
    try:
        if args.d:
            check_domain_dns_z_t(args.d)
        if args.f:
            check_domain_list_dns_z_t(args.f)

        if args.o:
            save_result(args.o)
    except KeyboardInterrupt as e:
        print("共用时:",time.time()-start_time)
        print("成功退出")
        os._exit(1)
    print("共用时:",time.time()-start_time)

    