importScripts('https://www.gstatic.com/firebasejs/3.9.0/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/3.9.0/firebase-messaging.js');

var config = {
  apiKey: "AIzaSyAW3kAvd1byTIeqvUKRr6s1tQOszDNPVwA",
  authDomain: "portal-gsti-1205.firebaseapp.com",
  databaseURL: "https://portal-gsti-1205.firebaseio.com",
  projectId: "portal-gsti-1205",
  storageBucket: "portal-gsti-1205.appspot.com",
  messagingSenderId: "784080308511"
};

firebase.initializeApp(config);

const messaging = firebase.messaging();

messaging.setBackgroundMessageHandler(function(payload){
  console.dir(payload);
  var title = payload.data.title;

  return self.registration.showNotification();
});