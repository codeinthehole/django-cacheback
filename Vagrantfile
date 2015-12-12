# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant::Config.run do |config|
    config.vm.box = "precise64"
    config.vm.box_url = "http://files.vagrantup.com/precise64.box"
    config.vm.forward_port 8000, 8080
    config.vm.provision "shell", path: "sandbox/provision.sh"
end
