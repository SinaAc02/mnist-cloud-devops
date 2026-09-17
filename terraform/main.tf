locals {
  resource_location = "Belgium Central"
}

resource "azurerm_resource_group" "main" {
  name     = "mnist-cloud-rg"
  location = "Denmark East"
  tags     = {}
}

resource "azurerm_virtual_network" "main" {
  name                = "vnet-belgiumcentral-1"
  location            = local.resource_location
  resource_group_name = azurerm_resource_group.main.name
  address_space       = ["172.16.0.0/16"]
}

resource "azurerm_subnet" "main" {
  name                 = "snet-belgiumcentral-1"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = ["172.16.0.0/24"]
}

resource "azurerm_network_security_group" "main" {
  name                = "mnist-cloud-vm-nsg"
  location            = local.resource_location
  resource_group_name = azurerm_resource_group.main.name
}

resource "azurerm_network_security_rule" "ssh" {
  name                        = "SSH"
  priority                    = 300
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "Tcp"
  source_port_range           = "*"
  destination_port_range      = "22"
  source_address_prefix       = "*"
  destination_address_prefix  = "*"
  resource_group_name         = azurerm_resource_group.main.name
  network_security_group_name = azurerm_network_security_group.main.name
}

resource "azurerm_network_security_rule" "http" {
  name                        = "allow-http"
  priority                    = 320
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "Tcp"
  source_port_range           = "*"
  destination_port_range      = "80"
  source_address_prefix       = "*"
  destination_address_prefix  = "*"
  resource_group_name         = azurerm_resource_group.main.name
  network_security_group_name = azurerm_network_security_group.main.name
}

resource "azurerm_public_ip" "main" {
  name                = "mnist-cloud-vm-ip"
  location            = local.resource_location
  resource_group_name = azurerm_resource_group.main.name
  allocation_method   = "Static"
  sku                 = "Standard"
}

resource "azurerm_network_interface" "main" {
  name                           = "mnist-cloud-vm55"
  location                       = local.resource_location
  resource_group_name            = azurerm_resource_group.main.name
  accelerated_networking_enabled = false
  ip_forwarding_enabled          = false

  ip_configuration {
    name                          = "ipconfig1"
    subnet_id                     = azurerm_subnet.main.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.main.id
  }
}

resource "azurerm_network_interface_security_group_association" "main" {
  network_interface_id      = azurerm_network_interface.main.id
  network_security_group_id = azurerm_network_security_group.main.id
}

resource "azurerm_ssh_public_key" "main" {
  name                = "mnist-cloud-vm_key"
  location            = local.resource_location
  resource_group_name = azurerm_resource_group.main.name
  public_key          = var.ssh_public_key
}

resource "azurerm_linux_virtual_machine" "main" {
  name                            = "mnist-cloud-vm"
  computer_name                   = "mnist-cloud-vm"
  location                        = local.resource_location
  resource_group_name             = azurerm_resource_group.main.name
  size                            = "Standard_B2ats_v2"
  admin_username                  = "azureuser"
  disable_password_authentication = true
  network_interface_ids           = [azurerm_network_interface.main.id]

  additional_capabilities {
    hibernation_enabled = false
    ultra_ssd_enabled   = false
  }

  admin_ssh_key {
    username   = "azureuser"
    public_key = var.ssh_public_key
  }

  os_disk {
    name                 = "mnist-cloud-vm_OsDisk_1_98a693bc1482477eb4a1180ec8e24bd4"
    caching              = "ReadWrite"
    storage_account_type = "Premium_LRS"
    disk_size_gb         = 30
  }

  source_image_reference {
    publisher = "canonical"
    offer     = "ubuntu-24_04-lts"
    sku       = "server"
    version   = "latest"
  }

  boot_diagnostics {}
}
