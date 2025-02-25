from rest_framework_simplejwt.tokens import RefreshToken 


# Function to generate JWT tokens with role information
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    refresh["role"] = user.role  # Store role in the token
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
        "role": user.role
    }
