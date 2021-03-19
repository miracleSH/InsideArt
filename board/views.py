from django.shortcuts import render
from board.models import Board, Reply
from django.core.paginator import Paginator, EmptyPage
from django.utils import timezone
from django.http.response import HttpResponseRedirect, HttpResponse
from datetime import datetime
from django.utils.dateformat import DateFormat
import json
# Create your views here.
def MainFunc(request):
    return render(request, "index.html")

def boardFunc(request):
    datas =Board.objects.all()
    paginator = Paginator(datas, 10) #10개씩 내보내기
    
    if request.GET.get("page"):
        page = request.GET.get("page") #페이지 번호 받기
        #print(page)
        
    else:
        page = 1
        
    try:
        data = paginator.page(page) #
    
    except EmptyPage:
        data = paginator.page(paginator.num_pages)
        
    return render(request, 'board.html', {'data':data})

def boardInsert(request):
    if request.method == 'GET':
        return render(request, 'boardinsert.html')
    else:
        writer = request.POST.get("writer")
        title = request.POST.get("title")
        content = request.POST.get("content")
        
        Board(
            writer = writer,
            title = title,
            content = content,
            write_time = DateFormat(datetime.today()).format('Y-m-d H:i:s'),
            read_count = 0
            ).save()
            
        return HttpResponseRedirect('/board')
    
def boardDetail(request):
    text_id = request.GET.get("id")
    text = Board.objects.get(id = text_id)
    text.read_count = text.read_count + 1
    text.save()
    reply_list = Reply.objects.filter(board_replied_id = text_id)
    #print(text.id)
    return render(request, 'boardDetail.html', {'text':text, "reply_list": reply_list})

def boardUpdate(request):
    if request.method == 'GET':
        text = Board.objects.get(id = request.GET.get('id'))
        return render(request, 'update_insert.html', {'text':text})
    else:
        text = Board.objects.get(id = request.POST.get('id'))
        text.title = request.POST.get("title")
        text.content = request.POST.get("content")
        text.write_time = datetime.today()
        text.save()
        return HttpResponseRedirect('/board')

def boardReply(request):
    replied_id = request.GET.get("replied_id")
    reply_content = request.GET.get("reply_val")
    #print(replied_id, reply_content)
    #msg = {'msg': "성공"}
    Reply(
        writer="임시",
        content = reply_content,
        write_time = DateFormat(datetime.today()).format('Y-m-d H:i:s'),
        read_count = 0,
        board_replied_id = replied_id
        ).save()
    list = []
    
    data = Reply.objects.filter(board_replied_id = replied_id)
    
    
    for a in data:
        print(a.write_time)
        list.append({"writer": a.writer, "reply_content": a.content, "reply_time": DateFormat(a.write_time).format('Y-m-d H:i:s')})
    print(list)
    
    
    msg = {'reply': list}
    return HttpResponse(json.dumps(msg), content_type="application/json")


def boardDelete(request):
    text_id = request.GET.get("id")
    del_text = Board.objects.get(id = text_id)
    del_text.delete()
    
    return HttpResponseRedirect("/board")




