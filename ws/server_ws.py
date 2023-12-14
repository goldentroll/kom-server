import asyncio
import websockets
import kom as k

class WS(k.Module):
    
    
    def __init__(self,
                 ip = '0.0.0.0',
                 port:int=None,
                 queue_size:int=-1,
                 verbose:bool = True):
        self.set_server(ip=ip, port=port, queue_size=queue_size, verbose=verbose)

    @staticmethod
    def start(**kwargs):
        WS(**kwargs)

    def set_server(self, ip = '0.0.0.0', port = None, queue_size = -1, verbose = False):
        self.ip = k.resolve_ip(ip)
        self.port = k.resolve_port(port)
        self.queue = k.queue(queue_size)
        self.address = f'ws://{self.ip}:{self.port}'
        self.server = websockets.serve(self.forward, self.ip, self.port)
        k.print(f'Starting Server on {self.ip}:{self.port}')
        asyncio.get_event_loop().run_until_complete(self.server)
        asyncio.get_event_loop().run_forever()


    def put(self, chunk):
        return self.queue.put(chunk)
    
    async def forward(self, websocket):
        k.print(f'Starting Server Forwarding from {self.ip}:{self.port}')

        while True:
            try:
                k.print('waiting for data')
                data = await websocket.recv()
                k.print(f'chunk -> {data}')
                await websocket.send(data)
                k.print(f'sent -> {data}')
            except Exception as e:
                k.print(f'An error occurred: {e}')  

    @classmethod
    def test(cls):
        k.print('Starting test')
        cls.remote_fn(fn='start', kwargs={})
        k.print('Finished test')


