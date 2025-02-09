// Initialize Three.js scene
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ 
    alpha: true,
    antialias: true 
});

// Set up the renderer
const container = document.getElementById('canvas-container');
if (container) {
    // Set renderer size to match container
    const updateRendererSize = () => {
        const rect = container.getBoundingClientRect();
        renderer.setSize(rect.width, rect.height);
        camera.aspect = rect.width / rect.height;
        camera.updateProjectionMatrix();
    };

    renderer.setClearColor(0x000000, 0);
    renderer.setPixelRatio(window.devicePixelRatio);
    container.appendChild(renderer.domElement);
    
    // Set initial size
    updateRendererSize();

    // Create particles
    const particlesGeometry = new THREE.BufferGeometry();
    const particlesCount = 1000;
    const posArray = new Float32Array(particlesCount * 3);

    for (let i = 0; i < particlesCount * 3; i++) {
        posArray[i] = (Math.random() - 0.5) * 5;
    }

    particlesGeometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3));

    // Create material
    const particlesMaterial = new THREE.PointsMaterial({
        size: 0.005,
        color: 0xFF1E1E,
        transparent: true,
        opacity: 0.8,
        sizeAttenuation: true
    });

    // Create mesh
    const particlesMesh = new THREE.Points(particlesGeometry, particlesMaterial);
    scene.add(particlesMesh);

    // Position camera
    camera.position.z = 2;

    // Mouse movement effect with damping
    let mouseX = 0;
    let mouseY = 0;
    let targetX = 0;
    let targetY = 0;
    const dampingFactor = 0.05;

    document.addEventListener('mousemove', (event) => {
        const rect = container.getBoundingClientRect();
        mouseX = ((event.clientX - rect.left) / rect.width) * 2 - 1;
        mouseY = -((event.clientY - rect.top) / rect.height) * 2 + 1;
    });

    // Animation loop
    const animate = () => {
        requestAnimationFrame(animate);

        // Smooth mouse movement
        targetX += (mouseX - targetX) * dampingFactor;
        targetY += (mouseY - targetY) * dampingFactor;

        particlesMesh.rotation.y += 0.001;
        particlesMesh.rotation.x += 0.001;

        // Smoother mouse follow effect
        particlesMesh.rotation.x += targetY * 0.05;
        particlesMesh.rotation.y += targetX * 0.05;

        renderer.render(scene, camera);
    };

    animate();

    // Handle window resize
    window.addEventListener('resize', updateRendererSize);
}

// Smooth scroll for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Project card hover effect
const projectCards = document.querySelectorAll('.project-card');
projectCards.forEach(card => {
    card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        const centerX = rect.width / 2;
        const centerY = rect.height / 2;

        const rotateX = (y - centerY) / 20;
        const rotateY = (centerX - x) / 20;

        card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateZ(10px)`;
    });

    card.addEventListener('mouseleave', () => {
        card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) translateZ(0)';
    });
});

// Rainbow particle effect
document.addEventListener('DOMContentLoaded', function() {
    const heroSection = document.querySelector('.hero-section');
    let isInHeroSection = false;
    let particles = [];

    function createParticle(x, y) {
        const particle = document.createElement('div');
        particle.className = 'rainbow-particle';
        
        // Random color from rainbow spectrum
        const hue = Math.random() * 360;
        particle.style.backgroundColor = `hsla(${hue}, 100%, 50%, 0.8)`;
        
        // Random size between 4px and 12px
        const size = 4 + Math.random() * 8;
        particle.style.width = `${size}px`;
        particle.style.height = `${size}px`;
        
        // Set initial position
        particle.style.left = `${x}px`;
        particle.style.top = `${y}px`;
        
        // Add to DOM
        document.body.appendChild(particle);
        
        // Random direction and speed
        const angle = Math.random() * Math.PI * 2;
        const velocity = 1 + Math.random() * 3;
        const vx = Math.cos(angle) * velocity;
        const vy = Math.sin(angle) * velocity;
        
        return {
            element: particle,
            x: x,
            y: y,
            vx: vx,
            vy: vy,
            life: 1
        };
    }

    function updateParticles() {
        for (let i = particles.length - 1; i >= 0; i--) {
            const particle = particles[i];
            
            // Update position
            particle.x += particle.vx;
            particle.y += particle.vy;
            particle.vy += 0.1; // Gravity
            particle.life -= 0.02;
            
            // Update DOM element
            particle.element.style.transform = `translate(${particle.x}px, ${particle.y}px)`;
            particle.element.style.opacity = particle.life;
            
            // Remove dead particles
            if (particle.life <= 0) {
                particle.element.remove();
                particles.splice(i, 1);
            }
        }
        requestAnimationFrame(updateParticles);
    }

    function sprayParticles(e) {
        if (!isInHeroSection) return;
        
        // Create multiple particles at once
        for (let i = 0; i < 3; i++) {
            const rect = heroSection.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            particles.push(createParticle(e.clientX, e.clientY));
        }
    }

    heroSection.addEventListener('mouseenter', () => {
        isInHeroSection = true;
    });

    heroSection.addEventListener('mouseleave', () => {
        isInHeroSection = false;
    });

    heroSection.addEventListener('mousemove', sprayParticles);
    updateParticles();
});