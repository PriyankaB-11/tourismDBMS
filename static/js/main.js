document.addEventListener('DOMContentLoaded', () => {
  const flashMessages = document.querySelectorAll('.alert');
  flashMessages.forEach((message) => {
    setTimeout(() => {
      if (message && message.parentNode) {
        message.classList.add('fade');
      }
    }, 4000);
  });
});
