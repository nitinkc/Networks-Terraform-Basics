terraform {
  required_version = ">= 1.5.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

variable "project_id" {
  description = "GCP project ID to deploy into"
  type        = string
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "us-central1"
}

# The cloud equivalent of drawing a network boundary in Packet Tracer
resource "google_compute_network" "first_vpc" {
  name                    = "tf-first-vpc"
  auto_create_subnetworks = false   # we will define subnets ourselves in lab 02
}