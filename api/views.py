from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from api.models import Task ,  Priority ,  Status
from api.serializers import TaskSerializer , PrioritySerializer , StatusSerializer , SignupSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.decorators import action
import os
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from decouple import config


class UserPrompt(APIView):

    def post(self , request):
        userMessage = request.data.get('userMessage','')

        if not userMessage:
            return Response({"error":"Prompt Not Found"},
                            status=status.HTTP_404_NOT_FOUND)

        GROQ_API_KEY = config("GROQ_API_KEY")                    
        GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"                    
        
        headers = {
            "Authorization":f"Bearer {GROQ_API_KEY}",
            "Content-Type":"application/json"
        }
        
        prompt = f""" 
        

        System Prompt:
        You are an accurate, concise research assistant.
        Analyze the user's input, whether it is a question, a problem, or a request for information.
        Provide an accurate, evidence-based answer.
     
        Requirements:
        Keep the response concise and targeted to the query.
        If the query involves news, articles, or theories, verify the information in your response.
        If a query is ambiguous, give the most likely answer and briefly mention alternatives.
     
        
        userMessage: {userMessage}
        
        """
        
        data ={
            "model":"llama-3.3-70b-versatile",
            "messages":[
                {
                    "role":"system",    
                    "content":"You are an expert task breakdown assistant. You break down tasks into clear, actionable bullet points. Always start each line with '- ' and make each point specific."    
                },
                {
                    "role":"user",
                    "content":userMessage
                }
            ],
            "temperature":0.7,
            "max_tokens":600,
            "top_p":0.9
        }

        
        try:
            print(f"Calling GROQ Api For {userMessage[:50]}")
            print(f"Using Model : {data['model']}")

            response = requests.post(GROQ_API_URL , headers=headers , json=data , timeout=30)
            print(F"GROQ Api Status : {response.status_code}")

            if response.status_code == 200:
                res = response.json()
                result = res["choices"][0]["message"]["content"]
                print (result)


                if result:
                    print("SuccessFully Generated Response")
                    return Response({"Response":result})
                else:
                    raise Exception("No Response Fetched")    

            elif response.status_code == 401:
                print(f"Invalid Groq Api Key") 
                return Response({"error":"Invalid Api Key"},
                                status=status.HTTP_401_UNAUTHORIZED)
            
            else:
                error_msg = f"Groq Error : {response.status_code}"
                try:
                    error_data = response.json()
                    error_msg += f" : {error_data.get('error',{}).get('message',response.text)}"
                except:
                    error_msg += f": {response.text[:200]}"    

                print(f"{error_msg}")    
                raise Exception(error_msg)


        except requests.exceptions.Timeout:
            print("Groq Service Timeout")
            return Response({"Error":"Api Service timeout. Try Again Later"},
                            status=status.HTTP_504_GATEWAY_TIMEOUT)

        except Exception as e:
            print(f"GROQ Api Exception {str(e)}")                    
            return Response({"error":"Failed To Fetch Response"},
                            status=status.HTTP_503_SERVICE_UNAVAILABLE)







        

class BreakTaskView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        description = request.data.get('description', '')
        
        if not description:
            return Response({'error': 'No description provided'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        GROQ_API_KEY = config("GROQ_API_KEY")
        GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        
        prompt = f"""Break this task into 5-7 specific, actionable bullet points.

Task: {description}

Requirements:
- Each bullet point must start with a verb (Research, Create, Write, etc.)
- Make them specific and actionable
- Include time estimates where appropriate
- Return ONLY the bullet points, one per line, starting with '- '

Example format:
- Research the topic and gather necessary materials (30 min)
- Create a step-by-step action plan (15 min)
- Execute the first phase of the task (1 hour)
- Review progress and adjust approach as needed (20 min)
- Complete remaining subtasks (2 hours)
- Final review and quality check (30 min)

Now break down this specific task:"""

        data = {
            "model": "llama-3.3-70b-versatile",  
            "messages": [
                {
                    "role": "system", 
                    "content": "You are an expert task breakdown assistant. You break down tasks into clear, actionable bullet points. Always start each line with '- ' and make each point specific."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 600,
            "top_p": 0.9
        }
        
        
        try:
            print(f"Calling GROQ API for: {description[:50]}...")
            print(f"Using model: {data['model']}")
            
            response = requests.post(GROQ_API_URL, headers=headers, json=data, timeout=30)
            
            print(f"📡 GROQ API Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                bullets_text = result['choices'][0]['message']['content']
                
                print(f" Raw response: {bullets_text[:200]}...")
                
                bullets = []
                for line in bullets_text.split('\n'):
                    line = line.strip()
                    if line.startswith('- '):
                        bullets.append(line[2:])  
                    elif line.startswith('•'):
                        bullets.append(line[1:].strip())
                    elif line.startswith('* '):
                        bullets.append(line[2:])
                    elif line and len(line) > 10 and not line.startswith('```'):
                        bullets.append(line)
                
                bullets = [b for b in bullets if b and len(b) > 5][:7]
                
                if bullets:
                    print(f" Success! Generated {len(bullets)} dynamic bullets")
                    return Response({'bullets': bullets})
                else:
                    raise Exception("No valid bullets parsed from response")
                    
            elif response.status_code == 401:
                print("Invalid GROQ API key")
                return Response(
                    {'error': 'Invalid API key'}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )
            else:
                error_msg = f"GROQ API Error {response.status_code}"
                try:
                    error_data = response.json()
                    error_msg += f": {error_data.get('error', {}).get('message', response.text)}"
                except:
                    error_msg += f": {response.text[:200]}"
                    
                print(f"{error_msg}")
                raise Exception(error_msg)
                
        except requests.exceptions.Timeout:
            print("GROQ API timeout")
            return Response(
                {'error': 'AI service timeout. Please try again.'}, 
                status=status.HTTP_504_GATEWAY_TIMEOUT
            )
        except Exception as e:
            print(f"GROQ API Exception: {str(e)}")
            return Response(
                {'error': f'Failed to get AI response: {str(e)}'}, 
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
class StatusViewSet(ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    
class PriorityViewSet(ModelViewSet):
    queryset = Priority.objects.all()
    serializer_class = PrioritySerializer    
    
class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        task = self.get_object()
        status_id = request.data.get('status_id')
        try:
            new_status = Status.objects.get(id=status_id)
            task.status = new_status
            task.save()
            serializer = self.get_serializer(task)
            return Response(serializer.data)
        except Status.DoesNotExist:
            return Response({'error': 'Status not found'}, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)    
    
class SignUpView(generics.CreateAPIView):
    queryset =  User.objects.all()   
    serializer_class = SignupSerializer
    