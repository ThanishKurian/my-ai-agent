import logging
import requests
import json
logger = logging.getLogger(__name__)

def input_prompt(input, model, logging_on=True):
    # This function takes an input prompt and a model name, and returns the output from the Gemini API.

    GEMINI_API_KEY = "AIzaSyDZov7d8dPIxrnsy3GMR-2ZoahYUgJb4QU"
    if logging_on:
        logger.info("API Key is set. Sending request to Gemini API... ")

    output_response = "No valid response received from Gemini API."

    try:
        response = requests.request(
            method="POST",
            url="https://generativelanguage.googleapis.com/v1beta/interactions",
            headers={
                "x-goog-api-key": GEMINI_API_KEY,
                "Content-Type": "application/json",
                "Api-Revision": "2026-05-20"
            },
            json={
                "model": model,
                "input": input
            }
        )

        if logging_on:
            logger.info("Request sent successfully. Processing response...")

        if response.status_code == 200:
            response_data = response.json()
            if logging_on:
                logger.info("Response received from Gemini API:")
                logger.info(json.dumps(response_data, indent=2))
                logger.info("Output from Gemini API:")
            output = response_data["steps"][1]["content"][0]["text"]
            return output
        else:
            if logging_on:
                logger.error("Failed to get a successful response from Gemini API.")
                logger.error("Status Code:", response.status_code)
                logger.error("Response Text:", response.text)

    except Exception as e:
        if logging_on:
            logger.error("Error occurred while sending request to Gemini API.")
            logger.error("Error message:", str(e))
        return "Error occurred while sending request to Gemini API."

    return output_response
