---
name: ui-ux-design-intelligence
description: "Comprehensive design system framework for choosing layout aesthetics, color harmony, user interface feedback states, and premium micro-interactions."
---

# Goal
Formulate high-fidelity, visually distinctive, and memorable user interfaces that express a cohesive aesthetic theme and provide real-time interactive feedback.

# Instructions
1. **Cohesive Design Direction**: Before coding, select a unified theme direction (e.g. *Editorial Minimalist*, *Retro-Futuristic*, *Modern Utilitarian*) and enforce it cleanly across all views.
2. **Color Palette Harmony**: Establish a strict HSL or CSS variables-based color system. Avoid default raw primary colors (e.g. raw blue, red, green) and use sophisticated muted tones, subtle gradients, and dark-mode compatible variables.
3. **Interactive Visual Feedback**:
   - Provide micro-interactions (subtle scale transforms, opacity shifts) on hover states.
   - Limit micro-interaction duration timings to 150-300ms for swift, premium-feeling transitions.
   - Always disable buttons and show loading states (skeletons or spinners) during asynchronous API calls to prevent repeat clicks.
4. **Data Visualization Principles**: When displaying charts or stats:
   - Ensure color palettes match accessible contrast patterns.
   - Use correct data mappings (e.g. bar charts for categories, line charts for trends, metric grids for summary numbers).

# Constraints
- Avoid mixed visual directions (do not combine more than two style paradigms).
- Never allow elements to abruptly "jump" due to missing placeholder dimensions during dynamic state modifications.
