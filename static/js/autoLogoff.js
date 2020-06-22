/*
* autoLogoff.js
*
* Every valid navigation (form submit, click on links) should
* set this variable to true.
*
* If it is left to false the page will try to invalidate the
* session via an AJAX call
*/
var validNavigation = false;

/*
* Invokes the servlet /endSession to invalidate the session.
* No HTML output is returned
*/
function endSession() {
   var formData = {
  'tag':'logout'
  };

  $.ajax({
    type:"POST",
    url:"services/router.php",
    data:formData,//correct value
    dataType:"json",
    success: function(data){
      if(data.code === "00"){
        window.event.close;
      }

      if(data.code === "01"){
        notificationDisplayMessage(data.msg,data.code);
      }
    },
    error: onAjaxError,
    timeout: 10000,
    cache:false
  });
}

function wireUpEvents() {

  /*
  * For a list of events that triggers onbeforeunload on IE
  * check http://msdn.microsoft.com/en-us/library/ms536907(VS.85).aspx
  */
  window.onbeforeunload = function() {
      if (!validNavigation) {
         endSession();
      }
  }

  // Attach the event click for all links in the page
  $("a").bind("click", function() {
     validNavigation = true;
  });

  // Attach the event submit for all forms in the page
  $("form").bind("submit", function() {
     validNavigation = true;
  });

}

// Wire up the events as soon as the DOM tree is ready
$(document).ready(function() {
    wireUpEvents();  
});