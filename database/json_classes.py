from typing import List, Optional, Any

from pydantic import BaseModel, Field


class ApiVariable(BaseModel):
    name: str  # Name of the variable
    value: Optional[str] = None  # Value to be filled later (e.g., user_id)


class ApiExpectedVariable(BaseModel):
    json_path: str  # JSON path to check the response data
    expected_value: Any


class ApiConfig(BaseModel):
    url: str
    method: str = "GET"  # HTTP method, defaults to GET
    path_variables: List[ApiVariable] = Field(default_factory=list)  # Variables for URL path
    param_variables: List[ApiVariable] = Field(default_factory=list)  # Query parameters
    authorization: Optional[str] = None  # Authorization header (e.g., Bearer token)
    expectations: List[ApiExpectedVariable] = Field(default_factory=list)


class BotApiConfig(BaseModel):
    metadata: Optional[str]
    api_config: ApiConfig  # API configuration for the bot


class UserActivityContext(BaseModel):
    callback_query_prefix: Optional[str] = Field(default=None)
