from django import forms
from .models     import Owner
from cafe.models import Cafe,Cafe_image
import bcrypt
import re

class loginPostForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control','placeholder': '이메일'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'placeholder': '비밀번호'}))


class signupPostForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control',
                                                            'placeholder': '이메일'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'placeholder': '비밀번호'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control offset-md-1',
                                                                 'placeholder': '비밀번호 확인'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                          'placeholder': '전화번호'}))
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control pe-150',
                                                         'placeholder': '카페명'}))
    human = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                                'maxlength': '4',
                                                                'placeholder': '최대수용인원'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control',
                                                            'maxlength': '20',
                                                            'id': 'address_kakao',
                                                            'readonly':'True',
                                                            'placeholder': '주소'}))
    address2 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'name': 'address_detail',
                                                             'placeholder':'상세 주소'}))
                                                            
    # 카페 이미지 추가해야함 


    # email이 이미 등록되었는지, 그리고 이메일 형식에 맞는지에 대한 validation
    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            Owner.objects.get(owner_id=email) # 필드에 email 값이 db에 존재하는지 확인
            raise forms.ValidationError("이미 등록된 이메일 입니다.")
        except Owner.DoesNotExist:
            pattern = re.compile('^.+@+.+\.+.+$') #이메일 '@'앞에는 아무 문자가 제한 없이 들어올 수 있음
            if not pattern.match(email):
                 raise forms.ValidationError("이메일 주소에 '@를 포함해 주세요")
            else:
                return email  #db에 존재하지 않고, 이메일 형식이 맞다면 데이터를 반환
    
    # 입력한 password가 조건에 맞는지에 대한 validation
    def check_password(self):
        password = self.cleaned_data.get("password") 
        # 영어,숫자,특수문자 포함하고 8~25자리수를 허용
        pattern = re.compile('^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*()])[\w\d!@#$%^&*()]{8,25}$')
        if not pattern.match(password):
            raise forms.ValidationError("비밀번호는 영문(소문자, 대문자), 숫자, 특수문자를 조합하여 8~25까지 가능합니다.")
        else:
            return password
            
    # 두개의 password가 일치한지에 대한 validation 
    def clean_password1(self):
        password = self.cleaned_data.get("password") 
        password2 = self.cleaned_data.get("password2") 
        if password != password2:
            raise forms.ValidationError("비밀번호가 다릅니다.")
        else:
            return password

    #DB에 저장
    def save(self):
        # 사장
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        phone = self.cleaned_data.get("phone")

        # 카페
        name = self.cleaned_data.get("name")
        human = self.cleaned_data.get("human")
        address = self.cleaned_data.get("address")
        address2 = self.cleaned_data.get("address2")
        #cafe_phone = self.cleaned_data.get("cafe_phone")

        # 카페이미지
        # image = self.cleaned_data.get("image")

        make = Cafe.objects.create(
            name = name,
            max_occupancy = human,
            address = address,
            datail_add = address2,
            cafe_phone = phone
        )

        Owner.objects.create(           
            owner_id = email,
            phone = phone,
            password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            cafe = make #모델 id만 넘기도록 작성하기
        )

        # Cafe_image.objects.create(
        #     image = image,
        #     cafe = make.cafe_id
        # )