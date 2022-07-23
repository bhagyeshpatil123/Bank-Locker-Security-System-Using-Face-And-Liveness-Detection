from django.db import models

#https://docs.djangoproject.com/en/3.2/ref/models/fields/

# Create your models here.
class UserModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, null=False, help_text='User Name')
    mobile = models.CharField(max_length=14, null=False, help_text='User Mobile', db_index=True) #apply indexes
    email = models.EmailField(max_length=40, unique=True, null=False, help_text='User Email')
    password = models.CharField(max_length=300, null=False, help_text='User Password')
    address = models.CharField(max_length=100, null=False, help_text='User Address')
    balance =models.IntegerField(null=False, default=1000, help_text='User Balance')

    #help_text attribute is used to display the “help” text along with the field in form in admin interface or ModelForm.
    #Putting {{ form.as_p }} (or just {{ form }}) in your template should display the help_text without additional code
    # use {{ form.field.help_text }} to access the help text of particular field.

    def __str__(self):
        return self.name

    class Meta:
        # table name
        db_table = 'user'

        #apply indexes
        indexes = [
            models.Index(fields=['email','password']),
        ]


class TransactionModel(models.Model):
    id = models.AutoField(primary_key=True)
    trans_from = models.ForeignKey(UserModel, on_delete=models.CASCADE, db_column='trans_from', help_text='Transfer From', related_name='trans_from2')
    trans_to = models.ForeignKey(UserModel, on_delete=models.CASCADE, db_column='trans_to', help_text='Transfer To', related_name='trans_to2')
    amount = models.IntegerField()
    trans_on = models.DateTimeField(auto_now_add=True, blank=False, null=False, help_text='Transaction Time',editable=False)  # cant edit this field because of editable

    def __str__(self):
        return str(self.id)

    class Meta:
        # table name
        db_table = 'transaction'
