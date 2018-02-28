from django.db import models

class Bulletin_Board(models.Model):
    subject = models.CharField(max_length=50, blank=True)
    name = models.CharField(max_length=50, blank=True)
    created_date = models.DateField(null=True, blank=True)
    mail = models.CharField(max_length=50, blank=True)
    memo = models.CharField(max_length=200, blank=True)
    hits = models.IntegerField(null=True, blank=True)
    secret_board = models.BooleanField(default=False)
    secret_board_key = models.CharField(max_length=10, blank=True)
	

    def __str__(self):
        return self.subject
	
	
class Reply(models.Model):
    subject_text = models.ForeignKey(Bulletin_Board, on_delete=models.CASCADE)
    reply_text = models.CharField(max_length=200)
    name = models.CharField(max_length=50, blank=True)
    pub_date = models.DateTimeField('date published')
	
    def __str__(self):
        return self.reply_text
