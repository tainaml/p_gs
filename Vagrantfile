Vagrant.configure(2) do |config|

  # Box
  config.vm.box = "ubuntu/trusty64"

  #config.vm.provider "virtualbox" do |v|
    #v.customize ["modifyvm", :id, "--cpuexecutioncap", "30"]
    #v.cpus = 1
    #v.memory = 256
  #end

  if Vagrant.has_plugin?("vagrant-cachier")
    config.cache.scope = :box
    config.cache.enable :apt
    config.cache.enable :gem
    config.cache.enable :apt_lists
    config.cache.enable :apt_cacher
  end

  # DJANGO
  config.vm.define "web", primary: true do |web|

    web.vm.box = "ubuntu/trusty64"

    web.vm.provider "virtualbox" do |v|
        v.memory = 256
        v.cpus = 1
    end

    web.vm.network "forwarded_port", guest: 8000, host: 8000

    web.vm.network "private_network", ip: "10.100.100.10"

    web.vm.synced_folder "./", "/var/www", create: true

    web.vm.provision "install_web", type: "shell",  path: "provision/install-web.sh"

  end

  config.vm.define "db" do |db|

    db.vm.box = "ubuntu/trusty64"

    db.vm.provider "virtualbox" do |v|
        v.memory = 256
        v.cpus = 1
    end

    db.vm.network "forwarded_port", guest: 5432, host: 15432

    db.vm.network "private_network", ip: "10.100.100.20"

    db.vm.provision "install_web", type: "shell",  path: "provision/install-database.sh"

  end


  #config.vm.network "forwarded_port", guest: 8888, host: 8888
  #config.vm.network "forwarded_port", guest: 5432, host: 15432

  # Sync Folders


  # Provision
    config.vm.provision "install-all",  type: "shell",  path: "provision/install-all.sh"

    #config.vm.provision "install",      type: "shell",  path: "provision/install.sh"
    #config.vm.provision "app-install",  type: "shell",  path: "provision/app-install.sh"
    #config.vm.provision "app-update",   type: "shell",  path: "provision/app-update.sh", run: "always"
    #config.vm.provision "services-up",  type: "shell",  path: "provision/services-up.sh", run: "always"
end