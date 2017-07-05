const messaging = firebase.messaging();
const LOGGED = 1;
const NOT_LOGGED = 0;


function getLoggedAttr() {
  return JSON.parse(document.body.dataset.logged) ? LOGGED : NOT_LOGGED;
}

function setLocalLogged() {
  var isLogged = getLoggedAttr();
  window.localStorage.setItem('isLogged', isLogged);
}

function getLoggedLocalAttr() {
  var localLogged  = window.localStorage.getItem('isLogged');

  if (localLogged) {
    setLocalLogged();
    return getLoggedLocalAttr();
  }

  return localLogged;
}

function hasLoggedStatusDifferent() {
  return getLoggedAttr() != getLoggedLocalAttr()
}

window.onload = function() {
  if (hasLoggedStatusDifferent() && getLoggedLocalAttr() == NOT_LOGGED){
    console.log("User logged, need to sent token again to server");
    setLocalLogged();
    setTokenSentToServer(false);
  }
};

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
        return window.localStorage.getItem('sentToServer') == LOGGED;
    }

    function setTokenSentToServer(sent) {
        window.localStorage.setItem('sentToServer', sent ? LOGGED : NOT_LOGGED);
    }
}
