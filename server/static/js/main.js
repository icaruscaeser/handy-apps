function send_ajax(url, input_json, method){
    var xhttp = new XMLHttpRequest();
    
    xhttp.onreadystatechange = function(){
        if(this.readyState == 4 && this.status = 200){
            console.log('success');
        }
    }
    
    xhttp.open(method, url);
    xhttp.send();
}