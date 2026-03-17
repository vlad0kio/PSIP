// scripts.js - ПОЛНЫЙ ФАЙЛ СО ВСЕМИ СКРИПТАМИ

document.addEventListener('DOMContentLoaded', () => {
    
    // ============================================
    // 1. ОРИГИНАЛЬНЫЕ СКРИПТЫ
    // ============================================
    
    // Переключение слайдов в hero-секции
    const btnLeft = document.querySelector('.btn1');
    const btnRight = document.querySelector('.btn2');
    const heroPhotos = document.querySelectorAll('.hero_Photo');
    const statusSegments = document.querySelectorAll('.status-bar .segment');
    let currentSlideIndex = 0;

    // Увеличение логотипа при наведении
    const logo = document.querySelector('.logo');
    if (logo) {
        logo.addEventListener('mouseenter', () => {
            logo.style.transform = 'scale(1.2)';
            logo.style.transition = 'transform 0.3s ease';
        });
        logo.addEventListener('mouseleave', () => {
            logo.style.transform = 'scale(1)';
        });
    }

    // Карусель в hero-секции
    const images = document.querySelectorAll('.hero-photo-container .hero_Photo');
    const totalImages = images.length;
    const heroStatusSegments = document.querySelectorAll('.status-bar .segment');
    let currentIndex = 0;

    const showImage = (index) => {
        images.forEach((img, i) => {
            img.style.display = i === index ? 'block' : 'none';
        });
        heroStatusSegments.forEach((segment, i) => {
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

    const nextBtn = document.querySelector('.btn2');
    const prevBtn = document.querySelector('.btn1');
    
    if (nextBtn && prevBtn) {
        nextBtn.addEventListener('click', goToNext);
        prevBtn.addEventListener('click', goToPrev);
        showImage(currentIndex);
    }

    // Копирование номера телефона
    document.querySelectorAll('.phone-number').forEach(element => {
        element.addEventListener('click', () => {
            const text = element.textContent;
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

    // Открытие ссылок мессенджеров
    document.querySelectorAll('.icons .icon').forEach(icon => {
        icon.addEventListener('click', () => {
            const url = icon.getAttribute('data-url');
            if (url) window.open(url, '_blank');
        });
    });

    // Увеличение изображений технологий при наведении
    document.querySelectorAll('.technologics-icons').forEach(img => {
        img.addEventListener('mouseenter', () => {
            img.style.transform = 'scale(1.2)';
            img.style.transition = 'transform 0.3s ease';
        });
        img.addEventListener('mouseleave', () => {
            img.style.transform = 'scale(1)';
        });
    });

    // ============================================
    // 2. ВАЛИДАЦИЯ НИЖНЕЙ ФОРМЫ (registr-form2)
    // ============================================
    
    const smetaForm = document.querySelector('.registr-form2');
    
    if (smetaForm) {
        const nameInput = smetaForm.querySelector('input[placeholder*="Имя"]');
        const phoneInput = smetaForm.querySelector('input[placeholder*="Телефон"]');
        const submitBtn = smetaForm.querySelector('.custom-button2');
        const checkbox = smetaForm.querySelector('input[type="checkbox"]');
        
        // Создаем контейнер для сообщений об ошибках
        const errorContainer = document.createElement('div');
        errorContainer.className = 'smeta-error-container';
        errorContainer.style.color = '#ff4444';
        errorContainer.style.fontSize = '14px';
        errorContainer.style.marginTop = '10px';
        errorContainer.style.textAlign = 'center';
        errorContainer.style.minHeight = '20px';
        smetaForm.appendChild(errorContainer);
        
        submitBtn.addEventListener('click', (e) => {
            e.preventDefault();
            
            // Удаляем предыдущие ошибки
            errorContainer.textContent = '';
            if (nameInput) nameInput.style.borderColor = '#E4E5E6';
            if (phoneInput) phoneInput.style.borderColor = '#E4E5E6';
            
            let isValid = true;
            let errorMessage = '';
            
            // Проверка имени (минимум 3 символа)
            if (!nameInput || nameInput.value.trim().length < 3) {
                isValid = false;
                if (nameInput) nameInput.style.borderColor = '#ff4444';
                errorMessage = 'Имя должно содержать минимум 3 символа';
            }
            
            // Проверка телефона (не пустой)
            if (isValid && (!phoneInput || phoneInput.value.trim() === '')) {
                isValid = false;
                if (phoneInput) phoneInput.style.borderColor = '#ff4444';
                errorMessage = 'Введите номер телефона';
            }
            
            // Проверка согласия
            if (isValid && checkbox && !checkbox.checked) {
                isValid = false;
                errorMessage = 'Необходимо согласие на обработку данных';
            }
            
            if (isValid) {
                // Успешная отправка
                errorContainer.style.color = '#4CAF50';
                errorContainer.textContent = 'Спасибо! Мы свяжемся с вами';
                
                // Очищаем форму
                if (nameInput) nameInput.value = '';
                if (phoneInput) phoneInput.value = '';
                if (checkbox) checkbox.checked = false;
                
                // Очищаем сообщение через 3 секунды
                setTimeout(() => {
                    errorContainer.textContent = '';
                    errorContainer.style.color = '#ff4444';
                }, 3000);
            } else {
                // Показываем ошибку
                errorContainer.textContent = errorMessage;
            }
        });
        
        // Очистка красной рамки при вводе
        if (nameInput) {
            nameInput.addEventListener('input', () => {
                nameInput.style.borderColor = '#E4E5E6';
                errorContainer.textContent = '';
            });
        }
        
        if (phoneInput) {
            phoneInput.addEventListener('input', () => {
                phoneInput.style.borderColor = '#E4E5E6';
                errorContainer.textContent = '';
            });
        }
        
        if (checkbox) {
            checkbox.addEventListener('change', () => {
                errorContainer.textContent = '';
            });
        }
    }

    // ============================================
    // 3. ДОПОЛНИТЕЛЬНЫЕ СКРИПТЫ
    // ============================================

    /**
     * 3.1 ПЛАВНАЯ ПРОКРУТКА К ЯКОРЯМ
     */
    document.querySelectorAll('a[href^="#"]').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    /**
     * 3.2 АНИМАЦИЯ ПОЯВЛЕНИЯ ЭЛЕМЕНТОВ ПРИ СКРОЛЛЕ
     */
    const animatedElements = document.querySelectorAll('.service-card, .method3, .hero_left, .free-section');
    
    const fadeInObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, { threshold: 0.1 });

    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        fadeInObserver.observe(el);
    });

    /**
     * 3.3 ВАЛИДАЦИЯ ВЕРХНЕЙ ФОРМЫ (registr-form)
     */
    const topForm = document.querySelector('.registr-form');
    
    if (topForm) {
        const nameInput = topForm.querySelector('input[placeholder*="Имя"]');
        const phoneInput = topForm.querySelector('input[placeholder*="Телефон"]');
        const submitBtn = topForm.querySelector('.custom-button2');
        const checkbox = topForm.querySelector('input[type="checkbox"]');
        
        const errorContainer = document.createElement('div');
        errorContainer.className = 'top-error-container';
        errorContainer.style.color = '#ff4444';
        errorContainer.style.fontSize = '14px';
        errorContainer.style.marginTop = '10px';
        errorContainer.style.textAlign = 'center';
        errorContainer.style.minHeight = '20px';
        topForm.appendChild(errorContainer);
        
        submitBtn.addEventListener('click', (e) => {
            e.preventDefault();
            
            errorContainer.textContent = '';
            if (nameInput) nameInput.style.borderColor = '#E4E5E6';
            if (phoneInput) phoneInput.style.borderColor = '#E4E5E6';
            
            let isValid = true;
            let errorMessage = '';
            
            if (!nameInput || nameInput.value.trim().length < 3) {
                isValid = false;
                if (nameInput) nameInput.style.borderColor = '#ff4444';
                errorMessage = 'Имя должно содержать минимум 3 символа';
            }
            
            if (isValid && (!phoneInput || phoneInput.value.trim() === '')) {
                isValid = false;
                if (phoneInput) phoneInput.style.borderColor = '#ff4444';
                errorMessage = 'Введите номер телефона';
            }
            
            if (isValid && checkbox && !checkbox.checked) {
                isValid = false;
                errorMessage = 'Необходимо согласие на обработку данных';
            }
            
            if (isValid) {
                errorContainer.style.color = '#4CAF50';
                errorContainer.textContent = 'Спасибо! Мы свяжемся с вами';
                
                if (nameInput) nameInput.value = '';
                if (phoneInput) phoneInput.value = '';
                if (checkbox) checkbox.checked = false;
                
                setTimeout(() => {
                    errorContainer.textContent = '';
                    errorContainer.style.color = '#ff4444';
                }, 3000);
            } else {
                errorContainer.textContent = errorMessage;
            }
        });
        
        if (nameInput) {
            nameInput.addEventListener('input', () => {
                nameInput.style.borderColor = '#E4E5E6';
                errorContainer.textContent = '';
            });
        }
        
        if (phoneInput) {
            phoneInput.addEventListener('input', () => {
                phoneInput.style.borderColor = '#E4E5E6';
                errorContainer.textContent = '';
            });
        }
        
        if (checkbox) {
            checkbox.addEventListener('change', () => {
                errorContainer.textContent = '';
            });
        }
    }

    /**
     * 3.4 ПАРАЛЛАКС ЭФФЕКТ
     */
    const parallaxSections = document.querySelectorAll('.free-art, .background-map');
    
    window.addEventListener('scroll', () => {
        parallaxSections.forEach(section => {
            const scrolled = window.pageYOffset;
            section.style.backgroundPositionY = `${scrolled * 0.3}px`;
        });
    });

    /**
     * 3.5 АКТИВНОЕ МЕНЮ
     */
    const sections = document.querySelectorAll('section');
    const navButtons = document.querySelectorAll('.nav-btn');
    
    window.addEventListener('scroll', () => {
        let current = '';
        const scrollPos = window.pageYOffset;
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop - 200;
            const sectionBottom = sectionTop + section.offsetHeight;
            
            if (scrollPos >= sectionTop && scrollPos < sectionBottom) {
                current = section.getAttribute('class') || '';
            }
        });

        navButtons.forEach(btn => {
            btn.style.color = '#333';
            btn.style.borderBottom = 'none';
            
            const btnText = btn.querySelector('span')?.textContent.trim().toLowerCase();
            if (btnText && current.toLowerCase().includes(btnText)) {
                btn.style.color = '#DCB658';
                btn.style.borderBottom = '2px solid #DCB658';
            }
        });
    });

    /**
     * 3.6 КНОПКА "НАВЕРХ"
     */
    const scrollTopBtn = document.createElement('button');
    scrollTopBtn.innerHTML = '↑';
    scrollTopBtn.style.position = 'fixed';
    scrollTopBtn.style.bottom = '30px';
    scrollTopBtn.style.right = '30px';
    scrollTopBtn.style.width = '50px';
    scrollTopBtn.style.height = '50px';
    scrollTopBtn.style.borderRadius = '50%';
    scrollTopBtn.style.backgroundColor = '#DCB658';
    scrollTopBtn.style.color = 'white';
    scrollTopBtn.style.border = 'none';
    scrollTopBtn.style.cursor = 'pointer';
    scrollTopBtn.style.fontSize = '24px';
    scrollTopBtn.style.zIndex = '100';
    scrollTopBtn.style.boxShadow = '0 2px 10px rgba(0,0,0,0.2)';
    scrollTopBtn.style.display = 'none';
    
    document.body.appendChild(scrollTopBtn);
    
    window.addEventListener('scroll', () => {
        scrollTopBtn.style.display = window.pageYOffset > 300 ? 'block' : 'none';
    });
    
    scrollTopBtn.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    /**
     * 3.7 ПРОГРЕСС-БАР ПРИ СКРОЛЛЕ
     */
    const progressBar = document.createElement('div');
    progressBar.style.position = 'fixed';
    progressBar.style.top = '0';
    progressBar.style.left = '0';
    progressBar.style.height = '3px';
    progressBar.style.backgroundColor = '#DCB658';
    progressBar.style.zIndex = '1000';
    progressBar.style.transition = 'width 0.1s ease';
    
    document.body.appendChild(progressBar);
    
    window.addEventListener('scroll', () => {
        const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
        const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        const scrolled = (winScroll / height) * 100;
        progressBar.style.width = scrolled + '%';
    });

    /**
     * 3.8 УЛУЧШЕННЫЕ ХОВЕР-ЭФФЕКТЫ
     */
    document.querySelectorAll('.method3').forEach(card => {
        card.addEventListener('mouseenter', () => {
            const icon = card.querySelector('.technologics-icons');
            const text = card.querySelector('.method3-text');
            
            if (icon) {
                icon.style.transform = 'scale(1.1) translateY(-5px)';
            }
            if (text) {
                text.style.color = '#DCB658';
            }
        });
        
        card.addEventListener('mouseleave', () => {
            const icon = card.querySelector('.technologics-icons');
            const text = card.querySelector('.method3-text');
            
            if (icon) {
                icon.style.transform = 'scale(1) translateY(0)';
            }
            if (text) {
                text.style.color = '';
            }
        });
    });

    /**
     * 3.9 ДИНАМИЧЕСКИЙ ГОД В КОПИРАЙТЕ
     */
    const copyrightElement = document.querySelector('div[style*="left: -500px"]');
    if (copyrightElement) {
        const currentYear = new Date().getFullYear();
        copyrightElement.textContent = copyrightElement.textContent.replace('2023', currentYear);
    }

    // Логируем успешную загрузку
    console.log('✅ Все скрипты успешно загружены и работают!');
});