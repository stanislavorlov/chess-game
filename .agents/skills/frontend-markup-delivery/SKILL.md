---
name: frontend-markup-delivery
description: "Rules and best practices for creating semantic, responsive, accessible, and structured HTML5/CSS markup for clean frontend delivery."
---

# Goal
Ensure that all frontend markup (HTML5 templates) and stylesheets (CSS/SCSS) adhere to web accessibility standards, clean semantic structure, and optimized responsive layout principles.

# Instructions
1. **Semantic Structure**: Always write semantic HTML5 elements (`<article>`, `<section>`, `<nav>`, `<header>`, `<footer>`, `<main>`) instead of nested generic `<div>` blocks. Use only a single `<h1>` per view, structured in descending hierarchical order (`<h2>`, `<h3>`).
2. **Accessibility (A11y)**:
   - Ensure all interactive elements (like icon buttons) have descriptive `aria-label` attributes.
   - Maintain visible `:focus` outline rings on all focusable elements for keyboard navigation.
   - Match logical keyboard tab order explicitly to the visual layout flow.
   - Maintain minimum color contrast ratio of 4.5:1 for normal body text.
3. **Responsive Spacing & Layout**:
   - Utilize CSS Grid or Flexbox for layout alignments; avoid absolute positioning for dynamic structures.
   - Ensure touch targets (buttons, links) are at least 44x44px to accommodate mobile devices.
   - Limit text reading line length to 65-75 characters to enhance readability.
4. **Performance Safety**:
   - Avoid structural layouts that cause Content Layout Shifts (CLS) during asynchronous data loading. Reserve container boundaries beforehand.
   - Keep animation execution limited to GPU-accelerated operations (like `transform` and `opacity`) instead of mutating layout boundaries (like `width` or `height`).

# Constraints
- Do not use structural HTML emojis as decorative icons; always utilize clean SVG vector assets.
- Never write hardcoded styling values directly on inline HTML attributes; keep layout declarations clean inside component classes or modular stylesheets.
