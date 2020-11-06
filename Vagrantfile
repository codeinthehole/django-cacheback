# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant::Config.run do |config|
    config.vm.box = "ubuntu/focal64"
    config.vm.forward_port 8000, 8080
    config.vm.provision "shell", path: "sandbox/provision.sh", privileged: false
end
