importScripts('https://www.gstatic.com/firebasejs/8.3.2/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/8.3.2/firebase-messaging.js');

var firebaseConfig = {
    apiKey: "AIzaSyAktNMg9BSj6waQvJBIZHvU52qBPRBWZIk",
    authDomain: "notifications-test-stefano.firebaseapp.com",
    projectId: "notifications-test-stefano",
    storageBucket: "notifications-test-stefano.appspot.com",
    messagingSenderId: "707914582679",
    appId: "1:707914582679:web:011c79c9b6dd3330fcb7d2",
    measurementId: "G-GRZSQ1P02K"
  };

  firebase.initializeApp(firebaseConfig);
  const messaging = firebase.messaging();


