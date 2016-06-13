# coding: utf-8
Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/xenial64"  # 设置box的名字
  config.vm.hostname = "WEB"
#  config.vm.synced_folder "/Users/dongweiming/web_develop", "/home/vagrant/web_develop"
  config.vm.network :forwarded_port, guest: 9000, host: 9000
  config.vm.network :forwarded_port, guest: 3141, host: 3141
  config.vm.network :forwarded_port, guest: 5000, host: 5000
  config.ssh.insert_key = false
  config.ssh.private_key_path = ["~/.ssh/id_rsa"]
  config.vm.provision "file", source: "~/.ssh/id_rsa.pub", destination: "~/.ssh/authorized_keys"
  config.vm.provider "virtualbox" do |v|
    v.customize ["modifyvm", :id, "--name", "web_dev", "--memory", "1536"]
  end
end
