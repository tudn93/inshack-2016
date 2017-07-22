var page = require('webpage').create();
var host = "127.0.0.1";
var port = "5000";
var url = "http://"+host+":"+port+"/backdoor-bot-csrf/X1YEGZmNX75vcsHl470CfS9pCvqbDcbajmXS14d2/ID_TO_REPLACE";
var timeout = 2000;
 
phantom.addCookie({
    'name': 'session',
    'value': 'SESSION_TO_REPLACE',
    'domain': host,
    'path': '/',
    'httponly': true
});
 
page.onNavigationRequested = function(url, type, willNavigate, main) {
    console.log("[URL] URL="+url);  
};
 
page.settings.resourceTimeout = timeout;
page.onResourceTimeout = function(e) {
    setTimeout(function(){
        console.log("[INFO] Timeout")
        phantom.exit();
    }, 1);
};
 
page.open(url, function(status) {
    console.log("[INFO] rendered page");
    setTimeout(function(){
        phantom.exit();
    }, 1);
});
