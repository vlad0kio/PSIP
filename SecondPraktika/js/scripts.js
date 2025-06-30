document.addEventListener('DOMContentLoaded', () => {
  // Переключение слайдов в hero-секции (если есть слайдер)
  const btnLeft = document.querySelector('.btn1');
  const btnRight = document.querySelector('.btn2');
  const heroPhotos = document.querySelectorAll('.hero_Photo');
  const statusSegments = document.querySelectorAll('.status-bar .segment');
  let currentSlideIndex = 0;

  // Обработка кнопок "Кнопки навигации" (если нужно раскрыть меню)
  const navBtn = document.querySelectorAll('.nav-btn');
  const orderButtons = document.querySelectorAll('.custom-button, .custom-button2');
  orderButtons.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      alert('Функция заказа пока недоступна.');
    });
  });
});

  document.addEventListener('DOMContentLoaded', () => {
    // Получаем все изображения с классом 'technologics-icons'
    const images = document.querySelectorAll('.technologics-icons');

    images.forEach((img) => {
      // При наведении увеличиваем изображение
      img.addEventListener('mouseenter', () => {
        img.style.transform = 'scale(1.2)';
        img.style.transition = 'transform 0.3s ease';
      });
      // При убирании курсора возвращаем исходный размер
      img.addEventListener('mouseleave', () => {
        img.style.transform = 'scale(1)';
        img.style.transition = 'transform 0.3s ease';
      });
    });
  });

    document.addEventListener('DOMContentLoaded', () => {
    const logo = document.querySelector('.logo');

    // Увеличение при наведении
    logo.addEventListener('mouseenter', () => {
      logo.style.transform = 'scale(1.2)'; // увеличиваем на 20%
      logo.style.transition = 'transform 0.3s ease'; // плавное увеличение
    });

    // Возврат к исходному размеру
    logo.addEventListener('mouseleave', () => {
      logo.style.transform = 'scale(1)';
    });
  });

  document.addEventListener('DOMContentLoaded', () => {
    const images = document.querySelectorAll('.hero-photo-container .hero_Photo');
    const totalImages = images.length;
    const statusSegments = document.querySelectorAll('.status-bar .segment');
    let currentIndex = 0;

    const showImage = (index) => {
      images.forEach((img, i) => {
        img.style.display = i === index ? 'block' : 'none';
      });
      // Обновление статуса
      statusSegments.forEach((segment, i) => {
        if (i === index) {
          segment.classList.add('filled');
        } else {
          segment.classList.remove('filled');
        }
      });
    };

    const goToNext = () => {
      currentIndex = (currentIndex + 1) % totalImages;
      showImage(currentIndex);
    };

    const goToPrev = () => {
      currentIndex = (currentIndex - 1 + totalImages) % totalImages;
      showImage(currentIndex);
    };

    // Обработчики для кнопок
    document.querySelector('.btn2').addEventListener('click', goToNext);
    document.querySelector('.btn1').addEventListener('click', goToPrev);

    // Изначально показываем первый слайд
    showImage(currentIndex);
  });

    // Получаем все элементы с классом 'phone-number'
  document.querySelectorAll('.phone-number').forEach(function(element) {
    element.addEventListener('click', function() {
      const text = this.textContent;
      // Создаем временный input для копирования
      const input = document.createElement('input');
      input.value = text;
      document.body.appendChild(input);
      input.select();
      try {
        document.execCommand('copy');
        alert('Номер скопирован в буфер обмена: ' + text);
      } catch (err) {
        alert('Не удалось скопировать номер.');
      }
      document.body.removeChild(input);
    });
  });
            
    document.querySelectorAll('.icons .icon').forEach(function(icon) {
        icon.addEventListener('click', function() {
        const url = this.getAttribute('data-url');
        window.open(url, '_blank');
        });
    });

    
  
    