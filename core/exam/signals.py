from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Question, Test


@receiver(post_save, sender=Question)
def update_question_count(sender, instance, **kwargs):
    # Update the question count for the associated test
    test = instance.test
    test.question_count = test.questions.count()
    test.save()
