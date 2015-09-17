Vagrant.configure(2) do |config|

  # Box
  config.vm.box = "ubuntu/trusty64"

  #config.vm.provider "virtualbox" do |v|
    #v.customize ["modifyvm", :id, "--cpuexecutioncap", "30"]
    #v.cpus = 1
    #v.memory = 256
  #end

  config.vm.provider "virtualbox" do |v|
     #v.customize ["modifyvm", :id, "--cpuexecutioncap", "30"]
     #v.cpus = 1
     v.memory = 1024
   end

  # DJANGO
  config.vm.network "forwarded_port", guest: 8000, host: 8000
  config.vm.network "forwarded_port", guest: 8888, host: 8888
  config.vm.network "forwarded_port", guest: 5432, host: 15432

  # Sync Folders
  config.vm.synced_folder "./", "/var/www", create: true

  # Provision
    config.vm.provision "install",      type: "shell",  path: "provision/install.sh"
    config.vm.provision "app-install",  type: "shell",  path: "provision/app-install.sh"
    config.vm.provision "app-update",   type: "shell",  path: "provision/app-update.sh", run: "always"
    config.vm.provision "services-up",  type: "shell",  path: "provision/services-up.sh", run: "always"
end