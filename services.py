import requests
import json
from django.core.cache import cache
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

# External aptitude questions API URLs (fallback options)
APTITUDE_API_URLS = [
    "https://gist.githubusercontent.com/cmota/f7919cd962a061126effb2d7118bec72/raw",
    "https://raw.githubusercontent.com/ajinkya007/Aptitude-Questions-API/master/questions.json",
    "https://raw.githubusercontent.com/surajr/Aptitude-Questions/main/questions.json"
]

CACHE_KEY = "external_aptitude_questions"
CACHE_TIMEOUT = 24 * 60 * 60  # 24 hours in seconds

def fetch_external_aptitude(force_refresh=False):
    """
    Fetch aptitude questions from external GitHub repositories with caching.
    
    Args:
        force_refresh (bool): If True, bypass cache and fetch fresh data
        
    Returns:
        dict: {
            'success': bool,
            'data': list of questions,
            'source': str,
            'message': str
        }
    """
    # Try to get from cache first (unless force refresh)
    if not force_refresh:
        cached_data = cache.get(CACHE_KEY)
        if cached_data:
            logger.info("Serving aptitude questions from cache")
            return {
                'success': True,
                'data': cached_data,
                'source': 'cache',
                'message': 'Questions loaded from cache'
            }
    
    # Fetch from external sources
    for url in APTITUDE_API_URLS:
        try:
            logger.info(f"Attempting to fetch from: {url}")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            # Parse JSON data
            questions_data = response.json()
            
            # Validate and normalize the data structure
            normalized_questions = normalize_questions(questions_data)
            
            if normalized_questions:
                # Cache the successful response
                cache.set(CACHE_KEY, normalized_questions, CACHE_TIMEOUT)
                logger.info(f"Successfully fetched and cached {len(normalized_questions)} questions from {url}")
                
                return {
                    'success': True,
                    'data': normalized_questions,
                    'source': url,
                    'message': f'Successfully loaded {len(normalized_questions)} questions'
                }
            else:
                logger.warning(f"No valid questions found in {url}")
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch from {url}: {str(e)}")
            continue
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON from {url}: {str(e)}")
            continue
        except Exception as e:
            logger.error(f"Unexpected error fetching from {url}: {str(e)}")
            continue
    
    # If all sources fail, try to return cached data even if expired
    cached_data = cache.get(CACHE_KEY)
    if cached_data:
        logger.warning("All external sources failed, serving expired cache as fallback")
        return {
            'success': True,
            'data': cached_data,
            'source': 'cache_fallback',
            'message': 'External sources unavailable, showing cached questions'
        }
    
    # Last resort: return sample questions
    sample_questions = get_sample_questions()
    logger.warning("All external sources failed and no cache available, using sample questions")
    return {
        'success': True,
        'data': sample_questions,
        'source': 'sample',
        'message': 'Showing sample questions (external sources unavailable)'
    }

def normalize_questions(raw_data):
    """
    Normalize different question formats into a consistent structure.
    
    Expected output format:
    [
        {
            'id': str,
            'question': str,
            'options': list of str,
            'answer': str or int,
            'category': str,
            'difficulty': str
        }
    ]
    """
    normalized = []
    
    try:
        # Handle different data structures
        if isinstance(raw_data, list):
            questions = raw_data
        elif isinstance(raw_data, dict) and 'questions' in raw_data:
            questions = raw_data['questions']
        elif isinstance(raw_data, dict) and 'data' in raw_data:
            questions = raw_data['data']
        else:
            questions = []
        
        for i, q in enumerate(questions[:50]):  # Limit to first 50 questions
            try:
                normalized_q = {
                    'id': str(q.get('id', i + 1)),
                    'question': str(q.get('question', q.get('text', ''))),
                    'options': [],
                    'answer': '',
                    'category': str(q.get('category', q.get('topic', 'General'))),
                    'difficulty': str(q.get('difficulty', 'Medium'))
                }
                
                # Handle options - support multiple formats
                if 'options' in q:
                    if isinstance(q['options'], list):
                        normalized_q['options'] = [str(opt) for opt in q['options']]
                    elif isinstance(q['options'], dict):
                        normalized_q['options'] = [str(v) for v in q['options'].values()]
                elif 'A' in q and 'B' in q and 'C' in q and 'D' in q:
                    # Handle format with A, B, C, D keys
                    normalized_q['options'] = [
                        str(q.get('A', '')),
                        str(q.get('B', '')),
                        str(q.get('C', '')),
                        str(q.get('D', ''))
                    ]
                elif 'choices' in q:
                    if isinstance(q['choices'], list):
                        normalized_q['options'] = [str(opt) for opt in q['choices']]
                    elif isinstance(q['choices'], dict):
                        normalized_q['options'] = [str(v) for v in q['choices'].values()]
                
                # Handle answer
                if 'answer' in q:
                    answer = q['answer']
                    if isinstance(answer, str) and answer.isdigit():
                        normalized_q['answer'] = int(answer)
                    else:
                        normalized_q['answer'] = str(answer)
                elif 'correct' in q:
                    normalized_q['answer'] = str(q['correct'])
                elif 'correct_answer' in q:
                    normalized_q['answer'] = str(q['correct_answer'])
                
                # Only include questions with valid text and options
                if normalized_q['question'] and len(normalized_q['question']) > 10:
                    normalized.append(normalized_q)
                    
            except Exception as e:
                logger.warning(f"Error normalizing question {i}: {str(e)}")
                continue
                
    except Exception as e:
        logger.error(f"Error normalizing questions data: {str(e)}")
        return []
    
    return normalized

def get_sample_questions():
    """Return sample aptitude questions as fallback"""
    return [
        {
            'id': '1',
            'question': 'A man rows a boat at a speed of 15 mph in still water. Find the speed of the river if it takes her 4 hours 30 minutes to row a boat to a place 30 miles away and return.',
            'options': ['5 mph', '10 mph', '12 mph', '20 mph'],
            'answer': '5 mph',
            'category': 'Speed, Time & Distance',
            'difficulty': 'Medium'
        },
        {
            'id': '2',
            'question': 'Working 5 hours a day, A can Complete a work in 8 days and working 6 hours a day, B can complete the same work in 10 days. Working 8 hours a day, they can jointly complete the work in how many days?',
            'options': ['3 days', '4 days', '4.5 days', '5.4 days'],
            'answer': '3 days',
            'category': 'Time & Work',
            'difficulty': 'Medium'
        },
        {
            'id': '3',
            'question': 'A mixture of 40 liters of milk and water contains 10% water. How much water should be added to this so that water may be 20% in the new mixture?',
            'options': ['6.5 liters', '5 liters', '4 liters', '7.5 liters'],
            'answer': '5 liters',
            'category': 'Mixture & Alligation',
            'difficulty': 'Easy'
        },
        {
            'id': '4',
            'question': 'Four different electronic devices make a beep after every 30 minutes, 1 hour, 3/2 hour and 1 hour 45 minutes respectively. All the devices beeped together at 12 noon. They will again beep together at:',
            'options': ['12 midnight', '3 a.m', '6 a.m', '9 a.m'],
            'answer': '9 a.m',
            'category': 'LCM & HCF',
            'difficulty': 'Hard'
        },
        {
            'id': '5',
            'question': 'If January 1, 1996, was Monday, what day of the week was January 1, 1997?',
            'options': ['Monday', 'Tuesday', 'Wednesday', 'Thursday'],
            'answer': 'Wednesday',
            'category': 'Calendar',
            'difficulty': 'Easy'
        }
    ]

def clear_aptitude_cache():
    """Clear the aptitude questions cache."""
    cache.delete(CACHE_KEY)
    logger.info("Aptitude questions cache cleared")
