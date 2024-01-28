from django.forms import ValidationError
from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        #['username', 'email', 'is_student']


#class TeacherSingUpSerializer(serializers.ModelSerializer):
#    password2 = serializers.CharField(style= {"input_type": "password"}, write_only = True)
#    class Meta:
#        model = User
#        fields = ['username', 'email', 'password','password2']
#        extra_kwargs={
#            'password':{'write_only': True}
#        }
#    def save(self, **kwargs):
#        user = User(
#            username=self.validated_data['username'],
#            email=self.validated_data['email']
#        )
#        password = self.validated_data['password']
#        password2 = self.validated_data['password2']
#
#        if password != password2:
#            raise ValidationError({"error": "password doesn't match"})
#
#        user.set_password(password)
#        user.is_teacher = True
#        user.save() 
#        Teacher.objects.create(user=user)
#        return user
#
#class StudentSingUpSerializer(serializers.ModelSerializer):
#    password2 = serializers.CharField(style= {"input_type": "password"}, write_only = True)
#    class Meta:
#        model = User
#        fields = ['username', 'email', 'password','password2']
#        extra_kwargs={
#            'password':{'write_only': True}
#        }
#    def save(self, **kwargs):
#        user = User(
#            username=self.validated_data['username'],
#            email=self.validated_data['email']
#        )
#        password = self.validated_data['password']
#        password2 = self.validated_data['password2']
#
#        if password != password2:
#            raise ValidationError({"error": "password doesn't match"})
#
#        user.set_password(password)
#        user.is_student = True
#        user.save() 
#        Student.objects.create(user=user)
#        return user


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
class ClassnameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classname
        fields = '__all__'
class TrCreateHourSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherCreateHour
        fields = '__all__'

    

class TeacherScanPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherScanPost
        fields = '__all__'
class AttendanceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceList
        fields = '__all__'
