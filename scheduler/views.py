from django.shortcuts import render
from django.views import View

class Dashboard(View):
    def get(self, request):
        userrole = request.session['user']['role']

        match userrole:
            case 'Supervisor':
                return render(request, "SupervisorDash.html", {"name": request.session['user']['username']})
            case 'Instructor':
                return render(request, "InstDash.html", {"name": request.session['user']['username']})
            case 'Teaching Assistant':
                return render(request, "TADash.html", {"name": request.session['user']['username']})

    def post(self, request): #Should not receive POST requests on dashboard page
        userrole = request.session['user']['role']

        match userrole:
            case 'Supervisor':
                return render(request, "SupervisorDash.html", {"name": request.session['user']['username']})
            case 'Instructor':
                return render(request, "InstDash.html", {"name": request.session['user']['username']})
            case 'Teaching Assistant':
                return render(request, "TADash.html", {"name": request.session['user']['username']})