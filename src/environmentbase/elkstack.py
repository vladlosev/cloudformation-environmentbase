from networkbase import NetworkBase
from troposphere import ec2, Tags

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
        res = ec2.Instance("logstash", InstanceType="m3.medium", ImageId="ami-951945d0", Tags=Tags(Name="logstash",))
        self.template.add_resource(res)

    def create_kibana(self):
        res = ec2.Instance("kibana", InstanceType="m3.medium", ImageId="ami-951945d0", Tags=Tags(Name="kibana",))
        self.template.add_resource(res)

    def create_elastisearch(self):
        res = ec2.Instance("es", InstanceType="m3.medium", ImageId="ami-951945d0", Tags=Tags(Name="es",))
        self.template.add_resource(res)

if __name__ == '__main__':
    ElkStack()
