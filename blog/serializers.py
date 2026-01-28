from rest_framework import serializers

from blog.models import Article, Author

# class ArticleSerializer(serializers.Serializer):
# id = serializers.IntegerField(read_only=True)
# title = serializers.CharField(max_length=200)
# content = serializers.CharField()
# is_published = serializers.BooleanField(default=False)
# created_by = serializers.PrimaryKeyRelatedField(read_only=True)
# created_at = serializers.DateTimeField(read_only=True)
# updated_at = serializers.DateTimeField(read_only=True)

# def create(self, validated_data):
#     """建立新的 Article 物件"""
#     return Article.objects.create(**validated_data)

# def update(self, instance, validated_data):
#     """更新現有的 Article 物件"""
#     instance.title = validated_data.get("title", instance.title)
#     instance.content = validated_data.get("content", instance.content)
#     instance.is_published = validated_data.get(
#         "is_published", instance.is_published
#     )
#     instance.save()
#     return instance


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "content",
            "is_published",
            "created_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_by", "created_at", "updated_at"]


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = [
            "name",
            "email",
            "created_at",
        ]
        read_only_fields = ["created_at"]
