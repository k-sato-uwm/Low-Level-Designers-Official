from django.shortcuts import render
from django.views import View

from scheduler.models import Course


class CourseManagement(View):
    template_name = 'CourseManagement.html'




    def get(self, request):
        courses = Course.objects.all()
        print(courses)
        context = {'courses': courses}
        return render(request,self.template_name,context)

    def post(self, request):
        print(request.POST)




        return self.get(request)
