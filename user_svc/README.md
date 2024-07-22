# User Management Service

## Overview

The User Management Service is a RESTful API for managing user authentication, registration, and profile management. It includes endpoints for user login, registration, profile management, and secure storage of sensitive information.

## Authentication

### Access Tokens and Refresh Tokens

The service uses two types of tokens to manage user sessions and authentication:

1. **Access Token**
   - **Purpose**: Used to authenticate requests to the server. Included in the `Authorization` header of HTTP requests.
   - **Lifetime**: Typically short-lived (e.g., 15 minutes) to minimize the risk of token compromise.
   - **Usage**: Provided upon successful login and used to access protected resources or endpoints.
   - **Expiration**: If the access token expires, the client must use the refresh token to obtain a new access token.

2. **Refresh Token**
   - **Purpose**: Used to obtain a new access token when the current one expires. Stored securely on the client side and exchanged for a new access token when needed.
   - **Lifetime**: Longer-lived than access tokens (e.g., 7 days) to allow users to stay logged in without frequent re-authentication.
   - **Usage**: Provided along with the access token during login and used to request a new access token when the current one expires.
   - **Expiration**: If the refresh token expires or is invalid, the user must log in again to obtain a new refresh token.

### Token Endpoints

- **Login**
  - **Endpoint**: `POST /token`
  - **Description**: Authenticates the user and returns an access token and refresh token.
  - **Request**: Requires `username` and `password`.
  - **Response**: Returns `access_token` and `refresh_token`.

- **Refresh Token**
  - **Endpoint**: `POST /token/refresh`
  - **Description**: Exchanges a valid refresh token for a new access token.
  - **Request**: Requires `old_refresh_token`.
  - **Response**: Returns a new `access_token`.

## Endpoints

### Registration
- **Endpoint**: `POST /register`
- **Description**: Registers a new user.
- **Request**: Requires `username`, `email`, and `password`.
- **Response**: Returns a confirmation message upon successful registration.

### User Profile
- **Create**: `POST /profile`
  - **Description**: Creates a new user profile.
  - **Request**: Requires user data such as `name`, `phone`, and `shipping_address`.
  - **Response**: Returns the created profile.

- **Get**: `GET /profile/me`
  - **Description**: Retrieves the current user's profile.
  - **Response**: Returns the user profile data.

- **Edit**: `PUT /profile`
  - **Description**: Updates the current user's profile.
  - **Request**: Requires updated profile data.
  - **Response**: Returns the updated profile.

- **Delete**: `DELETE /profile`
  - **Description**: Deletes the current user's profile.
  - **Response**: Returns a confirmation message upon successful deletion.

### Payment Information
- **Store**: `POST /profile/payment_info`
  - **Description**: Stores payment information securely.
  - **Request**: Requires `payment_token`.
  - **Response**: Returns a confirmation message upon successful storage.

- **Update**: `PUT /profile/payment_info`
  - **Description**: Updates stored payment information.
  - **Request**: Requires `payment_token`.
  - **Response**: Returns a confirmation message upon successful update.

## Security

- **Token Storage**: Tokens should be stored securely on the client side and never exposed to unauthorized parties.
- **Token Expiration**: Regularly monitor and refresh tokens to maintain security.
- **Error Handling**: Handle invalid or expired tokens appropriately by requesting the user to log in again.

## Development Notes

### Development Endpoint
- **Endpoint**: `/users`
- **Description**: Retrieves a list of all users. Use only during development and ensure it is removed or commented out before deploying to production.

## Major Concerns

- **Token Management**: Ensure that tokens are securely stored and transmitted. Access tokens should be short-lived, and refresh tokens should be kept secure to prevent unauthorized access.
- **Endpoint Security**: Protect sensitive endpoints with proper authentication and authorization checks.
- **Development Endpoints**: Remove or disable development-only endpoints in the production environment to avoid exposing sensitive data or functionality.
