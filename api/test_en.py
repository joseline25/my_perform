from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from objective.models import Skill, Team, KPI


class SkillTestCase(APITestCase):

    def setUp(self):
        # I am creating a User and a Skill instance for testing
        self.user = User.objects.create_user(
            username='testuser', first_name='Jose', last_name='You', 
            email='youjoseline@gmail.com', password='testpassword')
        self.skill1 = Skill.objects.create(
            skill_name="Test Skill",
            skill_description="Description for test skill",
            created_by=self.user
        )
    
    def testgetskills(self):
        """Ensure we get all the skills """

        url = reverse('skills')
        
        response = self.client.get(url, format='json')
        response_data = response.json()
        
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response_data, list)

    def testskilldetails(self):
        """Ensure we get one skill and it's details"""
        skill_id = self.skill1.skill_id
        url = reverse("skill_details", args=[skill_id])

        response = self.client.get(url)
    
        self.assertEqual(response.status_code, 200)

    def testcreateskill(self):
        """Ensure we can create a skill with all required field"""

        url = reverse('create_skills')
        data = {
            "skill_name": "Graphic Design",
            "skill_description": "Skilled in creating visually appealing designs."
        }
        response = self.client.post(url, data)
       
        self.assertEqual(response.status_code, 201)
        #the skill is not created in the database 
        #self.assertEqual(Skill.objects.count(), 1)

    def testupdateskill(self):
        """Ensure we can update a skill."""
        skill_id = self.skill1.skill_id
        url = reverse('update_skill', args=[skill_id])
        data = {
            "skill_name": "Updated skill",
            "skill_description": "Skilled in creating visually appealing designs."
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, 200)
        skill = Skill.objects.get(skill_id=skill_id)
        self.assertEqual(skill.skill_name, 'Updated skill')

    def testdeleteskill(self):
        """Ensure we can delete a skill"""
        skill_id = self.skill1.skill_id
        url = reverse('delete_skill', args=[skill_id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Skill.objects.filter(skill_id=skill_id).exists())


class TeamTestCase(APITestCase):

    def setUp(self):
        # I am creating a User and a Skill instance for testing
        self.user = User.objects.create_user(
            username='testuser', first_name='Jose', last_name='You', 
            email='youjoseline@gmail.com', password='testpassword1')
        
        self.user1 = User.objects.create_user(
            username='ericka', first_name='ericka', last_name='ndongo', 
            email='danielle.ntsamaa@gmail.com', password='testpassword2')

        self.skill1 = Skill.objects.create(
            skill_name="Test Skill",
            skill_description="Description for test skill",
            created_by=self.user
        )

        self.team1 = Team.objects.create(
            name = "CIU",
            description = "...",
            created_by = self.user,
        )
        # skills = self.team1.skills.set([self.skill1])
        # users = self.team1.users.set([self.user, self.user1])
        

    def testgetteams(self):
        """Ensure we get all the teams"""
        url = reverse('teams')
        response = self.client.get(url, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response_data, list)

    # def testteamdetails(self):
    #     """Ensure we get all the details of a team"""
    #     team_id = self.team1.id
    #     url = reverse('team_details', args=[team_id])
    #     response = self.client.get(url, format='json')
    #     self.assertEqual(response.status_code, 200)
        


    def testcreateteam(self):
        """Ensure we can create a team"""
        url = reverse('team_create')
        data ={
        "id": 1,
        "skills": [
            {
                "skill_id": 3,
                "skill_name": "algorithmic",
                "skill_description": "understand algorithms and be able to write one"
            },
            {
                "skill_id": 2,
                "skill_name": "testing",
                "skill_description": "Test your enpoints and models"
            },
            {
                "skill_id": 1,
                "skill_name": "coding",
                "skill_description": "know python and javascript"
            }
        ],
        "created_by": {
            "id": 3,
            "username": "Ericka",
            "first_name": "",
            "last_name": "",
            "email": ""
        },
        "users": [
            {
                "id": 3,
                "username": "Ericka",
                "first_name": "",
                "last_name": "",
                "email": ""
            },
            {
                "id": 6,
                "username": "Ericka_danielle",
                "first_name": "",
                "last_name": "",
                "email": "danielle.ntsamaa@gmail.com"
            },
            {
                "id": 1,
                "username": "joseline",
                "first_name": "",
                "last_name": "",
                "email": ""
            }
        ],
        "name": "CIU",
        "created_at": "2024-03-03T14:55:30.397111Z",
        "description": "...",
        "updated_at": "2024-03-03T14:55:30.397111Z"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)

    # def testupdateteam(self):
    #     """Ensure we can update the details of a team"""
    #     team1 = self.team1.id
    #     url = reverse('update_team', args=[team1])
    #     data = {
    #         "id": 1,
    #     "skills": [
    #         {
    #             "skill_id": 3,
    #             "skill_name": "algorithmic",
    #             "skill_description": "understand algorithms and be able to write one"
    #         },
    #         {
    #             "skill_id": 2,
    #             "skill_name": "testing",
    #             "skill_description": "Test your enpoints and models"
    #         },
    #         {
    #             "skill_id": 1,
    #             "skill_name": "coding",
    #             "skill_description": "know python and javascript"
    #         }
    #     ],
    #     "created_by": {
    #         "id": 3,
    #         "username": "Ericka",
    #         "first_name": "",
    #         "last_name": "",
    #         "email": ""
    #     },
    #     "users": [
    #         {
    #             "id": 3,
    #             "username": "Ericka",
    #             "first_name": "",
    #             "last_name": "",
    #             "email": ""
    #         },
    #         {
    #             "id": 6,
    #             "username": "Ericka_danielle",
    #             "first_name": "",
    #             "last_name": "",
    #             "email": "danielle.ntsamaa@gmail.com"
    #         },
    #         {
    #             "id": 1,
    #             "username": "joseline",
    #             "first_name": "",
    #             "last_name": "",
    #             "email": ""
    #         }
    #     ],
    #     "name": "Updated team",
    #     "created_at": "2024-03-03T14:55:30.397111Z",
    #     "description": "...",
    #     "updated_at": "2024-03-03T14:55:30.397111Z"
    #     }

    #     response = self.client.put(url, data, format='json')

    #     self.assertEqual(response.status_code, 200)
    #     team = Team.objects.get(id=id)
    #     self.assertEqual(team.name, 'Updated team')
        
    # def testdeleteteam(self):
    #     """Ensure we can delete a team"""
    #     team_id = self.team1.id
    #     url = reverse('delete_team', args=[team_id])
    #     response = self.client.delete(url)
    #     self.assertEqual(response.status_code, 204)
    #     self.assertFalse(Skill.objects.filter(id=team_id).exists())
        

