#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fabric.api import run, local, task, env
from fabric.colors import blue, red, green
from fabric.operations import put


env.building_dir = "/tmp/building_blog"
env.production_dir = "/srv/www.hacker.si"
env.backup_dir = "/srv/backup.www.hacker.si"
env.branch = "deploy"
env.repository = "git://github.com/hackerSi/www.hacker.si.git"
env.use_ssh_config = True


@task
def local_server_deploy():
    """docstring for local_server_deploy"""

    print blue("Bootstraping buildout ...")
    local('python bootstrap.py -d')
    print blue("Running buildout ...")
    local('bin/buildout')
    local('rm -rf output')
    local('mkdir output')
    update_blog()
    print green("Local deploy done.")


@task
def build_blog():
    """docstring for build_blog"""
    local("bin/pelican -d -s pelican.conf.py")


def copy_to_server():
    """docstring for copy_to_server"""
    print blue("Copying blog to server ...")
    run("mkdir %s" % env.production_dir)
    return put("output/*", env.production_dir).succeeded


def make_backup():
    """docstring for make_backup"""
    run(" cp -r %s %s" % (env.production_dir, env.backup_dir))


def revert_backup():
    """docstring for revert_backup"""
    print blue("Reverting backup ...")
    run(" cp -r %s %s" % (env.backup, env.production_dir))
    print green("Revert succeeded. Please try again.")


def clean_server():
    """docstring for clean_server"""
    print blue("Cleaning server ...")
    run("rm -r %s" % env.production_dir)


def remove_backup():
    """docstring for remove_backup"""
    print blue("Removing backup ...")
    run("rm -r %s" % env.backup_dir)
    print green("Backup removed.")


@task
def update_blog():

    build_blog()
    make_backup()
    clean_server()
    try:
        copy_to_server()
        remove_backup()
    except:
        print red("Copy failed. :(")
        revert_backup()
    else:
        print green("Copy succeeded. :D")
