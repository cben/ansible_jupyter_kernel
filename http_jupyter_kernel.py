import re
import requests

class HTTPKernel(Kernel):
    implementation = 'http_kernel'
    implementation_version = '0.1'
    language = 'HTTP'
    language_version = '1.1'  # TODO: plug in Hyper to support HTTP/2.0
    language_info = dict(
        name = 'http',
        mimetype = 'text/plain',
        file_extension = '.url',
    )
    banner = "HTTP kernel - WIP https://github.com/cben/ansible_jupyter_kernel"

    def request(self, code):
        http_method, url = code.split(Node, 1)
        assert http_method == 'GET'
        return requests.get(url)

    def do_execute(self, code, silent, store_history=True, user_expressions=None, allow_stdin=False):
        """
        GET http://google.com
        """

        response = self.request(code)

        if not silent:
            self.send_response(self.iopub_socket, 'stream',
                               dict(name='stdout', text= str(response.status_code)))
            self.send_response(self.iopub_socket, 'stream',
                               dict(name='stdout', text=response.text))  # TODO mime type

        return dict(
            status='ok',
            # The base class increments the execution count
            execution_count=self.execution_count,
            payload=[],
            user_expressions={},
        )

    def do_complete(self, code, cursor_position):
        prefix = code[:cursor_position]
        text = self.request(to_complete).text
        urls = re.findall(r'https?://[^"\'<>]*', text)
        matches = [u for u in urls if u.startswith(
        return dict(
            status='ok',
            cursor_start=len('GET '),
            cursor_end=cursor_position,
            matches=re.findall(url_re, text),
        )


# If this grows from a module to a package directory,
# this will go to ansible_jupyter_kernel/__main__.py
if __name__ == '__main__':
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=HTTPKernel)
