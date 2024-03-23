from rest_framework import serializers
from .models import Question, Answer


class PersonSerialiser(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    age = serializers.IntegerField()
    email = serializers.EmailField()


class QuestionSer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField()
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Question
        fields = '__all__'

    def get_answers(self, obj):
        resault = obj.qanswer.all()
        return AnswerSer(instance=resault, many=True).data


class AnswerSer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'
