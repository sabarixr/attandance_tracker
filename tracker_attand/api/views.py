from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from rest_framework import generics,status,permissions
from rest_framework.response import Response
from .permissions import *
from .searilizer import *
from .models import *
from rest_framework.authtoken.views import ObtainAuthToken,APIView

#class TeacherSingUpview(generics.GenericAPIView):
#    serializer_class = TeacherSingUpSerializer
#    def post(self, request,*args, **kwargs):
#        serializer = self.get_serializer(data= request.data)
#        serializer.is_valid(raise_exception = True)
#        user = serializer.save()
#        return Response({
#            "user": UserSerializer(user, context = self.get_serializer_context()).data,
#            "token": Token.objects.get(user=user).key,
#            "message": "Account created successfully"
#        })
    
#class StudentSingUpview(generics.GenericAPIView):
#    serializer_class = StudentSingUpSerializer
#    def post(self, request,*args, **kwargs):
#        serializer = self.get_serializer(data= request.data)
#        serializer.is_valid(raise_exception = True)
#        user = serializer.save()
#        return Response({
#            "user": UserSerializer(user, context = self.get_serializer_context()).data,
#            "token": Token.objects.get(user=user).key,
#            "message": "Account created successfully"
#        })
    
class LoginAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'is_student': user.is_student,
            'uid' : user.uid 
        })

    
class LogoutView(APIView):
    def post(self, request, format = None):
        request.user.auth_token.delete()
        return Response(status = status.HTTP_200_OK)
    
class TeacherOnlyView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsTeacher, permissions.IsAuthenticated]  

    def get_object(self):
        return self.request.user

class StudentOnlyView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsStudent, permissions.IsAuthenticated] 

    def get_object(self):
        return self.request.user



class CourseNameListView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class CourseNameDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class ClassNameListView(generics.ListCreateAPIView):
    serializer_class = ClassnameSerializer

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        return Classname.objects.filter(course_id=course_id)

    def perform_create(self, serializer):
        course_id = self.kwargs['course_id']
        course = get_object_or_404(Course, pk=course_id)
        serializer.save(course_id=course)  

class ClassNameDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ClassnameSerializer

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        return Classname.objects.filter(course_id=course_id)
class HourListCreateView(generics.ListCreateAPIView):
    serializer_class = TrCreateHourSerializer

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        class_id = self.kwargs['class_id']
        return TeacherCreateHour.objects.filter(course_id=course_id, class_id=class_id)

    def perform_create(self, serializer):
        course_id = self.kwargs['course_id']
        class_id = self.kwargs['class_id']
        course = get_object_or_404(Course, pk=course_id)
        classname = get_object_or_404(Classname, pk=class_id)
        serializer.save(course_id=course, class_id=classname)

class HourListDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TrCreateHourSerializer
    
    def get_queryset(self):
        students = User.objects.all()
        course_id = self.kwargs['course_id']
        class_id = self.kwargs['class_id']
        return TeacherCreateHour.objects.filter(course_id=course_id, class_id=class_id)
class TeacherScanView(APIView):
    def post(self, request, *args, **kwargs):
        user_info = User.objects.all()
        for students in user_info:
            print(students.uid)
        serializer = TeacherScanPostSerializer(data=request.data)
        if serializer.is_valid():
            scan_instance = serializer.save()
            self.create_attendance_entry(scan_instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create_attendance_entry(self, scan_instance):
        user_peops = User.objects.all()
        for students in user_peops:
            print(students.uid)
        print(scan_instance.special_uid)
        active_tr_scan = User.objects.filter(uid = scan_instance.special_uid).first()
        print(active_tr_scan)
        if active_tr_scan:
            course_det = Course.objects.filter(id=scan_instance.course_id.id).first()
            course_name = course_det.course_name if course_det else None
            print(scan_instance.course_id)
            print(scan_instance.class_id)
            print(scan_instance.hour_id)
            course_ = scan_instance.course_id.id
            print(course_)
            class_ = scan_instance.class_id.id
            print(class_)
            hour_ = scan_instance.hour_id.id
            print(class_)
            if course_name == active_tr_scan.course:
                AttendanceList.objects.create(
                    course_id = course_,
                    class_id =class_,
                    hour_id =hour_,
                    date = timezone.now().date(),
                    uid=active_tr_scan.email,
                    name=active_tr_scan.name
                    )

class AttendanceSessionListView(generics.ListAPIView):
    serializer_class = AttendanceListSerializer

    def get_queryset(self):
        #for _ in AttendanceList.objects.all():
            #print(_.course_id)
            #print(_.class_id)
            #print(_.hour_id)
            #print("\n")
        #course_id = self.kwargs.get('course_id')
        #class_id = self.kwargs.get('class_id')
        #hour_id = self.kwargs.get('hour_id')
        print(AttendanceList.objects.all())
        return AttendanceList.objects.all()
    #filter(course_id =course_id, class_id = class_id, hour_id=hour_id)