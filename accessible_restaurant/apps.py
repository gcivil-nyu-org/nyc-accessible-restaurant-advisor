from django.apps import AppConfig


class AccessibleRestaurantConfig(AppConfig):
    name = "accessible_restaurant"

    def ready(self):
        import accessible_restaurant.signals
