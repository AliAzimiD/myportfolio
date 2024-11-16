import './modules/navigation';
import './modules/animations';
import './modules/forms';
import './modules/projects';
import './modules/financial';
import './modules/assets';

// Initialize main application
document.addEventListener('DOMContentLoaded', () => {
  initNavigation();
  initAnimations();
  initForms();
  initProjects();
  initFinancial();
  initAssets();
});
