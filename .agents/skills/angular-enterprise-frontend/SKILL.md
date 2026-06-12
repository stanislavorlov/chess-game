---
name: angular-enterprise-frontend
description: 'Building, modifying, or debugging Angular components, services, RxJS reactive streams, or TypeScript architecture.'
---

# Goal
Generate highly performant, type-safe, modular Angular frontend code utilizing modern standalone component architectures and reactive data streaming paradigms.

# Instructions
1. **Strict Type Safety:** Avoid the use of `any`. Explicitly define TypeScript interfaces or types for all API payloads, component states, and service returns.
2. **Memory Leak Prevention:** For any imperative `.subscribe()` call within components, ensure proper cleanup. Prefer utilizing the `async` pipe in templates, or use RxJS operators like `takeUntilDestroyed()` within the injection context.
3. **Optimized Change Detection:** Default to using `changeDetection: ChangeDetectionStrategy.OnPush` for all custom components to prevent unnecessary lifecycle digest cycles.
4. **State Management Flow:** Keep components thin. Offload business logic, HTTP calls, and client-side data transformations into dedicated, injectable `@Injectable({ providedIn: 'root' })` services.

# Constraints
- Do not directly manipulate the DOM using native `document` queries; use Angular's `ElementRef` or `Renderer2` when structural directives cannot solve the problem.
- Never hardcode environment-specific variables or base URLs directly inside components or services; leverage centralized application configuration tokens or environment files.