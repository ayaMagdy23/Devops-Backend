from .strategy import ScalingStrategy

class AzureScalingStrategy(ScalingStrategy):
    def scale_up(self, instance):
        print(f"Scaling up Azure instance {instance.instance_id}")
        return f"Azure instance {instance.instance_id} scaled up"

    def scale_down(self, instance):
        print(f"Scaling down Azure instance {instance.instance_id}")
        return f"Azure instance {instance.instance_id} scaled down"
