from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class RegistrationSerializer(serializers.ModelSerializer):
    # RealWorldの入力は { "user": {...} } だが、シリアライザ自体は素直にフィールド定義でOK
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(), message="email is already taken")]
    )
    password = serializers.CharField(write_only=True, required=True, trim_whitespace=False)

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def validate_password(self, value: str) -> str:
        # Djangoのパスワードバリデータに通す（弱いパスワードを弾く）
        validate_password(value)
        return value

    def create(self, validated_data):
        # Userの作成（必ず set_password でハッシュ化）
        user = User(
            username=validated_data["username"],
            email=validated_data["email"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user
