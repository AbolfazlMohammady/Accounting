import re
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.exceptions import PermissionDenied
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status, viewsets, mixins, permissions

from .serializer import ProfileSeializer, UserSerializer
from .models import User


class LoginOrRegisterView(APIView):

    def validate_password(self, password):
        if len(password) <= 7:
            return "رمز عبور باید حداقل ۸ کاراکتر باشد."
        if not re.search(r'[a-z]',password):
            return "رمز عبور باید حداقل یک حرف کوچک انگلیسی داشته باشد."
        if not re.search(r'[0-9]',password):
            return "رمز عبور باید حداقل یک عدد داشته باشد."
        if len(password)>=16:
            return 'پسورد نمیتواند بیشتر از 16 کارکتر باشد'
        return None
    

    def post(self, request, *args, **kwargs):
        phone_or_email = request.data.get('phone_or_email')
        password = request.data.get('password')

        if not phone_or_email or not password:
            return Response(
                {"error": "شماره تلفن/ایمیل و رمز عبور الزامی است."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        password_error = self.validate_password(password)
        if password_error:
            return Response({'error': password_error},status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.filter(phone=phone_or_email).first() or User.objects.filter(email=phone_or_email).first()

        if user:
            if not user.check_password(password):
                return Response({'error':'رمز عبور اشتباه است🏴‍☠️'},status=status.HTTP_400_BAD_REQUEST)

            user_exists = True
        else:
            if '@' in phone_or_email:
                data = {'email':phone_or_email, 'password':password}
            else:
                data = {'phone':phone_or_email, 'password':password}

            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                user = serializer.save()
                user.set_password(password)
                user.save()
                user_exists = False
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        refresh = RefreshToken.for_user(user)
        
        return Response(
            {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'message': "کاربر جدید ثبت شد." if not user_exists else "ورود موفقیت‌آمیز.",
        },
        status=status.HTTP_200_OK
        )


class ProfileViewSet(viewsets.ViewSet):
    permission_classes =[permissions.IsAuthenticated]

    def retrieve(self, request):
        serializer = ProfileSeializer(request.user)
        return Response(serializer.data)

    def update(self, request):
        serializer = ProfileSeializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def change_password(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not old_password or not new_password:
            return Response(
                {"detail": "هر دو فیلد 'رمز عبور قدیمی' و 'رمز عبور جدید' لازم هستند."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not check_password(old_password, user.password):
            return Response(
                {"detail": "رمز عبور قدیمی اشتباه است."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        user.set_password(new_password)
        user.save()
        return Response({"detail": "رمز عبور با موفقیت تغییر کرد."}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def delete_account(self, request):
        user = request.user
        confirm = request.data.get('confirm')

        if confirm != "yes":
            return Response(
                {"detail": "برای حذف حساب، باید تایید کنید."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if confirm == "yes":
            user.is_active = False
            user.save()
            
            # user.delete()  

            return Response({"detail": "حساب کاربری شما با موفقیت حذف شد."}, status=status.HTTP_200_OK)