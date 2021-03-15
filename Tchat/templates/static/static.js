$('#postMessage').submit(function(event){ event.preventDefault();

     var $form = $(this),
      message = $form.find("input[name='message']").val(),
      url = $form.attr('action');
     $ajax({
          type: 'POST',
          url: url,
          data : JSON.stringify({message:message}),
          contentType: 'application/json',
          dataType: 'json',
          success :function() {location.reload();}
     });
});



function messagePoll(){
     $ajax({
          type:'GET',
          url:'/messages',
          dataType:"json",
          success :function(data){
               updateMessages(data)
          },
          timeout:500,
          complete :setTimeout(messagePoll, 1000)
})
}

function updateMessages(messages){
     var $messageContainer = $('#messageContainer');
     var messageList = []
     var EmptyMessages = '<p>No Messages!</p>';
     if (messages.length === 0){
          $messageContainer.html(emptyMessages)
     } else {
          $ .each(messages, function(index, value){
               var message = $(value.message).text() || value.message;
               messageList.push('<p>' + message + '</p>');
          });
          $messageContainer.html(messageList);
          }
     }