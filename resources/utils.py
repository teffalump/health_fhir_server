# Utility functions for resources

from server.health_fhir import Bundle

def prime_feed(request):
    per_page = int(request.args.get('_count', 10))
    page = int(request.args.get('page', 1))
    bd=Bundle(request=request,
                    total=total_recs,
                    per_page = per_page,
                    page = page)
    offset = (page-1) * per_page
    return bd

__all__=['prime_feed']
