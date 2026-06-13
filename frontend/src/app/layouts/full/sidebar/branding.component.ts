import { Component } from '@angular/core';
import { CoreService } from 'src/app/services/core.service';

@Component({
  selector: 'app-branding',
  imports: [],
  template: `
    <a href="/" class="logodark" style="display: flex; align-items: center; gap: 8px; text-decoration: none;">
      <img
        src="./assets/images/pieces/wk.png"
        class="align-middle m-2"
        alt="logo"
        style="width: 38px; height: 38px;"
      />
      <span style="font-size: 1.3rem; font-weight: 800; letter-spacing: 0.8px; color: #2c3e50; font-family: 'Outfit', sans-serif;">
        CHESS
      </span>
    </a>
  `,
})
export class BrandingComponent {
  options = this.settings.getOptions();
  constructor(private settings: CoreService) { }
}
