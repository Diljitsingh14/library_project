from rest_framework import serializers
from books.models import shells

class shellSerializer(serializers.ModelSerializer):
    class Meta:
        model = shells
        fields = "__all__"