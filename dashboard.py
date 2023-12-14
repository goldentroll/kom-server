
import kom as k
import streamlit as st
import pandas as pd

class ServerDashboard(k.Module):
    @classmethod
    def dashboard(cls):
        import pandas as pd
        self = cls()
        self.sidebar()
        self.st = k.module('streamlit')

        modules = k.modules()
        self.st.line_seperator()
        module2index = {m:i for i,m in enumerate(modules)}
        module_name  = st.selectbox('Select a Module', modules, module2index['agent'], key=f'serve.module')



        module = k.module(module_name)
        # n = st.slider('replicas', 1, 10, 1, 1, key=f'n.{prefix}')
                    

        with st.expander('serve'):
            cols = st.columns([2,2,1])
            tag = cols[0].text_input('tag', 'replica', key=f'serve.tag.{module}')
            tag = None if tag == '' else tag

            n = cols[1].number_input('Number of Replicas', 1, 30, 1, 1, key=f'serve.n.{module}')
            
            [cols[2].write('\n\n\n') for _ in range(2)]
            register = cols[2].checkbox('Register', key=f'serve.register.{module}')
            if register:
                stake = cols[2].number_input('Stake', 0, 100000, 1000, 100, key=f'serve.stake.{module}')
            st.write(f'### {module_name.upper()} kwargs')
            with st.form(key=f'serve.{module}'):
                kwargs = self.function2streamlit(module=module, fn='__init__' )

                serve = st.form_submit_button('Serve')


                if serve:

                    if 'None' == tag:
                        tag = None
                    if 'tag' in kwargs:
                        kwargs['tag'] = tag
                    for i in range(n):
                        try:
                            if tag != None:
                                s_tag = f'{tag}.{i}'
                            else:
                                s_tag = str(i)
                            response = module.serve( kwargs = kwargs, tag=s_tag, network=self.network)
                        except Exception as e:
                            e = k.detailed_error(e)
                            response = {'success': False, 'message': e}
            
                        if response['success']:
                            st.write(response)
                        else:
                            st.error(response)

        with st.expander('Code', expanded=False):
            code = module.code()
            st.markdown(f"""
                        ```python
                        {code}
                        ```
                        """)
            
        with st.expander('readme', expanded=False):
            
            markdown = module.readme()
            st.markdown(markdown)

        cols = st.columns([2,2])
            
        with st.expander('Add Server'):
            address = st.text_input('Server Address', '')
            add_server = st.button('Add Server')
            if add_server:
                k.add_server(address)
        
        with st.expander('Remove Server'):
            server = st.selectbox('Module Name', self.servers, 0)
            rm_server = st.button('Remove Server')
            if rm_server:
                k.rm_server(server)

    

    def playground_dashboard(self):
        

        server2index = {s:i for i,s in enumerate(self.servers)}
        default_servers = [self.servers[0]]
        cols = st.columns([1,1])
        self.server_name = cols[0].selectbox('Select Server',self.servers, 0, key=f'serve.module.playground')
        self.server = k.connect(self.server_name, network=self.network)
        
        
        try:
            self.server_info = self.server.info(schema=True, timeout=2)
        except Exception as e:
            st.error(e)
            return

        self.server_schema = self.server_info['schema']
        self.server_functions = list(self.server_schema.keys())
        self.server_address = self.server_info['address']

        self.fn = cols[1].selectbox('Select Function', self.server_functions, 0)

        self.fn_path = f'{self.server_name}/{self.fn}'
        st.write(f'**address** {self.server_address}')
        with st.expander(f'{self.fn_path} playground', expanded=True):

            kwargs = self.function2streamlit(fn=self.fn, fn_schema=self.server_schema[self.fn], salt='sidebar')

            cols = st.columns([3,1])
            timeout = cols[1].number_input('Timeout', 1, 100, 10, 1, key=f'timeout.{self.fn_path}')
            cols[0].write('\n')
            cols[0].write('\n')
            call = cols[0].button(f'Call {self.fn_path}')
            if call:
                try:
                    response = getattr(self.server, self.fn)(**kwargs, timeout=timeout)
                except Exception as e:
                    e = k.detailed_error(e)
                    response = {'success': False, 'message': e}
                st.write(response)
    
       
ServerDashboard.run(__name__)


