from django.shortcuts import render,redirect
from board.models import Bulletin_Board,Reply
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User

rowsPerPage = 10
def home(request):
	if request.GET.get('current_page') :
		current_page = int(request.GET['current_page'] )
	else:current_page=1
	start = (current_page-1)*rowsPerPage
	end = current_page*rowsPerPage
	boardList = Bulletin_Board.objects.order_by('-id')[start:end]
	totalCnt = Bulletin_Board.objects.count()
	
	pagingHelperIns = pagingHelper();
	totalPageList = pagingHelperIns.getTotalPageList(totalCnt,rowsPerPage)
	#print(totalPageList)
	return render(request,"board/board_home.html",{
		"totalCnt":totalCnt,
		"boardList":boardList,
		'totalPageList':totalPageList,
		'current_page':current_page
	})

def page_move(request):
	current_page = int(request.GET['current_page'])
	return HttpResponseRedirect('/board?current_page=' + str(current_page))  
	

class pagingHelper:
	def getTotalPageList(self, total_cnt, rowsPerPage):
		if((total_cnt%rowsPerPage) == 0):
			self.total_pages = int(total_cnt / rowsPerPage)
		else:
			self.total_pages = int(total_cnt / rowsPerPage) + 1
			
		self.totalPageList = []
		for j in range(self.total_pages):
			self.totalPageList.append(j+1)
		return self.totalPageList
	
	def __init__(self):
		self.total_pages = 0
		self.totalPageList = 0
		
def passCheck(request):
    p = request.POST['pass']
    pk= request.GET['memo_id']
    boardData = Bulletin_Board.objects.get(id=pk)
    if boardData.secret_board_key == p:
        replyData = Reply.objects.filter(subject_text = boardData)
        Bulletin_Board.objects.filter(id=pk).update(hits = boardData.hits + 1)
        return render(request,'board/viewMemo.html', {'memo_id': request.GET['memo_id'], 
                                                #'current_page':request.GET['current_page'], 
                                                'searchStr': None, 
                                                'boardData': boardData,
												'replyList': replyData
												 } )
    else:
        return render(request,'board/confirmation.html',{'memo_id':pk,'msg':"WRONG PASSWORD"})
		
def viewWork(request):	
	pk= request.GET['memo_id']
	
	boardData = Bulletin_Board.objects.get(id=pk)
	
	if (boardData.secret_board == True): return render(request,'board/confirmation.html',{'memo_id': pk})
	else:
		replyData = Reply.objects.filter(subject_text = boardData)
		Bulletin_Board.objects.filter(id=pk).update(hits = boardData.hits + 1)
		return render(request,'board/viewMemo.html', {'memo_id': request.GET['memo_id'], 
                                                #'current_page':request.GET['current_page'], 
                                                'searchStr': request.GET['searchStr'], 
                                                'boardData': boardData,
												'replyList': replyData
												 } )  
@csrf_exempt
def DoWriteBoard(request):
    if request.POST.get('secret_board'): t = True
    else: t = False
    userget = User.objects.get(username = request.user.get_username())
    br = Bulletin_Board (subject = request.POST['subject'],
         name = userget,
         mail = request.POST['email'],
         memo = request.POST['memo'],
         created_date = timezone.now(),
         hits = 0,
		 secret_board = t,
		 secret_board_key = request.POST['pass'])
    br.save()    
    url = '/board?current_page=1' 
    return HttpResponseRedirect(url)

@csrf_exempt
def DoWriteReply(request):
	userget = User.objects.get(username = request.user.get_username())
	memo_id = request.GET['memo_id']
	searchStr = request.GET['searchStr']
	p = Bulletin_Board.objects.get(id=memo_id)
	rr = Reply(subject_text = p,
			  reply_text = request.POST['reply_text'],
			  name = userget,
			  pub_date = timezone.now())
	rr.save()
	url = '/board/viewWork/?memo_id=' + memo_id + '&searchStr=' + searchStr
	return HttpResponseRedirect(url)

	
	

def writeBoard(request):
	return render(request,"board/writeBoard.html")

def DeleteSpecificRow(request):
    memo_id = request.GET['memo_id']
    #current_page = request.GET['current_page']
    
    p = Bulletin_Board.objects.get(id=memo_id)
    p.delete()            
            
    url = '/board?current_page=1'
    return HttpResponseRedirect(url)

def DeleteReply(request):
	reply_id = request.GET['reply_id']
	r = Reply.objects.get(id=reply_id)
	memo_id = request.GET['memo_id']
	searchStr = request.GET['searchStr']
	r.delete()
	url = '/board/viewWork/?memo_id=' + memo_id + '&searchStr=' + searchStr
	return HttpResponseRedirect(url)
	

@csrf_exempt
def ModifyRow(request):
    memo_id = request.GET['memo_id']
    searchStr = request.GET['searchStr']
    
    boardData = Bulletin_Board.objects.get(id=memo_id)
      
    return render(request,'board/viewForUpdate.html', {'memo_id': request.GET['memo_id'],
                                                'searchStr': request.GET['searchStr'], 
                                                'boardData': boardData } )

@csrf_exempt
def updateBoard(request):
    if request.POST.get('secret_board'): t = True
    else: t = False
    memo_id = request.POST['memo_id']
    searchStr = request.POST['searchStr']        
    
    # Update DataBase
    Bulletin_Board.objects.filter(id=memo_id).update(
                                                  mail= request.POST['mail'],
                                                  subject= request.POST['subject'],
                                                  memo= request.POST['memo'],
		                                          secret_board = t,
		                                          secret_board_key = request.POST['pass']
                                                  )
    url = '/board?current_page=1'
    return HttpResponseRedirect(url)   
	

