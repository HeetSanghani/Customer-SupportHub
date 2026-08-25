# 07 - JWT Session Lifecycle & Refresh Flow
## Token Specs
- HS256 algorithm with secret key from environment.
- Access token: 30 minutes.
- Refresh token: 7 days.
- Axios interceptor silently refreshes expired access tokens.
