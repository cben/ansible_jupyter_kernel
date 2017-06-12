import traceback
import yaml

from ipykernel.kernelbase import Kernel

#from ansible import constants as C
from ansible.cli import CLI
from ansible.errors import AnsibleError, AnsibleOptionsError, AnsibleParserError
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.inventory import Inventory
from ansible.parsing.dataloader import DataLoader
from ansible.playbook.play import Play
from ansible.vars import VariableManager
from ansible.release import __version__ as ansible_version

class UnknownInput(AnsibleParserError):
    """Error in shorthand syntaxes this kernel accepts."""
    # Not certain if this inheriting from AnsibleParserError is best, doesn't matter much.

class AnsibleKernel(Kernel):
    implementation = 'ansible_jupyter_kernel'
    implementation_version = '0.1'
    language = 'Ansible'
    language_version = ansible_version
    language_info = dict(
        name = 'ansible',
        # https://stackoverflow.com/questions/332129/yaml-mime-type
        # Actually text/vnd.yaml was proposed but the proposal hasn't advanced.
        mimetype = 'text/vnd.yaml',
        file_extension = '.yml',
        codemirror_mode = 'yaml',
    )
    banner = "Ansible kernel - WIP https://github.com/cben/ansible_jupyter_kernel"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        parser = CLI.base_parser(module_opts=True, fork_opts=True, runas_opts=True, check_opts=True)
        self.options, _ = parser.parse_args([])
        self.variable_manager = VariableManager()
        self.loader = DataLoader()
        self.inventory = Inventory(loader=self.loader, variable_manager=self.variable_manager)
        self.passwords = {}

    def task_queue_manager(self):
        return TaskQueueManager(
            inventory=self.inventory,
            variable_manager=self.variable_manager,
            loader=self.loader,
            options=self.options,
            passwords=self.passwords,
        )

    def play_from_code(self, code):
        """Support one task, list of tasks, or whole play without hosts."""
        data = orig_data = yaml.safe_load(code)
        if isinstance(data, dict) and 'tasks' not in data:
            data = [data]
        if isinstance(data, list):
            data = dict(tasks=data)
        if not isinstance(data, dict):
            raise UnknownInput("Expected task, list of tasks, or play, got {}".format(type(orig_data)))
        if 'hosts' not in data:
            data['hosts'] = 'localhost'
        return Play.load(data)

    def do_execute(self, code, silent, store_history=True, user_expressions=None, allow_stdin=False):
        try:
            self.task_queue_manager().run(self.play_from_code(code))
        except (yaml.YAMLError, AnsibleParserError) as e:
            message = ''.join(traceback.format_exception_only(type(e), e))
            stream_content = {'name': 'stderr', 'text': message}
        else:
            stream_content = {'name': 'stdout', 'text': 'ok'}

        if not silent:
            self.send_response(self.iopub_socket, 'stream', stream_content)

        return {'status': 'ok',
                # The base class increments the execution count
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {},
               }

# If this grows from a module to a package directory,
# this will go to ansible_jupyter_kernel/__main__.py
if __name__ == '__main__':
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=AnsibleKernel)
