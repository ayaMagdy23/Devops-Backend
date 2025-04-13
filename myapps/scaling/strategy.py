from abc import ABC, abstractmethod

class ScalingStrategy(ABC):
    """
    Abstract base class for scaling strategies.
    """

    @abstractmethod
    def scale_up(self, instance):
        pass

    @abstractmethod
    def scale_down(self, instance):
        pass
