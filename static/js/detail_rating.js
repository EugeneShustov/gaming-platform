document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('rating-form');
  if (!form) return;

  const submitButton = form.querySelector('button[type="submit"]');

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (submitButton) submitButton.disabled = true;

    const formData = new FormData(this);

    fetch(window.location.href, {
      method: 'POST',
      body: formData,
      headers: {
        'X-CSRFToken': getCookie('csrftoken')
      }
    })
      .then(response => {
        if (!response.ok) throw new Error('Ошибка при отправке формы');
        return response.json();
      })
      .then(data => {
        if (!data.game) throw new Error('Нет ID игры');

        return fetch(`/api/games/${data.game}/metascore/`);
      })
      .then(res => {
        if (!res.ok) throw new Error('Ошибка при получении оценки');
        return res.json();
      })
      .then(scoreData => {
        if (typeof scoreData.metascore !== 'number') {
          showMessage('Оценкb нет');
          return;
        }

        updateMetacriticScore(scoreData.metascore);
        showMessage('Оценка обновлена');
      })
      .catch(() => {
        showMessage('Попробуй позже');
      })
      .finally(() => {
        if (submitButton) submitButton.disabled = false;
      });
  });
});

function updateMetacriticScore(score) {
  const block = document.getElementById('metacritic-score');
  if (!block) return;

  const number = block.querySelector('.score-number');
  if (!number) return;

  number.textContent = score;
  block.classList.remove('low', 'medium', 'high');

  if (score < 50) block.classList.add('low');
  else if (score < 75) block.classList.add('medium');
  else block.classList.add('high');

  block.classList.add('pulse');
  setTimeout(() => block.classList.remove('pulse'), 600);
}

function showMessage(text) {
  const message = document.createElement('div');
  message.textContent = text;
  message.className = 'rating-message';
  document.body.appendChild(message);
  setTimeout(() => message.remove(), 3000);
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}


