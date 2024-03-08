from django.urls import reverse, resolve
from rest_framework.test import APITestCase 
from rest_framework import status 
from objectve.models import Team, Tool

class TeamApiTest(APITestCase):
    
    tool_get_url = reverse('all_tools')
    tool_create_url = reverse('create_tool')
    tool_get_single_url = reverse('tool_details')
    tool_update_url = reverse('update_tool')
    tool_delete_url = reverse('delete_tool')
    
    def setUp(self):
        self.team1 = Team.objects.create(name='UX/UI', description='Product design team')
        
        
    def test_tools_get(self):
        response = self.client.get(self.tool_get_single_url)     
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
    def test_post_tool(self):
        data = {
            'tool_name': 'vscode',
            'description': 'description',
            'created_by': 'created_by',
            'team': [str(self.team1.id)]
        }   
        response  = self.client.post(self.create_tool_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'vscode')
        id = response.data['tool_id']
        # saving id for later use
        self.tool_id = id
        
    def test_update_tool(self):
        data = {
            'tool_name': 'updated_vscode',
            'description': 'updated_description',
            'created_by': 'updated_created_by',
            'team': [str(self.team1.id)]
        }
        response = self.client.put(self.tool_update_url, kwargs={'pk': self.tool.tool_id}, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['tool_name'], 'updated_vscode')
        
    def test_delete_tool(self):
        response = self.client.delete(self.tool_delete_url, kwargs={'pk': self.tool.tool_id})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Tool.objects.filter(pk=self.tool.tool_id).exists())       
 
 
# class ActionsAPITest(APITestCase):
     
 
 
 
 
 
 
 
   
#def test_update_tool(self):
#     # Create a tool
#     data = {
#         'tool_name': 'vscode',
#         'description': 'description',
#         'created_by': 'created_by',
#         'team': [str(self.team1.id)]
#     }   
#     response = self.client.post(self.create_tool_url, data, format='json')
#     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#     id = response.data['tool_id']

#     # Update the tool
#     updated_data = {
#         'tool_name': 'updated_vscode',
#         'description': 'updated_description',
#         'created_by': 'updated_created_by',
#         'team': [str(self.team1.id)]
#     }
#     update_url = reverse('update_tool', kwargs={'pk': id})
#     response = self.client.put(update_url, updated_data, format='json')
#     self.assertEqual(response.status_code, status.HTTP_200_OK)
#     self.assertEqual(response.data['tool_name'], 'updated_vscode')

# def test_delete_tool(self):
#     # Create a tool
#     data = {
#         'tool_name': 'vscode',
#         'description': 'description',
#         'created_by': 'created_by',
#         'team': [str(self.team1.id)]
#     }   
#     response = self.client.post(self.create_tool_url, data, format='json')
#     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#     id = response.data['tool_id']

#     # Delete the tool
#     delete_url = reverse('delete_tool', kwargs={'pk': id})
#     response = self.client.delete(delete_url)
#     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#     # Ensure the tool was deleted successfully
#     self.assertFalse(Tool.objects.filter(pk=id).exists())