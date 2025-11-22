from typing import Dict, Any, List, Optional
import logging
import httpx
import json
from datetime import datetime
import re

logger = logging.getLogger(__name__)

class ToolService:
    """
    Service for executing various tools that can be used in workflows
    """
    
    async def execute_http_request(self, config: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute an HTTP request
        
        Config parameters:
        - method: HTTP method (GET, POST, PUT, DELETE)
        - url: URL to request
        - headers: Optional headers
        - params: Optional query parameters
        - body: Optional request body
        - timeout: Optional timeout in seconds
        """
        method = config.get("method", "GET").upper()
        url = config.get("url")
        headers = config.get("headers", {})
        params = config.get("params", {})
        body = config.get("body")
        timeout = config.get("timeout", 30)
        
        # Replace variables in URL, headers, params, and body
        url = self._replace_variables(url, context)
        headers = self._replace_variables_in_dict(headers, context)
        params = self._replace_variables_in_dict(params, context)
        if isinstance(body, str):
            body = self._replace_variables(body, context)
        elif isinstance(body, dict):
            body = self._replace_variables_in_dict(body, context)
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.request(
                    method=method,
                    url=url,
                    headers=headers,
                    params=params,
                    json=body if isinstance(body, dict) else None,
                    content=body if isinstance(body, str) else None,
                    timeout=timeout
                )
                
                # Try to parse response as JSON
                try:
                    response_data = response.json()
                except:
                    response_data = response.text
                
                return {
                    "status_code": response.status_code,
                    "headers": dict(response.headers),
                    "body": response_data,
                    "elapsed_ms": response.elapsed.total_seconds() * 1000
                }
        except Exception as e:
            logger.error(f"Error executing HTTP request: {str(e)}")
            return {
                "error": str(e),
                "status_code": None,
                "headers": {},
                "body": None
            }
    
    async def execute_data_transformation(self, config: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform data using JMESPath or simple templates
        
        Config parameters:
        - type: transformation type (jmespath, template)
        - input: input variable name
        - expression: JMESPath expression or template
        - output: output variable name
        """
        transform_type = config.get("type", "jmespath")
        input_var = config.get("input")
        expression = config.get("expression")
        output_var = config.get("output", "result")
        
        input_data = context.get(input_var) if input_var else context
        
        try:
            if transform_type == "jmespath":
                import jmespath
                result = jmespath.search(expression, input_data)
            elif transform_type == "template":
                # Simple template with variable substitution
                result = self._replace_variables(expression, context)
            else:
                raise ValueError(f"Unknown transformation type: {transform_type}")
            
            return {output_var: result}
        except Exception as e:
            logger.error(f"Error executing data transformation: {str(e)}")
            return {output_var: None, "error": str(e)}
    
    async def send_email(self, config: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send an email
        
        Config parameters:
        - to: recipient email address(es)
        - subject: email subject
        - body: email body
        - body_type: text or html
        - from_email: sender email address
        - smtp_server: SMTP server details
        """
        # Replace variables in config
        to = self._replace_variables(config.get("to", ""), context)
        subject = self._replace_variables(config.get("subject", ""), context)
        body = self._replace_variables(config.get("body", ""), context)
        
        # For hackathon, just simulate sending email
        logger.info(f"Simulating email to {to}, subject: {subject}")
        
        return {
            "email_sent": True,
            "to": to,
            "subject": subject,
            "timestamp": datetime.now().isoformat()
        }
    
    async def execute_ai_task(self, config: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute an AI task using Gemini
        
        Config:
        - task_type: summarize, extract, classify, generate
        - input: input variable name
        - prompt: additional prompt instructions
        - output: output variable name
        """
        from google import genai
        from ..core.config import settings
        
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        task_type = config.get("task_type", "generate")
        input_var = config.get("input")
        prompt = config.get("prompt", "")
        output_var = config.get("output", "ai_result")
        
        input_text = context.get(input_var, "") if input_var else ""
        
        # Replace variables in prompt
        prompt = self._replace_variables(prompt, context)
        
        try:
            if task_type == "summarize":
                system_message = "Summarize the following text concisely:"
            elif task_type == "extract":
                system_message = "Extract key information from the following text:"
            elif task_type == "classify":
                system_message = "Classify the following text:"
            else:  # generate
                system_message = "Generate text based on the following instructions:"
            
            full_prompt = f"{system_message}\n\n{prompt}\n\n{input_text}"
            
            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=full_prompt
            )
            
            result = response.text
            
            return {output_var: result}
        except Exception as e:
            logger.error(f"Error executing AI task: {str(e)}")
            return {output_var: None, "error": str(e)}
    
    def _replace_variables(self, text: str, context: Dict[str, Any]) -> str:
        """
        Replace variables in text with values from context
        Format: {{variable_name}}
        """
        if not text or not isinstance(text, str):
            return text
        
        def replace_var(match):
            var_name = match.group(1).strip()
            if "." in var_name:
                # Handle nested attributes
                parts = var_name.split(".")
                value = context
                for part in parts:
                    if isinstance(value, dict) and part in value:
                        value = value[part]
                    else:
                        # If path doesn't exist, return original placeholder
                        return match.group(0)
                return str(value)
            else:
                return str(context.get(var_name, match.group(0)))
        
        return re.sub(r'{{(.*?)}}', replace_var, text)
    
    def _replace_variables_in_dict(self, data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Replace variables in dictionary values with values from context
        """
        if not data or not isinstance(data, dict):
            return data
        
        result = {}
        for key, value in data.items():
            if isinstance(value, str):
                result[key] = self._replace_variables(value, context)
            elif isinstance(value, dict):
                result[key] = self._replace_variables_in_dict(value, context)
            elif isinstance(value, list):
                result[key] = [
                    self._replace_variables_in_dict(item, context) if isinstance(item, dict)
                    else self._replace_variables(item, context) if isinstance(item, str)
                    else item
                    for item in value
                ]
            else:
                result[key] = value
        
        return result

# Create singleton instance
tool_service = ToolService()