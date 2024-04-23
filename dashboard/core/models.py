from django.db import models

# Create your models here.

class category_list(models.Model):
    category_name = models.CharField(max_length=100)  

class English_Domain(models.Model):
    domain_name = models.CharField(max_length=256)
    category = models.ForeignKey(category_list, on_delete=models.CASCADE)

class language_list(models.Model):
    language_name = models.CharField(max_length=25)


# FOR instant display in status table 
class URL_dashboard(models.Model):
    English_domain =  models.ForeignKey(English_Domain, on_delete=models.CASCADE)
    Language = models.ForeignKey(language_list, on_delete=models.CASCADE)
    IDN_domain  =   models.TextField()
    ssl_configuration_status = models.BooleanField(default=True)
    idn_domain_running_status = models.BooleanField(default=True)
    content_language = models.TextField()
    updated_On = models.DateField(auto_now_add=True)
    Last_Updated_On = models.DateField(auto_now=True)
    Remark = models.TextField()

 
