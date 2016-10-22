from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from .models import Topic, Entry
from .forms import TopicForm, EntryForm, CommentForm

def index(request):
	return render(request,'web_board/index.html')
@login_required
def topics(request):
	topics = Topic.objects.order_by('date_added')
	context = {'topics': topics}
	return render(request, 'web_board/topics.html', context)
@login_required
def topic(request, topic_id):
	topic = Topic.objects.get(id=topic_id)
	# Make sure the topic belongs to the current user.
	#if topic.owner != request.user:        
	#	raise Http404 
	topic = get_object_or_404(Topic, id=topic_id)
	entries = topic.entry_set.order_by('-date_added')
	context = {'topic': topic, 'entries': entries} 
	return render(request, 'web_board/topic.html', context)
@login_required
def entry(request, entry_id):
	#topic = Topic.objects.get(id=topic_id)
	entry = Entry.objects.get(id=entry_id)
	comments = entry.comment_set.order_by('-date_added')
	# Make sure the topic belongs to the current user.
	#if topic.owner != request.user:        
	#	raise Http404 
	#entries = topic.entry_set.order_by('-date_added')
	context = {'entry': entry, 'comments': comments} 
	return render(request, 'web_board/entry.html', context)
@login_required
def comments(request):
	comments = Comment.objects.order_by('date_added')
	context = {'comments': commets}
	return render(request, 'web_board/comments.html', context)
@login_required
def new_topic(request):
	if request.method != 'POST':       
		form = TopicForm()    
	else:                
		form = TopicForm(request.POST)     
		if form.is_valid(): 
			#form.save()
			new_topic = form.save(commit=False)
			new_topic.owner = request.user
			new_topic.save()              
			return HttpResponseRedirect(reverse('web_board:topics'))
	context = {'form': form}    
	return render(request, 'web_board/new_topic.html', context)
@login_required
def new_entry(request, topic_id):
	topic = Topic.objects.get(id=topic_id)
	if request.method != 'POST':  
	    form = EntryForm()            
	else:       
		form = EntryForm(data=request.POST)        
		if form.is_valid(): 
			new_entry = form.save(commit=False)
			new_entry.topic = topic
			new_entry.save() 
			return HttpResponseRedirect(reverse('web_board:topic', args=[topic_id]))        
	context = {'topic': topic, 'form': form}
	return render(request, 'web_board/new_entry.html', context)
@login_required
def new_comment(request, entry_id):
	entry = Entry.objects.get(id=entry_id)
	if request.method != 'POST':       
		form = CommentForm()    
	else:                
		form = CommentForm(request.POST)     
		if form.is_valid(): 
			#form.save()
			new_comment = form.save(commit=False)
			new_comment.owner = request.user
			new_comment.entry = entry
			new_comment.save()              
			return HttpResponseRedirect(reverse('web_board:entry', args=[entry_id]))
	context = {'form': form, 'entry': entry}    
	return render(request, 'web_board/new_comment.html', context)

"""@login_required
def edit_entry(request, entry_id):    
	entry = Entry.objects.get(id=entry_id)    
	topic = entry.topic        
	if topic.owner != request.user:        
		raise Http404 
	if request.method != 'POST':        
		form = EntryForm(instance=entry)    
	else:               
		form = EntryForm(instance=entry, data=request.POST)        
		if form.is_valid(): 
			form.save()
			return HttpResponseRedirect(reverse('web_board:topic', args=[topic.id]))        
	context = {'entry': entry, 'topic': topic, 'form': form}    
	return render(request, 'web_board/edit_entry.html', context)
"""
	
# Create your views here.
