from django.db import models

class QA(models.Model):
    id = models.AutoField(primary_key=True)
    answer = models.CharField(max_length=10000, null=True)
    question = models.CharField(max_length=10000, null=True)
    tags = models.CharField(max_length=1000, null=True)

class Services(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=500, null=True)
    link = models.CharField(max_length=500, null=True)
    tags = models.CharField(max_length=255, null=True)
    how_to_use = models.CharField(max_length=10000, null=True)
    qa_id = models.CharField(max_length=1000, null=True)

class Prompts(models.Model):
    id = models.AutoField(primary_key=True)
    prompt = models.CharField(max_length=10000, null=True)
    description = models.CharField(max_length=10000, null=True)
    qa_id = models.CharField(max_length=1000, null=True)

class Videos(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=500, null=True)
    link = models.CharField(max_length=500, null=True)
    tags = models.CharField(max_length=255, null=True)
    qa_id = models.CharField(max_length=1000, null=True)

class Guides(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=500, null=True)
    link = models.CharField(max_length=500, null=True)
    tags = models.CharField(max_length=255, null=True)
    summary = models.CharField(max_length=10000, null=True)
    qa_id = models.CharField(max_length=1000, null=True)

class Books(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=500, null=True)
    link = models.CharField(max_length=500, null=True)
    tags = models.CharField(max_length=255, null=True)
    summary = models.CharField(max_length=10000, null=True)
    qa_id = models.CharField(max_length=1000, null=True)

class Docs(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=500, null=True)
    link = models.CharField(max_length=500, null=True)
    description = models.CharField(max_length=10000, null=True)
    qa_id = models.CharField(max_length=1000, null=True)

class Interviews(models.Model):
    id = models.AutoField(primary_key=True)
    topic = models.CharField(max_length=500, null=True)
    name = models.CharField(max_length=500, null=True)
    job_title = models.CharField(max_length=10000, null=True)
    response = models.CharField(max_length=10000, null=True)

class RequestsHistory(models.Model):
    user = models.CharField(max_length=100)
    content = models.CharField(max_length=10000)
    model = models.CharField(max_length=100)
    date = models.DateField()
    response = models.CharField(max_length=10000)