from .aws_scaling import AWSScalingStrategy
from .azure_scaling import AzureScalingStrategy

class ScalingContext:
    def __init__(self, instance):
        self.instance = instance
        self.strategy = self.get_strategy()

    def get_strategy(self):
        if self.instance.provider == "AWS":
            return AWSScalingStrategy()
        elif self.instance.provider == "Azure":
            return AzureScalingStrategy()
        else:
            raise ValueError("Unsupported cloud provider")

    def scale_up(self):
        return self.strategy.scale_up(self.instance)

    def scale_down(self):
        return self.strategy.scale_down(self.instance)
