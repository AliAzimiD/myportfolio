
export const initAnimations = () => {
  const animatedElements = document.querySelectorAll('[data-animate]');

  const observerCallback = (entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('animated');
      }
    });
  };

  const observer = new IntersectionObserver(observerCallback, {
    threshold: 0.1
  });

  animatedElements.forEach(el => observer.observe(el));
};

export default initAnimations;