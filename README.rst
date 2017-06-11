ansible_jupyter_kernel
======================

WIP Jupyter kernel for executing Ansible plays

License
-------

GPL v3 or later, same as Ansible.

Prior Art
---------

Some people have been using Ansible inside Jupyter:

- https://github.com/NII-cloud-operation/Literate-computing-Basics
  - https://www.youtube.com/watch?v=xyfdufiibQk
- http://enakai00.hatenablog.com/entry/2016/04/22/204125
- https://chusiang.gitbooks.io/automate-with-ansible/content/07.how-to-practive-the-ansible-with-jupyter1.html
- https://www.slideshare.net/irix_jp/osc2016-kyoto-heat-ansible-jupyter
- https://chusiang.gitbooks.io/automate-with-ansible/content/07.how-to-practive-the-ansible-with-jupyter1.html,
  https://chusiang.gitbooks.io/automate-with-ansible/content/08.how-to-practive-the-ansible-with-jupyter2.html

AFAICT all these are running a Python kernel and shelling out using `!ansible` syntax, or `%%writefile ...playbook.yml` followed by `!ansible-notebook`.

That might actually be more flexible (and less buggy) than a kernel that only runs ansible like I'm doing here — and they clearly unlike me have lots of experience actually achieving things using Ansible inside Jupyter — but the purpose of this exercise was seeing what I can gain from writing a kernel...

- But https://github.com/NII-cloud-operation also have some nbextensions
