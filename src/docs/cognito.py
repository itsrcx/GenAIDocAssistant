from fastapi import status

from src.schemas.standard import ErrorResponse


COGNITO_ERROR_MAP = {
    "NotAuthorizedException":          (status.HTTP_401_UNAUTHORIZED, "Not authorized"),
    "TooManyRequestsException":        (status.HTTP_429_TOO_MANY_REQUESTS, "Too many requests"),
    "InternalErrorException":          (status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal server error"),
    "ForbiddenException":              (status.HTTP_403_FORBIDDEN, "Forbidden"),
    "ResourceNotFoundException":       (status.HTTP_404_NOT_FOUND, "Resource not found"),
    "InvalidParameterException":       (status.HTTP_422_UNPROCESSABLE_ENTITY, "Invalid parameters"),
    "PasswordResetRequiredException":  (status.HTTP_400_BAD_REQUEST, "Password reset required"),
    "UserNotConfirmedException":       (status.HTTP_403_FORBIDDEN, "User not confirmed"),
    "InvalidPasswordException":        (status.HTTP_400_BAD_REQUEST, "Invalid password"),
    "UnexpectedLambdaException":       (status.HTTP_502_BAD_GATEWAY, "Unexpected Lambda failure"),
    "UserLambdaValidationException":   (status.HTTP_400_BAD_REQUEST, "User Lambda validation failed"),
    "TooManyFailedAttemptsException":  (status.HTTP_429_TOO_MANY_REQUESTS, "Too many failed attempts"),
    "CodeMismatchException":           (status.HTTP_400_BAD_REQUEST, "Code mismatch"),
    "ExpiredCodeException":            (status.HTTP_400_BAD_REQUEST, "Expired code"),
    "InvalidLambdaResponseException":  (status.HTTP_502_BAD_GATEWAY, "Invalid response from Lambda"),
    "AliasExistsException":            (status.HTTP_409_CONFLICT, "Alias already exists"),
    "LimitExceededException":          (status.HTTP_429_TOO_MANY_REQUESTS, "Limit exceeded"),
    "UserNotFoundException":           (status.HTTP_404_NOT_FOUND, "User not found"),
    "CodeDeliveryFailureException":    (status.HTTP_500_INTERNAL_SERVER_ERROR, "Code delivery failed"),
    "UnsupportedOperationException":            (status.HTTP_501_NOT_IMPLEMENTED, "Unsupported operation"),
    "InvalidUserPoolConfigurationException":    (status.HTTP_500_INTERNAL_SERVER_ERROR, "Invalid user pool configuration"),
    "InvalidSmsRoleAccessPolicyException":      (status.HTTP_500_INTERNAL_SERVER_ERROR, "Invalid SMS role access policy"),
    "InvalidEmailRoleAccessPolicyException":    (status.HTTP_500_INTERNAL_SERVER_ERROR, "Invalid email role access policy"),
    "InvalidSmsRoleTrustRelationshipException": (status.HTTP_500_INTERNAL_SERVER_ERROR, "Invalid SMS role trust relationship"),
    "PasswordHistoryPolicyViolationException":  (status.HTTP_400_BAD_REQUEST, "Password history policy violation"),
}

def generate_responses_for_errors(errors: list[str]) -> dict:
    responses = dict()
    for error_code in errors:
        http_status, message = COGNITO_ERROR_MAP.get(error_code, (400, "Bad Request"))
        responses[http_status] = {
            "model": ErrorResponse,
            "description": message,
            "content": {
                "application/json": {
                    "example": {
                        "status": "failed",
                        "message": message,
                        "error": error_code,
                        "details": f"Details about {error_code}"
                    }
                }
            }
        }
    return responses
