from django.db import models
# Create your models here.


class User(models.Model):
    name=models.CharField(max_length=50)
    age=models.IntegerField()
    location=models.CharField(max_length=100)
    phone_number = models.IntegerField()
    address=models.CharField(max_length=1000)
    email=models.CharField(max_length=50,default='a')
    password=models.CharField(max_length=50,default='a')
    image=models.ImageField(upload_to='user',default='nothing')
    def __str__(self):
        return self.name
    

class Game(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    timestamp=models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='games', null=True, blank=True)


    

class arena(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    def _str_(self):
        return self.title

class Slot(models.Model):
    arena = models.ForeignKey(arena, on_delete=models.CASCADE)
    start_time = models.DateField()
    end_time = models.DateField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    

class Event(models.Model):
    name=models.CharField(max_length=50,default='Arena')
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    # arena = models.ForeignKey(arena, on_delete=models.CASCADE)
    start_time = models.DateField()
    end_time = models.DateField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    max_players = models.IntegerField()
    timestamp=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

class Booking(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE,default='1')
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

class Payment(models.Model):
    bookid=models.ForeignKey(Booking,on_delete=models.CASCADE)
    cname=models.CharField(max_length=25)
    amount=models.IntegerField()
    cardno=models.IntegerField()
    cvv=models.IntegerField()
    def __str__(self):
        return self.cname
class Result(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    result =models.ImageField(upload_to='results/')
    feedback =models.CharField(max_length=100)
    def __str__(self):
        return self.feedback
class Winner(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    winner=models.ForeignKey(User,on_delete=models.CASCADE)

