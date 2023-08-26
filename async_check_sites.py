import asyncio
from urllib.parse import urlsplit

async def check_sts(url):
    url_pars = urlsplit(url)
    if url_pars.scheme == 'https':
        read, write = await asyncio.open_connection(url_pars.hostname, 443, ssl=True)
    else:
        read, write = await asyncio.open_connection(url_pars.hostname, 80)

    req = f'GET {url_pars.path} HTTP/1.1\r\Host: {url_pars.hostname}\r\n\r\n'
    write.write(req.encode())
    await write.drain()
    resp = await read.readline()
    write.close()
    
    sts = resp.decode().strip()
    return sts

async def main():
    sites = ['http://104.197.18.249/',
             'http://104.197.18.236/',
             'http://104.197.18.231/',
             'http://104.197.18.225/',
             'http://104.197.18.207/',
             'http://104.197.18.195/'
            ]
    tsk_to_url = {asyncio.create_task(check_sts(url)):url for url in sites}
    tsk_to_complete = await asyncio.wait(tsk_to_url)

    for task in tsk_to_url:
        url = tsk_to_url[task]
        sts = task.result()
        print(f'{url:30}:\t{sts}')

asyncio.run(main())





