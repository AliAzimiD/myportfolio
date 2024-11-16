
export const initNavigation = () => {
  const toggleNav = document.querySelector('.nav-toggle');
  const mobileNav = document.querySelector('.mobile-nav');

  const handleNavToggle = () => {
    mobileNav.classList.toggle('active');
    toggleNav.setAttribute('aria-expanded', 
      toggleNav.getAttribute('aria-expanded') === 'false' ? 'true' : 'false'
    );
  };

  toggleNav?.addEventListener('click', handleNavToggle);
};

export default initNavigation;