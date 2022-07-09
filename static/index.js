$('#twitter-button').on('click', function() {
    // Initialize with your OAuth.io app public key
    OAuth.initialize('vNh6GPQ75Fwe9bCaSkcUSbXuS');
    // Use popup for OAuth
    OAuth.popup('twitter').then(twitter => {
      console.log(twitter);
      // Retrieves user data from oauth provider
      console.log(twitter.me());
    });
  })