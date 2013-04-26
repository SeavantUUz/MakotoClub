$(document).ready(function() {
  $("[alt='用户上传图片']").each(function() {
    maxWidth=750;
    width = $(this).width();
    height = $(this).height();
    if (width>maxWidth) {
      ratio = maxWidth/width;
      $(this).css('width', maxWidth);
      $(this).css('height', height*ratio);
    }
  })
})