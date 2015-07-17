from networkbase import NetworkBase
from troposphere import ec2, Tags, Base64

class ElkStack(NetworkBase):
    '''
    ELK stack template generation
    '''

    def create_action(self):
        self.initialize_template()

        self.create_logstash()
        self.create_kibana()
        self.create_elastisearch()

        # This triggers serialization of the template and any child stacks
        self.write_template_to_file()

    def create_logstash(self):
        startup = '''#!/bin/bash

rpm --import https://packages.elasticsearch.org/GPG-KEY-elasticsearch

cat <<EOF >> /etc/yum.repos.d/elasticsearch.repo
[elasticsearch-1.4]
name=Elasticsearch repository for 1.4.x packages
baseurl=http://packages.elasticsearch.org/elasticsearch/1.4/centos
gpgcheck=1
gpgkey=http://packages.elasticsearch.org/GPG-KEY-elasticsearch
enabled=1
EOF

yum -y install elasticsearch

service elasticsearch restart

# it's listening to the world, lock down later and via SG and VPCs, etc...
# edit /etc/elasticsearch/elasticsearch.yml to change where it listens to.
        '''

        # this resource needs to be dropped into a VPC.  For now, we can use a public subnet.
        res = ec2.Instance("logstash", InstanceType="m3.medium", ImageId="ami-951945d0",
            Tags=Tags(Name="logstash",), UserData=Base64(startup))
        self.template.add_resource(res)

    def create_kibana(self):
        # this resource needs to be dropped into a VPC.  For now, we can use a public subnet.
        res = ec2.Instance("kibana", InstanceType="m3.medium", ImageId="ami-951945d0", Tags=Tags(Name="kibana",))
        self.template.add_resource(res)

    def create_elastisearch(self):
        # this resource needs to be dropped into a VPC.  For now, we can use a public subnet.
        res = ec2.Instance("es", InstanceType="m3.medium", ImageId="ami-951945d0", Tags=Tags(Name="es",))
        self.template.add_resource(res)

if __name__ == '__main__':
    ElkStack()
