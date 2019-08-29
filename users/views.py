from django.shortcuts import render, HttpResponseRedirect, reverse, Http404
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm

# Create your views here.


def register(request):
    """注册"""
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(request.POST)
        new_user = form.save()
        authenticate_user = authenticate(username = new_user.username, password = request.POST['password1'])
        login(request, authenticate_user)
        return HttpResponseRedirect(reverse('index:index'))

    context = {
        'form': form,
    }
    return render(request, 'users/register.html', context)


def logout_view(request):
    """登出"""
    logout(request)
    return HttpResponseRedirect(reverse('index:index'))


def check_project_owner(request, report):
    """检查请求的报告是否属于当前用户，避免使用输入链接的方式打开别人的工程信息"""
    if report.owner != request.user:
        raise Http404
