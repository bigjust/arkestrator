from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.shortcuts import render_to_response,get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from django.views.generic import list_detail
from django.core.paginator import Paginator, InvalidPage
from copy import copy


from models import PM, Recipient
from django.contrib.auth.models import User
import forms

@login_required
def new_pm(request):
    if request.method == 'POST':
        form =forms.NewPMForm(request.POST)
        if form.is_valid():
            form.save(request.user)
            return HttpResponseRedirect("/pms/inbox")
    else:
        form =forms.NewPMForm()
    return render_to_response('pms/new_pm.html',
            { 'form' : form },
            context_instance = RequestContext(request))


@login_required
def outbox(request):
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        raise Http404

    queryset = PM.objects.filter(sender=request.user).order_by(
        '-created_on').select_related('created_on', 'subject',
            'recipient','recipient__read',
            'recipient__recipient__username')
    paginator = Paginator(queryset, 50, allow_empty_first_page=True)
    page_obj = paginator.page(page)

    pm_list = page_obj.object_list
    
    pm_rec_list = []
    for pm in pm_list:
        rec_list = Recipient.objects.filter(message=pm)
        read_list = []
        for rec in rec_list:
            read_list.append([rec,rec.read])
        pm_rec_list.append([pm , read_list])
        
    return render_to_response('pms/outbox.html',
            { 'pm_rec_list' : pm_rec_list,
              'page_obj' : page_obj },
            context_instance = RequestContext(request))

@login_required
def inbox(request):
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        raise Http404
    
    queryset = PM.objects.filter(recipients=request.user).order_by(
        '-created_on').select_related('subject','created_on',
            'sender__username','recipient__read')
    paginator = Paginator(queryset, 50, allow_empty_first_page=True)
    page_obj = paginator.page(page)

    pm_list = page_obj.object_list
    
    read_list = []
    for pm in pm_list:
        read_list.append(Recipient.objects.get(
                recipient=request.user,
                message=pm).read)
    pm_read = zip(pm_list, read_list)
    return render_to_response('pms/inbox.html',
            { 'pm_read' : pm_read,
              'page_obj' : page_obj },
            context_instance = RequestContext(request))

@login_required
def mark_read(request):
    unread_list = Recipient.objects.filter(
        recipient=request.user,read=False).update(
            read=True)
    return HttpResponseRedirect("/pms/inbox")

@login_required
def view_pm(request, pm_id):
    pm = get_object_or_404(PM,pk=pm_id)
    #make sure only the sender and recipients can read it
    if pm.sender != request.user:
        read = get_object_or_404(Recipient,message=pm,recipient=request.user)
        if not read.read:
            read.read = True
            read.save()
    #this else is to make sure pms sent to oneself get marked read
    else:
        try:
            recip = Recipient.objects.get(message=pm,
                    recipient=request.user, read=False)
            recip.read=True
            recip.save()
        except Recipient.DoesNotExist:
            pass
    
    reply = copy(pm)
    reply.parent=pm
    reply.body = reply.body.replace('[hidden]','')
    reply.body = reply.body.replace('[/hidden]','')
    reply.body = '[hidden][quote]' + reply.body + '[/quote][/hidden]'

    #this is messy and slow and should be fixed
    rec_list = Recipient.objects.filter(message=pm)
    reply_recs = pm.sender.username
    for rec in rec_list:
        if rec.recipient != request.user:
            reply_recs = reply_recs + ' ' + rec.recipient.username

    if request.method == 'POST':
        form =forms.NewPMForm(request.POST,
                instance=reply)
        if form.is_valid():
            new_pm = form.save(request.user)
            new_pm.parent = pm
            new_pm.save()
            return HttpResponseRedirect("/pms/inbox")
    else:
        rec_str = pm.get_rec_str()
        form =forms.NewPMForm(instance=reply,
                initial={'recipients' : reply_recs})
    return render_to_response("pms/view_pm.html",
            { 'pm' : pm ,
              'rec_str' : rec_str,
              'form' : form },
            context_instance = RequestContext(request))
        
