from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from objective.models import Objective
from django.contrib.auth.models import User
import datetime
from django.utils import timezone


class ObjectiveAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser', first_name='Jose', last_name='You', email='youjoseline@gmail.com', password='testpassword')
        self.objective_1 = Objective.objects.create(
            objective_name='Objective 1',
            objective_id =  3,
            created_by=self.user,
            associated_task="Sample task details",
            start_date=timezone.datetime(
                2024, 3, 1, 9, 0, tzinfo=timezone.utc),
            end_date=timezone.datetime(2024, 3, 5, 17, 0, tzinfo=timezone.utc),
            priority="High",
            complexity="Hard",
            objective_type="Financial",
            number=10,
            units="units",
            status="Pending",
            estimated_hours=5
        )

        objective_data = {
            'objective_id': 2,
            'objective_name': 'Objective 2',
            'created_by': self.user,
            'associated_task': 'Sample task details',
            'start_date': timezone.datetime(2024, 3, 1, 9, 0, tzinfo=timezone.utc),
            'end_date': timezone.datetime(2024, 3, 5, 17, 0, tzinfo=timezone.utc),
            'priority': 'High',
            'complexity': 'Hard',
            'objective_type': 'Financial',
            'number': 10,
            'units': 'units',
            'status': 'Pending',
            'estimated_hours': 5
        }

        self.objective_2 = Objective.objects.create(**objective_data)

    def test_get_objectives(self):

        url = reverse('objectives_api')

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assuming you have two objectives in the database
        self.assertEqual(len(response.data), 2)

    def test_create_objective(self):
        # Replace 'objective-list' with your actual API endpoint
        url = reverse('create_objective_api')
        data = {
            "objective_id": 1,
            "objective_name": "Sample Objective",
            "assign_to": [],
            "visible_to": [],
            "created_by": 1,
            "associated_task": "Sample task details",
            "created_at": "2022-01-01T12:00:00Z",
            "updated_at": "2022-01-01T12:00:00Z",

            "repeat_date": "Daily",
            "deadline": "2022-01-10T18:00:00Z",
            "action_phrase": "Sample action phrase",
            "number": 10,
            "units": "units",
            "start_date": "2022-01-01T09:00:00Z",
            "end_date": "2022-01-05T17:00:00Z",
            "priority": "High",
            "complexity": "Hard",
            "objective_type": "Financial",
            "skills": [],
            "tools": [],
            "dog": "Sample dog field",



            "status": "Pending",

            "estimated_hours": 5
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # since we set up with 2 objectives initially and one is created now
        self.assertEqual(Objective.objects.count(), 3)

    def test_update_objective(self):
        # update the first objective
        objective_id = self.objective_1.objective_id

        url = reverse('update_objective', args=[objective_id])
        data = {
            'objective_name': 'Updated Objective',
            'objective_description': 'Updated Objective Description',
            'objective_type': "Non-Financial",
        }

        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        objective = Objective.objects.get(objective_id=objective_id)
        self.assertEqual(objective.objective_name, 'Updated Objective')

    def test_delete_objective(self):
        # delete the second objective
        objective_id = self.objective_2.objective_id

        url = reverse('objective_detail', args=[objective_id])
    
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Objective.objects.filter(objective_id=objective_id).exists())
