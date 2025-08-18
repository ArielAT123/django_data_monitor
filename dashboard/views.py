from django.conf import settings
import requests
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required

@login_required
@permission_required('dashboard.index_viewer', raise_exception=True)
def index(request):
    api_url = "https://arielarias.pythonanywhere.com/demo/rest/api/index/"
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        users = response.json()
        
        # Procesar datos para el dashboard
        total_users = len(users)
        active_users = sum(1 for user in users if user.get('is_active', False))
        inactive_users = total_users - active_users
        
        data = {
            'title': "Dashboard de Usuarios",
            'total_users': total_users,
            'active_users': active_users,
            'inactive_users': inactive_users,
            'users': users,
            'error': None
        }
        
    except requests.RequestException as e:
        data = {
            'title': "Dashboard de Usuarios",
            'error': f"No se pudo conectar con la API: {str(e)}",
            'total_users': 0,
            'active_users': 0,
            'inactive_users': 0,
            'users': []
        }
    
    return render(request, 'dashboard/index.html', data)