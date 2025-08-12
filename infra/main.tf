terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
  }
}

provider "azurerm" {
  features {}
}

# 1. Resource Group
resource "azurerm_resource_group" "rg" {
  name     = "flask-rg"
  location = "East US 2"
}

# 2. App Service Plan (Free Tier F1)
resource "azurerm_service_plan" "app_plan" {
  name                = "flask-service-plan"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  os_type             = "Linux"
  sku_name            = "B1"
}

# 3. App Service (Web App)
resource "azurerm_linux_web_app" "webapp" {
  name                = "flask-webapp-demo2345234532"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  service_plan_id     = azurerm_service_plan.app_plan.id

  site_config {
    application_stack {
      python_version = "3.12"
    }
  






  }

  app_settings = {
    "WEBSITES_ENABLE_APP_SERVICE_STORAGE" = "false"
  }
}








output "app_url" {
  value = azurerm_linux_web_app.webapp.default_hostname
}

