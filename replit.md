# Overview

This repository contains a Flask-based documentation website for Marzneshin, a modern multi-core proxy management tool. The application serves as a comprehensive documentation portal with a clean, modern interface featuring a homepage with hero sections, structured documentation pages, and search functionality. The site is built to showcase Marzneshin's features including multi-core optimization, user management, real-time monitoring, and support for various proxy protocols like VLESS, VMess, Trojan, and Hysteria.

# User Preferences

Preferred communication style: Simple, everyday language.

# Recent Changes

## Persian Language Support Added (August 3, 2025)
- Added full bilingual support for English (default) and Persian (فارسی)
- Implemented comprehensive translation system with 50+ translated strings
- Added RTL (right-to-left) layout support for Persian language
- Created language switching functionality in navigation
- Applied Persian font (Vazir) for better readability
- Updated all templates to use translation functions
- Added RTL-specific CSS styles for proper layout in Persian mode

# System Architecture

## Frontend Architecture
The application uses a server-side rendered approach with Flask templates and Bootstrap 5 for responsive design. The template structure follows a base template pattern with specialized templates for the homepage (`index.html`), documentation listing (`docs.html`), and individual documentation pages (`doc_page.html`). The frontend includes modern features like a fixed navigation bar with backdrop blur effects, hero sections with gradient text, feature cards, and a responsive sidebar navigation for documentation.

## Backend Architecture
The Flask application follows a simple MVC pattern with clear separation of concerns. The main application is initialized in `app.py` with configuration for sessions, proxy middleware, and logging. Route handling is separated into `routes.py` which manages homepage rendering, documentation structure, and markdown file processing. The application uses Python's markdown library with extensions for code highlighting, fenced code blocks, tables, and table of contents generation.

## Content Management
Documentation content is stored as Markdown files in a structured directory (`content/docs/`) and dynamically converted to HTML at request time. The documentation structure is hardcoded in the `get_doc_structure()` function, organizing content into logical sections like "Getting Started" and "Configuration". This approach allows for easy content updates without code changes while maintaining consistent navigation and breadcrumbs.

## Static Asset Management
The application uses a traditional Flask static file structure with custom CSS in `static/css/style.css` and JavaScript in `static/js/main.js`. The CSS implements a modern design system with CSS custom properties for theming, responsive layouts, and smooth animations. The JavaScript handles interactive features like search functionality, mobile menu behavior, smooth scrolling, and code highlighting.

# External Dependencies

## Core Framework
- **Flask**: Web framework for handling HTTP requests and template rendering
- **Werkzeug**: WSGI utilities including ProxyFix middleware for handling proxy headers

## Content Processing
- **Python Markdown**: Converts Markdown files to HTML with extensions for enhanced formatting
- **CodeHilite Extension**: Provides syntax highlighting for code blocks
- **Fenced Code Extension**: Enables GitHub-flavored markdown code blocks
- **Tables Extension**: Adds support for markdown tables
- **TOC Extension**: Generates table of contents from headers

## Database
- **Flask-SQLAlchemy**: ORM integration for Flask applications
- **psycopg2-binary**: PostgreSQL adapter for Python

## Server
- **Gunicorn**: Production WSGI server for deployment

## Frontend Libraries
- **Bootstrap 5**: CSS framework for responsive design and UI components
- **Font Awesome 6**: Icon library for consistent iconography throughout the interface

## Enhanced Features
- **Interactive Code Copy**: JavaScript-based copy functionality with visual feedback
- **Mobile Gesture Support**: Touch-based navigation with swipe gestures
- **Animated Theme Toggle**: Smooth transitions between light/dark themes
- **Performance Metrics**: Load time tracking and optimization indicators

## Requirements File
The complete requirements.txt content is documented in REQUIREMENTS.md since direct file creation is restricted. All dependencies are managed through the Replit package manager.

## Environment Configuration
The application reads configuration from environment variables, particularly for session secrets and deployment settings, making it suitable for various deployment environments including development and production.