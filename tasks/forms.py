from django import forms
from .models import Task
from django.contrib.auth.models import User

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'priority', 'due_date', 'assigned_to']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'assigned_to': forms.CheckboxSelectMultiple(),
        }

class TaskStatusForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['status']

class UserForm(forms.ModelForm):
    ROLE_CHOICES = [
        (False, 'User'),
        (True, 'Admin'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, label="Role")
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class UserEditForm(forms.ModelForm):
    ROLE_CHOICES = [
        (False, 'User'),
        (True, 'Admin'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, label="Role")

    class Meta:
        model = User
        fields = ['username', 'email']

    new_password = forms.CharField(
        widget=forms.PasswordInput(),
        required=False,
        label="New Password",
        help_text="Leave blank to keep current password."
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(),
        required=False,
        label="Confirm New Password",
    )
    old_password = forms.CharField(
        widget=forms.PasswordInput(),
        required=False,
        label="Old Password (Optional)",
        help_text="Leave blank to reset password without verification (admin override)."
    )

    def __init__(self, *args, **kwargs):
        self.request_user = kwargs.pop('request_user', None)
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields['role'].initial = self.instance.is_staff

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")
        old_password = cleaned_data.get("old_password")

        if new_password:
            if new_password != confirm_password:
                self.add_error('confirm_password', "Passwords do not match.")
            
            # Verify old password only if provided
            if old_password and not self.instance.check_password(old_password):
                self.add_error('old_password', "Incorrect old password.")
        
        return cleaned_data
