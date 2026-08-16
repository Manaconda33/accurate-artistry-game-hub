import './style.css';
import { mountAppShell } from './app/mountAppShell';

const root = document.querySelector<HTMLElement>('#app');

if (root === null) {
  throw new Error('App root #app was not found.');
}

mountAppShell(root);
