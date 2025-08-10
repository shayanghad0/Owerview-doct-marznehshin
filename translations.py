# Language translations for the Marzneshin documentation website
# Supports English (default) and Persian (فارسی)

import os
from flask import session, request

def get_current_language():
    """Get the current language from session, URL, or default to English"""
    # First check if language is specified in URL
    lang = request.args.get('lang')
    if lang and lang in ['en', 'fa']:
        session['language'] = lang
        return lang
    
    # Then check session
    if 'language' in session and session['language'] in ['en', 'fa']:
        return session['language']
    
    # Default to English
    return 'en'

def set_language(lang_code):
    """Set the current language in session"""
    if lang_code in ['en', 'fa']:
        session['language'] = lang_code

def get_text(key, lang=None):
    """Get translated text for the given key"""
    if lang is None:
        lang = get_current_language()
    
    return TRANSLATIONS.get(lang, TRANSLATIONS['en']).get(key, key)

# Translation dictionary
TRANSLATIONS = {
    'en': {
        # Navigation
        'nav_home': 'Home',
        'nav_docs': 'Documentation',
        'nav_github': 'GitHub',
        'language_switch': 'فارسی',
        
        # Hero section
        'hero_badge': 'Free & Open-source',
        'hero_title': 'Marzneshin: Modern',
        'hero_title_gradient': 'Multi-Core Proxy Manager',
        'hero_subtitle': 'An efficient, secure and user-friendly proxy management tool',
        'hero_get_started': 'Get Started',
        'hero_view_github': 'View on GitHub',
        
        # Features section
        'features_title': 'Why Choose Marzneshin?',
        'features_subtitle': 'Built for performance, security, and ease of use with modern technologies',
        
        'feature1_title': 'Fast & Feature-Rich',
        'feature1_desc': 'Simple interface with powerful features. Built for speed and efficiency with modern web technologies.',
        
        'feature2_title': 'Multi-Core Optimized',
        'feature2_desc': 'Maximize Xray and Hysteria performance with intelligent multi-core processing and resource management.',
        
        'feature3_title': 'User Management',
        'feature3_desc': 'Comprehensive user management system with detailed statistics and traffic monitoring capabilities.',
        
        'feature4_title': 'Multiple Protocols',
        'feature4_desc': 'Support for VLESS, VMess, Trojan, and Hysteria protocols with flexible configuration options.',
        
        'feature5_title': 'Real-time Monitoring',
        'feature5_desc': 'Live traffic monitoring with detailed analytics and performance metrics for optimal management.',
        
        'feature6_title': 'Secure & Reliable',
        'feature6_desc': 'Enterprise-grade security with reliable connections and automatic failover mechanisms.',
        
        # Footer
        'footer_desc': 'Modern Multi-Core Proxy Manager',
        'footer_desc2': 'Free & Open-source proxy management solution',
        'footer_docs': 'Documentation',
        'footer_get_started': 'Get Started',
        'footer_overview': 'Overview',
        'footer_installation': 'Installation',
        'footer_community': 'Community',
        'footer_copyright': '© 2024 Marzneshin. Open source under MIT License.',
        
        # Documentation
        'docs_title': 'Documentation',
        'docs_subtitle': 'Everything you need to know about Marzneshin',
        'docs_search_placeholder': 'Search documentation...',
        'docs_prev': 'Previous',
        'docs_next': 'Next',
        
        # Error pages
        'error_404_title': 'Oops! Page Not Found',
        'error_404_desc': "The page you're looking for doesn't exist.",
        'error_404_maybe': 'Maybe you typed the wrong URL? Or clicked on a broken link?',
        'error_go_home': 'Go Back Home',
        'error_500_title': 'Something Went Wrong',
        'error_500_desc': 'Our server encountered an error.',
        'error_500_not_fault': "Don't worry, it's not your fault! We're probably fixing it right now.",
        'error_try_again': 'Try Again',
    },
    
    'fa': {
        # Navigation
        'nav_home': 'خانه',
        'nav_docs': 'مستندات',
        'nav_github': 'گیت‌هاب',
        'language_switch': 'English',
        
        # Hero section
        'hero_badge': 'رایگان و متن‌باز',
        'hero_title': 'مرزنشین: مدیریت پروکسی',
        'hero_title_gradient': 'مدرن و چندهسته‌ای',
        'hero_subtitle': 'ابزار مدیریت پروکسی کارآمد، امن و کاربرپسند',
        'hero_get_started': 'شروع کنید',
        'hero_view_github': 'مشاهده در گیت‌هاب',
        
        # Features section
        'features_title': 'چرا مرزنشین را انتخاب کنید؟',
        'features_subtitle': 'ساخته شده برای عملکرد، امنیت و سهولت استفاده با تکنولوژی‌های مدرن',
        
        'feature1_title': 'سریع و پرقابلیت',
        'feature1_desc': 'رابط کاربری ساده با امکانات قدرتمند. ساخته شده برای سرعت و کارایی با تکنولوژی‌های وب مدرن.',
        
        'feature2_title': 'بهینه‌سازی چندهسته‌ای',
        'feature2_desc': 'حداکثر کارایی Xray و Hysteria با پردازش چندهسته‌ای هوشمند و مدیریت منابع.',
        
        'feature3_title': 'مدیریت کاربران',
        'feature3_desc': 'سیستم جامع مدیریت کاربران با آمار تفصیلی و قابلیت‌های نظارت بر ترافیک.',
        
        'feature4_title': 'پروتکل‌های متعدد',
        'feature4_desc': 'پشتیبانی از پروتکل‌های VLESS، VMess، Trojan و Hysteria با گزینه‌های پیکربندی انعطاف‌پذیر.',
        
        'feature5_title': 'نظارت بلادرنگ',
        'feature5_desc': 'نظارت زنده بر ترافیک با تجزیه و تحلیل تفصیلی و معیارهای عملکرد برای مدیریت بهینه.',
        
        'feature6_title': 'امن و قابل اطمینان',
        'feature6_desc': 'امنیت درجه سازمانی با اتصالات قابل اطمینان و مکانیزم‌های failover خودکار.',
        
        # Footer
        'footer_desc': 'مدیر پروکسی مدرن چندهسته‌ای',
        'footer_desc2': 'راه‌حل مدیریت پروکسی رایگان و متن‌باز',
        'footer_docs': 'مستندات',
        'footer_get_started': 'شروع کنید',
        'footer_overview': 'نمای کلی',
        'footer_installation': 'نصب',
        'footer_community': 'انجمن',
        'footer_copyright': '© ۲۰۲۴ مرزنشین. متن‌باز تحت مجوز MIT.',
        
        # Documentation
        'docs_title': 'مستندات',
        'docs_subtitle': 'همه چیزی که نیاز دارید درباره مرزنشین بدانید',
        'docs_search_placeholder': 'جستجو در مستندات...',
        'docs_prev': 'قبلی',
        'docs_next': 'بعدی',
        
        # Error pages
        'error_404_title': 'اوه! صفحه پیدا نشد',
        'error_404_desc': 'صفحه‌ای که دنبالش هستید وجود ندارد.',
        'error_404_maybe': 'شاید آدرس اشتباه تایپ کرده‌اید؟ یا روی لینک شکسته کلیک کرده‌اید؟',
        'error_go_home': 'بازگشت به خانه',
        'error_500_title': 'مشکلی پیش آمد',
        'error_500_desc': 'سرور ما با خطا مواجه شد.',
        'error_500_not_fault': 'نگران نباشید، تقصیر شما نیست! احتمالاً الان داریم درستش می‌کنیم.',
        'error_try_again': 'دوباره تلاش کنید',
    }
}

# Documentation navigation structure translations
DOC_TRANSLATIONS = {
    'en': {
        'Getting Started': 'Getting Started',
        'Configuration': 'Configuration', 
        'Help': 'Help',
        'About': 'About',
        'Installation': 'Installation',
        'Getting Started': 'Getting Started',
        'Overview': 'Overview',
        'Configuration': 'Configuration',
        'API Reference': 'API Reference',
        'Troubleshooting': 'Troubleshooting',
    },
    'fa': {
        'Getting Started': 'شروع کار',
        'Configuration': 'پیکربندی',
        'Help': 'راهنما',
        'About': 'درباره',
        'Installation': 'نصب',
        'Getting Started': 'شروع کار',
        'Overview': 'نمای کلی',
        'Configuration': 'پیکربندی',
        'API Reference': 'مرجع API',
        'Troubleshooting': 'عیب‌یابی',
    }
}

def get_doc_text(key, lang=None):
    """Get translated documentation text"""
    if lang is None:
        lang = get_current_language()
    
    return DOC_TRANSLATIONS.get(lang, DOC_TRANSLATIONS['en']).get(key, key)