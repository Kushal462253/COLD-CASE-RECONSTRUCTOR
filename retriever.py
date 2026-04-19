import wikipedia

def get_relevant_facts(case_input):
    try:
        # Search first to find the best matching page
        search_results = wikipedia.search(case_input, results=3)
        
        if not search_results:
            return "No relevant facts found for this case."
        
        # Try the top search result first
        for page_title in search_results:
            try:
                page = wikipedia.page(page_title, auto_suggest=False)
                summary = wikipedia.summary(page_title, sentences=10, auto_suggest=False)
                return summary
            except wikipedia.exceptions.DisambiguationError as e:
                try:
                    summary = wikipedia.summary(e.options[0], sentences=10, auto_suggest=False)
                    return summary
                except:
                    continue
            except wikipedia.exceptions.PageError:
                continue
            except Exception:
                continue
        
        return "No relevant facts found for this case."
    
    except Exception as e:
        return f"Retrieval error: {str(e)}"