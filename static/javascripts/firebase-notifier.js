const messaging = firebase.messaging();

if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register(`/static/javascripts/sw.js`)
    .then((registration) => {
        messaging.useServiceWorker(registration);
        messaging.requestPermission().then(() => getToken())
        .catch((err) => console.error('Unable to get permission to notify.', err));

        messaging.onTokenRefresh(() => {
            messaging.getToken()
            .then(function (refreshedToken) {
                setTokenSentToServer(false);
                sendTokenToServer(refreshedToken);
                getToken();
            })
            .catch((err) => console.error('Unable to retrieve refreshed token ', err));
        });
    });

    function getToken() {
        messaging.getToken()
        .then(function(currentToken) {
            if (currentToken) {
                sendTokenToServer(currentToken);
            } else {
                setTokenSentToServer(false);
            }
        })
        .catch((err) => setTokenSentToServer(false) );
    }

    function sendTokenToServer(currentToken) {
        if (!isTokenSentToServer()) {
            $.get('/push/subscribe/', {
                registration_id: currentToken
            });
            setTokenSentToServer(true);
        } else {
            console.info('Token already sent to server so won\'t send it again ' +
              'unless it changes');
        }
    }

    function isTokenSentToServer() {
        return window.localStorage.getItem('sentToServer') == 1;
    }
    function setTokenSentToServer(sent) {
        window.localStorage.setItem('sentToServer', sent ? 1 : 0);
    }
}
