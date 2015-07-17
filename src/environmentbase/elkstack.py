from networkbase import NetworkBase
from troposphere import ec2

class ElkStack(NetworkBase):
    '''
    ELK stack template generation
    '''

    def create_action(self):
        self.initialize_template()

        # Add some stuff
        res = ec2.Instance("ec2instance", InstanceType="m3.medium", ImageId="ami-951945d0")
        self.template.add_resource(res)

        # This triggers serialization of the template and any child stacks
        self.write_template_to_file()

if __name__ == '__main__':
    ElkStack()
