from dotenv import load_dotenv
import os

# Import namespaces
from azure.core.credentials import AzureKeyCredential
from azure.ai.language.questionanswering import QuestionAnsweringClient


def main():
    try:
        # Get Configuration Settings
        load_dotenv()
        ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
        ai_key = os.getenv('AI_SERVICE_KEY')
        ai_project_name = os.getenv('QA_PROJECT_NAME')
        ai_deployment_name = os.getenv('QA_DEPLOYMENT_NAME')

        # Create client using endpoint and key
        credential = AzureKeyCredential(key=ai_key)
        ai_client = QuestionAnsweringClient(endpoint=ai_endpoint, credential=credential)


        # Submit a question and display the answer
        user_question = ''
        while user_question.lower() != 'quit':
            user_question = input('\nQuestion:\n')
            response = ai_client.get_answers(project_name=ai_project_name, deployment_name=ai_deployment_name, question=user_question)
            for candidate in response.answers:
                print(candidate.answer)
                print('Confidence: {}'.format(candidate.confidence))
                print('Source: {}'.format(candidate.source))


    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()
