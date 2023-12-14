import asyncio
import websockets
import kom as k

class WSClient(k.Module):
    
    
    def __init__(self,
                 name , 
                 start:bool = True, 
                 network: dict = None,
                 ):
        if ':' in ip:
            ip, port = ip.split(':')

        namespace = k.namespace(network=network)
        self.address = namespace.get(name, None)
        

    def resolve_address(cls, address=None):
        if address == None:
            address = self.address
        if not 'ws://' in address:
            address = f'ws://{address}'
        assert isinstance(address, str), f'address must be a string, not {type(address)}'
        return address

    async def async_forward(self, data='hello', address = None):

        address = self.resolve_address(address=address)
        

        
        
        async with websockets.connect(address) as websocket:
            await websocket.send(data)
            response = await websocket.recv()
        
        return response
    
    def forward(self, data='hello', address = None):
        return asyncio.get_event_loop().run_until_complete(self.async_forward(data=data, address=address))

    @staticmethod
    async def recv(address):
        chunks = []
        async with websockets.connect(address) as websocket:
            chunk = await websocket.recv(address)
            chunks.append(chunk)
