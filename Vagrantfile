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

  # Provision
  config.vm.provision "install-all",  type: "shell",  path: "provision/base/install.sh"

  # DJANGO / POSTGRESQL
  config.vm.define "web", primary: true do |web|

    web.vm.box = "ubuntu/trusty64"

    web.vm.provider "virtualbox" do |v|
        v.memory = 384
        v.cpus = 1
    end

    web.vm.network "forwarded_port", guest: 8000, host: 8000
    web.vm.network "forwarded_port", guest: 5432, host: 15432

    web.vm.network "private_network", ip: "10.100.100.10"

    web.vm.synced_folder "./", "/var/www", create: true

    #web.vm.provision "web-base-install", type: "shell",  path: "provision/base/install.sh"
    web.vm.provision "web-install", type: "shell",  path: "provision/web/install.sh"
    web.vm.provision "database-install", type: "shell",  path: "provision/database/install.sh"
    web.vm.provision "install-app",  type: "shell",  path: "provision/web/install-app.sh"
    web.vm.provision "update-app",  type: "shell",  path: "provision/web/update-app.sh", run: "always"

  end

  config.vm.define "thumbor" do |thumbor|

    thumbor.vm.box = "ubuntu/trusty64"

    thumbor.vm.provider "virtualbox" do |v|
        v.memory = 256
        v.cpus = 1
    end

    #thumbor.vm.provision "thumbor-base-install", type: "shell",  path: "provision/base/install.sh"
    thumbor.vm.network "private_network", ip: "10.100.100.20"
    thumbor.vm.network "forwarded_port", guest_ip: "10.100.100.20", guest: 8888, host: 8888
    thumbor.vm.provision "thumbor-install", type: "shell",  path: "provision/thumbor/install.sh"
    thumbor.vm.provision "thumbor-service-up", type: "shell",  path: "provision/thumbor/up.sh", run: "always"

  end

end