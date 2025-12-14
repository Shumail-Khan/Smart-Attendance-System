from rest_framework import serializers
from .models import Person

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = "__all__"


# # apps/persons/serializers.py
# from rest_framework import serializers
# from .models import Person

# class PersonSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Person
#         fields = [
#             'pid', 'person_name', 'person_nic', 'person_father',
#             'person_designation', 'person_cat', 'person_embedding',
#             'created_at', 'updated_at',
#         ]
#         read_only_fields = ('created_at', 'updated_at',)

# class PersonCreateSerializer(serializers.ModelSerializer):
#     # Accept uploaded images as files (for enrollment, optional)
#     images = serializers.ListField(
#         child=serializers.ImageField(max_length=None, allow_empty_file=False, use_url=False),
#         write_only=True,
#         required=False,
#         help_text="Upload 3-5 images for enrollment"
#     )

#     class Meta:
#         model = Person
#         fields = [
#             'pid', 'person_name', 'person_nic', 'person_father',
#             'person_designation', 'person_cat', 'images',
#         ]

#     def create(self, validated_data):
#         # Pop images out - enrollment happens through separate endpoint
#         images = validated_data.pop('images', [])
#         person = Person.objects.create(**validated_data, person_embedding='')
#         # You can trigger background task here to call AI backend for embedding
#         # For now we just create the record; enrollment endpoint will update embedding.
#         return person
