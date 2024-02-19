

document.addEventListener('DOMContentLoaded', function () {

   



  
 });

function edit(post_id){
    console.log(post_id)
    var textarea = document.createElement("textarea");
    content_element = document.querySelector(`#content_${post_id}`)
    post_content = content_element.innerHTML
    textarea.innerHTML = post_content
    content_element.replaceWith(textarea);


    edit_btn =document.getElementById(`editpost_${post_id}`);
    var submit_btn = document.createElement('button')
    submit_btn.innerHTML ="submit"
    edit_btn.replaceWith(submit_btn)
    submit_btn.addEventListener('click',()=>{
        console.log("Submitted")
        fetch(`/edit/${post_id}`, {
            method: 'POST',
            headers: {"content-type":"application/json","X-CSRFToken": getCookie("csrftoken")},
            body: JSON.stringify({
              content: textarea.value,
            })
          })
            .then(response => response.json())
            .then(result => {
              // Print result
              content_element.innerHTML = result.data
              submit_btn.replaceWith(edit_btn)
              textarea.replaceWith(content_element);
            });
            
    })

   
}




// this is a fuction from Django docs for csrftoken Verification
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
