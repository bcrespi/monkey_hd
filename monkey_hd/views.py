from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from monkey_hd.forms import *


def index(request):
    return render(request, 'monkey_hd/index.html', {})


def user_login(request):
    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:

            if user.is_active:
                login(request, user)
                return redirect('index')
            else:
                return render(request, 'monkey_hd/index.html',
                              {"msg": "Your account has been disabled."})
        else:
            return render(request, 'monkey_hd/index.html',
                          {"msg": "Invalid login details. Check your username and password"})

    return render(request, 'monkey_hd/index.html', {})


@login_required(login_url='index')
def agile(request):
    if request.method == "POST":
        ticket_id = request.POST.get('search')
        username = request.POST.get('filter')
        if ticket_id is not None:
            return redirect('ticket', ticket_id)

        users = UserProfile.objects.all()
        user = UserProfile.objects.filter(user=User.objects.get(username=username))
        tickets = Ticket.objects.filter(Q(creator=user) | Q(owner=user))
        backlog = tickets.filter(status=Status.objects.get(name='backlog'))
        todo = tickets.filter(status=Status.objects.get(name='todo'))
        inprogress = tickets.filter(status=Status.objects.get(name='inprogress'))
        resolved = tickets.filter(status=Status.objects.get(name='resolved'))
        return render(request, 'monkey_hd/agile.html', {'users': users,
                                                            'backlog': backlog,
                                                            'todo': todo,
                                                            'inprogress': inprogress,
                                                            'resolved': resolved})
    else:
        user = UserProfile.objects.get(user=request.user)
        if user.permission.name == "admin":
            users = UserProfile.objects.all()
            backlog = Ticket.objects.filter(status=Status.objects.get(name='backlog'))
            todo = Ticket.objects.filter(status=Status.objects.get(name='todo'))
            inprogress = Ticket.objects.filter(status=Status.objects.get(name='inprogress'))
            resolved = Ticket.objects.filter(status=Status.objects.get(name='resolved'))
            return render(request, 'monkey_hd/agile.html', {'users': users,
                                                                'backlog': backlog,
                                                                'todo': todo,
                                                                'inprogress': inprogress,
                                                                'resolved': resolved})
        else:
            tickets = Ticket.objects.filter(Q(creator=user) | Q(owner=user))
            backlog = tickets.filter(status=Status.objects.get(name='backlog'))
            todo = tickets.filter(status=Status.objects.get(name='todo'))
            inprogress = tickets.filter(status=Status.objects.get(name='inprogress'))
            resolved = tickets.filter(status=Status.objects.get(name='resolved'))
            return render(request, 'monkey_hd/agile.html', {'backlog': backlog,
                                                                'todo': todo,
                                                                'inprogress': inprogress,
                                                                'resolved': resolved})


@login_required(login_url='index')
def ticket(request, pk):
    user = UserProfile.objects.get(user=request.user)
    ticket = get_object_or_404(Ticket, pk=pk)
    form = TicketFormView(instance=ticket)

    if user.permission.name == "admin" or user == ticket.creator or user == ticket.owner:
        return render(request, 'monkey_hd/ticket.html', {'user_profile': user,
                                                             'ticket': ticket,
                                                             'form': form})
    else:
        return render(request, 'monkey_hd/unauthorized.html', {})


@login_required(login_url='index')
def ticket_new(request):
    user = UserProfile.objects.get(user=request.user)

    if request.method == "POST":
        if user.permission.name == "admin":
            form = TicketFormAdminNew(request.POST)
        else:
            form = TicketForm(request.POST)

        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.priority = Priority.objects.get(name='unassigned')
            ticket.creator = UserProfile.objects.get(user=request.user)
            ticket.status = Status.objects.get(name='backlog')
            ticket.scalability = Scalability.objects.get(name='basic')
            ticket.save()
            return redirect('ticket', pk=ticket.pk)
    else:
        if user.permission.name == "admin":
            form = TicketFormAdminNew()
        else:
            form = TicketForm()

    return render(request, 'monkey_hd/ticket_new.html', {'user_profile': user,
                                                             'form': form})


@login_required(login_url='index')
def ticket_edit(request, pk):
    user = UserProfile.objects.get(user=request.user)
    ticket = get_object_or_404(Ticket, pk=pk)

    if request.method == "POST":
        if user.permission.name == "admin":
            form = TicketFormAdminEdit(request.POST, instance=ticket)
        elif user.permission.name == "developer":
            form = TicketFormDeveloper(request.POST, instance=ticket)
        else:
            form = TicketForm(request.POST, instance=ticket)

        if form.is_valid():

            ticket = form.save(commit=False)

            if ticket.status.name == "todo" or ticket.status.name == "inprogress":
                if ticket.owner is None:
                    ticket.owner = user
                if ticket.date_start is None:
                    ticket.date_start = timezone.now()

            if ticket.status.name == "resolved":
                if ticket.owner is None:
                    ticket.owner = user
                if ticket.date_start is None:
                    ticket.date_start = timezone.now()
                if ticket.date_solved is None:
                    ticket.date_solved = timezone.now()

            ticket.save()
            return redirect('ticket', pk=ticket.pk)
    else:

        if user.permission.name == "admin":
            form = TicketFormAdminEdit(instance=ticket)
        elif user.permission.name == "developer":
            form = TicketFormDeveloper(instance=ticket)
        else:
            form = TicketForm(instance=ticket)

    return render(request, 'monkey_hd/ticket_edit.html', {'user_profile': user,
                                                              'ticket': ticket,
                                                              'form': form})


@login_required(login_url='index')
def ticket_escalate(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)

    if ticket.scalability.name == "basic":
        ticket.scalability = Scalability.objects.get(name='technical')
    else:
        ticket.scalability = Scalability.objects.get(name='extreme')

    ticket.save()
    return redirect('ticket', pk=ticket.pk)


@login_required(login_url='index')
def ticket_delete(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    ticket.delete()

    return redirect('agile')


@login_required(login_url='index')
def user_logout(request):
    logout(request)
    return redirect('index')
