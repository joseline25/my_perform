# Model

```python
class ActionMainEntry(models.Model):
    achievements_values = [
        ('Learnings', 'Learnings'),
        ('Deliverable', 'Deliverable'),
        ('Work-Product', 'Work-Product'),
        ('innovation', 'innovation'),
        ('Miscellaneous', 'Miscellaneous'),
    ]

    date= models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=300)
    what_you_did_today = models.TextField()
    objective = models.ForeignKey(Objective, related_name='action_entry', on_delete=models.CASCADE)
    duration = models.IntegerField(null=True)
    achievements = models.CharField(choices=achievements_values, default='Learnings', max_length=20)
    collaborators = models.ManyToManyField(User, related_name="action_main_entry_collaborators")
    
    def __str__(self):
        return f"{self.name.first_name}'s actions for {self.date}"
```

## Fields

### date

Type: DateTimeField
Description: Date and time when the action was recorded.
Auto-generated with the current date and time when an instance is created.

### name

Type: CharField
Max Length: 300
Description: Name or title of the action.

### what_you_did_today

Type: TextField
Description: Description of what was done or accomplished.

### objective

Type: ForeignKey to Objective model
Related Name: 'action_entry'
Description: The objective to which the action is associated.
On Delete: CASCADE (Deleting the associated objective will also delete related actions.)

### duration

Type: IntegerField
Nullable: True
Description: Duration of the action in minutes.

### achievements

Type: CharField
Choices: 'Learnings', 'Deliverable', 'Work-Product', 'Innovation', 'Miscellaneous'
Default: 'Learnings'
Max Length: 20
Description: Type of achievement associated with the action.

### collaborators

Type: ManyToManyField to User model
Related Name: 'action_main_entry_collaborators'
Description: Users who collaborated on the action
