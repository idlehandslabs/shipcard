const ENDPOINT = 'https://orders.idlehandslabs.workers.dev/waitlist';

const form = document.getElementById('form');
const msg = document.getElementById('msg');
const go = document.getElementById('go');

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  go.disabled = true;
  msg.textContent = 'Adding you...';
  try {
    const res = await fetch(ENDPOINT, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({
        email: document.getElementById('email').value.trim(),
        project_type: document.getElementById('type').value,
      }),
    });
    if (res.ok) {
      msg.textContent = "You're on the list. I'll write when it opens.";
      form.reset();
    } else if (res.status === 400) {
      msg.textContent = "That email doesn't look right. Check it and try again.";
    } else {
      msg.textContent = 'Something went wrong on my side. Try again in a bit.';
    }
  } catch {
    msg.textContent = "Couldn't reach the waitlist. Check your connection and try again.";
  }
  go.disabled = false;
});
