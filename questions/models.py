from django.urls import reverse
from django.db import models

from hitcount.models import HitCount, HitCountMixin
from django.contrib.contenttypes.fields import GenericRelation

from groups.models import  Group

from django.contrib.auth import get_user_model
User = get_user_model()


class Question(models.Model, HitCountMixin):
    user = models.ForeignKey(User, related_name="questions", on_delete= models.DO_NOTHING('collector', 'field', 'sub_objs', 'using'))
    created_at = models.DateTimeField(auto_now=True)
    question = models.TextField()
    message_html = models.TextField(editable=False)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')
    group = models.ForeignKey(Group, related_name="questions",null=True, blank=True, on_delete= models.DO_NOTHING('collector', 'field', 'sub_objs', 'using'))
    # approved_answer = models.OneToOneField('Answer', null=True, related_name="question_accepting", on_delete= models.DO_NOTHING('collector', 'field', 'sub_objs', 'using'))

    def __str__(self):
        return self.question

    def save(self, *args, **kwargs):
        # self.message_html = misaka.html(self.message)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "questions:single",
            kwargs={
                "username": self.user.username,
                "pk": self.pk
            }
        )

    class Meta:
        ordering = ["-hit_count_generic__hits"]
        # ordering = ["-created_at"]
        unique_together = ["user", "question"]


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # user = models.ForeignKey(User, related_name="answers", on_delete= models.DO_NOTHING('collector', 'field', 'sub_objs', 'using'), null=True)
    created_at = models.DateTimeField(auto_now=True)
    answer = models.TextField()
    author = models.CharField(max_length=200, null=True)
    approved_answer = models.BooleanField(default=False)
    # message_html = models.TextField(editable=False)
    # group = models.ForeignKey(Group, related_name="answers",null=True, blank=True, on_delete= models.DO_NOTHING('collector', 'field', 'sub_objs', 'using'))

    def __str__(self):
        return self.answer

    # def save(self, *args, **kwargs):
    #     # self.message_html = misaka.html(self.message)
    #     super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "answers:single",
            kwargs={
                "username": self.user.username,
                "pk": self.pk
            }
        )

    def approve(self):
        self.approved_answer = True
        self.save()

    class Meta:
        ordering = ["-created_at"]
        # unique_together = ["user", "answer"]