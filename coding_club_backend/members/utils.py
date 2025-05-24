import openai
from django.conf import settings

def generate_meeting_summary(title, description, notes):
    client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
    
    prompt = f"""
    Meeting Title: {title}
    Description: {description}
    Notes: {notes}
    
    Please provide a SINGLE SENTENCE summary (25-30 words maximum) of this coding club meeting.
    Focus only on the main topic or goal of the meeting. Keep it extremely brief and student-friendly.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes coding club meetings in a single sentence."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=60,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except openai.RateLimitError:
        return f"Meeting about {title}. (AI summary unavailable - API rate limit reached)"
    except openai.AuthenticationError:
        return f"Meeting about {title}. (AI summary unavailable - API authentication error)"
    except Exception as e:
        return f"Meeting about {title}. (AI summary unavailable - {str(e)[:50]})" 