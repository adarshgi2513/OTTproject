from rest_framework import serializers

from .models import Sub

class subSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sub
        fields = '__all__'