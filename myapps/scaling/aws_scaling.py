from .strategy import ScalingStrategy

class AWSScalingStrategy(ScalingStrategy):
    def scale_up(self, instance):
        print(f"Scaling up AWS instance {instance.instance_id}")
        return f"AWS instance {instance.instance_id} scaled up"

    def scale_down(self, instance):
        print(f"Scaling down AWS instance {instance.instance_id}")
        return f"AWS instance {instance.instance_id} scaled down"
