from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from quotes.models import Quote, Author, Category

User = get_user_model()

class QuoteSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    category = serializers.StringRelatedField(many=True)

    class Meta:
        model = Quote
        fields = ['quote', 'author', 'category']

class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields='__all__'


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length = 150, validators = [UniqueValidator(queryset=User.objects.all(), message='Пользователь с таким логином уже существует')])
    first_name = serializers.CharField(required = False, allow_blank=True)
    last_name = serializers.CharField(required = False, allow_blank=True)
    email = serializers.EmailField(validators = [UniqueValidator(queryset=User.objects.all(), message='Пользователь с таким email уже существует')])
    password1 = serializers.CharField(write_only=True, min_length = 8, label = 'Пароль')
    password2 = serializers.CharField(write_only=True, min_length = 8, label = 'Подтверждение пароля')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
    
    def validate(self, attrs):
        
        if attrs['password1']!=attrs['password2']:
            raise serializers.ValidationError({'password2':'Пароли не совпадают'})
        return attrs
    

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            first_name=validated_data.get('first_name',''),
            last_name=validated_data.get('last_name',''),
            email=validated_data['email'],
            password=validated_data['password1'],
        )
        return user
        

class CreateQuoteSerializer(serializers.ModelSerializer):
    quote = serializers.CharField()
    author = serializers.PrimaryKeyRelatedField(queryset = Author.objects.all(), required=False)
    new_author = serializers.CharField(required = False, max_length = 250)
    biography = serializers.CharField(required = False)
    photo = serializers.ImageField(required = False)
    categories = serializers.PrimaryKeyRelatedField(queryset = Category.objects.all(), many=True,required = False)
    new_categories = serializers.CharField(required = False)


    class Meta:
        model = Quote
        fields = ['quote', 'author', 'new_author', 'biography', 'photo', 'categories', 'new_categories']
    
    def validate(self, attrs):
        if not attrs.get('author', '') and not attrs.get('new_author', ''):
            raise serializers.ValidationError({'author':'Вы должны выбрать уже существующего автора или написать своего'})
        
        if not attrs.get('categories', '') and not attrs.get('new_categories', ''):
            raise serializers.ValidationError({'categories':'Вы должны выбрать из уже существующих категорий или написать свои'})

        return attrs
    
    def create(self, validated_data):
        author = self.validated_data.get('author', None) if self.validated_data.get('author', None) else self.validated_data['new_author'].title()
        biography = self.validated_data.get('biography','')
        photo = self.validated_data.get('photo', None)
        categories = list(self.validated_data['categories'])

        if Author.objects.filter(name = author).exists():
            author =  Author.objects.get(name = author)
        else:
            author,_ = Author.objects.get_or_create(name=author, biography=biography, photo=photo)
        
        for cat in self.validated_data.get('new_categories','').split(','):
            if cat:
                cat = cat.strip().capitalize()
                category,_ = Category.objects.get_or_create(name = cat)
                categories.append(category)
        
        quote = Quote.objects.create(quote=self.validated_data['quote'], author = author)
        quote.category.set(categories)
        quote.user = self.context['request'].user
        quote.save()

        return quote

class SaveQuoteSerializer(serializers.Serializer):
    quote_id = serializers.IntegerField() 
    
    def validated_quote_id(self, value):
        if not Quote.objects.filter(id=value).exists():
            raise serializers.ValidationError('Данной цитаты не существует')
        return value
    
    def create(self, validated_data):
        quote = Quote.objects.get(id = validated_data.get('quote_id'))
        
        user = self.context['request'].user
        user.profile.saved_quotes.add(quote)
        user.save()
        return quote




class SuggestedQuotesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Quote
        fields = ['quote', 'author', 'category', 'status']



        
    


