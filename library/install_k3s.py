#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import subprocess

def generate_cmd(node_type, tls_san, flannel_iface, initial_server_ip):
    sc = [
        "curl", "-sfL", "https://get.k3s.io", "|"
    ]

    if node_type == 'initial':
        sc.extend([
            "sh", "-s", "-",
            "server", "--cluster-init", "--tls-san=https://{}:6443".format(tls_san)
        ])
    else:
        sc.extend([
            "K3S_TOKEN=$(cat token)", "sh", "-s",
            "agent" if node_type == 'agent' else "server",
            "--server", "https://{}:6443".format(initial_server_ip),
            "--tls-san={}".format(tls_san) if node_type == 'additional' else "",
            "--node-external-ip={}".format(initial_server_ip)
        ])

    sc.extend([
        "--flannel-iface={}".format(flannel_iface),
        "--write-kubeconfig-mode=\"644\"" if node_type != 'agent' else ""
    ])

    return " ".join(sc)

def run_module():
    module_args = dict(
        node_type=dict(type='str', required=True),
        tls_san=dict(type='str', required=True),
        flannel_iface=dict(type='str', required=True),
        initial_server_ip=dict(type='str', required=False)       
    )

    result = dict(
        changed=False,
        original_message='',
        message=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    def validate_args(module):
        node_type = module.params['node_type']
        initial_server_ip = module.params['initial_server_ip']

        if node_type != 'initial' and not initial_server_ip:
            module.fail_json(msg="'initial_server_ip' is required when 'node_type' is not 'initial'")
    
    validate_args(module)


    
    shell_command = generate_cmd(module.params['node_type'], module.params['tls_san'], module.params['flannel_iface'], module.params['initial_server_ip'])



    if module.check_mode:
        module.exit_json(**result)


    try:
        result = subprocess.run(shell_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, universal_newlines=True)
        output = result.stdout
        error = result.stderr
        rc = result.returncode
        
    except subprocess.CalledProcessError as e:
        output = "",
        error = str(e)
        rc = e.returncode

    
    module.exit_json(changed=False, rc=rc, stdout=shell_command, stderr=error)
    # module.exit_json(changed=False, rc=rc, stdout=output, stderr=error)

def main():
    run_module()

if __name__ == '__main__':
    main()
