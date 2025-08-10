# all my route handlers and helper functions
# this is where the magic happens tbh
import os
import markdown
from flask import render_template, abort, request, jsonify, redirect, url_for, session
from app import my_awesome_app as app  # renamed for consistency
from translations import get_current_language, set_language, get_doc_text

def load_markdown_content(file_path):
    """
    loads a markdown file and converts it to html
    this function has saved me so many times when dealing with docs
    """
    try:
        # open the file and read all content - basic file operations
        with open(file_path, 'r', encoding='utf-8') as markdown_file:
            raw_content = markdown_file.read()
            
            # setup markdown parser with all the cool extensions
            # took me forever to figure out the right config for syntax highlighting
            markdown_parser = markdown.Markdown(extensions=[
                'codehilite',      # syntax highlighting - makes code look pretty
                'fenced_code',     # github style code blocks with ```
                'tables',          # because who doesn't love tables
                'toc',            # table of contents generation
                'nl2br'           # converts newlines to <br> tags
            ], extension_configs={
                'codehilite': {
                    'css_class': 'highlight',     # css class for styling
                    'use_pygments': True,         # use pygments for highlighting
                    'guess_lang': False           # don't guess language, be explicit
                }
            })
            
            # convert markdown to html - this is where the magic happens
            html_output = markdown_parser.convert(raw_content)
            return html_output
            
    except FileNotFoundError:
        # file doesn't exist, return None so we can handle it properly
        print(f"yo, couldn't find the file: {file_path}")  # debug info
        return None
    except Exception as e:
        # catch any other weird errors that might pop up
        print(f"something went wrong loading markdown: {e}")
        return None

def get_docs_navigation():
    """
    returns the structure for the documentation sidebar
    organized this way to make it super easy to add new docs later
    just add a new entry here and create the markdown file - boom!
    """
    current_lang = get_current_language()
    
    # this dictionary defines our entire docs structure
    # keeping it simple but organized - learned this from reading other projects
    docs_menu = {
        get_doc_text('Getting Started', current_lang): [
            {'title': get_doc_text('About', current_lang), 'slug': 'about'},                      # what is marzneshin
            {'title': get_doc_text('Installation', current_lang), 'slug': 'installation'},         # how to install it
            {'title': get_doc_text('Getting Started', current_lang), 'slug': 'getting-started'},   # first steps tutorial  
            {'title': get_doc_text('Overview', current_lang), 'slug': 'overview'},                # general overview
        ],
        get_doc_text('Configuration', current_lang): [
            {'title': get_doc_text('Configuration', current_lang), 'slug': 'configuration'},       # config options
            {'title': get_doc_text('API Reference', current_lang), 'slug': 'api-reference'},      # api docs
        ],
        get_doc_text('Help', current_lang): [
            {'title': get_doc_text('Troubleshooting', current_lang), 'slug': 'troubleshooting'},  # when things break
        ]
    }
    
    return docs_menu

@app.route('/set-language/<lang_code>')
def set_language_route(lang_code):
    """
    language switching route - allows users to change between English and Persian
    redirects back to the previous page after setting the language
    """
    if lang_code in ['en', 'fa']:
        set_language(lang_code)
        print(f"language changed to: {lang_code}")
    
    # redirect back to the referring page or homepage if no referrer
    referrer = request.referrer or url_for('homepage')
    return redirect(referrer)

@app.route('/')
def homepage():
    """
    the main landing page - this is what people see first
    kept it simple with a nice hero section and feature cards
    """
    return render_template('index.html')

@app.route('/docs')
def docs_homepage():
    """
    documentation landing page - shows all available docs
    basically a table of contents for everything
    """
    navigation_structure = get_docs_navigation()
    return render_template('docs.html', doc_structure=navigation_structure)

@app.route('/docs/<page_slug>')
def show_documentation_page(page_slug):
    """
    displays individual documentation pages
    handles loading markdown files and rendering them with navigation
    also figures out prev/next page links automatically
    """
    # get our navigation structure
    navigation_structure = get_docs_navigation()
    
    # build the file path for the markdown file
    markdown_file_path = os.path.join('content', 'docs', f'{page_slug}.md')
    
    # try to load the markdown content
    page_content = load_markdown_content(markdown_file_path)
    
    # if file doesn't exist, show 404 - user probably typed wrong url
    if page_content is None:
        print(f"404: couldn't find page for slug '{page_slug}'")
        abort(404)
    
    # figure out the page title and navigation stuff
    current_page_title = page_slug.replace('-', ' ').title()  # fallback title
    previous_page = None
    next_page = None
    
    # create a flat list of all pages in order for navigation
    all_documentation_pages = []
    
    # flatten the nested structure into a simple list
    for section_name, section_pages in navigation_structure.items():
        for page_info in section_pages:
            all_documentation_pages.append(page_info)
            # if this is our current page, grab the proper title
            if page_info['slug'] == page_slug:
                current_page_title = page_info['title']
    
    # find the previous and next pages for navigation
    # this creates those handy "previous" and "next" buttons
    for index, page_info in enumerate(all_documentation_pages):
        if page_info['slug'] == page_slug:
            # get previous page if we're not at the beginning
            if index > 0:
                previous_page = all_documentation_pages[index - 1]
            # get next page if we're not at the end
            if index < len(all_documentation_pages) - 1:
                next_page = all_documentation_pages[index + 1]
            break
    
    # render the template with all the data
    return render_template('doc_page.html', 
                         content=page_content, 
                         page_title=current_page_title,
                         doc_structure=navigation_structure,
                         current_slug=page_slug,
                         prev_page=previous_page,
                         next_page=next_page)

@app.route('/search')
def search_documentation():
    """
    search functionality for the documentation
    searches both page titles and content - pretty basic but it works
    returns json for the frontend javascript to handle
    """
    # get the search query from url parameters
    search_query = request.args.get('q', '').strip().lower()
    
    # if no query provided, return empty results
    if not search_query:
        return jsonify([])
    
    search_results = []
    navigation_structure = get_docs_navigation()
    
    print(f"searching for: '{search_query}'")  # debug info
    
    # search through all our documentation files
    for section_name, section_pages in navigation_structure.items():
        for page_info in section_pages:
            # build file path for this page
            page_file_path = os.path.join('content', 'docs', f'{page_info["slug"]}.md')
            
            try:
                # open and read the markdown file
                with open(page_file_path, 'r', encoding='utf-8') as markdown_file:
                    file_content = markdown_file.read().lower()
                    
                    # check if search query appears in content or title
                    title_match = search_query in page_info['title'].lower()
                    content_match = search_query in file_content
                    
                    if title_match or content_match:
                        # found a match! add it to results
                        search_results.append({
                            'title': page_info['title'],
                            'slug': page_info['slug'],
                            'section': section_name
                        })
                        print(f"found match in: {page_info['title']}")
                        
            except FileNotFoundError:
                print(f"warning: couldn't find file {page_file_path}")
                continue  # skip missing files
            except Exception as e:
                print(f"error reading {page_file_path}: {e}")
                continue
    
    # limit results to 10 max to keep things fast
    # nobody wants to scroll through 100 search results anyway
    limited_results = search_results[:10]
    
    print(f"returning {len(limited_results)} search results")
    return jsonify(limited_results)

@app.errorhandler(404)
def page_not_found_handler(error):
    """
    handles 404 errors - when someone tries to access a page that doesn't exist
    happens a lot when people mistype urls or click broken links
    """
    from translations import get_text
    
    error_message = f'''
    <div class="text-center py-5">
        <h1 class="display-4">{get_text('error_404_title')}</h1>
        <p class="lead">{get_text('error_404_desc')}</p>
        <p>{get_text('error_404_maybe')}</p>
        <a href="/" class="btn btn-primary">{get_text('error_go_home')}</a>
    </div>
    '''
    print(f"404 error: someone tried to access {request.url}")
    return render_template('base.html', content=error_message), 404

@app.errorhandler(500)
def server_error_handler(error):
    """
    handles 500 errors - when something breaks on our end
    this is usually my fault lol - bad code or server issues
    """
    from translations import get_text
    
    # log the error so i can debug it later
    app.logger.error(f'Server crashed! Error: {error}')
    print(f"500 error occurred: {error}")  # also print to console
    
    error_message = f'''
    <div class="text-center py-5">
        <h1 class="display-4">{get_text('error_500_title')}</h1>
        <p class="lead">{get_text('error_500_desc')}</p>
        <p>{get_text('error_500_not_fault')}</p>
        <a href="/" class="btn btn-primary">{get_text('error_try_again')}</a>
    </div>
    '''
    return render_template('base.html', content=error_message), 500
