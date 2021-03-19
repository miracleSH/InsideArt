from django.db import models

# Create your models here.
class Board(models.Model):
    writer = models.CharField(max_length = 20)
    title = models.CharField(max_length = 50)
    content = models.TextField()
    write_time = models.DateTimeField()
    read_count = models.IntegerField()
    
    class Meta:
        ordering = ('-id',)
    
class Reply(models.Model):
    board_replied = models.ForeignKey(Board, on_delete=models.CASCADE)
    writer = models.CharField(max_length = 20)
    content = models.TextField()
    write_time = models.DateTimeField()
    read_count = models.IntegerField()