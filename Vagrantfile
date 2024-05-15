# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
config.vm.boot_timeout = 600
nodes = [ 
	{ :name => "s1",  :hostname => "server1",       :IPAddr => "192.168.56.11" },
	{ :name => "s2",  :hostname => "server2",       :IPAddr => "192.168.56.12" },
	{ :name => "s3",  :hostname => "server3",       :IPAddr => "192.168.56.13" }
	]

  config.vm.box = "gusztavvargadr/ubuntu-server-2204-lts"
  config.vm.synced_folder '.', '/vagrant', disabled: true

  nodes.each_with_index do |node, index|
    config.vm.define node[:name] do |s|
      s.vm.hostname = node[:hostname] 
      s.vm.network "private_network", ip: node[:IPAddr] 
    end
  end

  config.vm.provider "virtualbox" do |v|
    v.customize ["modifyvm", :id, "--memory", "2048"]
    v.customize ["modifyvm", :id, "--cpus", "1"]
  end

end
