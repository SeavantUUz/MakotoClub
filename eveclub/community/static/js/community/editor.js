function hideAllEmotionPage() {
  for (i=1;i<=page_num;i=i+1) {
    id='#page'+i;
    $(id).hide();
  }
}

function showEmotionPage(n) {
  hideAllEmotionPage();
  id='#page'+n
  $(id).show();
}

function insertAtCaret(areaId,text) {
  var txtarea = document.getElementById(areaId);
  var scrollPos = txtarea.scrollTop;
  var strPos = 0;
  var br = ((txtarea.selectionStart || txtarea.selectionStart == '0') ? "ff" : (document.selection ? "ie" : false ) );
  if (br == "ie") { 
    txtarea.focus();
    var range = document.selection.createRange();
    range.moveStart ('character', -txtarea.value.length);
    strPos = range.text.length;
  }
  else if (br == "ff") strPos = txtarea.selectionStart;

  var front = (txtarea.value).substring(0,strPos);  
  var back = (txtarea.value).substring(strPos,txtarea.value.length); 
  txtarea.value=front+text+back;
  strPos = strPos + text.length;
  if (br == "ie") { 
    txtarea.focus();
    var range = document.selection.createRange();
    range.moveStart ('character', -txtarea.value.length);
    range.moveStart ('character', strPos);
    range.moveEnd ('character', 0);
    range.select();
  }
  else if (br == "ff") {
    txtarea.selectionStart = strPos;
    txtarea.selectionEnd = strPos;
    txtarea.focus();
  }
  txtarea.scrollTop = scrollPos;
}

function insertEmotion(emotion) {
  emotion_str = '[em '+emotion+']';
  insertAtCaret('editor', emotion_str);
}

function insertA() {
  a_text=$("#a_text");
  a_url=$("#a_url");
  a_text_value=a_text.val();
  a_url_value=a_url.val();
  re=/^(http|https|ftp)\:\/\//i;

  if (a_text_value.length<1) {
    alert("请输入链接文字！");
    return false;
  }
  if (!re.test(a_url_value)) {
    alert("请输入正确的地址！");
    return false;

  }
  a_str = '['+a_text_value+']('+a_url_value+')';
  insertAtCaret('editor', a_str);
}

function insertImg(url) {
  img_str = "![用户上传图片]("+url+")";
  insertAtCaret('editor', img_str);
}

function reply(floor, post_id) {
  $('#reply_form').show();
  if (floor!=0) {
    url = '/community/post/get_for_reply/'+post_id+'/';
    $.get(url, function(data) {
      if (data!='') {
        content = '回复第'+floor+'楼:\n'+data+'\n\n';
        $("#editor").html(content);
      }
      else return false;
    });
  }
  $("#editor").focus();
}

$(document).keypress(function(e){
  if (e.ctrlKey && e.which == 13 || e.which == 10) { 
    $("#editor_form").submit();
    document.body.focus();
  }     
})

$(document).ready(function() {
  page_num = 5;
  hideAllEmotionPage();
  showEmotionPage(1);
})