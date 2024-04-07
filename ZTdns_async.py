import dns.asyncresolver
import dns.asyncquery
import asyncio
import dns.zone
from lib.colorprint import cprint,Color
import argparse
import time
import os


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



xfr_dns_domain_list = []
async def check_domain_dns_z_t(domain):
    result = None  # 初始化 result 变量
    try:
        zone = dns.zone.Zone(domain)
        resolver = dns.asyncresolver.Resolver()
        resolver.nameservers = ['8.8.8.8','114.114.114.114']
        result = await resolver.resolve(domain, "NS")
    except:
        pass

    async def execute_xfr(ns_cord):
        try:
            await dns.asyncquery.inbound_xfr(str(ns_cord)[:-1], zone)
            cprint(f"域名为{domain},dns服务器为{str(ns_cord)[:-1]}存在dns域传输漏洞\n",Color.RED)
            warning_str = f"域名为{domain},dns服务器为{str(ns_cord)[:-1]}存在dns域传输漏洞"
            xfr_dns_domain_list.append(warning_str)
        except Exception as e:
            cprint(f"域名为{domain},dns服务器为{str(ns_cord)[:-1]}不存在dns域传输漏洞\n",Color.GREEN)

    if result:  # 检查 result 是否有值
        tasks = [asyncio.create_task(execute_xfr(ns_cord)) for ns_cord in result]
        await asyncio.gather(*tasks)


async def check_domain_list_dns_z_t(file_path):
    with open(file_path) as file:
        for i in file:
            domain = i.strip()
            await asyncio.gather(asyncio.create_task(check_domain_dns_z_t(domain)))


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
    cprint(f"{logo}",style=Color.PURPLE)
    parse = argparse.ArgumentParser()
    mu_group = parse.add_mutually_exclusive_group()
    mu_group.add_argument("-d",metavar="domain",help="指定探测域名")
    mu_group.add_argument("-f",metavar="domain_file",help="指定domain列表文件")
    parse.add_argument("-o",metavar="save_path",help="写入文件的路径")
    args = parse.parse_args()
    start_time = time.time()
    try:
        if args.d:
            asyncio.run(check_domain_dns_z_t(args.d))
        if args.f:
            asyncio.run(check_domain_list_dns_z_t(args.f))

        if args.o:
            save_result(args.o)
    except KeyboardInterrupt as e:
        print("共用时:",time.time()-start_time)
        print("成功退出")
        os._exit(1)
    print("共用时:",time.time()-start_time)
