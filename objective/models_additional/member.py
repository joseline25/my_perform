
# from django.db import models
# import uuid
# from django.conf import settings
# from . import general_model
# from django.contrib.auth.models import AbstractUser

# # Create your models here.


# class Division(general_model.Common_Info):
#     #
#     class Meta:
#         db_table = 'Division'

#     def __str__(self) -> str:
#         return self.name


# class Position(general_model.Common_Info):
#     #
#     class Meta:
#         db_table = 'Position'

#     def __str__(self) -> str:
#         return self.name


# class Role(general_model.Common_Info):
#     # g2fdxs386d
#     class Meta:
#         db_table = 'Role'

#     def __str__(self) -> str:
#         return self.name


# class Location(general_model.Common_Info):
#     #
#     class Meta:
#         db_table = 'Location'

#     def __str__(self) -> str:
#         return self.name


# class User(AbstractUser):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     email = models.EmailField(unique=True)
#     first_name = models.CharField(max_length=50, blank=False, null=False)
#     last_name = models.CharField(max_length=50)

#     # USERNAME_FIELD = 'email'


# class Member(models.Model):
#     """This is the member class model,fields with 'blank=True' implies the form field is required at the view level
#     At the database level, it is left empty """
#     SEX_CHOICE = [
#         ('M', 'Male'),
#         ('F', 'Female')
#     ]
#     STATUS_CHOICE = [
#         ("inactive", "Inactive "),
#         ("active", "Active"),
#     ]
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     member_id = models.CharField(max_length=50, blank=True)
#     first_name = models.CharField(max_length=50, blank=False, null=False)
#     last_name = models.CharField(max_length=50)
#     date_of_birth = models.DateField(null=True)  # Date format in "YYYY-MM-DD"
#     sex = models.CharField(max_length=1, choices=SEX_CHOICE, null=True)
#     address = models.CharField(max_length=250)
#     profile_pic = models.ImageField(blank=True, null=True)
#     phone_number1 = models.CharField(max_length=50, blank=False, unique=True)
#     phone_number2 = models.CharField(max_length=50)
#     email = models.EmailField(blank=False, unique=True)
#     division = models.ForeignKey(
#         Division, on_delete=models.SET_NULL, null=True, blank=True, db_column='division')
#     position = models.ForeignKey(
#         Position, on_delete=models.SET_NULL, null=True, blank=True, db_column='position')
#     location = models.ForeignKey(
#         Location, on_delete=models.SET_NULL, null=True, blank=True, db_column='location')
#     roles = models.ManyToManyField(
#         Role, through='Member_Role', through_fields=('member_id', 'role_id'))
#     supervisor_id = models.ForeignKey(
#         'self', on_delete=models.SET_NULL, null=True, blank=True, db_column="supervisor_id")
#     hired_date = models.DateField(null=True, blank=True)
#     lastUpdate = models.DateTimeField(auto_now=True)
#     user = models.OneToOneField(
#         settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     created_by = models.ForeignKey('self', on_delete=models.SET_NULL,
#                                    related_name="registered_by", null=True, db_column="created_by")
#     updated_by = models.ForeignKey('self', on_delete=models.SET_NULL,
#                                    null=True, related_name="edited_by", db_column="updated_by")

#     class Meta:
#         """This enforces  """
#         db_table = "Member"
#         indexes = [
#             models.Index(fields=["first_name", "last_name", "email"])]

#     @property
#     def full_name(self):
#         "Returns the person's full name."
#         return '%s %s' % (self.user.first_name, self.user.last_name)

#     def __str__(self) -> str:
#         return self.first_name


# class Member_Role(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     member_id = models.ForeignKey(Member, on_delete=models.CASCADE)
#     role_id = models.ForeignKey(
#         Role, on_delete=models.CASCADE, db_column='role')
#     start_date = models.DateField(auto_now=True)
#     end_date = models.DateField(auto_now=True, null=True, blank=True)
#     assigned_by = models.ForeignKey(Member, on_delete=models.CASCADE, null=True,
#                                     blank=True, related_name='assigned_by', db_column='assigned_by')

#     class Meta:
#         """This enforces  """
#         db_table = "Member_Role"
