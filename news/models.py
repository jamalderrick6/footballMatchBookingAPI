from hashlib import blake2b

from django.db import models

class Post(models.Model):
    url = models.CharField(max_length=300, unique=True);
    name = models.CharField(max_length=200)
    tags = models.TextField(max_length=1000)
    image = models.CharField(max_length=1000)
    hash_value = models.CharField(max_length=32, blank=True, null=True, unique=True)

    class Meta:
        managed = True
        db_table = 'post'

    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)
        if not self.hash_value:
            self.hash_value = blake2b(
                key=type(self).__name__.lower().encode(), digest_size=16)
            self.hash_value.update(str(self.id).encode())
            self.hash_value = self.hash_value.hexdigest()
            self.save(update_fields=['hash_value'])
