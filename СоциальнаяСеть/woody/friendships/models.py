from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q


class FriendRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('accepted', 'Принята'),
        ('rejected', 'Отклонена'),
    ]

    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Заявка от {self.from_user} к {self.to_user} ({self.status})'


class Friendship(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends2')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user1', 'user2']
        ordering = ['-created_at']

    def __str__(self):
        return f'Дружба: {self.user1} и {self.user2}'


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['follower', 'following']
        indexes = [
            models.Index(fields=['follower', 'following']),
        ]

    def __str__(self):
        return f'{self.follower.username} подписан на {self.following.username}'

    def save(self, *args, **kwargs):
        created = not self.pk
        super().save(*args, **kwargs)

        if created:
            self.follower.profile.following_count = Follow.objects.filter(follower=self.follower).count()
            self.follower.profile.save()

            self.following.profile.followers_count = Follow.objects.filter(following=self.following).count()
            self.following.profile.save()

    def delete(self, *args, **kwargs):
        follower_profile = self.follower.profile
        following_profile = self.following.profile

        super().delete(*args, **kwargs)

        follower_profile.following_count = Follow.objects.filter(follower=self.follower).count()
        follower_profile.save()

        following_profile.followers_count = Follow.objects.filter(following=self.following).count()
        following_profile.save()