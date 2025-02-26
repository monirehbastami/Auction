from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items')
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='items/', blank=True, null=True)  
    bid_count = models.IntegerField(default=0)
    views_count = models.IntegerField(default=0)
    likes_count = models.IntegerField(default=0)
    status = models.CharField(max_length=20, default='Active')

    def get_time_left(self):
        import re
        from datetime import timedelta
        from django.utils import timezone

        total_duration = timedelta()
        matches = re.findall(r'(\d+)\s*(day|d|hour|h|minute|min|m)', self.duration, re.IGNORECASE)
        for amount, unit in matches:
            amount = int(amount)
            unit = unit.lower()
            if unit in ['day', 'd']:
                total_duration += timedelta(days=amount)
            elif unit in ['hour', 'h']:
                total_duration += timedelta(hours=amount)
            elif unit in ['minute', 'min', 'm']:
                total_duration += timedelta(minutes=amount)
        end_time = self.created_at + total_duration
        now = timezone.now()
        time_left = end_time - now
        if time_left.total_seconds() <= 0:
            return "Expired"
        days = time_left.days
        seconds = time_left.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        parts = []
        if days > 0:
            parts.append(f"{days}d")
        if hours > 0 or days > 0:
            parts.append(f"{hours}h")
        parts.append(f"{minutes}m")
        return " ".join(parts)

    def __str__(self):
        return self.name


class Bid(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='bids')
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bidder.username} bid ${self.amount} on {self.item.name}"