#! /usr/bin/env python3
import argparse
import sys
import logging
from typing import List
import subprocess
parser = argparse.ArgumentParser()

parser.add_argument('action', nargs='?', default='help',
                    help="Action to perfrom: fetch|tag|push|show")
parser.add_argument('--dry-run', type=bool, default=False,
                    help='Dry run, output commands to stdout')
parser.add_argument('--registry', type=str,
                    help='Private docker registry address for tagging and pushing images')
args = parser.parse_args()
IMAGES = [
    "registry.access.redhat.com/openshift-istio-tech-preview/citadel:0.5.0",
    "registry.access.redhat.com/openshift-istio-tech-preview/mixer:0.5.0",
    "registry.access.redhat.com/openshift-istio-tech-preview/sidecar-injector:0.5.0",
    "registry.access.redhat.com/openshift-istio-tech-preview/proxyv2:0.5.0",
    "registry.access.redhat.com/openshift-istio-tech-preview/proxy-init:0.5.0",
    "registry.access.redhat.com/openshift-istio-tech-preview/pilot:0.5.0",
    "registry.access.redhat.com/openshift-istio-tech-preview/galley:0.5.0",
    "registry.access.redhat.com/openshift-istio-tech-preview/istio-operator:0.5.0",
    "registry.access.redhat.com/distributed-tracing-tech-preview/jaeger-query:1.8.1",
    "registry.access.redhat.com/distributed-tracing-tech-preview/jaeger-collector:1.8.1",
    "registry.access.redhat.com/distributed-tracing-tech-preview/jaeger-agent:1.8.1",
    "registry.access.redhat.com/openshift-istio-tech-preview/openshift-ansible:0.5.0",
    "registry.access.redhat.com/distributed-tracing-tech-preview/jaeger-elasticsearch:5.6.10",
    "docker.io/grafana/grafana:5.2.3",
    "docker.io/kiali/kiali:v0.10.1",
    "docker.io/prom/prometheus:v2.3.1",
]


def tag_images():
    private_registry = args.registry
    commands = []
    for image in IMAGES:
        cmd = f'docker tag {image} {private_registry}/{image.split("/")[-1]}'
        commands.append(cmd)
    return commands


def command_executer(cmds: List[str]):
    if args.dry_run:
        logging.info('Dry run, not gonna executed any command, print only')
        logging.info(" *** dry run  start ***")
        for cmd in cmds:
            logging.info(cmd)
        logging.info(" *** dry run end ***")
        return
    for cmd in cmds:
        logging.info(f"Executing: {cmd}")
        p = subprocess.Popen(cmd, shell=True)
        p.communicate()


def fetch_mesh_images() -> List[str]:
    commands = []
    for image in IMAGES:
        commands.append(f"docker pull {image}")
    return commands


def push_mesh_images():
    private_registry = args.registry
    commands = []
    for image in IMAGES:
        cmd = f'docker push {private_registry}/{image.split("/")[-1]}'
        commands.append(cmd)
    return commands


def get_orig_images():
    for image in IMAGES:
        logging.info(image)


def main():
    log_format = '[%(asctime)s %(levelname)s] %(message)s'
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        stream=sys.stdout
    )
    if args.action == 'help':
        parser.print_help()
    if args.action == 'fetch':
        cmds = fetch_mesh_images()
        command_executer(cmds)
    if args.action == 'tag':
        if args.registry is None:
            logging.error("Missing registry parameter")
            exit(1)
        cmds = tag_images()
        command_executer(cmds)
    if args.action == 'push':
        if args.registry is None:
            logging.error("Missing registry parameter")
            exit(1)
        cmds = push_mesh_images()
        command_executer(cmds)
    if args.action == 'show':
        get_orig_images()


if __name__ == "__main__":
    main()
