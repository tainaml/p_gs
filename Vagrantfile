Vagrant.configure(2) do |config|

  # Box
  config.vm.box = "ubuntu/trusty64"

  # DJANGO
  config.vm.network "forwarded_port", guest: 8000, host: 8000
  config.vm.network "forwarded_port", guest: 5432, host: 15432

  # Sync Folders
  config.vm.synced_folder "./", "/var/www", create: true

  # Provision
    config.vm.provision "install",    type: "shell",  path: "provision/install.sh"
    config.vm.provision "app-install",  type: "shell",  path: "provision/app-install.sh"
    config.vm.provision "app-update",   type: "shell",  path: "provision/app-update.sh"
end