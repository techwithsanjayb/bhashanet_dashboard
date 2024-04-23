from django.db import models
from django.utils import timezone
# Create your models here.

class category_list(models.Model):
    category_name = models.CharField(max_length=100)
    updated_On = models.DateField(default=timezone.now)
    Last_Updated_On = models.DateField(auto_now=True)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name_plural = "category_list"

class English_Domain(models.Model):
    domain_name = models.CharField(max_length=256)
    category = models.ForeignKey(category_list, on_delete=models.CASCADE)
    updated_On = models.DateField(default=timezone.now)
    Last_Updated_On = models.DateField(auto_now=True)

    def __str__(self):
        return self.domain_name

    class Meta:
        verbose_name_plural = "English_Domain"

class language_list(models.Model):
    language_name = models.CharField(max_length=25)
    updated_On = models.DateField(default=timezone.now)
    Last_Updated_On = models.DateField(auto_now=True)

    def __str__(self):
        return self.language_name

    class Meta:
        verbose_name_plural = "language_list"


# FOR instant display in status table 
class URL_dashboard(models.Model):
    English_domain =  models.ForeignKey(English_Domain, on_delete=models.CASCADE)
    Language = models.ForeignKey(language_list, on_delete=models.CASCADE)
    IDN_domain  =   models.TextField()
    ssl_configuration_status = models.TextField()
    idn_domain_running_status = models.TextField()
    content_language = models.TextField()
    updated_On = models.DateField(default=timezone.now)
    Last_Updated_On = models.DateField(auto_now=True)
    Remark = models.TextField()

    def __str__(self):
        return self.IDN_domain

    class Meta:
        verbose_name_plural = "URL_dashboard"
 
