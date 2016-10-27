from django.db import models


class SystemData(models.Model):

    class Meta:
        verbose_name = "System Data"
        verbose_name_plural = "System Data"

    name = models.CharField(max_length=45)
    description = models.TextField()
    keywords = models.TextField()
    author = models.CharField(max_length=50)
    acronym_author = models.CharField(max_length=7)
    site_author = models.URLField()

    brand = models.ImageField(upload_to='dashboard/logos', help_text='Height: 64px', blank=True)
    favicon = models.ImageField(upload_to='dashboard/logos', help_text='Resolution: 64x64', blank=True)
    primary_color_class = models.CharField(max_length=45)
    primary_color_hex = models.CharField(max_length=7)
    secondary_color_class = models.CharField(max_length=45)
    secondary_color_hex = models.CharField(max_length=7)

    def __str__(self):
        return self.name


class MenuItem(models.Model):

    class Meta:
        verbose_name = "Menu Item"
        verbose_name_plural = "Menu Items"

    label = models.CharField(max_length=45)
    url = models.CharField(max_length=45)
    icon = models.CharField(max_length=45)
    order = models.PositiveIntegerField(unique=True)

    def __str__(self):
        return self.label
    