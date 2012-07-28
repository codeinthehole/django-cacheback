# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant::Config.run do |config|
    config.vm.box = "precise64"
	config.vm.forward_port 8000, 8080
    config.vm.provision :puppet do |puppet|
        puppet.manifests_path = "sandbox/puppet/manifests"
        puppet.manifest_file = "default.pp"
        puppet.module_path = "sandbox/puppet/modules"
    end
end
