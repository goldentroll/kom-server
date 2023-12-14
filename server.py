import kom as k

class Server(k.Module):


    @classmethod
    def test(cls) -> dict:
        servers = k.servers()
        k.print(servers)
        tag = 'test'
        module_name = k.serve(module='module', tag=tag)['name']
        k.wait_for_server(module_name)
        assert module_name in k.servers()

        response = k.call(module_name)
        k.print(response)

        k.kill(module_name)
        assert module_name not in k.servers()
        return {'success': True, 'msg': 'server test passed'}
    
    @classmethod
    def dashboard(cls):
        return k.module('server.dashboard').dashboard()
    
Server.run(__name__)