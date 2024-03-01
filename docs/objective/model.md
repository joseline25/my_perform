# Model

```python
class Objective(models.Model):
    priorities = [('Low', 'Low'), ('Intermediate',
                                   'Intermediate'), ('High', 'High')]
    complexities = [('Easy', 'Easy'), ('Hard', 'Hard')]
    objective_types = [('Financial', 'Financial'),
                       ('Non-Financial', 'Non-Financial')]
    repeat_frequency = [('Daily', 'Daily'), ('Weekly',
                                             'Weekly'), ('Monthly', 'Monthly')]
    status_choices = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    objective_id = models.AutoField(primary_key=True)
    objective_name = models.CharField(max_length=300, blank=True, null=True)
    assign_to = models.ManyToManyField(
        to=User, unique=False, related_name="objectives_assigned_to", blank=True)
    visible_to = models.ManyToManyField(
        User,  related_name="visible_objectives", blank=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="objectives_created", default=1,)
    associated_task = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    evaluator = models.ForeignKey(
        User, related_name="evaluator", on_delete=models.CASCADE, blank=True, null=True)
    repeat_date = models.CharField(
        choices=repeat_frequency, max_length=100, blank=True, null=True)
    deadline = models.DateTimeField(null=True, blank=True)
    action_phrase = models.CharField(max_length=300, null=False, blank=True)
    number = models.IntegerField(null=False)
    units = models.CharField(max_length=10)
    start_date = models.DateTimeField(null=False)
    end_date = models.DateTimeField(null=False)
    priority = models.CharField(choices=priorities, max_length=100)
    complexity = models.CharField(choices=complexities, max_length=100)
    objective_type = models.CharField(choices=objective_types, max_length=100)
    skills = models.ManyToManyField(
        Skill, related_name='objectives_skill', blank=True)
    tools = models.ManyToManyField(
        Tool, related_name='objectives_tool', blank=True)
    dog = models.TextField()
    is_draft = models.BooleanField(default=False)
    repeat = models.BooleanField(default=False)
    status = models.CharField(choices=status_choices, default='Pending', max_length=20)
    completion_date = models.DateTimeField(blank=True, null=True)
    estimated_hours = models.IntegerField(default=0, help_text="Estimated number of hours to complete the task")

    # test assign_to a team or user

    # use GenericForeignKey to allow assignment to either User or Team
    assign_to_to_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, null=True, blank=True)
    assign_to_to_id = models.PositiveIntegerField(null=True, blank=True)
    assign_to_to = GenericForeignKey('assign_to_to_type', 'assign_to_to_id')

    # GenericRelation to store reverse relations
    assign_to_to_objectives = GenericRelation(
        'Objective', related_query_name='assign_to_to_objectives')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.objective_name}"

    # override the save method
    def save(self, *args, **kwargs):

        if not self.objective_name:  # Check if objective_name is null
            # Concatenate the desired fields for the default value
            self.objective_name = f"{self.objective_id} {self.action_phrase} {self.number} {self.units} {self.deadline}"
        # check if end_date is further than deadline
        if self.deadline and self.end_date and self.deadline < self.end_date:
            # set the end_date to the deadline
            self.end_date = self.deadline

        # check that repeat == True before setting repeat date
        if self.repeat == False:
            self.repeat_date = None

        # management de assign_to avec User and Team
        # set assign_to_totype based on the instance type
        if isinstance(self.assign_to_to, User):
            self.assign_to_to_type = ContentType.objects.get_for_model(User)
        elif isinstance(self.assign_to_to, Team):
            self.assign_to_to_type = ContentType.objects.get_for_model(Team)
            
        # update the status field depending on the date  
        # check if the objective is in progress
        if self.start_date <= timezone.now() <= self.end_date:
            self.status = 'In Progress'
        # # check if the objective is completed
        # elif timezone.now() >= self.deadline:
        #     self.status = 'Completed'
        
        # manage completion_date
        # if the status has changed to "Completed" update the completion_date to the current datetime
        if self.status == 'Completed' and self.completion_date is None:
            self.completion_date = timezone.now()
        elif self.status != 'Completed':
            # keep  it to None
            self.completion_date = None
        # on renvoit la main à la méthode save originale
        super().save(*args, **kwargs)

```

## Fields

### objective_id

Type: AutoField, auto-generated integer primary key.
Description: Unique identifier for the objective.

### objective_name

Type: CharField
Max Length: 300
Description: Name or title of the objective.

### assign_to

Type: ManyToManyField to User
Description: Users or teams assigned to work on the objective.

### visible_to

Type: ManyToManyField to User
Description: Users who have access to view the objective.

### created_by

Type: ForeignKey to User
Description: User who created the objective.

### associated_task

Type: TextField
Description: Description of the task associated with the objective.

### created_a

Type: DateTimeField
Description: Date and time when the objective was created.

### updated_at

Type: DateTimeField
Description: Date and time when the objective was last updated.

### evaluator

Type: ForeignKey to User
Description: User responsible for evaluating the objective.

### repeat_date

Type: CharField with choices
Description: Frequency of objective repetition (Daily, Weekly, Monthly).

### deadline

Type: DateTimeField
Description: Date and time by which the objective should be completed.

### action_phrase

Type: CharField
Description: Action phrase describing what needs to be done to achieve the objective.

### number

Type: IntegerField
Description: Number of outputs expected from the objective.

### units

Type: CharField
Description: Unit of measurement for the objective outputs.

### start_date

Type: DateTimeField
Description: Date and time when the objective is scheduled to start.

### end_date

Type: DateTimeField
Description: Date and time when the objective is scheduled to end.

### priority

Type: CharField with choices
Description: Priority level of the objective (Low, Intermediate, High).

### complexity

Type: CharField with choices
Description: Estimated difficulty level of executing the objective (Easy, Hard).

### objective_type

Type: CharField with choices
Description: Type of objective (Financial, Non-Financial).

### skills

Type: ManyToManyField to Skill
Description: Required competencies for completing the objective.

### tools

Type : ManyToManyField to Tool
Description: Recommended tools for achieving the objective.

### dog

Type: TextField
Description: Definition of Good criteria for evaluating the objective.

### is_draft

Type: BooleanField
Description: Indicates whether the objective is in draft status.

### repeat

Type: BooleanField
Description: Indicates whether the objective should be repeated.

### status

Type: CharField with choices
Description: Current status of the objective (Pending, In Progress, Completed).

### completion_date

Type: DateTimeField
Description: Date and time when the objective was completed.
estimated_hours (IntegerField):

Description: Estimated number of hours required to complete the objective

### save() Method

The save method of the Objective model contains custom logic that is executed when saving an instance of the Objective model. This method overrides the default save behavior to perform additional actions before the object is saved to the database.

#### Logic

1. Setting default objective name

Description: If the objective_name field is empty, this method generates a default name for the objective by concatenating other relevant fields.
Implementation: If objective_name is null, the method constructs a default name using objective_id, action_phrase, number, units, and deadline.
2. Setting end date to deadline

Description: If the deadline field is set and is earlier than the end_date, this method updates the end_date to match the deadline.
Implementation: If deadline and end_date are both set and deadline is earlier than end_date, the end_date is set to match the deadline.
3. Managing repeat date

Description: If the repeat field is set to False, the repeat_date field is set to None.
Implementation: If repeat is False, repeat_date is set to None.
4. Managing assign to with user and team

Description: This method determines the type of the assign_to_to field (either User or Team) and sets the assign_to_to_type field accordingly.
Implementation: If assign_to_to is an instance of User, assign_to_to_type is set to the content type of User. If it's an instance of Team, assign_to_to_type is set to the content type of Team.
5.  Updating status based on dates

Description: This method updates the status field of the objective based on the current date and its start and end dates.
Implementation: If the current date falls within the objective's start and end dates, the status is set to 'In Progress'.
6. Managing completion date

Description: If the status of the objective changes to "Completed", the completion_date field is updated to the current datetime. Otherwise, completion_date is set to None.
Implementation: If the status is 'Completed' and completion_date is None, completion_date is set to the current datetime. Otherwise, completion_date remains None.
7. Calling original save method

Description: Finally, the method calls the original save method to perform the default save behavior.
Implementation: The method calls super().save(*args, **kwargs) to execute the original save behavior.

## Usage

```python
# Example usage of the Objective model
objective = Objective.objects.create(
    objective_name='Project Launch',
    assign_to=[user1, user2],
    visible_to=[user3, user4],
    created_by=user5,
    associated_task='Develop and launch a new product.',
    deadline=datetime.datetime(2024, 12, 31),
    action_phrase='Develop',
    number=1,
    units='Product',
    start_date=datetime.datetime(2024, 1, 1),
    end_date=datetime.datetime(2024, 12, 31),
    priority='High',
    complexity='Hard',
    objective_type='Financial',
    dog='Successfully launch the product.',
    is_draft=False,
    repeat=False,
    status='Pending',
    estimated_hours=100
)

```
