chrome.tabs.query({'active': true, 'lastFocusedWindow': true, 'currentWindow': true}, function (tabs) {
    var url = tabs[0].url;
    document.body.innerHTML += url;
});