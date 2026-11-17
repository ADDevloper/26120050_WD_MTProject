/* ═══════════════════════════════════════════════════════
   SCRIPT.JS — Interactive Animations & Micro-interactions
   Portfolio Website — Abhay Dewangan
   Pure Vanilla JavaScript (no libraries)
   ═══════════════════════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', () => {
    'use strict';

    // ─────────────────────────────────────────
    // 1. TYPEWRITER EFFECT
    // ─────────────────────────────────────────
    const typedEl = document.getElementById('typed-name');
    const phrases = [
        'Abhay Dewangan',
        'a Startup Founder',
        'Building FlowLab',
        'Building Closet',
        'a Developer'
    ];
    let phraseIndex = 0;
    let charIndex = 0;
    let isDeleting = false;
    let typeSpeed = 100;

    function typeWriter() {
        const current = phrases[phraseIndex];

        if (isDeleting) {
            typedEl.textContent = current.substring(0, charIndex - 1);
            charIndex--;
            typeSpeed = 50;
        } else {
            typedEl.textContent = current.substring(0, charIndex + 1);
            charIndex++;
            typeSpeed = 100;
        }

        // Finished typing current phrase
        if (!isDeleting && charIndex === current.length) {
            typeSpeed = 2000; // Pause at end
            isDeleting = true;
        }

        // Finished deleting
        if (isDeleting && charIndex === 0) {
            isDeleting = false;
            phraseIndex = (phraseIndex + 1) % phrases.length;
            typeSpeed = 300; // Brief pause before next
        }

        setTimeout(typeWriter, typeSpeed);
    }

    // Start typewriter after a short delay
    setTimeout(typeWriter, 800);


    // ─────────────────────────────────────────
    // 2. PARTICLES CANVAS (Background)
    // ─────────────────────────────────────────
    const canvas = document.getElementById('particles-canvas');
    const ctx = canvas.getContext('2d');
    let particles = [];
    let mouseX = 0;
    let mouseY = 0;

    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }

    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    class Particle {
        constructor() {
            this.reset();
        }

        reset() {
            this.x = Math.random() * canvas.width;
            this.y = Math.random() * canvas.height;
            this.size = Math.random() * 2 + 0.5;
            this.speedX = (Math.random() - 0.5) * 0.5;
            this.speedY = (Math.random() - 0.5) * 0.5;
            this.opacity = Math.random() * 0.4 + 0.1;
        }

        update() {
            this.x += this.speedX;
            this.y += this.speedY;

            // Mouse repulsion (subtle)
            const dx = this.x - mouseX;
            const dy = this.y - mouseY;
            const dist = Math.sqrt(dx * dx + dy * dy);
            if (dist < 120) {
                const force = (120 - dist) / 120;
                this.x += (dx / dist) * force * 1.5;
                this.y += (dy / dist) * force * 1.5;
            }

            // Wrap around edges
            if (this.x < 0) this.x = canvas.width;
            if (this.x > canvas.width) this.x = 0;
            if (this.y < 0) this.y = canvas.height;
            if (this.y > canvas.height) this.y = 0;
        }

        draw() {
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(232, 115, 74, ${this.opacity})`;
            ctx.fill();
        }
    }

    // Create particles
    const particleCount = Math.min(80, Math.floor(window.innerWidth / 15));
    for (let i = 0; i < particleCount; i++) {
        particles.push(new Particle());
    }

    function drawConnections() {
        for (let i = 0; i < particles.length; i++) {
            for (let j = i + 1; j < particles.length; j++) {
                const dx = particles[i].x - particles[j].x;
                const dy = particles[i].y - particles[j].y;
                const dist = Math.sqrt(dx * dx + dy * dy);

                if (dist < 150) {
                    const opacity = (1 - dist / 150) * 0.15;
                    ctx.beginPath();
                    ctx.moveTo(particles[i].x, particles[i].y);
                    ctx.lineTo(particles[j].x, particles[j].y);
                    ctx.strokeStyle = `rgba(232, 115, 74, ${opacity})`;
                    ctx.lineWidth = 0.5;
                    ctx.stroke();
                }
            }
        }
    }

    function animateParticles() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        particles.forEach(p => {
            p.update();
            p.draw();
        });

        drawConnections();
        requestAnimationFrame(animateParticles);
    }

    animateParticles();

    // Track mouse for particle interaction
    document.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
    });


    // ─────────────────────────────────────────
    // 3. CURSOR GLOW EFFECT (Desktop Only)
    // ─────────────────────────────────────────
    const cursorGlow = document.getElementById('cursor-glow');

    if (window.matchMedia('(hover: hover) and (pointer: fine)').matches && cursorGlow) {
        document.addEventListener('mousemove', (e) => {
            cursorGlow.style.left = e.clientX + 'px';
            cursorGlow.style.top = e.clientY + 'px';
        });
    }


    // ─────────────────────────────────────────
    // 4. SCROLL PROGRESS BAR
    // ─────────────────────────────────────────
    const progressBar = document.getElementById('progress-bar');

    function updateProgressBar() {
        const scrollTop = document.documentElement.scrollTop;
        const scrollHeight = document.documentElement.scrollHeight - window.innerHeight;
        const progress = (scrollTop / scrollHeight) * 100;
        progressBar.style.width = progress + '%';
    }

    window.addEventListener('scroll', updateProgressBar);


    // ─────────────────────────────────────────
    // 5. NAVBAR — Scroll State & Active Link
    // ─────────────────────────────────────────
    const navbar = document.getElementById('navbar');
    const navLinks = document.querySelectorAll('.nav-link[data-section]');
    const sections = document.querySelectorAll('.section');

    // Add scrolled class to navbar
    function handleNavScroll() {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    }

    window.addEventListener('scroll', handleNavScroll);

    // Active link highlighting with Intersection Observer
    const sectionObserverOptions = {
        root: null,
        rootMargin: '-20% 0px -60% 0px',
        threshold: 0
    };

    const sectionObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const id = entry.target.id;
                navLinks.forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('data-section') === id) {
                        link.classList.add('active');
                    }
                });
            }
        });
    }, sectionObserverOptions);

    sections.forEach(section => sectionObserver.observe(section));


    // ─────────────────────────────────────────
    // 6. MOBILE HAMBURGER MENU & OVERLAY
    // ─────────────────────────────────────────
    const hamburger = document.getElementById('hamburger');
    const navLinksContainer = document.getElementById('nav-links');
    const navOverlay = document.getElementById('nav-overlay');

    function closeMobileMenu() {
        if (hamburger) hamburger.classList.remove('active');
        if (navLinksContainer) navLinksContainer.classList.remove('open');
        if (navOverlay) navOverlay.classList.remove('active');
        document.body.style.overflow = '';
    }

    function toggleMobileMenu() {
        const isOpen = navLinksContainer.classList.toggle('open');
        hamburger.classList.toggle('active', isOpen);
        if (navOverlay) navOverlay.classList.toggle('active', isOpen);
        document.body.style.overflow = isOpen ? 'hidden' : '';
    }

    if (hamburger) {
        hamburger.addEventListener('click', toggleMobileMenu);
    }

    if (navOverlay) {
        navOverlay.addEventListener('click', closeMobileMenu);
    }

    // Close menu on link click
    navLinksContainer.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', closeMobileMenu);
    });


    // ─────────────────────────────────────────
    // 7. SCROLL REVEAL ANIMATION
    // ─────────────────────────────────────────
    const revealElements = document.querySelectorAll('.reveal');

    const revealObserverOptions = {
        root: null,
        rootMargin: '0px 0px -80px 0px',
        threshold: 0.1
    };

    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                // Add staggered delay for sibling elements
                const siblings = entry.target.parentElement.querySelectorAll('.reveal');
                let delay = 0;
                siblings.forEach((sibling, i) => {
                    if (sibling === entry.target) {
                        delay = i * 100;
                    }
                });

                setTimeout(() => {
                    entry.target.classList.add('revealed');
                }, delay);

                revealObserver.unobserve(entry.target);
            }
        });
    }, revealObserverOptions);

    revealElements.forEach(el => revealObserver.observe(el));


    // ─────────────────────────────────────────
    // 8. CARD TILT EFFECT (3D Hover — Desktop Only)
    // ─────────────────────────────────────────
    if (window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
        const tiltCards = document.querySelectorAll('[data-tilt]');

        tiltCards.forEach(card => {
            card.addEventListener('mousemove', (e) => {
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                const centerX = rect.width / 2;
                const centerY = rect.height / 2;

                const rotateX = ((y - centerY) / centerY) * -5;
                const rotateY = ((x - centerX) / centerX) * 5;

                card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.02, 1.02, 1.02)`;
            });

            card.addEventListener('mouseleave', () => {
                card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) scale3d(1, 1, 1)';
            });
        });
    }


    // ─────────────────────────────────────────
    // 9. COUNTER ANIMATION (Stats)
    // ─────────────────────────────────────────
    const statNumbers = document.querySelectorAll('.stat-number[data-target]');
    let countersAnimated = false;

    function animateCounters() {
        statNumbers.forEach(stat => {
            const target = parseInt(stat.getAttribute('data-target'));
            const duration = 2000;
            const startTime = performance.now();

            function updateCounter(currentTime) {
                const elapsed = currentTime - startTime;
                const progress = Math.min(elapsed / duration, 1);

                // Ease out cubic
                const eased = 1 - Math.pow(1 - progress, 3);
                const current = Math.round(eased * target);

                stat.textContent = current;

                if (progress < 1) {
                    requestAnimationFrame(updateCounter);
                }
            }

            requestAnimationFrame(updateCounter);
        });
    }

    // Trigger counter when stats row is visible
    const statsRow = document.querySelector('.stats-row');
    if (statsRow) {
        const counterObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && !countersAnimated) {
                    countersAnimated = true;
                    animateCounters();
                    counterObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });

        counterObserver.observe(statsRow);
    }


    // ─────────────────────────────────────────
    // 10. SMOOTH SCROLL (Enhanced)
    // ─────────────────────────────────────────
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetEl = document.querySelector(targetId);

            if (targetEl) {
                const offset = 80; // Navbar height
                const targetPosition = targetEl.getBoundingClientRect().top + window.scrollY - offset;

                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });


    // ─────────────────────────────────────────
    // 11. PARALLAX EFFECT ON HERO SHAPES
    // ─────────────────────────────────────────
    const heroShapes = document.querySelectorAll('.shape');

    window.addEventListener('scroll', () => {
        const scrolled = window.scrollY;

        heroShapes.forEach((shape, index) => {
            const speed = 0.1 + (index * 0.05);
            shape.style.transform = `translateY(${scrolled * speed}px)`;
        });
    });


    // ─────────────────────────────────────────
    // 12. MAGNETIC BUTTON EFFECT
    // ─────────────────────────────────────────
    const magneticBtns = document.querySelectorAll('.btn');

    magneticBtns.forEach(btn => {
        btn.addEventListener('mousemove', (e) => {
            const rect = btn.getBoundingClientRect();
            const x = e.clientX - rect.left - rect.width / 2;
            const y = e.clientY - rect.top - rect.height / 2;

            btn.style.transform = `translate(${x * 0.2}px, ${y * 0.2}px)`;
        });

        btn.addEventListener('mouseleave', () => {
            btn.style.transform = 'translate(0, 0)';
        });
    });


    // ─────────────────────────────────────────
    // 13. SKILL TAG STAGGERED ANIMATION
    // ─────────────────────────────────────────
    const skillCategories = document.querySelectorAll('.skill-category');

    skillCategories.forEach(category => {
        const tags = category.querySelectorAll('.skill-tag');

        const tagObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    tags.forEach((tag, i) => {
                        tag.style.opacity = '0';
                        tag.style.transform = 'translateY(10px) scale(0.9)';
                        tag.style.transition = `all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1) ${i * 80}ms`;

                        setTimeout(() => {
                            tag.style.opacity = '1';
                            tag.style.transform = 'translateY(0) scale(1)';
                        }, 100);
                    });
                    tagObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.3 });

        tagObserver.observe(category);
    });


    // ─────────────────────────────────────────
    // 14. SECTION LINE DRAW ANIMATION
    // ─────────────────────────────────────────
    const sectionLines = document.querySelectorAll('.section-line');

    sectionLines.forEach(line => {
        line.style.width = '0px';
        line.style.transition = 'width 0.8s cubic-bezier(0.16, 1, 0.3, 1)';

        const lineObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    setTimeout(() => {
                        entry.target.style.width = '60px';
                    }, 400);
                    lineObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });

        lineObserver.observe(line);
    });


    // ─────────────────────────────────────────
    // 15. RIPPLE EFFECT ON BUTTONS
    // ─────────────────────────────────────────
    document.querySelectorAll('.btn').forEach(btn => {
        btn.addEventListener('click', function (e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();

            ripple.style.cssText = `
                position: absolute;
                background: rgba(255,255,255,0.3);
                border-radius: 50%;
                width: 0; height: 0;
                left: ${e.clientX - rect.left}px;
                top: ${e.clientY - rect.top}px;
                transform: translate(-50%, -50%);
                animation: rippleAnim 0.6s ease-out forwards;
                pointer-events: none;
            `;

            this.appendChild(ripple);
            setTimeout(() => ripple.remove(), 600);
        });
    });

    // Add ripple animation keyframes dynamically
    const rippleStyle = document.createElement('style');
    rippleStyle.textContent = `
        @keyframes rippleAnim {
            to {
                width: 300px;
                height: 300px;
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(rippleStyle);


    // ─────────────────────────────────────────
    // 16. TIMELINE DOT PULSE ON SCROLL
    // ─────────────────────────────────────────
    const timelineDots = document.querySelectorAll('.timeline-dot');

    timelineDots.forEach((dot, index) => {
        const dotObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    setTimeout(() => {
                        dot.style.transition = 'all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1)';
                        dot.style.transform = 'scale(1.5)';
                        setTimeout(() => {
                            dot.style.transform = 'scale(1)';
                        }, 300);
                    }, index * 200);
                    dotObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });

        dotObserver.observe(dot);
    });


    // ─────────────────────────────────────────
    // 17. FOOTER YEAR (Auto-update)
    // ─────────────────────────────────────────
    const footerYear = document.querySelector('.footer-year');
    if (footerYear) {
        const year = new Date().getFullYear();
        footerYear.innerHTML = `&copy; ${year} — All Rights Reserved`;
    }


    // ─────────────────────────────────────────
    // PERFORMANCE: Throttle scroll events
    // ─────────────────────────────────────────
    let ticking = false;
    window.addEventListener('scroll', () => {
        if (!ticking) {
            window.requestAnimationFrame(() => {
                updateProgressBar();
                handleNavScroll();
                ticking = false;
            });
            ticking = true;
        }
    });

    // Log to console for fun 😄
    console.log(
        '%c🚀 Built by Abhay Dewangan',
        'color: #E8734A; font-size: 16px; font-weight: bold;'
    );
    console.log(
        '%c19-y/o Founder | Building FlowLab & Closet in Public\nIIM Bangalore — BBA in DBE',
        'color: #A1A1AA; font-size: 12px;'
    );
});
