# import openai
# from django.conf import settings

# openai_client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

# def generate_pipeline_script(user_inputs):
#     """
#     Generate a DevOps pipeline script using OpenAI based on user inputs.
    
#     :param user_inputs: A dictionary containing user selections.
#     :return: Generated script as a string.
#     """
#     prompt = f"""
#     Generate a DevOps pipeline script based on these requirements:
#     - Deployment type: {user_inputs.get('deployment_type')}
#     - Testing needs: {user_inputs.get('testing_needs')}
#     - Framework: {user_inputs.get('framework')}
#     - Programming language: {user_inputs.get('language')}
#     - Application type: {user_inputs.get('application_type')}
#     - Hosting platform: {user_inputs.get('hosting_platform')}
    
#     The script should follow best DevOps practices.
#     """

#     response = openai_client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "You are a DevOps expert."},
#             {"role": "user", "content": prompt}
#         ]
#     )

#     return response.choices[0].message.content

# myapps/services/openai_service.py
# myapps/utils.py

import openai
from django.conf import settings

def generate_pipeline_script(user_inputs):
    """
    Generate a DevOps pipeline script using OpenAI based on user inputs.

    Args:
        user_inputs (dict): Contains all user selections including:
            - deployment_type
            - testing_needs
            - framework
            - language
            - application_type
            - hosting_platform
            - stage

    Returns:
        str: Generated script content
    """
    stage = user_inputs.get('stage', 'Development').lower()

    # Stage-specific prompts
    stage_prompts = {
        'planning': "Create a project setup and planning document including:",
        'development': "Generate a development environment setup script including:",
        'testing': "Create a comprehensive testing script with:",
        'deployment': "Generate a deployment script for:",
        'monitoring': "Create a monitoring setup script with:"
    }

    base_prompt = f"""
    {stage_prompts.get(stage, "Generate a DevOps script for")}:
    - Project type: {user_inputs.get('application_type', 'web application')}
    - Programming language: {user_inputs.get('language', 'Python')}
    - Framework: {user_inputs.get('framework', 'Django')}
    - Hosting platform: {user_inputs.get('hosting_platform', 'AWS')}
    - Deployment type: {user_inputs.get('deployment_type', 'containerized')}
    - Testing needs: {user_inputs.get('testing_needs', 'basic')}

    The script should:
    1. Follow industry best practices
    2. Include clear comments
    3. Be modular where appropriate
    4. Handle errors gracefully
    5. Be specific to the {user_inputs.get('hosting_platform', 'AWS')} platform

    Output only the script content with no additional explanations or markdown formatting.
    """

    try:
        # Make OpenAI API call to generate script
        response = openai.Completion.create(
            model="gpt-3.5-turbo" , # model you prefer
            messages=[
                {"role": "system", "content": "You are a senior DevOps engineer. Generate only executable scripts with no additional commentary."},
                {"role": "user", "content": base_prompt}
            ],
            temperature=0.7,
            max_tokens=1500
        )

        script_content = response['choices'][0]['message']['content']
        
        # Clean up the response content
        if "```" in script_content:
            script_content = script_content.split("```")[1]
            if script_content.startswith("bash\n"):
                script_content = script_content[5:]

        return script_content.strip()

    except Exception as e:
        print(f"Error generating script: {str(e)}")
        return f"# Error generating script. Please try again.\n# {str(e)}"
