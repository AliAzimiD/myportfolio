
// Import modules
import { AssetManager } from './modules/asset-manager.js';
import { TransactionManager } from './modules/transaction-manager.js';

// Initialize modules when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new AssetManager();
    new TransactionManager();
});