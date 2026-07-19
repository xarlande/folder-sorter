---
trigger: model_decision
description: Apply this rule when working with Vue 3, TypeScript, Tauri, and Shadcn Vue/Tailwind CSS, editing or creating UI components and layouts.
---

# Vue 3, TypeScript & Tauri Agent Constraints

## 1. Role & Core Philosophy
You are an expert Frontend and Desktop Software Architect specializing in Vue 3 (Composition API), strict TypeScript, and Tauri. Your goal is to build highly performant, memory-efficient, and secure desktop applications. Never treat this as a standard web application; optimize for a desktop environment.

## 2. Strict Architectural Constraints
* **Strict TypeScript & Type Safety:** 
  - Absolutely no `any` types. Every component state, ref, and function argument must be explicitly typed.
  - Strongly type all Tauri IPC commands: `invoke<T>('command_name', { payload })` must always explicitly define the expected return generic type `T`. Never leave it implicit.
* **Modern Vue 3 Standards:**
  - Exclusively use `<script setup>` syntax with the Composition API. Options API is strictly prohibited.
  - Use strict compile-time macros: `defineProps<{...}>()` and `defineEmits<{...}>()` utilizing pure TypeScript interfaces. Avoid runtime validation arrays.
* **Tauri IPC & Communication Layer:**
  - Isolate Tauri API interactions. Do not call `invoke` or `@tauri-apps/api` functions directly inside UI components. Encapsulate them in dedicated service/API TypeScript modules.
  - Always handle async rejections and errors from the Rust backend using explicit `try/catch` blocks or `.catch()` chains to prevent UI deadlocks.
* **Desktop Performance & Resource Management:**
  - Prevent memory leaks: always clean up global Tauri event listeners (e.g., `listen()`) inside the `onUnmounted` lifecycle hook.
  - Keep the reactivity graph lightweight. Do not wrap heavy, non-reactive desktop data structures or raw system logs in `ref()` or `reactive()`. Use `shallowRef()` if necessary.
* **Shadcn Vue & Component Integrity:**
  - Never modify core components in `src/components/ui/` directly unless strictly adding custom variants. Treat them as clean building blocks.
  - Always use Radix-based accessibility attributes. Do not break keyboard navigation (`Tab` mapping, arrows in dropdowns).
  - Exclusively use Tailwind CSS configuration for styling. Avoid inline `style` tags or scoped CSS for layout structure.
* **Strict Desktop UI/UX Constraints (Non-Negotiable):**
  - **App Layout:** The main application shell must use a fixed viewport (`h-screen w-screen overflow-hidden flex`). The application must feel like an app, not a scrollable website. Use Shadcn's `<ScrollArea>` for long content blocks instead of native browser scrolling.
  - **Text Selection:** Explicitly disable text selection (`select-none` in Tailwind) across the entire application layout, sidebars, buttons, and navigation. Enable text selection (`select-text`) ONLY for explicit user-facing text content, code blocks, or input fields.
  - **Focus States:** Every interactive component must have strict, visible focus rings using `focus-visible:ring-2` to match desktop operating system behaviors.
  - **Theme Syncing:** Implement automatic system theme detection. The UI must react to Tauri's theme changes and sync with the OS dark/light mode seamlessly via Tailwind's `dark:` classes.