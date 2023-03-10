from django.db import models

# Create your models here.
class Word(models.Model):
    word_id = models.AutoField(primary_key=True)
    spelling = models.CharField(max_length=20) # TODO: Create Full-text search index
    pronunciation = models.CharField(max_length=20)

class Meaning(models.Model):
    meaning_id = models.AutoField(primary_key=True)
    meaning = models.TextField()
    opposite_meaning_id = models.OneToOneField(
        'self',
        on_delete=models.SET_NULL,
        to_field='meaning_id',
        null=True,
        related_name='+'
    )
    N = '1'
    V = '2'
    ADJ = '3'
    ADV = '4'
    PRON = '5'
    PREP = '6'
    CONJ = '7'
    INTERJ = '8'
    PART_OF_SPEECH_CHOICES = [
        (N, 'Noun'),
        (V, 'Verb'),
        (ADJ, 'Adjective'),
        (ADV, 'Adverb'),
        (PRON, 'Pronoun'),
        (PREP, 'Preposition'),
        (CONJ, 'Conjunction'),
        (INTERJ, 'Interjection'),
    ]
    part_of_speech = models.CharField(max_length=1, choices=PART_OF_SPEECH_CHOICES) #TODO: Help text?

class Tag(models.Model):
    tag_id = models.AutoField(primary_key=True)
    tag = models.CharField(max_length=50)

class Definition(models.Model):
    definition_id = models.AutoField(primary_key=True)
    word_id = models.ForeignKey(
        Word,
        on_delete=models.CASCADE,
        to_field='word_id'
    )
    meaning_id = models.ForeignKey(
        Meaning,
        on_delete=models.CASCADE,
        to_field='meaning_id'
    )
    tag_id = models.OneToOneField(
        Tag,
        on_delete=models.SET_NULL,
        to_field='tag_id',
        null=True
    )

class Example(models.Model):
    example_id = models.AutoField(primary_key=True)
    example = models.TextField()
    definition_id = models.ForeignKey(
        Definition,
        on_delete=models.CASCADE,
        to_field='definition_id'
    )