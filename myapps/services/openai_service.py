import openai
from django.conf import settings

openai_client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

def generate_pipeline_script(user_inputs):
    """
    Generate a DevOps pipeline script using OpenAI based on user inputs.
    
    :param user_inputs: A dictionary containing user selections.
    :return: Generated script as a string.
    """
    prompt = f"""
    Generate a DevOps pipeline script based on these requirements:
    - Deployment type: {user_inputs.get('deployment_type')}
    - Testing needs: {user_inputs.get('testing_needs')}
    - Framework: {user_inputs.get('framework')}
    - Programming language: {user_inputs.get('language')}
    - Application type: {user_inputs.get('application_type')}
    - Hosting platform: {user_inputs.get('hosting_platform')}
    
    The script should follow best DevOps practices.
    """

    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a DevOps expert."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content

