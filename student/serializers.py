from rest_framework import serializers
from .models import PlacementProfile

class PlacementProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlacementProfile
        exclude = ("user",)

    def create(self, validated_data):
        user = self.context["request"].user
        return PlacementProfile.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()
        return instance
