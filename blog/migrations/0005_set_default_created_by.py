from django.db import migrations


def set_default_created_by(apps, schema_editor):
    User = apps.get_model("auth", "User")
    Article = apps.get_model("blog", "Article")

    # 建立或取得「未知使用者」
    unknown_user, _ = User.objects.get_or_create(
        username="unknown",
        defaults={
            "email": "unknown@example.com",
            "first_name": "未知",
            "last_name": "使用者",
        },
    )

    # 將所有 created_by 為 NULL 的文章設定為 unknown_user
    Article.objects.filter(created_by__isnull=True).update(created_by=unknown_user)


def reverse_set_default_created_by(apps, schema_editor):
    User = apps.get_model("auth", "User")
    Article = apps.get_model("blog", "Article")

    # 清空所有文章的 created_by
    Article.objects.filter(created_by__username="unknown").update(created_by=None)

    # 刪除未知使用者
    User.objects.filter(username="unknown").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0004_article_created_by"),
    ]

    operations = [
        migrations.RunPython(
            set_default_created_by,
            reverse_set_default_created_by,
        ),
    ]
