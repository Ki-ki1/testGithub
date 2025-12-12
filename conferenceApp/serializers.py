from rest_framework import serializers
from .models import Conference

class ConferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conference
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")