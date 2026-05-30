#!/usr/bin/env python3
"""Script to inject the CSS styles for the SPA multipage navigation into the HTML."""

import re

def main():
    html_path = "/home/ubuntu/calculadora_biodigestor/calculadora_biodigestor.html"
    
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # CSS to inject for the SPA pages and navbar
    spa_css = """
        /* --- ESTILOS DE LA NAVEGACIÓN MULTIPÁGINA (SPA) --- */
        .spa-navbar {
            width: 100%;
            background-color: var(--primary-green);
            border-bottom: 4px solid var(--accent-terracota);
            position: sticky;
            top: 0;
            z-index: 1000;
            box-shadow: var(--shadow-soft);
        }

        .navbar-container {
            max-width: 1100px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 16px;
        }

        .navbar-brand {
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .brand-logo {
            font-size: 1.5rem;
        }

        .brand-title {
            font-family: 'Playfair Display', Georgia, serif;
            color: #FAF6EE;
            font-weight: 700;
            font-size: 1.15rem;
        }

        .navbar-links {
            display: flex;
            gap: 8px;
        }

        .nav-btn {
            background: none;
            border: none;
            color: #E6DCD2;
            padding: 8px 14px;
            font-size: 0.9rem;
            font-weight: 700;
            cursor: pointer;
            border-radius: 6px;
            transition: all 0.2s var(--ease-out);
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .nav-btn:hover {
            color: #FAF6EE;
            background-color: rgba(255, 255, 255, 0.08);
        }

        .nav-btn.active {
            color: #FAF6EE;
            background-color: var(--accent-terracota);
            box-shadow: 0 2px 6px rgba(162, 72, 35, 0.3);
        }

        .spa-page {
            display: none;
            width: 100%;
            animation: fadeIn 0.4s var(--ease-out);
        }

        .spa-page.active {
            display: block;
        }

        @media (max-width: 768px) {
            .navbar-container {
                flex-direction: column;
                gap: 10px;
                padding: 12px;
            }
            .navbar-links {
                width: 100%;
                overflow-x: auto;
                justify-content: flex-start;
                padding-bottom: 4px;
                -webkit-overflow-scrolling: touch;
            }
            .nav-btn {
                flex-shrink: 0;
                font-size: 0.8rem;
                padding: 6px 10px;
            }
        }
    """
    
    # We will inject this CSS right before the closing </style> tag
    if "</style>" in content:
        # Check if it was already injected
        if ".spa-navbar" not in content:
            new_content = content.replace("</style>", spa_css + "\n    </style>")
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print("CSS inyectado exitosamente.")
        else:
            print("El CSS ya estaba inyectado.")
    else:
        print("Error: No se encontró la etiqueta </style>.")

if __name__ == "__main__":
    main()
