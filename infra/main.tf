provider "oci" {
  tenancy_ocid = "${var.tenancy_ocid}"
  user_ocid = "${var.user_ocid}"
  fingerprint = "${var.fingerprint}"
  private_key_path = "${var.private_key_path}"
  region = "${var.region}"
}

data "oci_identity_availability_domains" "ads" {
  compartment_id = "${var.tenancy_ocid}"
}

resource "oci_identity_policy" "faas_policy" {
    compartment_id = "${var.tenancy_ocid}"
    description = "faas_service_policy"
    name = "faas_service_policy"
    statements = ["allow service FAAS to use virtual-network-family in tenancy", "allow service FAAS to read repos in tenancy"]
}

resource "oci_identity_policy" "user_policy" {
    compartment_id = "${var.tenancy_ocid}"
    description = "faas_user_policy"
    name = "faas_user_policy"
    statements = [
      "allow group faas_devs to manage repos in tenancy",
      "allow group faas_devs to use virtual-network-family in tenancy",
      "allow group faas_devs to manage functions-family in tenancy",
      "allow group faas_devs to read metrics in tenancy",
      "allow group faas_devs to use cloud-shell in tenancy"
    ]
}

resource "oci_identity_policy" "api_gateway_policy" {
    compartment_id = "${var.tenancy_ocid}"
    description = "api_gateway_policy"
    name = "api_gateway_policy"
    statements = [
      "ALLOW any-user to use functions-family in tenancy where ALL { request.principal.type= 'ApiGateway', request.resource.compartment.id = '${var.tenancy_ocid}'}",
    ]
}

resource "oci_core_vcn" "function_vcn" {
    cidr_block = "10.0.0.0/16"
    compartment_id = "${var.tenancy_ocid}"
      display_name = "gilda_vcn"
}

resource "oci_core_default_route_table" "functions_route_table" {
    manage_default_resource_id = "${oci_core_vcn.function_vcn.default_route_table_id}"

    route_rules {
        network_entity_id = "${oci_core_internet_gateway.function_internet_gateway.id}"
        cidr_block = "0.0.0.0/0"
    }
}

resource "oci_core_subnet" "function_subnet" {
    cidr_block = "10.0.0.0/24"
    compartment_id = "${var.tenancy_ocid}"
    vcn_id = "${oci_core_vcn.function_vcn.id}"
    display_name = "gilda_vcn"
}

resource "oci_core_default_security_list" "function_security_list" {
    manage_default_resource_id = "${oci_core_vcn.function_vcn.default_security_list_id}"
    egress_security_rules {
        destination = "0.0.0.0/0"
        protocol = "all"
    }
    ingress_security_rules {
        # TODO: lock this down better
        protocol = "all"
        source = "0.0.0.0/0"
    }
}

resource "oci_core_internet_gateway" "function_internet_gateway" {
    compartment_id = "${var.tenancy_ocid}"
    vcn_id = "${oci_core_vcn.function_vcn.id}"
    enabled = "true"
}

resource "oci_functions_application" "test_application" {
    compartment_id = "${var.tenancy_ocid}"
    display_name = "Gilda"
    subnet_ids = ["${oci_core_subnet.function_subnet.id}"]

    config = "${var.application_config}"
}

resource "oci_apigateway_gateway" "function_gateway" {
    compartment_id = "${var.tenancy_ocid}"
    endpoint_type = "PUBLIC"
    subnet_id = "${oci_core_subnet.function_subnet.id}"

    display_name = "Gilda Gateway"
}

# TODO: build a api gateway deployment

# TODO: Create Repository

# Output the result
output "show-ads" {
  value = "${data.oci_identity_availability_domains.ads.availability_domains}"
}
