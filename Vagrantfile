#
# Vagrantfile to create layout development environment.
#


VAGRANTFILE_API_VERSION   = "2"
BOX                       = "OSX109"
PROVIDER_NAME             = "vmware_fusion"
PROJECT_NAME              = "layout"
VM_NAME                   = PROJECT_NAME
PROJECT_GITHUB_URL        = "https://github.com/milewdev/#{PROJECT_NAME}.git"
PROJECT_VM_DIR            = "/Users/vagrant/Documents/#{PROJECT_NAME}"
PROVISIONER_URL           = "https://raw.githubusercontent.com/milewdev/vm-provisioner/v2/Provisioner.rb"


Vagrant.configure(VAGRANTFILE_API_VERSION) do |vagrant_config|

  vagrant_config.vm.box = BOX

  vagrant_config.vm.provider(PROVIDER_NAME) do |vb|
    vb.name = VM_NAME
    vb.gui = true
  end

  with vagrant_config do
    install_atom
    install_iterm2
    install_gpg                                         # needed to sign git commits
    install_git                                         # source is on github
    install_github_for_mac
    install_python3
    install_virtualenv
    git_clone PROJECT_GITHUB_URL, PROJECT_VM_DIR
    cd PROJECT_VM_DIR do
      virtualenv_create
    end
    reboot_vm
  end

end


def with(vagrant_config, &block)
  require "open-uri"
  File.write "Provisioner.rb", open(PROVISIONER_URL).read
  require_relative "Provisioner"
  Provisioner.provision(vagrant_config, &block)
  File.delete "Provisioner.rb"
end
