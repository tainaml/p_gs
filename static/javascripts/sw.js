importScripts('https://www.gstatic.com/firebasejs/4.0.0/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/4.0.0/firebase-messaging.js');
importScripts('/static/javascripts/firebase-init.js');

const messaging = firebase.messaging();
messaging.setBackgroundMessageHandler( function(payload) {
  var title = payload.data.title;

  return self.registration.showNotification();
});
