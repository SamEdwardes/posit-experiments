"""An AWS Python Pulumi program"""

import pulumi
from dataclasses import dataclass, field
from pulumi_aws import ec2, rds

from typing import List, Dict

@dataclass 
class ConfigValues:
    """A single object to manage all config files."""
    config: pulumi.Config = field(default_factory=lambda: pulumi.Config())
    email: str = field(init=False)
    public_key: str = field(init=False)

    def __post_init__(self):
        self.email = self.config.require("email")
        self.public_key = self.config.require("public_key")   



def make_server(
    tags: Dict, 
    key_pair: ec2.KeyPair, 
    vpc_group_ids: List[str]
):
    # Stand up a server.
    server = ec2.Instance(
        f"server",
        instance_type="t3.medium",
        vpc_security_group_ids=vpc_group_ids,
        ami="ami-0fb653ca2d3203ac1",  # Ubuntu Server 20.04 LTS (HVM), SSD Volume Type
        tags=tags,
        key_name=key_pair.key_name
    )
    
    # Export final pulumi variables.
    pulumi.export(f'server_public_ip', server.public_ip)
    pulumi.export(f'server_public_dns', server.public_dns)
    pulumi.export(f'server_subnet_id', server.subnet_id)
    return server

def make_database(tags: Dict, security_group: ec2.SecurityGroup):
    db = rds.Instance(
        "pg-db",
        instance_class="db.t3.micro",
        allocated_storage=5,
        username="rsw_db_admin",
        password="password",
        db_name="rstudio_pm",
        engine="postgres",
        publicly_accessible=True,
        skip_final_snapshot=True,
        tags=tags | {"Name": "rsw-db"},
        vpc_security_group_ids=[security_group.id]
    )

    pulumi.export("db_port", db.port)
    pulumi.export("db_address", db.address)
    pulumi.export("db_endpoint", db.endpoint)
    pulumi.export("db_name", db.name)
    pulumi.export("db_domain", db.domain)
    return db


def main():
    config = ConfigValues()

    tags = {
        "rs:environment": "development",
        "rs:owner": config.email,
        "rs:project": "solutions",
    }

    security_group = ec2.SecurityGroup(
        "pulumi-security-group",
        description="Sam security group for Pulumi deployment",
        ingress=[
            {"protocol": "TCP", "from_port": 22, "to_port": 22, 'cidr_blocks': ['0.0.0.0/0'], "description": "SSH"},
            {"protocol": "TCP", "from_port": 8787, "to_port": 8787, 'cidr_blocks': ['0.0.0.0/0'], "description": "RSW"},
            {"protocol": "TCP", "from_port": 4242, "to_port": 4242, 'cidr_blocks': ['0.0.0.0/0'], "description": "RSPM"},
            {"protocol": "TCP", "from_port": 80, "to_port": 80, 'cidr_blocks': ['0.0.0.0/0'], "description": "HTTP"},
            {"protocol": "TCP", "from_port": 5432, "to_port": 5432, 'cidr_blocks': ['0.0.0.0/0'], "description": "POSTGRESQL"},
        ],
        egress=[
            {"protocol": "All", "from_port": -1, "to_port": -1, 'cidr_blocks': ['0.0.0.0/0'], "description": "Allow all outbound traffic"},
        ],
        tags=tags
    )

    key_pair = ec2.KeyPair(
        "ec2 key pair",
        key_name=f"{config.email}-keypair-for-pulumi",
        public_key=config.public_key,
        tags=tags | {"Name": f"{config.email}-key-pair"},
    )

    server = make_server(
        tags=tags | {"Name": "server"},
        key_pair=key_pair,
        vpc_group_ids=[security_group.id]
    )

    db = make_database(
        tags=tags | {"Name": "pgdatabase"},
        security_group=security_group
    )
    
if __name__ == '__main__':
    main()