from typing import Dict, Optional
from django.http import HttpRequest
from django.utils import timezone
from urllib.parse import urlsplit, urlunsplit, quote


def user_profile(request: HttpRequest) -> Dict[str, object]:
    """Injects `profile` and `profile_photo_url` into all template contexts for authenticated users."""
    user = getattr(request, 'user', None)
    ctx: Dict[str, Optional[object]] = {'profile': None, 'profile_photo_url': None}
    if user and getattr(user, 'is_authenticated', False):
        try:
            profile = user.get_profile()
            ctx['profile'] = profile
            if profile and getattr(profile, 'photo', None):
                # Build absolute, safely-encoded URL with cache-busting version
                try:
                    raw_url = profile.photo.url  # may contain spaces/newlines
                    abs_url = request.build_absolute_uri(raw_url)
                    parts = urlsplit(abs_url)
                    safe_path = quote(parts.path)
                    safe_url = urlunsplit((parts.scheme, parts.netloc, safe_path, parts.query, parts.fragment))
                    version = int(getattr(profile, 'updated_at', timezone.now()).timestamp())
                    sep = '&' if parts.query else ''
                    ctx['profile_photo_url'] = f"{safe_url}{sep}?v={version}"
                except Exception:
                    ctx['profile_photo_url'] = None
        except Exception:
            pass
    return ctx
